# LiteratureReviewBot

Create a bot that scans pubmed literature and github for publications related to a topic and summarizes them in a table.

## Dependencies

You'll need to have an Ollama installed on your machine. You can download it by going [here](https://ollama.com/download). Once you have it installed you can download the LLama3.1 model by running the following command:

```bash
ollama pull llama3.1
```

Create a new virtual environment and install the dependencies by running the following commands:

```bash
conda create -n litrevbot python=3.12
pip install pipx
pipx install poetry
conda activate litrevbot
poetry install .
```

## Usage

To run the bot, you can use the following command:

```bash
conda activate litrevbot
python -m streamlit run app.py
```
