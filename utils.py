import asyncio
import time
from functools import wraps
import aiohttp
import random
import re
import requests

# ----------------------------
# 🔁 Retry Decorator
# ----------------------------
def retry(max_retries=3, delay=2, backoff=2):
    """
    Retry decorator for sync functions.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tries = max_retries
            wait = delay
            while tries > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"⚠️ Error: {e}. Retrying in {wait}s...")
                    time.sleep(wait)
                    tries -= 1
                    wait *= backoff
            raise Exception(f"❌ Function {func.__name__} failed after {max_retries} attempts.")
        return wrapper
    return decorator

# ----------------------------
# ⚡ Async GET Request (for APIs like Datamuse or Quotable)
# ----------------------------
async def async_get(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    except Exception as e:
        print(f"⚠️ Async GET failed: {e}")
        return None

# ----------------------------
# 🚀 Run Multiple Async Calls
# ----------------------------
async def async_fetch_all(urls: list):
    async with aiohttp.ClientSession() as session:
        tasks = [async_get(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# ----------------------------
# ✂️ Text Cleaning (optional)
# ----------------------------
def clean_text(text: str) -> str:
    """
    Remove extra whitespace and Markdown formatting artifacts.
    """
    return ' '.join(text.replace("*", "").replace("_", "").split())

# ----------------------------
# 🧪 Random Quote Generator (Optional Stub)
# ----------------------------
def random_quote():
    return random.choice([
        "Knowledge is power.",
        "The only way to do great work is to love what you do.",
        "Simplicity is the soul of efficiency.",
        "Code is like humor. When you have to explain it, it’s bad."
    ])

# ----------------------------
# 🧹 Slugify text (for file names)
# ----------------------------
def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

# ----------------------------
# 🔤 Datamuse API for related keywords
# ----------------------------
def get_related_keywords(topic):
    url = f"https://api.datamuse.com/words?ml={topic}&max=10"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            words = response.json()
            return [w['word'] for w in words]
        else:
            print("❌ Failed to fetch from Datamuse")
            return []
    except Exception as e:
        print(f"❌ Datamuse error: {e}")
        return []

# ----------------------------
# 📜 Quotable.io random inspirational quote
# ----------------------------
def get_random_quote():
    try:
        response = requests.get("https://api.quotable.io/random?tags=inspirational|technology")
        if response.status_code == 200:
            return response.json().get("content")
        return random_quote()
    except Exception as e:
        print(f"❌ Quotable.io error: {e}")
        return random_quote()
