# Classic Rock Hits CLI

Discover the greatest hits of classic rock from any year with the power of AI! This CLI application uses both local (Llama) and cloud-based (GPT-4) AI models to generate lists of top classic rock artists and their hit songs for any given year.

## 🎸 Features

- Fetch classic rock hits for any specified year
- Choose between local Llama model or OpenAI's GPT-4 for generation
- Output results in beautifully formatted Markdown
- Save results to a file for easy sharing and reference
- Robust error handling and retry mechanism for API calls
- Easy-to-use command-line interface

## 🚀 Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/classic-rock-hits-cli.git
   cd classic-rock-hits-cli
   ```

2. Install Poetry if you haven't already:

   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install project dependencies:

   ```
   poetry install
   ```

4. Set up your environment variables by creating a `.env` file in the project root:
   ```
   API_URL=http://localhost:11434/api/generate
   MODEL_NAME=llama3.1:latest
   PORT=3000
   OPENAI_MODEL_NAME=gpt-4o-mini-2024-07-18
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   Replace `your_openai_api_key_here` with your actual OpenAI API key.

## 🎵 Usage

Run the CLI application using Poetry:

```
poetry run python -m classic_rock_hits_cli.main --model [llama|gpt4]
```

You'll be prompted to enter a year, and the application will generate a list of classic rock hits for that year using the specified AI model.

### Examples

1. Using the local Llama model:

   ```
   poetry run python -m classic_rock_hits_cli.main --model llama
   ```

2. Using OpenAI's GPT-4 model:
   ```
   poetry run python -m classic_rock_hits_cli.main --model gpt4
   ```

The results will be displayed in the console and saved to a Markdown file in your current directory.

## 🛠️ Development

To set up the development environment:

1. Clone the repository (if you haven't already)
2. Install dependencies: `poetry install`
3. Activate the virtual environment: `poetry shell`
4. Run tests: `pytest`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to the Anthropic team for the Llama model
- Thanks to OpenAI for the GPT-4 model
- Shout out to all the classic rock artists who've given us such great music!

## 🎉 Enjoy the music!

Rock on and enjoy discovering (or rediscovering) classic hits from any era!
