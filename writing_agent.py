import os
import requests
from dotenv import load_dotenv
from gemini_client import call_gemini
from utils import get_random_quote
from utils import clean_text

load_dotenv()

def generate_blog(topic: str, subtopics: list, context: dict, tone: str = "educational") -> str:
    """
    Uses Gemini API to write a complete blog post in markdown format.

    Args:
        topic (str): Blog topic
        subtopics (list): List of H2 subtopics
        context (dict): News articles and extra content
        tone (str): Tone of writing (educational, formal, creative)

    Returns:
        str: Full blog content in Markdown
    """
    # Build context info
    news_context = ""
    if context.get("news_articles"):
        news_context = "\n\nRecent news articles:\n"
        for article in context["news_articles"]:
            news_context += f"- [{article['title']}]({article['link']}): {article['description']}\n"

    # Full content to assemble
    blog_md = ""

    # 1. Introduction
    intro_prompt = f"""Write an engaging introduction (100–150 words) for a blog titled '{topic}'.
Tone: {tone}.
Context: {news_context if news_context else 'N/A'}"""
    intro = call_gemini(intro_prompt)
    blog_md += f"# {topic}\n\n{intro}\n\n"

    # 2. Body Sections
    for heading in subtopics:
        section_prompt = f"""Write a detailed (200–300 words) blog section titled '{heading}'.
Tone: {tone}.
Context: {news_context if news_context else 'N/A'}"""
        section = call_gemini(section_prompt)
        section = clean_text(section.lstrip("#").strip())
        blog_md += f"## {heading}\n\n{section}\n\n"

    # 3. Conclusion
    conclusion_prompt = f"""Write a strong conclusion with a call-to-action for a blog on '{topic}'.
Tone: {tone}.
Context: {news_context if news_context else 'N/A'}"""
    conclusion = call_gemini(conclusion_prompt)
    quote = get_random_quote()
    blog_md += f"## Conclusion\n\n{conclusion}\n\n> Quote of the Day: \"{quote}\"\n"

    return blog_md
