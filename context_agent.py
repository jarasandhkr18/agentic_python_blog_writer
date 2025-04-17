import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")

def gather_context(topic: str, subtopics: list) -> dict:
    """
    Fetches contextual data like recent news articles for the blog topic.
    
    Args:
        topic (str): Main topic of the blog
        subtopics (list): List of subtopics from topic analyzer
        
    Returns:
        dict: Context data including news articles
    """
    context_data = {
        "news_articles": [],
    }

    # Build query string
    query = quote(topic)

    try:
        print("Fetching recent news...")
        url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q={query}&language=en"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "results" in data:
            articles = data["results"][:5]  # limit to 5 articles
            context_data["news_articles"] = [
                {
                    "title": article.get("title"),
                    "link": article.get("link"),
                    "description": article.get("description")
                } for article in articles
            ]

    except Exception as e:
        print(f"NewsData fetch failed: {e}")

    return context_data
