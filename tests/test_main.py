import pytest
from unittest.mock import patch, MagicMock
from classic_rock_hits_cli.main import query_ai_model, get_classic_rock_hits, format_as_markdown, parse_ai_response

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

def test_parse_ai_response_json():
    json_response = '{"The Beatles": ["Hey Jude", "Let It Be"]}'
    result = parse_ai_response(json_response)
    assert isinstance(result, dict)
    assert "The Beatles" in result

def test_parse_ai_response_python_literal():
    python_literal = "{'The Beatles': ['Hey Jude', 'Let It Be']}"
    result = parse_ai_response(python_literal)
    assert isinstance(result, dict)
    assert "The Beatles" in result

def test_parse_ai_response_invalid():
    invalid_response = "This is not a valid JSON or Python literal"
    result = parse_ai_response(invalid_response)
    assert result is None

def test_get_classic_rock_hits(mock_response):
    with patch('classic_rock_hits_cli.main.query_ai_model') as mock_query:
        with patch('classic_rock_hits_cli.main.parse_ai_response') as mock_parse:
            mock_query.return_value = "Raw AI response"
            mock_parse.return_value = mock_response
            
            result = get_classic_rock_hits(1970)
            assert isinstance(result, dict)
            assert "The Beatles" in result
            assert "Led Zeppelin" in result

def test_get_classic_rock_hits_error():
    with patch('classic_rock_hits_cli.main.query_ai_model') as mock_query:
        with patch('classic_rock_hits_cli.main.parse_ai_response') as mock_parse:
            mock_query.return_value = "Raw AI response"
            mock_parse.return_value = None
            
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