#Topic Analyzer.py
import re
def analyze_topic(topic: str) -> list:
    """
    Breaks a topic into subtopics using basic keyword patterning.
    More advanced methods (e.g., GPT/Gemini/NLP) can be plugged in later.
    
    Args:
        topic (str): The main blog topic.
        
    Returns:
        List[str]: A list of subtopic strings (H2 headings).
    """
    
    topic = topic.strip().lower()

    # Heuristics for basic topic decomposition (could be replaced with Gemini later)
    subtopics = []

    if "python" in topic and "ai" in topic:
        subtopics = [
            "Introduction to Python in AI",
            "Popular Python Libraries for AI (e.g., TensorFlow, PyTorch)",
            "Real-World Use Cases of Python in AI",
            "How Python Compares with Other AI Languages",
            "Getting Started: Python Tools & Resources for AI"
        ]
    elif "data science" in topic:
        subtopics = [
            "Introduction to Data Science",
            "Key Tools and Languages for Data Science",
            "Role of Python in Data Science",
            "Case Studies Using Python in Data Projects",
            "How to Start Learning Python for Data Science"
        ]
    else:
        # Fallback generic headings
        subtopics = [
            f"Understanding {topic.title()}",
            f"Why {topic.title()} Matters Today",
            f"Tools and Technologies in {topic.title()}",
            f"Use Cases of {topic.title()}",
            f"How to Get Started with {topic.title()}"
        ]
    
    return subtopics
