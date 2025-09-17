import feedparser
from markdownify import markdownify as md
from datetime import datetime
import os
import re  # for slug sanitization

# Your Medium RSS feed
RSS_URL = "https://medium.com/feed/@sohith.bme"

feed = feedparser.parse(RSS_URL)

# Folder to save markdown posts
POST_DIR = "_posts/medium"
os.makedirs(POST_DIR, exist_ok=True)

for entry in feed.entries[:5]:  # Change number of posts if you want
    # Format date
    date_struct = entry.published_parsed
    date_str = datetime(*date_struct[:6]).strftime("%Y-%m-%d")

    # Generate safe slug
    slug = entry.title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)  # replace non-alphanumeric with hyphen
    slug = re.sub(r'-+', '-', slug).strip('-')  # remove repeated hyphens and edges

    # Markdown filename
    filename = f"{POST_DIR}/{date_str}-{slug}.md"

    # Convert Medium content to Markdown
    content_md = md(entry.content[0].value) if 'content' in entry else md(entry.summary)

    # Front matter
    front_matter = f"""---
title: "{entry.title}"
date: {date_str}
permalink: /posts/medium/{slug}/
tags:
  - medium
---
"""

    # Write file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write("\n")
        f.write(content_md)

print("Medium posts fetched and saved!")
