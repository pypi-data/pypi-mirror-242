# %%
%load_ext autoreload
%autoreload 2
from atopile.project.config import make_config, Config
from atopile.project.project import Project
from pathlib import Path
from omegaconf import OmegaConf

#%%
configs = {}
for ato_path in Path("/Users/mattwildoer/Projects/atopile-workspace/").glob("**/ato.yaml"):
    try:
        configs[ato_path] = make_config(ato_path)
    except Exception as e:
        print(f"Failed to load {ato_path}: {e}")


# %%
config: Config = list(configs.values())[0]

# %%
config.paths.abs_build
# %%
