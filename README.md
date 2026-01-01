# File Explainer Agent

A simple AI agent that reads a code file and explains what it does in plain English using Claude.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key**
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   ```

   Get your API key from [console.anthropic.com](https://console.anthropic.com/)

## Usage

```bash
python -m file_explainer.cli path/to/file.py
```

### Examples

```bash
# Explain a Python file
python -m file_explainer.cli src/utils.py

# Explain a JavaScript file
python -m file_explainer.cli app.js

# Use a different model
python -m file_explainer.cli --model claude-3-5-sonnet-20241022 script.py
```

## Testing

```bash
pytest
```

## Architecture

```
file_explainer/
├── agent.py     # Core agent logic
├── cli.py       # Command-line interface
└── __init__.py

tests/
├── test_agent.py       # Test suite
└── fixtures/           # Sample files for testing
```

## API

```python
from file_explainer import FileExplainerAgent

agent = FileExplainerAgent(api_key="your-key")
explanation = agent.explain_file("script.py")
print(explanation)
```

## AWS Deployment

This agent is fully portable and can run on:
- **AWS Lambda**: Serverless function triggered by events
- **ECS/Fargate**: Container-based deployment
- **EC2**: Traditional server deployment

Store your API key in AWS Secrets Manager, not in code.

## Error Handling

- `FileNotFoundError`: File doesn't exist
- `ValueError`: Invalid file (directory, binary, etc.)
- `RuntimeError`: API call failed

All errors include helpful messages.
