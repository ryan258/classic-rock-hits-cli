import os
import click
import requests
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get API details from environment variables
API_URL = os.getenv('API_URL')
MODEL_NAME = os.getenv('MODEL_NAME')

def query_ai_model(prompt):
    """
    Send a query to the local Ollama model and return the response.
    """
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(API_URL, json=data)
    
    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Error: Unable to get response from AI model. Status code: {response.status_code}"

def get_classic_rock_hits(year):
    """
    Get classic rock hits for a specific year using the AI model.
    """
    prompt = f"Give me a list of the top 10 classic rock artists from {year} and their top 5 hits of all time. Format the response as a Python dictionary."
    
    response = query_ai_model(prompt)
    
    try:
        data = json.loads(response)
        return data
    except json.JSONDecodeError:
        return {"error": "Unable to parse AI response into valid JSON"}

def format_as_markdown(year, data):
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
@click.option('--year', prompt='Enter the year', help='The year to get classic rock hits for')
def main(year):
    """
    Main function to run the Classic Rock Hits CLI application.
    """
    click.echo("Fetching classic rock hits...")
    hits_data = get_classic_rock_hits(year)
    
    if "error" in hits_data:
        click.echo(f"Error: {hits_data['error']}")
        return
    
    markdown_output = format_as_markdown(year, hits_data)
    
    click.echo("\nClassic Rock Hits:")
    click.echo(markdown_output)

if __name__ == '__main__':
    main()