import json
import os

PREFS_DIR = "/home/golem/.config/chromium/Default"
PREFS_FILE = os.path.join(PREFS_DIR, "Preferences")
DOWNLOAD_DIR = "/home/golem/Downloads"

def ensure_prefs():
    if not os.path.exists(PREFS_DIR):
        os.makedirs(PREFS_DIR, exist_ok=True)
    
    prefs = {}
    if os.path.exists(PREFS_FILE):
        try:
            with open(PREFS_FILE, 'r') as f:
                prefs = json.load(f)
        except:
            pass 

    # --- ENFORCE DOWNLOAD SETTINGS (CRITICAL FOR KIOSK) ---
    prefs.setdefault('download', {})
    prefs['download']['default_directory'] = DOWNLOAD_DIR
    prefs['download']['prompt_for_download'] = False  # Don't ask, just save
    prefs['download']['directory_upgrade'] = True
    
    # --- ENFORCE UI SETTINGS ---
    prefs.setdefault('browser', {})
    prefs['browser']['has_seen_welcome_page'] = True
    prefs['browser']['check_should_create_default_profile'] = False
    
    # --- WRITE BACK ---
    with open(PREFS_FILE, 'w') as f:
        json.dump(prefs, f)
    print(f"Chromium Configured: Auto-save to {DOWNLOAD_DIR}")

if __name__ == "__main__":
    ensure_prefs()
