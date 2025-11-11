#!/usr/bin/env python3
"""
Move .md files from root directory to posts directory.
This script organizes markdown files by moving them to appropriate subdirectories.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

def extract_date_from_filename(filename):
    """Try to extract date from filename (YYYY-MM-DD format)."""
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        return date_match.group(1)
    return None

def extract_category_from_content(content):
    """Extract category from content to determine subdirectory."""
    content_lower = content.lower()
    
    # Define category keywords
    categories = {
        'data-science': ['data science', 'machine learning', 'ml', 'ai', 'artificial intelligence', 'statistics'],
        'programming': ['python', 'javascript', 'r', 'code', 'programming', 'development', 'software'],
        'tutorial': ['tutorial', 'how to', 'guide', 'step by step', 'learn'],
        'web-development': ['html', 'css', 'web', 'frontend', 'backend', 'javascript'],
        'visualization': ['visualization', 'plot', 'chart', 'graph', 'dashboard'],
        'analysis': ['analysis', 'analytics', 'research', 'study'],
        'tools': ['tool', 'software', 'application', 'platform'],
        'news': ['news', 'announcement', 'update', 'release']
    }
    
    # Count matches for each category
    category_scores = {}
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in content_lower)
        if score > 0:
            category_scores[category] = score
    
    # Return category with highest score, or default
    if category_scores:
        return max(category_scores, key=category_scores.get)
    
    return 'blog'  # Default category

def create_directory_name(title, date, category):
    """Create a directory name from title, date, and category."""
    # Clean title: lowercase, replace spaces and special chars with hyphens
    clean_title = re.sub(r'[^\w\s-]', '', title.lower())
    clean_title = re.sub(r'[-\s]+', '-', clean_title)
    clean_title = clean_title.strip('-')
    
    # Limit length
    if len(clean_title) > 50:
        clean_title = clean_title[:50].rstrip('-')
    
    # If date exists, use date-title format, otherwise just title
    if date:
        return f"{date}-{clean_title}"
    else:
        return clean_title

def move_md_to_posts():
    """Move .md files from root to posts directory."""
    root_dir = Path(".")
    posts_dir = Path("posts")
    
    if not posts_dir.exists():
        posts_dir.mkdir(exist_ok=True)
        print(f"📁 Created posts directory")
    
    moved_count = 0
    skipped_count = 0
    
    # Find all .md files in root directory (excluding README and other special files)
    for md_file in root_dir.glob("*.md"):
        # Skip important files
        if md_file.name.lower() in ['readme.md', 'license.md', 'contributing.md']:
            print(f"⏭️  Skipping {md_file.name} (protected file)")
            skipped_count += 1
            continue
        
        # Skip files that are already in posts directory structure
        if any(md_file.name in existing.name for existing in posts_dir.rglob("*.md")):
            print(f"⏭️  Skipping {md_file.name} (already exists in posts)")
            skipped_count += 1
            continue
        
        try:
            # Read the file content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata
            date = extract_date_from_filename(md_file.name)
            category = extract_category_from_content(content)
            
            # Extract title from first h1 or filename
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else md_file.stem.replace('-', ' ').title()
            
            # Create directory name
            dir_name = create_directory_name(title, date, category)
            target_dir = posts_dir / category / dir_name
            
            # Create directory if it doesn't exist
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Move the file
            target_file = target_dir / "index.md"
            shutil.move(str(md_file), str(target_file))
            
            print(f"📝 Moved: {md_file.name} → posts/{category}/{dir_name}/index.md")
            print(f"   📂 Category: {category}")
            print(f"   📅 Date: {date or 'auto-generated'}")
            print(f"   🏷️  Title: {title}")
            print()
            
            moved_count += 1
            
        except Exception as e:
            print(f"❌ Error moving {md_file.name}: {str(e)}")
            skipped_count += 1
    
    print(f"🎉 Operation complete: {moved_count} files moved, {skipped_count} files skipped")
    
    if moved_count > 0:
        print("\n📋 Summary of moved files:")
        for category_dir in posts_dir.iterdir():
            if category_dir.is_dir():
                for post_dir in category_dir.iterdir():
                    if post_dir.is_dir() and (post_dir / "index.md").exists():
                        print(f"   - posts/{category_dir.name}/{post_dir.name}/")

if __name__ == "__main__":
    move_md_to_posts()