# Agentic Python Blog Writer

A smart, agent-based Python application that generates a complete SEO-optimized blog post using Gemini and public APIs — available via CLI or web interface.

---

## Features

- AI-generated blog content using Gemini
- Real-time news injection using NewsData.io
- Semantic SEO keywords via Datamuse
- Inspirational quote from Quotable.io
- Tone customization (e.g. educational, formal, creative)
- Exports blog in .md and metadata in .json
- Calculates Flesch-Kincaid readability score
- Batch mode for generating multiple blogs at once
- Streamlit web interface for non-technical use

---

## How to Run (CLI)

Basic command:

```bash
python main.py "Your Blog Topic Here" --tone educational
```

Example:

```bash
python main.py "How Python is used in AI" --tone educational
```

Supported tone options:  
educational, formal, creative, conversational, technical, persuasive, humorous, inspirational

---

## Batch Mode (Multiple Topics)

Create a text file (e.g. topics.txt) with one blog topic per line:

```txt
How AI is transforming education
Applications of Python in healthcare
The impact of AI on mental health
```

Then run:

```bash
python main.py --batch topics.txt --tone formal
```

---

## Readability Score

Each blog is analyzed for reading difficulty using the Flesch-Kincaid Grade Level, shown in the CLI summary (e.g., “Readability Grade: 8.2”).

---

## Run via Streamlit Web App

Use a friendly web interface to generate blogs without touching code.

Launch the app:

```bash
streamlit run streamlit_app.py
```

You can:

- Enter a topic and tone
- View live progress
- See the blog and metadata
- Download generated .md and .json files

---

## Setup Instructions

1. Clone the repo:

```bash
git clone https://github.com/jarasandhkr18/agentic_python_blog_writer.git
cd agentic_python_blog_writer
```

2. Create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate   # On macOS/Linux: source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your API keys to .env:

```env
GEMINI_API_KEY=your_gemini_api_key_here
NEWSDATA_API_KEY=your_newsdata_api_key_here
```

(No key required for Datamuse or Quotable.io)

---

## Example Output Files

Markdown file:  
output/2025-04-17-python-in-ai-how-it-powers-artificial-intelligence-machine-learning.md

Metadata file:  
output/2025-04-17-metadata.json

---

## APIs Used

- [Gemini (Google AI)](https://ai.google.dev)
- [NewsData.io](https://newsdata.io)
- [Datamuse API](https://www.datamuse.com/api/)
- [Quotable.io](https://github.com/lukePeavey/quotable)
- [textstat (for readability)](https://pypi.org/project/textstat/)

---
