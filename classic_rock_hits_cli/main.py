import os
import sys
import click
import logging
import json
from typing import Dict, List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# 🎸 Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 🔑 Load environment variables
load_dotenv()

# 🔐 Check for OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logger.error("🚫 OPENAI_API_KEY is not set in environment variables.")
    sys.exit(1)

# 🤖 Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# 📊 Define data models
class BandInfo(BaseModel):
    songs: List[str]
    career_phase: str

class MusicHits(BaseModel):
    artists: Dict[str, BandInfo]

# 🎤 Query AI model
def query_ai_model(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 🚀 Using GPT-4 for better results
            messages=[
                {"role": "system", "content": "You are a helpful music historian specializing in classic rock. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"❌ Error querying AI model: {str(e)}")
        raise

# 🧠 Parse AI response
def parse_ai_response(response: str) -> Optional[Dict[str, BandInfo]]:
    try:
        # Remove any JSON code block formatting if present
        if response.startswith('```') and response.endswith('```'):
            response = response.strip('`').strip()
        
        parsed = json.loads(response)
        if "artists" in parsed:
            return {artist: BandInfo(**info) for artist, info in parsed["artists"].items()}
        return {artist: BandInfo(**info) for artist, info in parsed.items()}
    except json.JSONDecodeError:
        logger.error(f"❌ Failed to parse AI response: {response}")
        return None

def get_music_hits(year: int, genre: str) -> Dict[str, BandInfo]:
    logger.info(f"🔍 Getting {genre} hits for year {year}")
    prompt = f"""Provide information about the top 10 {genre} artists who were active or particularly influential in {year}, 
    along with their most popular or significant songs released in {year} and a brief description of their career phase during that year. 
    Format the response as a JSON object with the structure: 
    {{"artists": {{"Artist Name": {{"songs": ["Song 1", "Song 2", ...], "career_phase": "Brief description"}}, ...}}}}
    Ensure that the response is valid JSON and matches this exact structure. Do not include any markdown formatting or code block indicators."""
    
    try:
        raw_response = query_ai_model(prompt)
        parsed_response = parse_ai_response(raw_response)
        if parsed_response:
            return parsed_response
        else:
            raise ValueError(f"Failed to parse AI response: {raw_response}")
    except Exception as e:
        logger.error(f"❌ Error getting {genre} hits: {str(e)}")
        return {"error": str(e)}

def format_as_markdown(year: int, genre: str, data: Dict[str, BandInfo]) -> str:
    logger.info(f"📊 Formatting {genre} data as markdown")
    markdown = f"# 🎵 {genre.capitalize()} Hits from {year}\n\n"
    for artist, info in data.items():
        markdown += f"## 🎤 {artist}\n"
        markdown += f"*{info.career_phase}*\n\n"
        for song in info.songs:
            markdown += f"- 🎵 {song}\n"
        markdown += "\n"
    return markdown

def save_to_file(content: str, year: int, genre: str):
    filename = f"{genre.lower().replace(' ', '_')}_hits_{year}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"💾 Data saved to {filename}")

@click.command()
def main(test_mode=False):
    year = click.prompt("🎸 Enter the year", type=int)
    genre = click.prompt("🎵 Enter the genre (default: classic rock)", default="classic rock")
    click.echo(f"🔍 Fetching {genre} hits for {year}...")
    
    try:
        hits_data = get_music_hits(year, genre)
        if isinstance(hits_data, dict) and "error" in hits_data:
            click.echo(f"❌ An error occurred: {hits_data['error']}")
        else:
            formatted_data = format_as_markdown(year, genre, hits_data)
            click.echo(formatted_data)
            save_to_file(formatted_data, year, genre)
            click.echo(f"🎉 Successfully saved {genre} hits for {year}!")
    except Exception as e:
        click.echo(f"❌ An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()