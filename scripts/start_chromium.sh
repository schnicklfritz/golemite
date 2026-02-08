#!/bin/bash
# 1. Enforce preferences (Disable "Ask where to save", set paths)
python /home/golem/scripts/configure_chromium.py

# 2. Build Flags
FLAGS="--no-sandbox --disable-gpu --no-first-run --user-data-dir=/home/golem/.config/chromium"

# 3. Kiosk vs Desktop Logic
if [ "$DESKTOP_ENV" == "matchbox-window-manager" ]; then
    # KIOSK: Full screen, no borders, no OS UI
    FLAGS="$FLAGS --kiosk --start-maximized"
else
    # DESKTOP: Normal window
    FLAGS="$FLAGS --start-maximized"
fi

# 4. Launch opening the Landing Page
exec chromium $FLAGS "file:///home/golem/scripts/landing.html"
