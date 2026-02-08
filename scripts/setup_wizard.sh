#!/bin/bash
# A visual wizard for Zero-Knowledge users

# If we are in Kiosk mode (no zenity), exit immediately
if ! command -v zenity &> /dev/null; then
    exit 0
fi

# 1. Welcome Dialog
zenity --info --title="Welcome to Golem Desktop" \
       --text="This desktop environment helps you download AI models and sync them to the cloud.\n\nWe need to configure your Cloud Storage (Backblaze/AWS/Drive) so you can save files permanently." \
       --width=400

# 2. Ask to Config
if zenity --question --text="Do you want to configure Cloud Storage now via Rclone?"; then
    
    # Launch xterm running interactive rclone config
    # We use xterm because rclone is a text-based tool
    xterm -T "Rclone Configuration" -geometry 100x30 -e "echo 'Follow the prompts to add a New Remote.'; echo 'Recommended: Type n, name it b2, select Backblaze B2'; echo ''; rclone config"
    
    # After xterm closes (config done), show success
    if [ -f "/home/golem/.config/rclone/rclone.conf" ]; then
        zenity --info --text="✅ Configuration complete!\n\nYou can now use the 'Panic Upload' button on the desktop to sync downloads to the cloud."
    else
         zenity --warning --text="⚠️ It looks like configuration was cancelled or failed."
    fi
else
    zenity --warning --text="No storage configured. Files will only stay on this Pod until it is destroyed."
fi
