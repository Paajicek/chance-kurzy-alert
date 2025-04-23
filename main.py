import os
import time
import requests
from playwright.sync_api import sync_playwright

# 🔐 Token a chat ID pro Telegram (doplněno napevno)
TELEGRAM_TOKEN = "7785381597:AAFPf-jjYqSO_Db9w7avMXa3lq3PP3GbNb0"
TELEGRAM_CHAT_ID = "1842186722"

# 🔍 Hledané hodnoty
HLEDANE_TEXTY = ["+17", "+21", "+22"]
ZASLANE = set()

# 🌐 URL Chance.cz s kurzy na tenis
URL = "https://www.chance.cz/kurzy/tenis-43"

# 📩 Posílá zprávu na Telegram
def odesli_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Chyba při odesílání zprávy: {e}")

# 🕵️‍♂️ Kontrola stránky
def check_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_timeout(5000)  # čekání na načtení obsahu

        html = page.content()

        for hledany in HLEDANE_TEXTY:
            if hledany in html and hledany not in ZASLANE:
                zapasy = page.locator("div.competition-event__competitors")
                eventy = page.locator("div.competition-event")
                nalezen = False
                for i in range(eventy.count()):
                    if hledany in eventy.nth(i).inner_html():
                        text_zapasu = zapasy.nth(i).inner_text()
                        odesli_telegram(f"📢 Detekováno {hledany} u zápasu: {text_zapasu}")
                        ZASLANE.add(hledany)
                        nalezen = True
                        break
                if not nalezen:
                    odesli_telegram(f"📢 Detekováno {hledany}, ale název zápasu nebyl nalezen")
                    ZASLANE.add(hledany)

        browser.close()

# 🔁 Neustálá kontrola každých 15 sekund
while True:
    try:
        check_page()
    except Exception as e:
        print(f"Chyba při kontrole: {e}")
    time.sleep(40)
