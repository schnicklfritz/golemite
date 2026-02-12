#!/bin/bash
# A visual wizard for Zero-Knowledge users

# 1. Environment Fixes (The "Grandmaster" patches)
export DISPLAY=:0
export NO_AT_BRIDGE=1  # Suppresses annoying accessibility bus warnings
export LIBGL_ALWAYS_SOFTWARE=1 # Prevents DRI hardware errors in containers

# Exit if not in Desktop mode
if ! command -v zenity &> /dev/null; then
    echo "Zenity not found. Exiting."
    exit 0
fi

# 2. Welcome Dialog
zenity --info --title="Setup Wizard" \
       --text="Welcome to Golem Desktop.\n\nConfigure your Cloud Storage (Backblaze/AWS) to enable the Panic Button." \
       --width=400

# 3. Config Logic
if zenity --question --text="Launch Rclone Configuration?"; then
    xterm -T "Rclone Config" -geometry 100x30 -e "echo 'Running rclone config...'; echo ''; rclone config"
    
    if [ -f "/home/golem/.config/rclone/rclone.conf" ]; then
        zenity --info --text="✅ Configuration Saved!"
    fi
fi
