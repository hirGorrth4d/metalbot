import requests
from bs4 import BeautifulSoup
from typing import List, Dict

BASE = "https://www.ticketek.com.ar"
KEYWORDS = [
    "metal", "heavy", "death", "black", "thrash", "doom",
    "argentina", "buenos aires", "cordoba", "rosario",
    "recital", "show", "tour", "entradas", "gira"
]

def fetch_ticketek_events() -> List[Dict]:
    events = []
    try:
        url = f"{BASE}/search?q=metal"  # Busqueda por metal
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for card in soup.select("div.event-card, .result-item"):
            title_el = card.select_one("h3")
            title = title_el.get_text(strip=True) if title_el else card.get_text(strip=True)
            link = card.find('a', href=True)
            link = link['href'] if link else None
            if link and not link.startswith("http"):
                link = BASE + link

            if any(k.lower() in title.lower() for k in KEYWORDS):
                events.append({
                    "source": "ticketek",
                    "title": title,
                    "url": link
                })
    except Exception as e:
        print("Ticketek scrape error:", e)
    return events
