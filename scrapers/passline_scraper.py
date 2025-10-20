import cloudscraper # <-- Nuevo import
from bs4 import BeautifulSoup
from typing import List, Dict
import requests # Mantenemos requests en caso de necesitar sus excepciones

BASE = "https://home.passline.com/home"
KEYWORDS = [
    "metal", "heavy", "death", "black", "thrash", "doom",
    "argentina", "buenos aires", "cordoba", "rosario",
    "recital", "show", "tour", "entradas", "gira"
]

def fetch_passline_events() -> List[Dict]:
    events = []
    
    # 1. Crear una instancia de cloudscraper
    # cloudscraper manejará los headers y User-Agent automáticamente.
    scraper = cloudscraper.create_scraper() 
    
    url = BASE
    
    try:
        # 2. Usar el objeto scraper para hacer la solicitud
        # Hemos eliminado la definición manual de 'headers'
        resp = scraper.get(url, timeout=15) # Aumenté el timeout preventivamente
        
        # raise_for_status() sigue siendo útil para manejar otros errores HTTP
        resp.raise_for_status() 
        
        soup = BeautifulSoup(resp.text, "html.parser")

        for card in soup.select("a.card-event, .card-event"):
            title_el = card.select_one(".card-event__title, .event-title, h3")
            title = title_el.get_text(strip=True) if title_el else card.get_text(strip=True)
            link = card.get('href') or (card.a and card.a.get('href'))
            
            if link and not link.startswith("http"):
                link = BASE + link # O la lógica correcta para construir la URL absoluta

            if any(k.lower() in title.lower() for k in KEYWORDS):
                events.append({
                    "source": "passline",
                    "title": title,
                    "url": link
                })
                
    except requests.exceptions.HTTPError as e:
        # Esto capturará el 403 o cualquier otro error HTTP que persista
        print(f"Passline scrape error (HTTP): {e}")
        return []
    except Exception as e:
        # Para capturar errores de conexión, parsing u otros
        print("Passline scrape error (General):", e)
    
    return events