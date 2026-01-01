"""
High-value tests for File Explainer Agent.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from file_explainer.agent import FileExplainerAgent


# Fixtures
@pytest.fixture
def sample_py_file():
    """Path to sample Python file."""
    return Path(__file__).parent / "fixtures" / "sample.py"


@pytest.fixture
def sample_js_file():
    """Path to sample JS file."""
    return Path(__file__).parent / "fixtures" / "sample.js"


# Core Functionality Tests
class TestFileReading:
    """Test file reading with real edge cases."""

    def test_read_valid_file(self, sample_py_file):
        """Read a real file successfully."""
        agent = FileExplainerAgent(api_key="test-key")
        content = agent.read_file(str(sample_py_file))

        assert "fibonacci" in content.lower()
        assert len(content) > 0

    def test_missing_file_raises_error(self):
        """Missing file raises FileNotFoundError."""
        agent = FileExplainerAgent(api_key="test-key")

        with pytest.raises(FileNotFoundError, match="File not found"):
            agent.read_file("/nonexistent/path/file.py")

    def test_directory_raises_error(self, tmp_path):
        """Directory instead of file raises ValueError."""
        agent = FileExplainerAgent(api_key="test-key")

        with pytest.raises(ValueError, match="not a file"):
            agent.read_file(str(tmp_path))

    def test_binary_file_raises_error(self, tmp_path):
        """Binary file raises ValueError."""
        binary_file = tmp_path / "test.bin"
        # Write invalid UTF-8 sequence
        binary_file.write_bytes(b"\xff\xfe\xfd\xfc")

        agent = FileExplainerAgent(api_key="test-key")

        with pytest.raises(ValueError, match="not a text file"):
            agent.read_file(str(binary_file))


class TestAPIKeyHandling:
    """Test API key validation and configuration."""

    def test_api_key_from_parameter(self):
        """API key passed as parameter works."""
        agent = FileExplainerAgent(api_key="test-key-123")
        assert agent.api_key == "test-key-123"

    def test_api_key_from_env(self, monkeypatch):
        """API key read from environment variable."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "env-key-456")
        agent = FileExplainerAgent()
        assert agent.api_key == "env-key-456"

    def test_missing_api_key_raises_error(self, monkeypatch):
        """Missing API key raises ValueError."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        with pytest.raises(ValueError, match="API key must be provided"):
            FileExplainerAgent()


class TestExplainFile:
    """Test the explain_file method with mocked API."""

    @patch('file_explainer.agent.anthropic.Anthropic')
    def test_explain_file_calls_api_correctly(self, mock_anthropic, sample_py_file):
        """Verify API is called with correct parameters."""
        # Setup mock
        mock_client = Mock()
        mock_anthropic.return_value = mock_client
        mock_response = Mock()
        mock_response.content = [Mock(text="This is a Fibonacci calculator.")]
        mock_client.messages.create.return_value = mock_response

        # Run agent
        agent = FileExplainerAgent(api_key="test-key")
        explanation = agent.explain_file(str(sample_py_file))

        # Verify
        assert "fibonacci" in explanation.lower()
        mock_client.messages.create.assert_called_once()
        call_args = mock_client.messages.create.call_args[1]
        assert call_args["model"] == "claude-3-5-sonnet-20241022"
        assert "fibonacci" in call_args["messages"][0]["content"].lower()

    @patch('file_explainer.agent.anthropic.Anthropic')
    def test_api_error_is_handled(self, mock_anthropic, sample_py_file):
        """API errors are caught and wrapped."""
        mock_client = Mock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API failure")

        agent = FileExplainerAgent(api_key="test-key")

        with pytest.raises(RuntimeError, match="Failed to get explanation"):
            agent.explain_file(str(sample_py_file))
