import pytest
from unittest.mock import patch, MagicMock
from classic_rock_hits_cli.main import query_ai_model, get_classic_rock_hits, format_as_markdown

@pytest.fixture
def mock_response():
    return {
        "The Beatles": ["Hey Jude", "Let It Be", "Yesterday", "Come Together", "Here Comes the Sun"],
        "Led Zeppelin": ["Stairway to Heaven", "Kashmir", "Whole Lotta Love", "Black Dog", "Immigrant Song"]
    }

def test_query_ai_model():
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"response": "Test response"}
        
        result = query_ai_model("Test prompt")
        assert result == "Test response"

def test_query_ai_model_error():
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 500
        
        result = query_ai_model("Test prompt")
        assert "Error" in result

def test_get_classic_rock_hits(mock_response):
    with patch('classic_rock_hits_cli.main.query_ai_model') as mock_query:
        mock_query.return_value = '{"The Beatles": ["Hey Jude", "Let It Be"], "Led Zeppelin": ["Stairway to Heaven", "Kashmir"]}'
        
        result = get_classic_rock_hits(1970)
        assert isinstance(result, dict)
        assert "The Beatles" in result
        assert "Led Zeppelin" in result

def test_get_classic_rock_hits_error():
    with patch('classic_rock_hits_cli.main.query_ai_model') as mock_query:
        mock_query.return_value = 'Invalid JSON'
        
        result = get_classic_rock_hits(1970)
        assert "error" in result

def test_format_as_markdown(mock_response):
    year = 1970
    result = format_as_markdown(year, mock_response)
    assert f"# Classic Rock Hits from {year}" in result
    assert "## The Beatles" in result
    assert "- Hey Jude" in result
    assert "## Led Zeppelin" in result
    assert "- Stairway to Heaven" in result