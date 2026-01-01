"""
File Explainer Agent

A simple AI agent that reads a file and explains what it does in plain English.
"""

import os
from pathlib import Path
from typing import Optional

import anthropic


class FileExplainerAgent:
    """Agent that explains what a file does using Claude AI."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize the File Explainer Agent.

        Args:
            api_key: Anthropic API key. If None, reads from ANTHROPIC_API_KEY env var.
            model: Claude model to use for explanations.

        Raises:
            ValueError: If API key is not provided and not found in environment.
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided or set in ANTHROPIC_API_KEY environment variable"
            )

        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def read_file(self, file_path: str) -> str:
        """
        Read file contents safely.

        Args:
            file_path: Path to the file to read.

        Returns:
            File contents as string.

        Raises:
            FileNotFoundError: If file doesn't exist.
            PermissionError: If file can't be read.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise ValueError(f"File is not a text file or has unsupported encoding: {file_path}")

    def explain_file(self, file_path: str) -> str:
        """
        Explain what a file does in plain English.

        Args:
            file_path: Path to the file to explain.

        Returns:
            Human-readable explanation of the file.

        Raises:
            FileNotFoundError: If file doesn't exist.
            anthropic.APIError: If API call fails.
        """
        # Read file contents
        file_contents = self.read_file(file_path)
        file_name = Path(file_path).name

        # Create prompt for Claude
        prompt = f"""Please explain what this file does in clear, plain English.

File name: {file_name}

File contents:
```
{file_contents}
```

Provide a concise explanation that covers:
1. The main purpose of this file
2. Key components or functions
3. How it might be used or fit into a larger system

Keep the explanation accessible to someone learning to code."""

        # Call Claude API
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return message.content[0].text

        except Exception as e:
            raise RuntimeError(f"Failed to get explanation from Claude API: {e}")
