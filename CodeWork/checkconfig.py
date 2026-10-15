import tomllib
from pathlib import Path

config_path = Path("pyproject.toml")

with config_path.open("rb") as file:
    config = tomllib.load(file)

print(config)