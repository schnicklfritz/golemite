#!/bin/bash
# Panic Button: Finds the first Rclone remote and Syncs Downloads

# Function to show graphical alerts since this runs from a GUI icon
alert() {
    if command -v zenity &> /dev/null; then
        zenity --info --text="$1"
    else
        echo "$1"
    fi
}

error() {
    if command -v zenity &> /dev/null; then
        zenity --error --text="$1"
    else
        echo "Error: $1"
    fi
}

# 1. Check if Config exists
if [ ! -f "/home/golem/.config/rclone/rclone.conf" ]; then
    error "No Cloud Storage configured!\nPlease run the Setup Wizard first."
    exit 1
fi

# 2. Get list of remotes (stripping newlines)
REMOTE=$(rclone listremotes | head -n 1)

if [ -z "$REMOTE" ]; then
    error "Rclone config found, but no Remotes are defined."
    exit 1
fi

# 3. Open terminal to show progress (User needs to see it happening)
xterm -T "Panic Syncing..." -hold -e "
echo '--- 🚨 PANIC SYNC INITIATED 🚨 ---'
echo '✅ Found Remote: $REMOTE'
echo '📂 Source: /home/golem/Downloads'
echo '☁️  Dest:   ${REMOTE}panic-backup/'
echo '---'
echo 'Syncing now... (This may take time)'
rclone copy '/home/golem/Downloads' '${REMOTE}panic-backup/' -P
echo '---'
echo '✅ Sync Complete.'
"
