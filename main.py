import requests
import random
import re
import time
import os
from datetime import datetime, timedelta

# Webhook URL tuleb Railway environment variables alt (WEBHOOK_URL)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

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

    # --- Fun fact solvang failist ---
    with open("solvangud.txt", "r", encoding="utf-8") as f:
        solvangud = [line.strip() for line in f if line.strip()]
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

def send_to_discord(msg):
    data = {"content": msg}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("[INFO] Sõnum saadetud edukalt.")
    else:
        print(f"[ERROR] Discord vastas {response.status_code}: {response.text}")

if __name__ == "__main__":
    # vali random kellaaeg vahemikus 08:00–22:00
    now = datetime.now()
    random_hour = random.randint(8, 22)
    random_minute = random.randint(0, 59)
    target_time = datetime(now.year, now.month, now.day, random_hour, random_minute)

    if target_time <= now:
        target_time += timedelta(days=1)

    wait_seconds = (target_time - now).total_seconds()
    print(f"[INFO] Valitud kellaaeg: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[INFO] Ootan {wait_seconds/3600:.2f} tundi...")

    time.sleep(wait_seconds)  # oota kuni suvaline kellaaeg
    msg = kaitsevaekalk()
    send_to_discord(msg)

