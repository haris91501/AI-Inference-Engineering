import json
import os
from unittest import mock
from inference_client.config import Config, load_config, write_sample_config


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


def test_load_config_from_json(tmp_path):
    config_file = tmp_path / "custom-config.json"
    data = {
        "base_url": "http://192.168.1.100:8000",
        "api_key": "test-key-123",
        "timeout": 15.0,
        "model": "mistral-7b"
    }
    config_file.write_text(json.dumps(data), encoding="utf-8")

    cfg = load_config(config_file)
    assert cfg.base_url == "http://192.168.1.100:8000"
    assert cfg.api_key == "test-key-123"
    assert cfg.timeout == 15.0
    assert cfg.model == "mistral-7b"


def test_write_sample_config(tmp_path):
    output_file = tmp_path / "infer-config.json"
    write_sample_config(output_file)
    assert output_file.is_file()
    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert "base_url" in data
    assert "model" in data
