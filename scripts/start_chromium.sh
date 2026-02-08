k#!/bin/bash
# 1. Enforce preferences
python /home/golem/scripts/configure_chromium.py

# 2. Build Flags
FLAGS="--no-sandbox --disable-gpu --no-first-run --user-data-dir=/home/golem/.config/chromium"

# 3. Kiosk vs Desktop Logic
if [ "$DESKTOP_ENV" == "openbox" ]; then
    # KIOSK MODE:
    # --kiosk forces fullscreen
    FLAGS="$FLAGS --kiosk --start-maximized"
else
    # DESKTOP MODE:
    # Normal window with title bar
    FLAGS="$FLAGS --start-maximized"
fi

# 4. Launch
exec chromium $FLAGS "file:///home/golem/scripts/landing.html"
