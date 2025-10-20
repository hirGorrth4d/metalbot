import json
import os
from typing import Set




def load_seen(path: str = "seen_posts.json") -> Set[str]:
    if not os.path.exists(path):
        return set()
    try:
        with open(path) as f:
            data = json.load(f)
            return set(data)
    except Exception:
        return set()




def save_seen(seen: Set[str], path: str = "seen_posts.json") -> None:
    with open(path, "w") as f:
        json.dump(list(seen), f)