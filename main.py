import requests
import random
import re
import time
import os
from datetime import datetime, timedelta


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
    #if kaitsevaegi_percent > 100:
     #   kaitsevaegi_percent = 100.0

    sbk_percent = round(sbk_percent, 3)
    kaitsevaegi_percent = round(kaitsevaegi_percent, 3)
    
    # --- AJEK ---
    ajek_start = datetime(datetime.now().year, 9, 8)   # 8. september
    ajek_end = datetime(datetime.now().year, 11, 30)   # 30. november
    ajek_total_days = (ajek_end - ajek_start).days + 1

    if now < ajek_start:
        ajek_percent = 0.0
    elif now > ajek_end:
        ajek_percent = 100.0
    else:
        ajek_elapsed = (now - ajek_start).total_seconds()
        ajek_percent = (ajek_elapsed / (ajek_total_days * 86400)) * 100

    # Ümardamine
    sbk_percent = round(sbk_percent, 7)
    kaitsevaegi_percent = round(kaitsevaegi_percent, 3)
    ajek_percent = round(ajek_percent, 3)

    # --- Fun fact ---
    with open("solvangud.txt", "r", encoding="utf-8") as f:
        solvangud = [line.strip() for line in f if line.strip()]
    puhastatud = [re.sub(r"^\d+\.\s*", "", s) for s in solvangud]
    solvang = random.choice(puhastatud)

    return f"""
Kell on päev nr {days_passed} 
s.t
**
> Läbitud on {days_passed} päeva, {hours_passed} tundi ja {minutes_passed} minutit
> > SBK on ~{sbk_percent}% läbi
> > AJEK on ~{ajek_percent}% läbi
> > Kaitsevägi on ~{kaitsevaegi_percent}% läbi
**

Fun fact: {solvang}
"""
# --- discord ---
def send_to_discord(msg):
    data = {"content": msg}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Sõnum saadetud")
    else:
        print(f"[ERROR] Discord vastas {response.status_code}: {response.text}")

if __name__ == "__main__":
    
    now = datetime.now()
    random_hour = random.randint(4, 20)
    random_minute = random.randint(0, 59)
    target_time = datetime(now.year, now.month, now.day, random_hour, random_minute)

    if target_time <= now:
        target_time += timedelta(days=1)

    wait_seconds = (target_time - now).total_seconds()
    print(f"[INFO] Valitud kellaaeg: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[INFO] Ootan {wait_seconds/3600:.2f} tundi...")

    time.sleep(wait_seconds)
    msg = kaitsevaekalk()
    send_to_discord(msg)



