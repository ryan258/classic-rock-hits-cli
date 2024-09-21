import os
import sys
import click
import logging
import json
from typing import Dict, List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set in environment variables.")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

class ClassicRockHits(BaseModel):
    classic_rock_artists: Dict[str, List[str]]

def query_ai_model(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful music historian specializing in classic rock. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error querying AI model: {str(e)}")
        raise

def parse_ai_response(response: str) -> Optional[Dict[str, List[str]]]:
    try:
        # Remove any JSON code block formatting if present
        if response.startswith('```') and response.endswith('```'):
            response = response.strip('`').strip()
        
        parsed = json.loads(response)
        if "classic_rock_artists" in parsed:
            return parsed["classic_rock_artists"]
        return parsed
    except json.JSONDecodeError:
        logger.error(f"Failed to parse AI response: {response}")
        return None

def get_classic_rock_hits(year: int) -> Dict[str, List[str]]:
    logger.info(f"Getting classic rock hits for year {year}")
    prompt = f"""Provide information about the top 10 rock artists who were active or particularly influential in {year}, 
    along with their most popular or significant songs released in {year}. 
    Format the response as a JSON object with the structure: 
    {{"classic_rock_artists": {{"Artist Name": ["Song 1", "Song 2"], ...}}}}
    Ensure that the response is valid JSON and matches this exact structure. Do not include any markdown formatting or code block indicators."""
    
    try:
        raw_response = query_ai_model(prompt)
        parsed_response = parse_ai_response(raw_response)
        if parsed_response:
            return parsed_response
        else:
            raise ValueError(f"Failed to parse AI response: {raw_response}")
    except Exception as e:
        logger.error(f"Error getting classic rock hits: {str(e)}")
        return {"error": str(e)}

def format_as_markdown(year: int, data: Dict[str, List[str]]) -> str:
    logger.info("Formatting data as markdown")
    markdown = f"# Classic Rock Hits from {year}\n\n"
    for artist, songs in data.items():
        markdown += f"## {artist}\n"
        for song in songs:
            markdown += f"- {song}\n"
        markdown += "\n"
    return markdown

def save_to_file(content: str, year: int):
    filename = f"classic_rock_hits_{year}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Data saved to {filename}")

@click.command()
def main():
    year = click.prompt("Enter the year", type=int)
    click.echo(f"🔍 Fetching classic rock hits for {year}...")
    
    try:
        hits_data = get_classic_rock_hits(year)
        if "error" in hits_data:
            click.echo(f"An error occurred: {hits_data['error']}")
        else:
            formatted_data = format_as_markdown(year, hits_data)
            click.echo(formatted_data)
            save_to_file(formatted_data, year)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()