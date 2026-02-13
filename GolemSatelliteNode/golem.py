import requests
import os
import folder_paths
from urllib.parse import quote
from tqdm import tqdm # Added for "Wisdom" progress tracking

class GolemSatellite:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "golem_url": ("STRING", {"default": "http://IP:40XXX", "multiline": False}),
                "filename": ("STRING", {"default": "auto", "multiline": False}),
                "target_type": (["checkpoints", "loras", "vae", "controlnet", "embeddings", "output"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "fetch"
    CATEGORY = "Golem"

    def fetch(self, golem_url, filename, target_type):
        golem_url = golem_url.rstrip('/')
        # 1. BROWSER MASK: Bypass RunPod Proxy filters
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*"
        }

        # 2. AUTO-DISCOVERY
        if filename.lower() in ["auto", ""]:
            try:
                r = requests.get(f"{golem_url}/api/latest", headers=headers, timeout=10)
                r.raise_for_status()
                filename = r.json().get("filename")
                if not filename: raise ValueError("No file found on satellite.")
                print(f"¿ [Golem] Target identified: {filename}")
            except Exception as e:
                raise ValueError(f"¿ [Golem] Antenna Lost! Check IP/Port. Error: {e}")

        # 3. PATH LOGIC
        target_dir = folder_paths.get_folder_paths(target_type)[0] if target_type != "output" else folder_paths.get_output_directory()
        local_path = os.path.join(target_dir, filename)

        if os.path.exists(local_path):
            print(f"¿ [Golem] File already exists: {filename}")
            return (local_path,)

        # 4. HIGH-SPEED DOWNLOAD
        print(f"¿ [Golem] Initiating Download: {filename}")
        remote_url = f"{golem_url}/{quote(filename)}"
        
        try:
            # Increased timeout to 0 (infinite) for massive 50GB models
            with requests.get(remote_url, headers=headers, stream=True, timeout=None) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                
                with open(local_path + ".tmp", 'wb') as f, tqdm(
                    desc=f"¿ Golem: {filename}",
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in r.iter_content(chunk_size=1024*1024): # 1MB Chunks
                        size = f.write(chunk)
                        bar.update(size)

            os.rename(local_path + ".tmp", local_path)
            return (local_path,)
        except Exception as e:
            if os.path.exists(local_path + ".tmp"): os.remove(local_path + ".tmp")
            raise ValueError(f"¿ [Golem] Signal Dropped mid-transfer: {e}")

NODE_CLASS_MAPPINGS = { "GolemSatellite": GolemSatellite }
NODE_DISPLAY_NAME_MAPPINGS = { "GolemSatellite": "¿ Golem Auto-Fetcher" }
