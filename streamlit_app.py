import streamlit as st
from topic_analyzer import analyze_topic
from context_agent import gather_context
from writing_agent import generate_blog
from seo_agent import generate_seo_metadata
from export_agent import export_blog_and_metadata
from utils import get_random_quote
from dotenv import load_dotenv
import textstat
import os
import time
import tempfile
import shutil
import json

load_dotenv()

st.set_page_config(page_title="Agentic Python Blog Writer")
st.title("Agentic Python Blog Writer")
st.markdown("Generate AI-powered blog posts with SEO metadata.")

option = st.radio("Choose input mode:", ("Single Topic", "Batch Mode"))

tone = st.selectbox("Choose tone", [
    "educational", "formal", "conversational", "creative", "technical", "inspirational"
])

if option == "Single Topic":
    topic = st.text_input("Enter blog topic")
    if st.button("Generate Blog") and topic:
        with st.spinner("Generating blog..."):
            start_time = time.time()

            subtopics = analyze_topic(topic)[:2]
            context = gather_context(topic, subtopics)
            blog_md = generate_blog(topic, subtopics, context, tone)
            metadata = generate_seo_metadata(topic, blog_md)

            if not isinstance(metadata, dict):
                st.error("Metadata generation failed.")
            else:
                files = export_blog_and_metadata(blog_md, metadata, output_dir="output")
                end_time = time.time()

                st.success("Blog generated!")
                st.markdown(f"Time taken: {round(end_time - start_time, 2)} seconds")
                st.markdown(f"Readability Grade: {textstat.flesch_kincaid_grade(blog_md)}")
                st.markdown(f"Quote of the Day: \n> {get_random_quote()}")
                st.markdown(f"Markdown File: `{files['blog_file']}`")
                st.markdown(f"Metadata JSON: `{files['metadata_file']}`")

                with st.expander("View Blog Markdown"):
                    st.markdown(blog_md)

                with st.expander("SEO Metadata"):
                    st.json(metadata)

                # Offer download buttons
                with open(files['blog_file'], "r", encoding="utf-8") as f:
                    st.download_button("Download Blog (.md)", f.read(), file_name=os.path.basename(files['blog_file']))

                with open(files['metadata_file'], "r", encoding="utf-8") as f:
                    st.download_button("Download Metadata (.json)", f.read(), file_name=os.path.basename(files['metadata_file']))

elif option == "Batch Mode":
    batch_input = st.text_area("Paste or type one topic per line:", height=200)
    topics = [line.strip() for line in batch_input.splitlines() if line.strip()]

    if st.button("Generate Blogs in Batch"):
        with st.spinner("Generating blogs..."):
            temp_dir = tempfile.mkdtemp()
            blog_files = []

            for topic in topics:
                st.markdown(f"---\n### Processing: `{topic}`")
                subtopics = analyze_topic(topic)[:2]
                context = gather_context(topic, subtopics)
                blog_md = generate_blog(topic, subtopics, context, tone)
                metadata = generate_seo_metadata(topic, blog_md)

                if not isinstance(metadata, dict):
                    metadata = {
                        "title": topic,
                        "description": f"A blog about {topic}",
                        "keywords": topic.lower().split(),
                        "estimated_reading_time": "3 min read",
                        "slug": topic.replace(" ", "-").lower()
                    }

                blog_file = os.path.join(temp_dir, metadata['slug'] + ".md")
                meta_file = os.path.join(temp_dir, metadata['slug'] + ".json")

                with open(blog_file, "w", encoding="utf-8") as bf:
                    bf.write(blog_md)

                with open(meta_file, "w", encoding="utf-8") as jf:
                    json.dump(metadata, jf, indent=4)

                blog_files.append((metadata['title'], blog_file, meta_file))

                st.success(f"Done: {metadata['title']}")

            st.markdown("---")
            st.markdown("Download All Files")

            for title, md_path, json_path in blog_files:
                with open(md_path, "r", encoding="utf-8") as f:
                    st.download_button(f"Download {title} (.md)", f.read(), file_name=os.path.basename(md_path))
                with open(json_path, "r", encoding="utf-8") as f:
                    st.download_button(f"Download {title} Metadata (.json)", f.read(), file_name=os.path.basename(json_path))
