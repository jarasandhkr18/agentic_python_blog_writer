import argparse
from topic_analyzer import analyze_topic
from context_agent import gather_context
from writing_agent import generate_blog
from seo_agent import generate_seo_metadata
from export_agent import export_blog_and_metadata as export_blog
import textstat
import time

def main():
    parser = argparse.ArgumentParser(description="Agentic Blog Writer")
    parser.add_argument("topic", type=str, help="Main topic for the blog")
    parser.add_argument("--tone", type=str, default="educational", help="Tone of the blog (options: educational, formal, conversational, persuasive, technical, creative, humorous, inspirational)")
    parser.add_argument("--batch", type=str, help="Path to a text file with multiple blog topics (one per line)")
    
    args = parser.parse_args()
    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            topics = [line.strip() for line in f if line.strip()]
    elif args.topic:
        topics = [args.topic]
    else:
        print("Please provide a topic or a --batch file.")
        return

    tone = args.tone
    for topic in topics:
        print(f"\nGenerating blog for topic: '{topic}' with tone: '{tone}'...\n")
        start_time = time.time()

        # 1. Analyze Topic
        subtopics = analyze_topic(topic)
        subtopics = subtopics[:2]  # Limit to 2 to stay within Gemini free-tier rate limits
        print(f"Subtopics: {subtopics}")

        # 2. Gather Research Context
        context = gather_context(topic, subtopics)
        print(f"Context and Research Collected.\n")

        # 3. Generate Blog Content
        blog_md = generate_blog(topic, subtopics, context, tone)
        print(f"Blog content generated.\n")

        # 4. SEO Metadata
        metadata = generate_seo_metadata(topic, blog_md)

        # SAFETY CHECK
        if not isinstance(metadata, dict):
            print("Metadata generation failed. Using fallback metadata.")
            metadata = {
                "title": topic,
                "description": f"A blog about {topic}",
                "keywords": topic.lower().split(),
                "estimated_reading_time": "3 min read",
                "slug": topic.replace(" ", "-").lower()
            }

        # 5. Export to Files
        export_blog(blog_md, metadata, output_dir="output")
        print(f"Blog and metadata exported.\n")

        # Blog readability score
        readability_score = textstat.flesch_kincaid_grade(blog_md)
        print(f"Readability (Flesch-Kincaid Grade Level): {readability_score}")

        # Blog ease score
        ease_score = textstat.flesch_reading_ease(blog_md)
        print(f"Reading Ease Score: {ease_score}")

        # Summary
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        print(f"Done in {duration} seconds.")
        print(f"Output saved in /output directory.\n")
        print(f"Readability Grade (Flesch-Kincaid): {readability_score}")
        print(f"Reading Ease Score: {ease_score}")

if __name__ == "__main__":
    main()
