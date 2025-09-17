import feedparser
from markdownify import markdownify as md
from datetime import datetime
import os

# Your Medium RSS feed
RSS_URL = "https://medium.com/feed/@sohith.bme"

feed = feedparser.parse(RSS_URL)

# Folder to save markdown posts
POST_DIR = "_posts/medium"
os.makedirs(POST_DIR, exist_ok=True)

for entry in feed.entries[:5]:  # Change number of posts if you want
    date_struct = entry.published_parsed
    date_str = datetime(*date_struct[:6]).strftime("%Y-%m-%d")
    slug = entry.title.lower().replace(" ", "-").replace("/", "-")
    filename = f"{POST_DIR}/{date_str}-{slug}.md"

    content_md = md(entry.content[0].value) if 'content' in entry else md(entry.summary)

    front_matter = f"""---
title: "{entry.title}"
date: {date_str}
permalink: /posts/medium/{slug}/
tags:
  - medium
---
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write("\n")
        f.write(content_md)

print("Medium posts fetched and saved!")
