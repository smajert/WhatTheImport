from pathlib import Path
import tomllib

with open(Path(__file__).parent.parent / "pyproject.toml", "rb") as proj_toml:
    __version__ = tomllib.load(proj_toml)["project"]["version"]
