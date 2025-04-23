from playwright.sync_api import sync_playwright
import os
import requests
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TARGET_TEXTS = ["+17", "+21", "+22"]
ALERTED_MATCHES = set()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_page():
    global ALERTED_MATCHES
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.chance.cz/kurzy/tenis-43", wait_until="networkidle")
        rows = page.locator("div.oddsCell__row")
        count = rows.count()

        for i in range(count):
            row = rows.nth(i)
            row_text = row.inner_text()
            for target in TARGET_TEXTS:
                if target in row_text:
                    match = row.locator("xpath=ancestor::div[contains(@class, 'matchRow')]").locator(".matchRow__matchName").inner_text()
                    if (match, target) not in ALERTED_MATCHES:
                        send_telegram_message(f"Změna detekována: {target} u zápasu \"{match}\"")
                        ALERTED_MATCHES.add((match, target))
                    break
        browser.close()

if __name__ == "__main__":
    while True:
        check_page()
        time.sleep(15)
