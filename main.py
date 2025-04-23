import os
import time
import requests
from playwright.sync_api import sync_playwright

# Telegram credentials
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Hledané texty
HLEDANE_TEXTY = ["+17", "+21", "+22"]
ZASLANE = set()

# URL s kurzy
URL = "https://www.chance.cz/kurzy/tenis-43"

def odesli_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Chyba při odesílání zprávy: {e}")

def check_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path="/usr/bin/chromium-browser"  # ruční cesta
        )
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_timeout(5000)
        html = page.content()

        for hledany in HLEDANE_TEXTY:
            if hledany in html and hledany not in ZASLANE:
                # Pokus o vytažení zápasu (zjednodušený)
                nadpisy = page.locator("div.competition-event__competitors")
                nalezen = False
                for i in range(nadpisy.count()):
                    text_zapasu = nadpisy.nth(i).inner_text()
                    if hledany in page.locator("div.competition-event").nth(i).inner_html():
                        odesli_telegram(f"Změna detekována: {hledany} u zápasu: {text_zapasu}")
                        ZASLANE.add(hledany)
                        nalezen = True
                        break
                if not nalezen:
                    odesli_telegram(f"Změna detekována: {hledany} (název zápasu se nepodařilo získat)")
                    ZASLANE.add(hledany)

        browser.close()

while True:
    try:
        check_page()
    except Exception as e:
        print(f"Chyba při kontrole: {e}")
    time.sleep(15)
