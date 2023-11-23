"""
Walk the dm1 tree and create dm2 analogs.

Step 1 is to create hollow dm2 objects that have the same structure as dm1

Step 2 requires name resolution, which is a smidge tricky.
If we pass-down lexical scoping information as we walk the tree,
we can resolve all lexically scoped names, including references to supers.

However, we need this information for all objects in order to be able to "hop"
between scopes. For example, "a.b.c" is a reference to "c" in the scope of
"a.b", but from within a scope containing "a", we don't necessarily know that
"b" or "c" exist, we just (after step 1), know what "a" is.
"""

import logging
import collections
import itertools
from pathlib import Path
from typing import Any, Iterable, Optional, Mapping

from attrs import define, resolve_types

from atopile.model2 import datamodel1 as dm1
from atopile.model2 import errors

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@define
class Link:
    start_instance: Optional["Object"] = None
    start_node: Optional["Object"] = None
    end_instance: Optional["Object"] = None
    end_node: Optional["Object"] = None


@define
class Replace:
    original: Optional["Object"] = None
    replacement: Optional["Object"] = None


@define
class Import:
    what: Optional["Object"] = None


@define
class Object:
    # these are populated by Wendy
    locals_: Optional[Mapping] = None
    supers: Optional[tuple["Object"]] = None

    # these are created by Wendy, for the next guy
    name_bindings: Optional[Mapping] = None
    closure: Optional[Mapping] = None


for cls in [Object, Link, Replace, Import]:
    resolve_types(cls)


MODULE = Object()
COMPONENT = Object(supers=(Object))


PIN = Object()
SIGNAL = Object()
INTERFACE = Object()


BUILTINS = {
    dm1.MODULE[-1][0]: MODULE,
    dm1.COMPONENT[-1][0]: COMPONENT,
    dm1.PIN[-1][0]: PIN,
    dm1.SIGNAL[-1][0]: SIGNAL,
    dm1.INTERFACE[-1][0]: INTERFACE,
}


class Wendy:
    def __init__(self) -> None:
        self.dm1_id_object_map: dict[int, Object] = collections.defaultdict(Object)
        self.dm1_id_name_binding_map: dict[int, dict[str, Any]] = {}
        self.dm1_id_closure_map: dict[int, collections.ChainMap[dm1.Ref, Any]] = {}
        self.collected_errors: list[errors.AtoError] = []

    def collect_error(self, error: errors.AtoError):
        self.collected_errors.append(error)

    def visit(self, dm1_obj: dm1.Object, closure: collections.ChainMap) -> None:
        assert id(dm1_obj) not in self.dm1_id_object_map
        self.dm1_id_closure_map[id(dm1_obj)] = Object()
        binding_map = self.dm1_id_name_binding_map[id(dm1_obj)] = dict(filter(lambda x: x[0] is not None, dm1_obj.locals_))
        self.dm1_id_closure_map[id(dm1_obj)] = closure

        child_closure = closure.new_child(binding_map)
        for _, child in dm1_obj.locals_:
            if not isinstance(child, dm1.Object):
                continue
            self.visit(child, child_closure)

    def visit_roots(self, objs: Iterable[dm1.Object]) -> None:
        """
        Expected to be called on an iterable of file objects, which are generally the roots of these trees
        """
        builtins_map = collections.ChainMap(BUILTINS)
        for obj in objs:
            self.visit(obj, builtins_map)
        if self.collected_errors:
            raise ExceptionGroup("Errors occurred while visiting roots", self.collected_errors)


class Lofty:
    """
    Lofty's job is to walk the tree, filling in the dm2 objects
    """
    def __init__(
        self,
        dm1_id_object_map: dict[int, Object],
        dm1_id_name_binding_map: dict[int, dict[str, Any]],
        dm1_id_closure_map: dict[int, collections.ChainMap[dm1.Ref, Any]],
        search_paths: Iterable[Path],
        path_dm1_map: dict[Path, dm1.Object],
    ) -> None:
        # these name-bindings and lexical scopes are created by Wendy
        # their keys are the names for the given scope, and the values
        # are the dm1 objects
        self.dm1_id_object_map = dm1_id_object_map
        self.dm1_id_name_binding_map = dm1_id_name_binding_map
        self.dm1_id_closure_map = dm1_id_closure_map
        self.search_paths = search_paths
        self.path_dm1_map = path_dm1_map

        self.errors: list[errors.AtoError] = []

    def collect_error(self, error: errors.AtoError) -> errors.AtoError:
        """
        Collect up the errors so non-fatal errors can be reported collectively, reducing noise
        This also returns the error, so it can be raised on the spot if desired
        """
        self.errors.append(error)
        return error

    def search_file_path(self, dep_name: str) -> Path:
        for search_path in self.search_paths:
            candidate_path = search_path.joinpath(dep_name)
            if candidate_path.exists():
                return candidate_path.resolve().absolute()
        raise errors.AtoImportNotFoundError(f"Could not find import: {dep_name}")

    def visit_generic(self, thing: Any, dm2_closure: collections.ChainMap) -> Any:
        """
        Handle visiting something - it'll work out where to dispatch the call.
        """
        match thing:
            case dm1.Object:
                return self.visit_dm1_Object(thing, dm2_closure)
            case dm1.Link:
                return self.visit_dm1_Link(thing, dm2_closure)
            case dm1.Replace:
                return self.visit_dm1_Replace(thing, dm2_closure)
            case dm1.Import:
                return self.visit_dm1_Import(thing, dm2_closure)
            case _:
                return self.visit_default(thing, dm2_closure)

    def visit_default(self, thing: Any, dm2_closure: collections.ChainMap) -> Any:
        """
        Do this if nothing else
        """
        return thing

    def visit_dm1_Object(self, dm1_obj: dm1.Object, dm2_closure: collections.ChainMap) -> Object:
        """
        """
        dm1_closure = self.dm1_id_closure_map[id(dm1_obj)]
        dm1_name_binding_map = self.dm1_id_name_binding_map[id(dm1_obj)]

        internal_dm1_name_map = dm1_closure.new_child(dm1_name_binding_map)

        dm2_obj = self.dm1_id_object_map[id(dm1_obj)]

        # find the objects representing the supers
        # FIXME: this should do an actual lookup, not just a name-based one
        # this should only be an issue with multi-part refs
        dm2_obj.supers = tuple(self.dm1_id_object_map[id(internal_dm1_name_map[super_ref])] for super_ref in dm1_obj.supers)
        dm2_obj.locals_ = tuple((name, self.visit_generic(obj)) for name, obj in dm1_obj.locals_)
        dm2_obj.name_bindings = dict(filter(lambda x: x[0] is not None, dm2_obj.locals_))
        dm2_obj.closure = dm2_closure.new_child(dm2_obj.name_bindings)

    def visit_dm1_Link(self, dm1_thing: dm1.Link, dm2_closure: collections.ChainMap) -> Link:
        """
        Handle visiting a dm1.Link
        """
        raise NotImplementedError
        return Link(

        )

    def visit_dm1_Replace(self, dm1_thing: dm1.Replace, dm2_closure: collections.ChainMap) -> Replace:
        """
        Handle visiting a dm1.Replace
        """
        return Replace(
            
        )

    def visit_dm1_Import(self, dm1_thing: dm1.Import, dm2_closure: collections.ChainMap) -> Import:
        """
        Handle visiting a dm1.Import
        """


class Scoop:
    """
    Scoop's job is to come through and build all the name-binding maps and attach them to all the dm2 objects
    """
