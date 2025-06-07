#!/usr/bin/env python3
"""
SEO Article Generator
--------------------
This script generates SEO-optimized articles based on user-provided topics,
preferred length, and backlinks.
"""

import os
import json
import argparse
import time
import re
import random
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import google.generativeai as genai

class ArticleGenerator:
    """Main class for generating SEO-optimized articles."""
    
    # length presets
    LENGTHS = {
        "small": 800,
        "medium": 1500,
        "long": 2200
    }
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        """Initialize the article generator with API credentials.
        
        Args:
            api_key: Google AI API key
            model: Model name to use (default: gemini-1.5-pro)
        """
        self.api_key = api_key
        self.model = model
        
        # Configure API
        genai.configure(api_key=self.api_key)
        
        self.available_models = {
            "gemini-1.5-pro": "gemini-1.5-pro",
            "gemini-1.5-flash": "gemini-1.5-flash",
            "gemini-2.5-preview": "gemini-pro-latest"
        }
        
        # Set the model
        self.generation_model = genai.GenerativeModel(self.available_models.get(model, "gemini-1.5-pro"))
        
    def set_model(self, model_name: str) -> None:
        """Change the AI model being used.
        
        Args:
            model_name: Name of the model to use
        """
        if model_name in self.available_models:
            self.model = model_name
            self.generation_model = genai.GenerativeModel(self.available_models[model_name])
            print(f"Model changed to {model_name}")
        else:
            available = ", ".join(self.available_models.keys())
            print(f"Model {model_name} not available. Available models: {available}")
    
    def generate_filename(self, topic: str) -> str:
        """Generate a SEO-friendly filename based on the topic.
        
        Args:
            topic: The article topic
            
        Returns:
            A filename string with format topic-related-name.mdx
        """
        # Clean the topic for a friendly slug
        slug = re.sub(r'[^a-zA-Z0-9\s]', '', topic.lower())
        slug = re.sub(r'\s+', '-', slug)
        
        timestamp = int(time.time())
        
        return f"{slug}-{timestamp}.mdx"
    
    def generate_article_outline(self, topic: str, length_preference: str) -> str:
        """Generate an article outline based on the topic.
        
        Args:
            topic: The article topic
            length_preference: Preferred article length (small/medium/long)
            
        Returns:
            Article outline as string
        """
        prompt = f"""
        Create a detailed outline for an SEO-optimized article on "{topic}".
        This outline should include:
        1. A catchy, SEO-friendly title
        2. H2 and H3 headings that cover important aspects of the topic
        3. Key points to cover under each heading
        4. Questions the article should answer
        5. SEO keywords to incorporate
        
        The article will be {self.LENGTHS.get(length_preference.lower(), 1500)} words long.
        Structure the outline in markdown format.
        """
        
        response = self.generation_model.generate_content(prompt)
        return response.text
    
    def generate_image_description(self, topic: str, context: str = "") -> str:
        """Generate an image description for alt text based on the topic.
        
        Args:
            topic: The article topic
            context: Additional context for the image
            
        Returns:
            Image description for alt text
        """
        prompt = f"""
        Create a detailed, descriptive alt text for an image that would be perfect for 
        an article about "{topic}".
        
        Additional context: {context}
        
        The alt text should:
        1. Be descriptive and informative 
        2. Include relevant keywords naturally
        3. Be 10-20 words long
        4. Focus on what would be visually compelling for this topic
        """
        
        response = self.generation_model.generate_content(prompt)
        alt_text = response.text.strip()
        
        # Ensure it's not too long
        if len(alt_text.split()) > 25:
            alt_text = " ".join(alt_text.split()[:20]) + "..."
        
        return alt_text
    
    def insert_backlinks(self, content: str, backlinks: List[Dict[str, str]], min_links: int = 4) -> str:
        """Insert backlinks naturally into the article content.
        
        Args:
            content: The article content
            backlinks: List of backlink dictionaries {backlink: description}
            min_links: Minimum number of backlinks to insert
        
        Returns:
            Updated content with backlinks
        """
        # First, ask the model to suggest good insertion points
        if not backlinks or len(backlinks) == 0:
            return content
            
        backlinks_json = json.dumps(backlinks)
        
        prompt = f"""
        I have an article with the following content:
        
        {content[:4000]}  # Only send the first part to avoid token limitations
        
        And I need to insert these backlinks naturally:
        {backlinks_json}
        
        Please identify {max(min_links, len(backlinks))} good places in the article to insert these backlinks naturally.
        For each backlink, provide:
        1. The sentence before the backlink
        2. The exact anchor text with the backlink
        3. The sentence after the backlink
        
        Format your response as a valid JSON array of objects with these keys:
        - backlink_url: the URL to insert
        - insertion_point: description of where to insert (like "after the 3rd paragraph")
        - surrounding_text: the text surrounding where the link should be inserted
        - anchor_text: the text that should be linked
        """
        
        try:
            response = self.generation_model.generate_content(prompt)
            insertion_suggestions = json.loads(response.text)
            
            # Now insert the backlinks based on the suggestions
            modified_content = content
            inserted_count = 0
            
            for suggestion in insertion_suggestions:
                if inserted_count >= min_links:
                    break
                    
                backlink = suggestion["backlink_url"]
                anchor_text = suggestion["anchor_text"]
                surrounding_text = suggestion["surrounding_text"]
                
                # Find the surrounding text and replace it with the linked version
                if surrounding_text in modified_content:
                    linked_text = surrounding_text.replace(
                        anchor_text, f"[{anchor_text}]({backlink})"
                    )
                    modified_content = modified_content.replace(surrounding_text, linked_text)
                    inserted_count += 1
            
            if inserted_count < min_links:
                # Manually insert remaining backlinks at paragraph endings
                paragraphs = modified_content.split("\n\n")
                backlink_index = 0
                for i in range(min(len(paragraphs), min_links - inserted_count)):
                    if backlink_index >= len(backlinks):
                        backlink_index = 0
                    
                    # Get backlink details
                    backlink_url = list(backlinks[backlink_index].keys())[0]
                    description = list(backlinks[backlink_index].values())[0]
                    
                    # Add a sentence with the backlink at the end of a paragraph
                    transition = f" For more information, check out [this helpful resource]({backlink_url}) on {description}."
                    paragraphs[i*2 + 1] = paragraphs[i*2 + 1] + transition
                    
                    backlink_index += 1
                    inserted_count += 1
                
                modified_content = "\n\n".join(paragraphs)
            
            return modified_content
            
        except Exception as e:
            print(f"Error inserting backlinks: {e}")
            # Fallback: insert links manually at reasonable intervals
            paragraphs = content.split("\n\n")
            step = max(1, len(paragraphs) // (min_links + 1))
            
            for i in range(min(min_links, len(backlinks))):
                insert_idx = min((i + 1) * step, len(paragraphs) - 1)
                backlink_url = list(backlinks[i % len(backlinks)].keys())[0]
                description = list(backlinks[i % len(backlinks)].values())[0]
                
                # Add backlink at the end of the selected paragraph
                transition = f" For more information, you might want to check out [this resource]({backlink_url}) about {description}."
                paragraphs[insert_idx] += transition
                
            return "\n\n".join(paragraphs)
    
    def generate_full_article(self, 
                             topic: str, 
                             length_preference: str = "medium", 
                             backlinks: Optional[List[Dict[str, str]]] = None) -> str:
        """Generate a full SEO-optimized article.
        
        Args:
            topic: The article topic
            length_preference: Preferred article length (small/medium/long)
            backlinks: List of backlink dictionaries {backlink: description}
            
        Returns:
            Full article content in markdown format
        """
        # target word count
        target_length = self.LENGTHS.get(length_preference.lower(), 1500)
        
        # generate an outline
        outline = self.generate_article_outline(topic, length_preference)
        
        # header image description
        header_image_alt = self.generate_image_description(topic)
        
        # Construct the prompt for the full article
        prompt = f"""
        Write a comprehensive, SEO-optimized article on "{topic}" based on the following outline:
        
        {outline}
        
        The article should:
        1. Be approximately {target_length} words
        2. Include a catchy introduction that hooks the reader
        3. Follow a logical structure with H2 and H3 headings from the outline
        4. Incorporate relevant SEO keywords naturally
        5. Have a solid conclusion with a call to action
        
        Format the article in markdown with proper headings, paragraphs, bullet points, etc.
        Start with a level 1 heading as the article title.
        DO NOT include any backlinks or images - I will add those separately.
        DO NOT prefix the markdown with ```markdown or end it with ```.
        """
        
        # Generate the article
        response = self.generation_model.generate_content(prompt)
        content = response.text
        
        # Insert the header image after the first couple sentences
        first_paragraph_end = content.find("\n\n")
        if first_paragraph_end > 0:
            first_paragraph = content[:first_paragraph_end]
            sentences = first_paragraph.split('. ')
            insert_point = '. '.join(sentences[:min(2, len(sentences))]) + '.'
            image_markdown = f"\n\n![{header_image_alt}](image-link-here)\n\n"
            
            content = content.replace(insert_point, insert_point + image_markdown)
        else:
            # Fallback: insert at the beginning
            content = f"![{header_image_alt}](image-link-here)\n\n" + content
        
        # Insert backlinks if provided
        if backlinks:
            content = self.insert_backlinks(content, backlinks)
        
        return content
    
    def save_article(self, topic: str, content: str, output_dir: str = ".") -> str:
        """Save the generated article to a file.
        
        Args:
            topic: The article topic
            content: The article content
            output_dir: Directory to save the article
            
        Returns:
            The path to the saved file
        """
        filename = self.generate_filename(topic)
        
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return file_path
        
    def add_frontmatter(self, content: str, topic: str) -> str:
        """Add SEO-friendly frontmatter to the MDX file.
        
        Args:
            content: The article content
            topic: The article topic
            
        Returns:
            Content with frontmatter added
        """
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else topic
        
        prompt = f"""
        Generate a compelling SEO meta description for an article titled "{title}" 
        on the topic of "{topic}". The description should be:
        1. Under 160 characters
        2. Include relevant keywords
        3. Be enticing to readers
        4. Accurately represent the article content
        """
        
        response = self.generation_model.generate_content(prompt)
        description = response.text.strip()
        
        # Generate keywords
        prompt = f"""
        Generate 5-7 SEO keywords/phrases for an article titled "{title}"
        on the topic of "{topic}". Format the response as a comma-separated list.
        """
        
        response = self.generation_model.generate_content(prompt)
        keywords = response.text.strip()
        
        # Create frontmatter
        date = datetime.now().strftime("%Y-%m-%d")
        frontmatter = f"""---
title: "{title}"
description: "{description}"
date: "{date}"
keywords: [{keywords}]
---

"""
        return frontmatter + content

def parse_backlinks(backlinks_str: str) -> List[Dict[str, str]]:
    """Parse backlinks from a JSON string.
    
    Args:
        backlinks_str: JSON string of backlinks
        
    Returns:
        List of backlink dictionaries
    """
    try:
        return json.loads(backlinks_str)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format for backlinks")
        return []

def main():
    """Main function to run the article generator."""
    parser = argparse.ArgumentParser(description="Generate SEO-optimized articles with AI")
    
    parser.add_argument("--topic", type=str, required=True, help="Article topic")
    parser.add_argument("--length", type=str, default="medium", 
                        choices=["small", "medium", "long"],
                        help="Article length: small (800 words), medium (1000-1600 words), long (1800-2400 words)")
    parser.add_argument("--backlinks", type=str, default="[]",
                        help='JSON string of backlinks in format [{backlink:description},{backlink:description}]')
    parser.add_argument("--output-dir", type=str, default="./articles",
                        help="Directory to save the generated article")
    parser.add_argument("--model", type=str, default="gemini-1.5-pro",
                        choices=["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
                        help="Google AI model to use")
    parser.add_argument("--api-key", type=str, help="Google AI API key (or set GOOGLE_API_KEY env var)")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: Google AI API key must be provided via --api-key or GOOGLE_API_KEY environment variable")
        return
    
    # Parse backlinks
    backlinks = parse_backlinks(args.backlinks)
    
    generator = ArticleGenerator(api_key=api_key, model=args.model)
    
    print(f"Generating {args.length} article on: {args.topic}")
    content = generator.generate_full_article(
        topic=args.topic,
        length_preference=args.length,
        backlinks=backlinks
    )
    
    # frontmatter
    content_with_frontmatter = generator.add_frontmatter(content, args.topic)
    
    # Save the article
    file_path = generator.save_article(
        topic=args.topic,
        content=content_with_frontmatter,
        output_dir=args.output_dir
    )
    
    print(f"Article generated and saved to: {file_path}")

if __name__ == "__main__":
    main()
