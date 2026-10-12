"""Configuration settings for inference client."""

from dataclasses import dataclass, field, asdict
import json
import os
from pathlib import Path


DEFAULT_CONFIG_FILENAME = "infer-config.json"


@dataclass
class Config:
    base_url: str = field(default_factory=lambda: os.getenv("INFERENCE_BASE_URL", "http://localhost:8000"))
    api_key: str | None = field(default_factory=lambda: os.getenv("INFERENCE_API_KEY", None))
    timeout: float = field(default_factory=lambda: float(os.getenv("INFERENCE_TIMEOUT", "30.0")))
    model: str = field(default_factory=lambda: os.getenv("INFERENCE_MODEL", "default-model"))


def load_config(path: str | Path | None = None) -> Config:
    """Load configuration from a JSON file, environment variables, or defaults.
    
    Priority:
    1. If a path is explicitly provided and exists, load values from it.
    2. If no path is provided and default 'infer-config.json' exists in CWD, load from it.
    3. Values not specified in JSON fall back to Config dataclass defaults (which read env vars).
    """
    config_path = Path(path) if path else Path(DEFAULT_CONFIG_FILENAME)

    if path and not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    if config_path.is_file():
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        valid_keys = {"base_url", "api_key", "timeout", "model"}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return Config(**filtered_data)

    return Config()


def write_sample_config(output_file: str | Path = DEFAULT_CONFIG_FILENAME) -> None:
    """Generate a sample inference-client configuration file."""
    config = Config()
    output_path = Path(output_file)
    output_path.write_text(
        json.dumps(asdict(config), indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Sample configuration created: {output_path.resolve()}")
