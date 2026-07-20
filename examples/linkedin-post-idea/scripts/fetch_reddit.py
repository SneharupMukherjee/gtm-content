#!/usr/bin/env python3
"""
Fetch top posts from coaching subreddits via Reddit's public JSON API.
No API key required. Outputs structured post data for the LinkedIn idea agent.

Usage:
  python3 scripts/fetch_reddit.py [--mode hot|top] [--timeframe day|week] [--limit N]

Defaults: --mode hot --timeframe week --limit 10
"""

import json
import sys
import time
import urllib.request
import urllib.error
import argparse

SUBREDDITS = [
    "lifecoaching",
    "coaching",
    "Solopreneur",
    "smallbusiness",
    "freelance",
]

USED_POSTS_LOG = "output/used-posts.log"
USER_AGENT = "linkedin-idea-agent/1.0 by pineway"


def load_used_posts():
    try:
        with open(USED_POSTS_LOG) as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()


def fetch_subreddit(sub, mode="hot", timeframe="week", limit=10):
    if mode == "top":
        url = f"https://www.reddit.com/r/{sub}/top.json?t={timeframe}&limit={limit}"
    else:
        url = f"https://www.reddit.com/r/{sub}/hot.json?limit={limit}"

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
        return data["data"]["children"]
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, KeyError):
        return []


def extract_image(post_data):
    url = post_data.get("url", "")
    if any(url.endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".gif", ".webp")):
        return url
    preview = post_data.get("preview", {}).get("images", [])
    if preview:
        # unescape Reddit's preview URL
        src = preview[0]["source"]["url"].replace("&amp;", "&")
        return src
    return None


def score_post(post_data, used_posts):
    title = post_data.get("title", "")
    ups = post_data.get("ups", 0)
    comments = post_data.get("num_comments", 0)
    permalink = post_data.get("permalink", "")

    if permalink in used_posts:
        return -1  # skip already-used posts

    score = 0
    if comments > 50:
        score += 3
    elif comments >= 10:
        score += 2
    if ups > 500:
        score += 2
    elif ups > 100:
        score += 1
    if post_data.get("is_self") is False and post_data.get("crosspost_parent"):
        score += 2

    pain_words = ["admin", "overwhelmed", "buried", "tools", "clients", "scheduling",
                  "invoic", "payment", "manual", "time", "burnout", "exhausted",
                  "struggling", "help", "advice", "workflow", "automation"]
    title_lower = title.lower()
    for word in pain_words:
        if word in title_lower:
            score += 1
            break  # only +1 even if multiple matches

    # question posts tend to generate more comments and signal real pain
    if "?" in title:
        score += 1

    return score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["hot", "top"], default="hot")
    parser.add_argument("--timeframe", choices=["day", "week", "month"], default="week")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    used_posts = load_used_posts()
    all_posts = []

    for sub in SUBREDDITS:
        posts = fetch_subreddit(sub, mode=args.mode, timeframe=args.timeframe, limit=args.limit)
        for post in posts:
            pd = post["data"]
            score = score_post(pd, used_posts)
            if score < 0:
                continue
            all_posts.append({
                "subreddit": sub,
                "title": pd.get("title", ""),
                "ups": pd.get("ups", 0),
                "comments": pd.get("num_comments", 0),
                "permalink": f"https://reddit.com{pd.get('permalink', '')}",
                "image": extract_image(pd),
                "score": score,
                "flair": pd.get("link_flair_text", ""),
                "created_utc": pd.get("created_utc", 0),
            })
        time.sleep(0.5)  # respect rate limits between subreddit calls

    # sort by score descending
    all_posts.sort(key=lambda x: x["score"], reverse=True)

    # output top 15 as structured JSON for the agent to read
    output = {
        "fetched_at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "mode": args.mode,
        "timeframe": args.timeframe,
        "subreddits": SUBREDDITS,
        "posts": all_posts[:15],
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
