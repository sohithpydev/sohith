import feedparser
from datetime import datetime
import os

# YouTube RSS feed
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCUylbdgx1yEc0WxIGz6s_0g"

feed = feedparser.parse(RSS_URL)

# Folder to save markdown posts
POST_DIR = "_posts/youtube"
os.makedirs(POST_DIR, exist_ok=True)

for entry in feed.entries[:5]:  # Latest 5 videos
    date_struct = entry.published_parsed
    date_str = datetime(*date_struct[:6]).strftime("%Y-%m-%d")

    # Clean slug
    import re
    slug = entry.title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')

    filename = f"{POST_DIR}/{date_str}-{slug}.md"

    content_md = f"[Watch on YouTube]({entry.link})\n\n{entry.title}"

    front_matter = f"""---
title: "{entry.title}"
date: {date_str}
permalink: /youtube/{slug}/
tags:
  - youtube
---
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write("\n")
        f.write(content_md)

print("YouTube videos fetched and saved!")
