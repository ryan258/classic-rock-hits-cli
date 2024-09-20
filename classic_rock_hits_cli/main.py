import os
import click
import requests
from dotenv import load_dotenv
import json
import ast
import logging
from typing import Dict, List, Union, Tuple
import re
from functools import wraps
import time

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get API details from environment variables
API_URL = os.getenv('API_URL', 'http://localhost:11434/api/generate')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.1:latest')

def retry(exceptions, tries=4, delay=3, backoff=2):
    """
    Retry decorator with exponential backoff.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"{func.__name__} failed. Retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry((requests.RequestException, requests.ConnectionError), tries=3, delay=1)
def query_ai_model(prompt: str) -> str:
    """
    Send a query to the local Ollama model and return the response.
    """
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(API_URL, json=data, timeout=30)
    response.raise_for_status()
    return response.json()['response']

def extract_dict_from_response(response: str) -> Tuple[Union[Dict[str, List[str]], None], str]:
    """
    Extract a Python dictionary from the AI response.
    """
    # First, try to parse the entire response as JSON
    try:
        return json.loads(response), "json"
    except json.JSONDecodeError:
        pass

    # Next, try to find and evaluate a Python dictionary in the response
    try:
        # Find content between triple backticks
        code_block_match = re.search(r'```python\s*(.*?)```', response, re.DOTALL)
        if code_block_match:
            code_block = code_block_match.group(1)
            # Extract the dictionary assignment
            dict_match = re.search(r'=\s*(\{.*\})', code_block, re.DOTALL)
            if dict_match:
                dict_str = dict_match.group(1)
                return ast.literal_eval(dict_str), "code_block"
    except (SyntaxError, ValueError):
        pass

    # If all else fails, try to extract key-value pairs
    pattern = r'(["\w\s]+)"?\s*:\s*\[((?:["\w\s]+,?\s*)+)\]'
    matches = re.findall(pattern, response)
    if matches:
        result = {}
        for artist, songs in matches:
            artist = artist.strip().strip('"')
            songs = [s.strip().strip('"') for s in songs.split(',')]
            result[artist] = songs[:5]  # Limit to top 5 songs
        return result, "extracted"

    return None, "failed"

def get_classic_rock_hits(year: int) -> Dict[str, Union[List[str], str]]:
    """
    Get classic rock hits for a specific year using the AI model.
    """
    prompt = (f"Provide a Python dictionary of the top 10 classic rock artists from {year} "
              f"and their top 5 hits of all time. The keys should be artist names and the "
              f"values should be lists of their top hits. Format your response as a Python code block.")
    
    try:
        response = query_ai_model(prompt)
        logger.debug(f"Raw AI response: {response[:500]}...")  # Log first 500 chars for brevity
        
        parsed_response, method = extract_dict_from_response(response)
        logger.debug(f"Parsed response using {method} method: {parsed_response}")
        
        if parsed_response is None:
            return {"error": f"Unable to parse AI response. Raw response: {response[:100]}..."}
        
        return parsed_response
    except Exception as e:
        logger.error(f"Error in get_classic_rock_hits: {str(e)}")
        return {"error": f"An error occurred: {str(e)}"}

def format_as_markdown(year: int, data: Dict[str, List[str]]) -> str:
    """
    Format the classic rock hits data as a markdown string.
    """
    markdown = f"# Classic Rock Hits from {year}\n\n"
    
    for artist, songs in data.items():
        markdown += f"## {artist}\n\n"
        for song in songs:
            markdown += f"- {song}\n"
        markdown += "\n"
    
    return markdown

@click.command()
@click.option('--year', prompt='Enter the year', help='The year to get classic rock hits for', type=int)
def main(year: int):
    """
    Main function to run the Classic Rock Hits CLI application.
    """
    click.echo(f"Fetching classic rock hits for {year}...")
    hits_data = get_classic_rock_hits(year)
    
    if isinstance(hits_data, dict) and "error" in hits_data:
        click.echo(click.style(f"Error: {hits_data['error']}", fg='red'))
        return
    
    if not hits_data:
        click.echo(click.style("No data returned from the AI model.", fg='yellow'))
        return
    
    markdown_output = format_as_markdown(year, hits_data)
    
    click.echo("\nClassic Rock Hits:")
    click.echo(markdown_output)
    
    # Save the output to a file
    filename = f"classic_rock_hits_{year}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_output)
    click.echo(click.style(f"\nOutput saved to {filename}", fg='green'))

if __name__ == '__main__':
    main()