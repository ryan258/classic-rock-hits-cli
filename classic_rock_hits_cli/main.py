import os
import click
import logging
from typing import Dict, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI

# 🛠️ Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 🌍 Load environment variables from .env file
load_dotenv()

# 🔑 Get API details from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 🤖 Set up OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

class ClassicRockHits(BaseModel):
    classic_rock_artists: Dict[str, List[str]] = Field(..., alias="classic_rock_artists")

def get_classic_rock_hits_prompt(year: int) -> str:
    """
    📝 Generate an enhanced prompt for querying classic rock hits.
    """
    prompt = f"""As a music historian specializing in classic rock, provide information about the top 10 rock artists who were active or particularly influential in {year}, along with their most popular or significant songs released in {year}. Please follow these guidelines:

    1. Focus on artists who were releasing music, touring, or having a significant impact on the music scene in {year}.
    2. For each artist, list their most popular or influential songs, from {year}, when they were released.
    3. Ensure the artists and songs are accurately associated with the rock genre.
    4. Format your response as a JSON object with the following structure:
       {{
         "classic_rock_artists": {{
           "Artist Name 1": ["Song 1", "Song 2", "Song 3", "Song 4", "Song 5", ...],
           "Artist Name 2": ["Song 1", "Song 2", "Song 3", "Song 4", "Song 5", ...],
           ...

         }}
       }}

    Remember to focus on {year} for artist selection and include their top hits from {year} in their career."""

    return prompt

def get_classic_rock_hits(year: int) -> ClassicRockHits:
    """
    🎸 Get classic rock hits for a specific year using the OpenAI API with structured outputs.
    """
    logger.debug(f"Getting classic rock hits for year {year}")
    prompt = get_classic_rock_hits_prompt(year)
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a helpful music historian specializing in classic rock. Provide responses in JSON format."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        
        # Log the raw response for debugging
        logger.debug(f"Raw API response: {completion.choices[0].message.content}")
        
        # Parse the response into our Pydantic model
        hits_data = ClassicRockHits.model_validate_json(completion.choices[0].message.content)
        logger.debug(f"🔍 Parsed response: {hits_data}")
        
        return hits_data
    except Exception as e:
        logger.error(f"❌ Error in get_classic_rock_hits: {str(e)}")
        raise

def format_as_markdown(year: int, data: ClassicRockHits) -> str:
    """
    📊 Format the classic rock hits data as a markdown string.
    """
    logger.debug("Formatting data as markdown")
    markdown = f"# 🎵 Classic Rock Hits from {year}\n\n"
    
    markdown += "⚠️ **Disclaimer**: This information is generated for educational purposes only. "
    markdown += "All rights belong to their respective owners. Please respect copyright laws.\n\n"
    
    for artist, songs in data.classic_rock_artists.items():
        markdown += f"## 🎤 {artist}\n\n"
        for song in songs:
            markdown += f"- 🎶 {song}\n"
        markdown += "\n"
    
    return markdown

@click.command()
@click.option('--year', prompt='Enter the year', help='The year to get classic rock hits for', type=int)
def main(year: int):
    """
    🚀 Main function to run the Classic Rock Hits CLI application.
    """
    try:
        click.echo(f"🔍 Fetching classic rock hits for {year}...")
        hits_data = get_classic_rock_hits(year)
        
        markdown_output = format_as_markdown(year, hits_data)
        
        click.echo("\n🎵 Classic Rock Hits:")
        click.echo(markdown_output)
        
        # 💾 Save the output to a file
        filename = f"classic_rock_hits_{year}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        click.echo(click.style(f"\n✅ Output saved to {filename}", fg='green'))
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        click.echo(click.style(f"❌ An unexpected error occurred: {str(e)}", fg='red'))

if __name__ == '__main__':
    main()