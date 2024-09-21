import pytest
import json
import os
import sys
from unittest.mock import patch, MagicMock
from openai import OpenAIError
from classic_rock_hits_cli.main import query_ai_model, get_classic_rock_hits, format_as_markdown, parse_ai_response, save_to_file

@pytest.fixture
def mock_response():
    return {
        "The Beatles": ["Hey Jude", "Let It Be", "Yesterday", "Come Together", "Here Comes the Sun"],
        "Led Zeppelin": ["Stairway to Heaven", "Kashmir", "Whole Lotta Love", "Black Dog", "Immigrant Song"]
    }

def test_query_ai_model_success():
    with patch('openai.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content = '{"response": "Test response"}'
        
        result = query_ai_model("Test prompt")
        assert result == '{"response": "Test response"}'

def test_query_ai_model_error():
    with patch('openai.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = OpenAIError("API Error")
        
        with pytest.raises(OpenAIError):
            query_ai_model("Test prompt")

@pytest.mark.parametrize("input_json,expected", [
    ('{"classic_rock_artists": {"The Beatles": ["Hey Jude"]}}', {"The Beatles": ["Hey Jude"]}),
    ('{"The Beatles": ["Hey Jude"]}', {"The Beatles": ["Hey Jude"]}),
    ('Invalid JSON', None)
])
def test_parse_ai_response(input_json, expected):
    result = parse_ai_response(input_json)
    assert result == expected

def test_get_classic_rock_hits_success(mock_response):
    with patch('classic_rock_hits_cli.main.query_ai_model') as mock_query:
        mock_query.return_value = json.dumps({"classic_rock_artists": mock_response})
        
        result = get_classic_rock_hits(1970)
        assert result == mock_response

def test_get_classic_rock_hits_api_error():
    with patch('classic_rock_hits_cli.main.query_ai_model') as mock_query:
        mock_query.side_effect = OpenAIError("API Error")
        
        result = get_classic_rock_hits(1970)
        assert "error" in result

def test_get_classic_rock_hits_parsing_error():
    with patch('classic_rock_hits_cli.main.query_ai_model') as mock_query:
        mock_query.return_value = "Invalid JSON"
        
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

@pytest.mark.parametrize("year,content", [
    (1970, "Test content"),
    (1980, "Another test content")
])
def test_save_to_file(tmp_path, year, content):
    save_to_file(content, year, directory=str(tmp_path))
    file_path = tmp_path / f"classic_rock_hits_{year}.md"
    assert file_path.read_text() == content

def test_main(mock_response):
    from classic_rock_hits_cli.main import main
    
    with patch('classic_rock_hits_cli.main.click.prompt', return_value=1970), \
         patch('classic_rock_hits_cli.main.get_classic_rock_hits', return_value=mock_response), \
         patch('classic_rock_hits_cli.main.click.echo') as mock_echo, \
         patch('classic_rock_hits_cli.main.save_to_file') as mock_save, \
         patch.object(sys, 'exit') as mock_exit:
        
        main()
        
        mock_echo.assert_called()
        mock_save.assert_called()
        mock_exit.assert_called_once_with(0)