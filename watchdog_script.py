import time
import os
import subprocess
from pathlib import Path

DOWNLOAD_DIR = "/home/golem/Downloads"
RCLONE_REMOTE = "b2:my-golem-bucket/incoming"

def upload_file(filepath):
    print(f"Detected new file: {filepath}")
    # Wait for .crdownload file to disappear (meaning download finished)
    while str(filepath).endswith('.crdownload'):
        time.sleep(1)
    
    # Run Rclone
    cmd = ["rclone", "move", str(filepath), RCLONE_REMOTE, "--progress"]
    subprocess.run(cmd)
    print(f"Uploaded {filepath} to Cloud Storage")

def monitor():
    print(f"Watching {DOWNLOAD_DIR}...")
    existing_files = set(os.listdir(DOWNLOAD_DIR))
    
    while True:
        time.sleep(2)
        current_files = set(os.listdir(DOWNLOAD_DIR))
        new_files = current_files - existing_files
        
        for f in new_files:
            if not f.endswith('.tmp') and not f.endswith('.crdownload'):
                full_path = Path(DOWNLOAD_DIR) / f
                upload_file(full_path)
        
        existing_files = current_files

if __name__ == "__main__":
    monitor()
