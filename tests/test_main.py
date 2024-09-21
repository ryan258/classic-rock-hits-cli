import pytest
from unittest.mock import patch, MagicMock
from classic_rock_hits_cli.main import query_ai_model, get_classic_rock_hits, format_as_markdown, parse_ai_response, save_to_file, BandInfo, main

@pytest.fixture
def mock_response():
    return {
        "The Beatles": BandInfo(
            songs=["Hey Jude", "Let It Be"],
            career_phase="Late career, experimenting with new sounds"
        ),
        "Led Zeppelin": BandInfo(
            songs=["Whole Lotta Love", "Ramble On"],
            career_phase="Early career, establishing their heavy blues-rock sound"
        )
    }

def test_query_ai_model_success():
    with patch('openai.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content = '```json\n{"response": "Test response"}\n```'
        
        result = query_ai_model("Test prompt")
        assert '```json' in result
        assert 'response' in result

# def test_query_ai_model_error():
#     with patch('openai.OpenAI') as mock_openai:
#         mock_client = MagicMock()
#         mock_openai.return_value = mock_client
#         mock_client.chat.completions.create.side_effect = Exception("API Error")

#         result = query_ai_model("Test prompt")

#         # Check if the result is a valid JSON string containing a response
#         try:
#             import json
#             parsed_result = json.loads(result)
#             assert "response" in parsed_result
#             assert isinstance(parsed_result["response"], str)
#             assert len(parsed_result["response"]) > 0
#         except json.JSONDecodeError:
#             pytest.fail(f"Result is not a valid JSON string: {result}")
#         except AssertionError as e:
#             pytest.fail(f"Unexpected result structure: {e}")

#         # Print the result for debugging
#         print(f"query_ai_model result: {result}")

def test_parse_ai_response():
    input_json = '{"classic_rock_artists": {"The Beatles": {"songs": ["Hey Jude"], "career_phase": "Late career"}}}'
    expected = {"The Beatles": BandInfo(songs=["Hey Jude"], career_phase="Late career")}
    result = parse_ai_response(input_json)
    assert result == expected

def test_get_classic_rock_hits_success(mock_response):
    with patch('classic_rock_hits_cli.main.query_ai_model') as mock_query:
        mock_query.return_value = '{"classic_rock_artists": {"The Beatles": {"songs": ["Hey Jude", "Let It Be"], "career_phase": "Late career, experimenting with new sounds"}, "Led Zeppelin": {"songs": ["Whole Lotta Love", "Ramble On"], "career_phase": "Early career, establishing their heavy blues-rock sound"}}}'
        
        result = get_classic_rock_hits(1969)
        assert result == mock_response

def test_get_classic_rock_hits_api_error():
    with patch('classic_rock_hits_cli.main.query_ai_model') as mock_query:
        mock_query.side_effect = Exception("API Error")
        
        result = get_classic_rock_hits(1970)
        assert "error" in result

def test_format_as_markdown(mock_response):
    year = 1969
    result = format_as_markdown(year, mock_response)
    assert f"# 🎸 Classic Rock Hits from {year}" in result
    assert "## 🎤 The Beatles" in result
    assert "*Career Phase: Late career, experimenting with new sounds*" in result
    assert "- 🎵 Hey Jude" in result

def test_save_to_file():
    content = "Test content"
    year = 1970
    file_path = f"classic_rock_hits_{year}.md"
    
    with patch('builtins.open', new_callable=MagicMock) as mock_file:
        save_to_file(content, year)
        mock_file.assert_called_once_with(file_path, "w", encoding="utf-8")

def test_main_success():
    with patch('classic_rock_hits_cli.main.click.prompt', return_value=1969), \
         patch('classic_rock_hits_cli.main.get_classic_rock_hits') as mock_get_hits, \
         patch('classic_rock_hits_cli.main.click.echo') as mock_echo, \
         patch('classic_rock_hits_cli.main.save_to_file') as mock_save, \
         patch('sys.exit') as mock_exit:
        
        mock_get_hits.return_value = {"The Beatles": BandInfo(songs=["Hey Jude"], career_phase="Late career")}
        
        main()
        mock_echo.assert_any_call("🔍 Fetching classic rock hits for 1969...")
        mock_save.assert_called_once()
        mock_exit.assert_called_once_with(0)

def test_main_error():
    with patch('classic_rock_hits_cli.main.click.prompt', return_value=1970), \
         patch('classic_rock_hits_cli.main.get_classic_rock_hits', return_value={"error": "API Error"}), \
         patch('classic_rock_hits_cli.main.click.echo') as mock_echo, \
         patch('sys.exit') as mock_exit:
        
        main()
        mock_echo.assert_any_call("🔍 Fetching classic rock hits for 1970...")
        mock_echo.assert_any_call("❌ An error occurred: API Error")
        mock_exit.assert_called_once_with(0)