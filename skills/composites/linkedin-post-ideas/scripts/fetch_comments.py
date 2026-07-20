#!/usr/bin/env python3
"""
Fetch top comments from a Reddit post URL.
Used by the writer subagent to get raw material for full LinkedIn post bodies.

Usage:
  python3 scripts/fetch_comments.py <reddit_permalink_url> [--limit N]

Example:
  python3 scripts/fetch_comments.py https://reddit.com/r/smallbusiness/comments/1ta5kzs/... --limit 15
"""

import json
import sys
import time
import urllib.request
import urllib.error
import argparse


USER_AGENT = "linkedin-idea-agent/1.0 by pineway"


def fetch_comments(permalink, limit=15):
    # Normalise URL — strip trailing slash, ensure .json suffix
    url = permalink.rstrip("/")
    if not url.endswith(".json"):
        url += ".json"
    url += f"?limit={limit}&sort=top"

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError) as e:
        print(json.dumps({"error": str(e), "url": url}))
        sys.exit(1)

    # data[0] = post, data[1] = comments
    post_data = data[0]["data"]["children"][0]["data"]
    comments_data = data[1]["data"]["children"]

    post = {
        "title": post_data.get("title", ""),
        "selftext": post_data.get("selftext", ""),
        "ups": post_data.get("ups", 0),
        "num_comments": post_data.get("num_comments", 0),
        "subreddit": post_data.get("subreddit", ""),
        "permalink": f"https://reddit.com{post_data.get('permalink', '')}",
    }

    comments = []
    for c in comments_data:
        d = c.get("data", {})
        body = d.get("body", "")
        if not body or body in ("[deleted]", "[removed]"):
            continue
        comments.append({
            "ups": d.get("ups", 0),
            "body": body,
        })

    # Sort by upvotes, return top comments
    comments.sort(key=lambda x: x["ups"], reverse=True)

    return {"post": post, "comments": comments[:limit]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Reddit permalink URL")
    parser.add_argument("--limit", type=int, default=15)
    args = parser.parse_args()

    result = fetch_comments(args.url, args.limit)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
