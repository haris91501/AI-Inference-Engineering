"""Configuration settings for inference client."""

from dataclasses import dataclass, field
import os


@dataclass
class Config:
    base_url: str = field(default_factory=lambda: os.getenv("INFERENCE_BASE_URL", "http://localhost:8000"))
    api_key: str | None = field(default_factory=lambda: os.getenv("INFERENCE_API_KEY", None))
    timeout: float = field(default_factory=lambda: float(os.getenv("INFERENCE_TIMEOUT", "30.0")))
    model: str = field(default_factory=lambda: os.getenv("INFERENCE_MODEL", "default-model"))
