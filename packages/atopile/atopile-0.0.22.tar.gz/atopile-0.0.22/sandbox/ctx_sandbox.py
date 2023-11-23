#%%
from atopile.model2.parse import parse_text_as_file
from atopile.model2.errors import write_errors_to_log
from textwrap import dedent
import logging
#%%
logging.basicConfig(level=logging.DEBUG)
#%%
class Test:
    pass

with write_errors_to_log(reraise=False):
    tree = parse_text_as_file(
        dedent("""
            module test_module:
                signal a
        """).strip()
    )
# %%
