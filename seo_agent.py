import re
import math
from gemini_client import call_gemini
from utils import get_related_keywords

def estimate_reading_time(text: str) -> str:
    words = len(text.split())
    minutes = max(1, math.ceil(words / 200))
    return f"{minutes} min read"

def slugify(title: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

def generate_seo_metadata(topic: str, blog_md: str) -> dict:
    print("🧠 Generating SEO metadata...")

    prompt = f"""Generate SEO metadata for a blog titled '{topic}'.\nRespond in the format:\n\nTitle: [Your SEO-friendly title]\nDescription: [A meta description under 160 characters]\nKeywords: [Comma-separated keywords or a list]"""

    response = call_gemini(prompt)

    if not response or not isinstance(response, str):
        return {
            "title": topic,
            "description": f"Learn more about {topic}",
            "keywords": topic.lower().split(),
            "estimated_reading_time": estimate_reading_time(blog_md),
            "slug": slugify(topic)
        }

    title_match = re.search(r"Title:\s*(.*)", response)
    description_match = re.search(r"Description:\s*(.*)", response)
    keywords_match = re.search(r"Keywords:\s*(.*)", response)

    title = title_match.group(1).strip() if title_match else topic
    description = description_match.group(1).strip() if description_match else "Learn more about " + topic
    raw_keywords = keywords_match.group(1).strip() if keywords_match else ""

    if raw_keywords.startswith("[") and raw_keywords.endswith("]"):
        raw_keywords = raw_keywords.strip("[]").replace('"', '').replace("'", "")
        keywords = [k.strip() for k in raw_keywords.split(",")]
    else:
        keywords = [k.strip() for k in raw_keywords.split(",") if k.strip()]

    # Enhance keywords with Datamuse
    datamuse_keywords = get_related_keywords(topic)
    final_keywords = list(set(keywords + datamuse_keywords))

    metadata = {
        "title": title,
        "description": description[:160],
        "keywords": final_keywords,
        "estimated_reading_time": estimate_reading_time(blog_md),
        "slug": slugify(title)
    }

    return metadata
