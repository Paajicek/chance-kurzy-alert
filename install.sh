#!/bin/bash
pip install -r requirements.txt

# Workaround – Playwright někdy ignoruje chromium install
python -m playwright install chromium

# Kontrola existence prohlížeče
if [ ! -f "/opt/render/.cache/ms-playwright/chromium-1084/chrome-linux/chrome" ]; then
  echo "❌ Chromium nebyl nainstalován správně."
  exit 1
else
  echo "✅ Chromium byl úspěšně nainstalován!"
fi
