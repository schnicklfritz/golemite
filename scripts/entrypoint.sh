#!/bin/bash

# --- 1. Silent Storage Mapping ---
# Zero Config assumption: The user wants files in /workspace (Standard for QuickPod/RunPod)
TARGET_DIR="${DOWNLOAD_DIR:-/workspace}"

if [ ! -d "$TARGET_DIR" ]; then
    # Create it silently if missing
    mkdir -p "$TARGET_DIR"
fi

# Link internal Downloads to the persistent workspace
if [ -d "/home/golem/Downloads" ] && [ ! -L "/home/golem/Downloads" ]; then
    rm -rf /home/golem/Downloads
fi
ln -sfn "$TARGET_DIR" /home/golem/Downloads

# --- 2. VNC Password (Optional) ---
VNC_AUTH_FLAG="-nopw"
if [ ! -z "$VNC_PASSWORD" ]; then
    mkdir -p /home/golem/.vnc
    x11vnc -storepasswd "$VNC_PASSWORD" /home/golem/.vnc/passwd
    VNC_AUTH_FLAG="-rfbauth /home/golem/.vnc/passwd"
fi
export VNC_AUTH_FLAG

# --- 3. Set Window Manager Command ---
case "$DESKTOP_ENV" in
    "fluxbox")
        WM_COMMAND="fluxbox"
        ;;
    "openbox")
        WM_COMMAND="openbox"
        ;;
    *)
        WM_COMMAND="fluxbox"  # Default fallback
        ;;
esac
export WM_COMMAND

# --- 4. Launch ---
echo "✅ Golem Satellite Started."
echo "📂 Downloads mapping: /home/golem/Downloads -> $TARGET_DIR"
echo "🖥️  Mode: $DESKTOP_ENV"

exec supervisord -c /etc/supervisord.conf
