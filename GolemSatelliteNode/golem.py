import requests
import os
import folder_paths
import sys
import re
from tqdm import tqdm
from urllib.parse import quote

class GolemSatellite:
    """
    Connects to a Golem Satellite (Port 8000) to pull models via HTTP.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "golem_url": ("STRING", {"default": "http://127.0.0.1:8000", "multiline": False}),
                "filename": ("STRING", {"default": "model.safetensors", "multiline": False}),
                "target_type": (["checkpoints", "loras", "vae", "controlnet", "embeddings", "output"],),
                "force_redownload": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("local_path",)
    FUNCTION = "fetch"
    CATEGORY = "Golem"
    OUTPUT_NODE = True

    def _get_target_dir(self, target_type):
        """Resolves ComfyUI folder paths safely."""
        try:
            if target_type == "output":
                return folder_paths.get_output_directory()
            
            # ComfyUI helper returns a list of valid paths for this type
            paths = folder_paths.get_folder_paths(target_type)
            if not paths:
                print(f"⚠️ [Golem] No path found for type '{target_type}'. Defaulting to output.")
                return folder_paths.get_output_directory()
            
            return paths[0] # Return the first valid path (e.g. models/checkpoints)
        except Exception as e:
            print(f"❌ [Golem] Error resolving path: {e}")
            return "/tmp"

    def fetch(self, golem_url, filename, target_type, force_redownload):
        golem_url = golem_url.rstrip('/')
        target_dir = self._get_target_dir(target_type)
        local_path = os.path.join(target_dir, filename)
        
        # 1. Check if we already have it
        if os.path.exists(local_path) and not force_redownload:
            print(f"✅ [Golem] File exists: {local_path}")
            return (local_path,)

        # 2. Construct Remote URL (Handle spaces)
        safe_filename = quote(filename)
        remote_url = f"{golem_url}/{safe_filename}"
        
        print(f"🚀 [Golem] Downloading from {remote_url} to {local_path}...")
        
        # 3. Download Logic
        try:
            with requests.get(remote_url, stream=True, timeout=10) as r:
                if r.status_code == 404:
                    print(f"❌ [Golem] File not found on Satellite: {filename}")
                    # Try to list files to help user debug
                    try:
                        list_r = requests.get(golem_url, timeout=5)
                        print(f"Available files at {golem_url}:")
                        print(list_r.text[:500]) # Print first 500 chars of directory listing
                    except:
                        pass
                    raise ValueError(f"File not found: {filename}")
                
                r.raise_for_status()
                
                total_size = int(r.headers.get('content-length', 0))
                block_size = 1024 * 1024 # 1MB chunks
                
                # Use a .tmp file to avoid corrupting existing files on interrupt
                temp_path = local_path + ".tmp"
                
                with open(temp_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            
            # Rename on success
            if os.path.exists(local_path):
                os.remove(local_path)
            os.rename(temp_path, local_path)
            
            print(f"🏁 [Golem] Download Complete: {local_path}")
            return (local_path,)

        except Exception as e:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

NODE_CLASS_MAPPINGS = {
    "GolemSatellite": GolemSatellite
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "GolemSatellite": "🛰️ Golem Direct Downloader"
}

