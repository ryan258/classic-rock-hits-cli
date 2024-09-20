# Classic Rock Hits CLI

Discover the greatest hits of classic rock from any year with the power of AI! This CLI application uses OpenAI's GPT-4 model to generate lists of top classic rock artists and their hit songs for any given year.

## 🎸 Features

- Fetch classic rock hits for any specified year
- Use OpenAI's GPT-4 model for accurate and contextual information
- Output results in beautifully formatted Markdown
- Save results to a file for easy sharing and reference
- Robust error handling and logging
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
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   Replace `your_openai_api_key_here` with your actual OpenAI API key.

## 🎵 Usage

Run the CLI application using Poetry:

```
poetry run python -m classic_rock_hits_cli.main
```

You'll be prompted to enter a year, and the application will generate a list of classic rock hits for that year using OpenAI's GPT-4 model.

### Example

```
poetry run python -m classic_rock_hits_cli.main
Enter the year: 1969
🔍 Fetching classic rock hits for 1969...
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

- Thanks to OpenAI for providing the GPT-4 model
- Shout out to all the classic rock artists who've given us such great music!

## 🎉 Enjoy the music!

Rock on and enjoy discovering (or rediscovering) classic hits from any era!
