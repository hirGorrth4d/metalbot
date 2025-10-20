import os
import asyncio
import discord
from dotenv import load_dotenv

from scrapers.instagram_scraper import fetch_instagram_posts
from scrapers.passline_scraper import fetch_passline_events
from scrapers.alpogo_scraper import fetch_alpogo_events
from scrapers.ticketek_scraper import fetch_ticketek_events
from scrapers.allaccess_scraper import fetch_allaccess_events
from utils.helpers import load_seen, save_seen
load_dotenv()


TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_SECONDS"))


intents = discord.Intents.default()
client = discord.Client(intents=intents)


seen = load_seen()


async def gather_all_events():
    items = []


    # Instagram
    try:
        items.extend(fetch_instagram_posts())
    except Exception as e:
        print("Error instagram:", e)


    # Scrapers
    for f in (fetch_passline_events, fetch_alpogo_events, fetch_ticketek_events, fetch_allaccess_events):
        try:
            items.extend(f())
        except Exception as e:
            print(f"Error en scraper {f.__name__}: {e}")


    # filtrar por duplicados ya en cache
    new_items = [it for it in items if it.get('url') and it['url'] not in seen]
    return new_items


@client.event

async def on_ready():
    print(f"Conectado como {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("Canal no encontrado. Revisa CHANNEL_ID en .env")
        return
    while True:
        print("Revisando fuentes...")
        new = await gather_all_events()
        for e in new:
            try:
                embed = discord.Embed(
                    title=e.get('title') or 'Evento',
                    description=f"Fuente: {e.get('source')}",
                    url=e.get('url')
                )
                if e.get('caption'):
                    embed.add_field(name='Info', value=e.get('caption')[:1024], inline=False)
                # thumbnail si existe
                if e.get('thumbnail'):
                    embed.set_thumbnail(url=e.get('thumbnail'))
                await channel.send(embed=embed)
                seen.add(e['url'])
            except Exception as ex:
                print("Error enviando embed:", ex)
        save_seen(seen)
        await asyncio.sleep(CHECK_INTERVAL)
if __name__ == '__main__':
    client.run(TOKEN)