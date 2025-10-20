import requests
from bs4 import BeautifulSoup
from typing import List, Dict

BASE = "https://alpogo.com"
KEYWORDS = [
    "metal", "heavy", "death", "black", "thrash", "doom",
    "argentina", "buenos aires", "cordoba", "rosario",
    "recital", "show", "tour", "entradas", "gira"
]

def fetch_alpogo_events() -> List[Dict]:
    events = []
    try:
        url = BASE  # URL actualizada
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8"} # A veces ayuda simular idioma
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for card in soup.select("div.event-card, article"):
            title_el = card.select_one("h3")
            title = title_el.get_text(strip=True) if title_el else card.get_text(strip=True)
            link = card.find('a', href=True)
            link = link['href'] if link else None
            if link and not link.startswith("http"):
                link = BASE + link

            if any(k.lower() in title.lower() for k in KEYWORDS):
                events.append({
                    "source": "alpogo",
                    "title": title,
                    "url": link
                })
    except Exception as e:
        print("AlPogo scrape error:", e)
    return events