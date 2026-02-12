kimport requests
import os
import folder_paths
from urllib.parse import quote

class GolemSatellite:
    """
    Auto-fetches models from Golem Satellite. 
    Leave filename as 'auto' to grab the most recent download.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "golem_url": ("STRING", {"default": "http://127.0.0.1:8000", "multiline": False}),
                "filename": ("STRING", {"default": "auto", "multiline": False}),
                "target_type": (["checkpoints", "loras", "vae", "controlnet", "embeddings", "output"],),
                "delete_after_download": ("BOOLEAN", {"default": False, "label_on": "Yes (Clean Satellite)", "label_off": "No (Keep Backup)"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("local_path",)
    FUNCTION = "fetch"
    CATEGORY = "Golem"
    OUTPUT_NODE = True

    def _get_target_dir(self, target_type):
        try:
            if target_type == "output":
                return folder_paths.get_output_directory()
            paths = folder_paths.get_folder_paths(target_type)
            return paths[0] if paths else folder_paths.get_output_directory()
        except:
            return "."

    def fetch(self, golem_url, filename, target_type, delete_after_download):
        golem_url = golem_url.rstrip('/')
        
        # 1. AUTO DISCOVERY
        if filename == "auto" or filename == "":
            print(f"📡 [Golem] Asking satellite for latest file...")
            try:
                api_r = requests.get(f"{golem_url}/api/latest", timeout=5)
                data = api_r.json()
                if "error" in data:
                    raise ValueError(f"Satellite reported error: {data['error']}")
                filename = data['filename']
                print(f"🎯 [Golem] Found new file: {filename}")
            except Exception as e:
                raise ValueError(f"Could not connect to Golem at {golem_url}. Is the pod running? Error: {e}")

        # 2. Setup Paths
        target_dir = self._get_target_dir(target_type)
        local_path = os.path.join(target_dir, filename)

        if os.path.exists(local_path):
            print(f"✅ [Golem] File exists locally: {filename}. Skipping.")
            return (local_path,)

        # 3. Download
        safe_filename = quote(filename)
        remote_url = f"{golem_url}/{safe_filename}"
        print(f"🚀 [Golem] Downloading {filename}...")

        try:
            with requests.get(remote_url, stream=True, timeout=20) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                # Write to temp
                with open(local_path + ".tmp", 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024*1024): # 1MB chunks
                        f.write(chunk)
            
            os.rename(local_path + ".tmp", local_path)
            print(f"🏁 [Golem] Saved to {local_path}")
            
            # Optional: Delete from Satellite? 
            # (Note: Requires a delete endpoint, effectively implemented via rclone on panic button side usually, 
            # or manual. For HTTP safety, I did not enable remote deletion via this node yet to prevent accidents.)
            
            return (local_path,)

        except Exception as e:
            if os.path.exists(local_path + ".tmp"):
                os.remove(local_path + ".tmp")
            raise e

NODE_CLASS_MAPPINGS = { "GolemSatellite": GolemSatellite }
NODE_DISPLAY_NAME_MAPPINGS = { "GolemSatellite": "🛰️ Golem Auto-Fetcher" }
