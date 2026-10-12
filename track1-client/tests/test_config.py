import os
from unittest import mock
from inference_client.config import Config


def test_default_config():
    with mock.patch.dict(os.environ, {}, clear=True):
        cfg = Config()
        assert cfg.base_url == "http://localhost:8000"
        assert cfg.api_key is None
        assert cfg.timeout == 30.0
        assert cfg.model == "default-model"


def test_env_override():
    env_vars = {
        "INFERENCE_BASE_URL": "https://api.example.com",
        "INFERENCE_API_KEY": "secret-key",
        "INFERENCE_TIMEOUT": "45.5",
        "INFERENCE_MODEL": "meta-llama/Llama-3-8b",
    }
    with mock.patch.dict(os.environ, env_vars, clear=True):
        cfg = Config()
        assert cfg.base_url == "https://api.example.com"
        assert cfg.api_key == "secret-key"
        assert cfg.timeout == 45.5
        assert cfg.model == "meta-llama/Llama-3-8b"
