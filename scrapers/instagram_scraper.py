import instaloader
import json
import os
from typing import List, Dict

L = instaloader.Instaloader()

KEYWORDS = ["argentina", "buenos aires", "bsas", "show", "concierto", "evento", "festival", "entradas", "tickets", "metal", "rock", "recital", "gira"]

def fetch_instagram_posts(accounts_file: str="../accounts.json", limit_per_profile: int=5) -> List[Dict]:
    try:
        with open(accounts_file) as f:
            accounts = json.load(f).get("accounts", [])
    except Exception:
        accounts = []

    results = []
    
    for account in accounts:
        try:
            profile = instaloader.Profile.from_username(L.context, account)
            count = 0
            for post in profile.get_posts():
                if count >= limit_per_profile:
                    break
                shortcode = post.shortcode
                caption = (post.caption or "").strip()
                text = caption.lower()
                if any(k in text for k in KEYWORDS):
                    item = {
                        "source": "instagram",
                        "source_account": account,
                        "title": f"Post de {account}",
                        "url": f"https://www.instagram.com/p/{shortcode}/",
                        "caption": (caption[:800] + '...') if len(caption) > 800 else caption,
                    }
                    if post.typename == "GraphImage":
                        item["thumbnail"] = post.url
                    results.append(item)
                    count += 1
                count += 1
        except Exception as e:
            print(f"Error fetching posts for {account}: {e}")
    return results