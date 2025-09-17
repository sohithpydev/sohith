import feedparser
from datetime import datetime
import os
import re

# YouTube RSS feed
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCUylbdgx1yEc0WxIGz6s_0g"

feed = feedparser.parse(RSS_URL)

POST_DIR = "_posts/youtube"
os.makedirs(POST_DIR, exist_ok=True)

for entry in feed.entries[:5]:
    date_struct = entry.published_parsed
    date_str = datetime(*date_struct[:6]).strftime("%Y-%m-%d")

    # Safe slug
    slug = entry.title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')

    # Extract video ID
    video_id_match = re.search(r'v=([A-Za-z0-9_-]+)', entry.link)
    video_id = video_id_match.group(1) if video_id_match else ""

    filename = f"{POST_DIR}/{date_str}-{slug}.md"

    front_matter = f"""---
title: "{entry.title}"
date: {date_str}
permalink: /youtube/{slug}/
tags:
  - youtube
video_id: {video_id}
---
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write("\n")
        f.write(f"[Watch on YouTube]({entry.link})")

print("YouTube videos fetched and saved!")
