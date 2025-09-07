import discord
import asyncio
import random
import re
import os
from datetime import datetime, timedelta

TOKEN = os.getenv("DISCORD_TOKEN")  # Railway Variables menüüs pead selle lisama
CHANNEL_ID = 123456789012345678     # <-- pane siia oma Discordi kanali ID (integer!)

def kaitsevaekalk():
    total_days = 334
    sbk_days = 55
    end_date = datetime(2026, 6, 14)
    start_date = end_date - timedelta(days=total_days)

    now = datetime.now()
    elapsed = now - start_date
    days_passed = elapsed.days
    hours_passed = elapsed.seconds // 3600
    minutes_passed = (elapsed.seconds % 3600) // 60

    if days_passed < 0:
        days_passed, hours_passed, minutes_passed = 0, 0, 0
    if days_passed > total_days:
        days_passed, hours_passed, minutes_passed = total_days, 0, 0

    sbk_percent = min(100.0, (elapsed.total_seconds() / (sbk_days * 86400)) * 100)
    kaitsevaegi_percent = (elapsed.total_seconds() / (total_days * 86400)) * 100
    if kaitsevaegi_percent > 100:
        kaitsevaegi_percent = 100.0

    sbk_percent = round(sbk_percent, 3)
    kaitsevaegi_percent = round(kaitsevaegi_percent, 3)

    # --- Fun fact solvangud failist ---
    with open("solvangud.txt", "r", encoding="utf-8") as f:
        solvangud = [line.strip() for line in f if line.strip()]

    # eemalda alguse numbrid + punkt (nt "13. ")
    puhastatud = [re.sub(r"^\d+\.\s*", "", s) for s in solvangud]
    solvang = random.choice(puhastatud)

    return f"""
käes on {days_passed} päev
**
> Läbitud on {days_passed} päeva, {hours_passed} tundi ja {minutes_passed} minutit
> > SBK on ~{sbk_percent}%
> > Kaitsevägi on ~{kaitsevaegi_percent}%
**

Fun fact: {solvang}
"""

# ---- Discord Bot ----
intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def send_daily_message():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        now = datetime.now()
        random_hour = random.randint(8, 22)   # ainult 08:00–22:00 vahel
        random_minute = random.randint(0, 59)
        target_time = datetime(now.year, now.month, now.day, random_hour, random_minute)
        if target_time <= now:
            target_time += timedelta(days=1)

        wait_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        msg = kaitsevaekalk()
        await channel.send(msg)

        # oota järgmise päevani
        await asyncio.sleep(24 * 3600)

@client.event
async def on_ready():
    print(f"Bot logis sisse: {client.user}")

client.loop.create_task(send_daily_message())
client.run(TOKEN)
