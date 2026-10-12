# track1-client

Client component for AI Inference Engineering.

## Structure

```text
track1-client/
├── .venv/
├── pyproject.toml
├── src/
│   └── inference_client/
│       ├── __init__.py
│       ├── config.py
│       └── cli.py
├── tests/
│   └── test_config.py
└── README.md
```

## Setup & Installation

1. Activate your virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. Install editable package with development/test dependencies:
   ```powershell
   pip install -e ".[dev]"
   ```

## Usage

Run the CLI:
```powershell
python -m inference_client.cli --base-url "http://localhost:8000" --model "my-model"
```

## Testing

Run tests with pytest:
```powershell
pytest
```
