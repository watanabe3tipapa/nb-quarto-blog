#!/usr/bin/env python3
"""
Convert .md files to .qmd files in the posts directory.
This script converts Markdown files to Quarto format with proper frontmatter.
"""

import os
import re
import frontmatter
import yaml
from pathlib import Path
from datetime import datetime

def extract_title_from_content(content):
    """Extract title from markdown content (first h1 or filename)."""
    # Look for first h1 heading
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    # Look for first h2 heading if no h1 found
    h2_match = re.search(r'^##\s+(.+)$', content, re.MULTILINE)
    if h2_match:
        return h2_match.group(1).strip()
    
    return None

def extract_date_from_filename(filepath):
    """Try to extract date from filename (YYYY-MM-DD format)."""
    filename = filepath.stem
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        return date_match.group(1)
    return None

def extract_categories_from_content(content):
    """Extract categories from content or use default."""
    # Look for tags or categories in content
    tags_match = re.search(r'(?:tags?|categories?):\s*\[([^\]]+)\]', content, re.IGNORECASE)
    if tags_match:
        tags_str = tags_match.group(1)
        # Clean up and split by comma
        tags = [tag.strip().strip('"\'') for tag in tags_str.split(',')]
        return [tag for tag in tags if tag]
    
    # Look for hashtags in content
    hashtags = re.findall(r'#(\w+)', content)
    if hashtags:
        return hashtags
    
    return ["blog"]  # Default category

def create_frontmatter(title, author, date, categories, image=None):
    """Create Quarto frontmatter."""
    frontmatter_data = {
        "title": title,
        "author": author,
        "date": date,
        "categories": categories
    }
    
    if image:
        frontmatter_data["image"] = image
    
    return frontmatter_data

def convert_md_to_qmd(md_path, qmd_path):
    """Convert a single .md file to .qmd format."""
    try:
        # Read the markdown file
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract existing frontmatter if present
        post = frontmatter.loads(content)
        
        # Extract metadata
        title = post.metadata.get('title') or extract_title_from_content(post.content)
        if not title:
            title = md_path.stem.replace('-', ' ').title()
        
        author = post.metadata.get('author', 'watanabe3tipapa')
        
        # Try to get date from existing metadata, filename, or use today
        date = post.metadata.get('date')
        if not date:
            date = extract_date_from_filename(md_path)
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        categories = post.metadata.get('categories') or extract_categories_from_content(post.content)
        image = post.metadata.get('image')
        
        # Create new frontmatter
        new_frontmatter = create_frontmatter(title, author, date, categories, image)
        
        # Create Quarto file
        qmd_post = frontmatter.Post(post.content, **new_frontmatter)
        
        # Write the .qmd file
        with open(qmd_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(qmd_post))
        
        print(f"✅ Converted: {md_path.name} → {qmd_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting {md_path.name}: {str(e)}")
        return False

def main():
    """Main conversion function."""
    posts_dir = Path("posts")
    if not posts_dir.exists():
        print("❌ posts directory not found")
        return
    
    converted_count = 0
    total_count = 0
    
    # Find all .md files in posts directory and subdirectories
    for md_file in posts_dir.rglob("*.md"):
        # Skip if .qmd file already exists and is newer
        qmd_file = md_file.with_suffix('.qmd')
        if qmd_file.exists() and qmd_file.stat().st_mtime > md_file.stat().st_mtime:
            print(f"⏭️  Skipping {md_file.name} (already converted)")
            continue
        
        total_count += 1
        if convert_md_to_qmd(md_file, qmd_file):
            # Remove the source .md so .md/.qmd cannot coexist in the same
            # directory (Quarto fails to render when both resolve to index.html)
            md_file.unlink()
            converted_count += 1
    
    print(f"\n🎉 Conversion complete: {converted_count}/{total_count} files converted")
    
    if converted_count > 0:
        print("\n📝 Converted files:")
        for qmd_file in posts_dir.rglob("*.qmd"):
            md_file = qmd_file.with_suffix('.md')
            if not md_file.exists():
                print(f"   - {qmd_file.relative_to(posts_dir)}")

if __name__ == "__main__":
    main()