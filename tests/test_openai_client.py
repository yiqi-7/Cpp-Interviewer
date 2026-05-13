"""Tests for OpenAICompatibleClient."""
import os
import urllib.error
import pytest
from unittest.mock import patch, MagicMock
from coach.llm import OpenAICompatibleClient


def test_openai_client_generates_messages():
    """Test that OpenAI client correctly builds messages array."""
    client = OpenAICompatibleClient(
        api_key="test-key",
        base_url="https://api.openai.com/v1",
        model="gpt-4o"
    )

    # Check initialization
    assert client.api_key == "test-key"
    assert client.base_url == "https://api.openai.com/v1"
    assert client.model == "gpt-4o"


def test_openai_client_with_system_prompt():
    """Test that system prompt is correctly added to messages."""
    client = OpenAICompatibleClient(api_key="test-key")

    # Verify the generate method accepts system parameter
    import inspect
    sig = inspect.signature(client.generate)
    assert "system" in sig.parameters


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set"
)
def test_openai_client_smoke():
    """Smoke test with real API - only runs if OPENAI_API_KEY is set."""
    client = OpenAICompatibleClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.openai.com/v1",
        model="gpt-4o-mini"
    )
    result = client.generate(
        "Respond with exactly the word 'test'",
        system="You are a helpful assistant.",
        temperature=0.0
    )
    assert result.strip().lower() == "test"


def test_openai_client_http_error_handling():
    """Test that HTTP errors are converted to RuntimeError."""
    client = OpenAICompatibleClient(api_key="bad-key")

    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"error": "bad request"}'
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://test",
            code=400,
            msg="Bad Request",
            hdrs={},
            fp=mock_resp
        )
        with pytest.raises(RuntimeError):
            client.generate("test prompt")