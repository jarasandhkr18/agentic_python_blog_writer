import os
import json
from datetime import datetime
from utils import slugify

def save_blog_to_md(blog_content: str, topic: str, output_dir: str) -> str:
    """
    Save the generated blog content into a markdown (.md) file.

    Args:
        blog_content (str): Full blog post in markdown format
        topic (str): The blog topic (used for file naming)
        output_dir (str): Directory to save the file
    
    Returns:
        str: File path of the saved blog
    """
    # Create folder structure
    os.makedirs(output_dir, exist_ok=True)

    # Generate file name based on the topic and current date
    file_name = f"{datetime.now().strftime('%Y-%m-%d')}-{slugify(topic)}.md"
    file_path = os.path.join(output_dir, file_name)

    # Write to the markdown file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(blog_content)

    
    print(f"✅ Blog saved as {file_path}")
    return file_path

def save_metadata_to_json(metadata: dict, output_dir: str) -> str:
    """
    Save the SEO metadata into a JSON file.

    Args:
        metadata (dict): SEO metadata to be saved
        output_dir (str): Directory to save the file
    
    Returns:
        str: File path of the saved metadata
    """
    # Create folder structure
    os.makedirs(output_dir, exist_ok=True)

    # Generate file name based on current date
    file_name = f"{datetime.now().strftime('%Y-%m-%d')}-metadata.json"
    file_path = os.path.join(output_dir, file_name)

    # Write to the JSON file
    with open(file_path, "w") as json_file:
        json.dump(metadata, json_file, indent=4)

    print(f"✅ Metadata saved as {file_path}")
    return file_path

def export_blog_and_metadata(blog_content: str, metadata: dict, output_dir: str) -> dict:
    """
    Save both the blog and metadata.

    Args:
        blog_content (str): Full blog content in markdown format
        metadata (dict): SEO metadata to be saved
        output_dir (str): Directory to save both files
    
    Returns:
        dict: File paths for both blog and metadata
    """
    blog_file = save_blog_to_md(blog_content, metadata['title'], output_dir)
    metadata_file = save_metadata_to_json(metadata, output_dir)

    return {"blog_file": blog_file, "metadata_file": metadata_file}
