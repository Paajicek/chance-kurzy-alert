#!/bin/bash

# Instalace Python balíčků
pip install -r requirements.txt

# Ruční stažení prohlížeče Chromium přes Python modul (tohle Render zvládá!)
python -m playwright install chromium

# Ověření instalace – výpis, který uvidíme v logu
if [ -f "/opt/render/.cache/ms-playwright/chromium-1067/chrome-linux/chrome" ]; then
  echo "✅ Chromium byl úspěšně nainstalován!"
else
  echo "❌ Chromium pořád chybí."
  exit 1
fi
