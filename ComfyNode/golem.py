import requests
import os
import folder_paths
import sys
from tqdm import tqdm
import re

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
                "golem_url": ("STRING", {"default": "http://localhost:8000", "multiline": False}),
                "filename": ("STRING", {"default": "model.safetensors", "multiline": False}),
                "target_folder": (["checkpoints", "loras", "vae", "controlnet", "embeddings", "output"],),
            },
            "optional": {
                "force_redownload": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("local_path",)
    FUNCTION = "fetch"
    CATEGORY = "Golem"
    OUTPUT_NODE = True

    def _get_local_path(self, target_folder, filename):
        """Resolves where to save the file based on ComfyUI config"""
        if target_folder == "output":
            base_dir = folder_paths.get_output_directory()
        else:
            # Get the first configured path for this type (usually the standard models/type folder)
            paths = folder_paths.get_folder_paths(target_folder)
            base_dir = paths[0] if paths else "output"
        
        return os.path.join(base_dir, filename)

    def _list_remote_files(self, base_url):
        """Helper to print available files on the Golem if download fails"""
        try:
            r = requests.get(base_url, timeout=5)
            if r.status_code == 200:
                # Poor man's HTML parsing to find links
                files = re.findall(r'href=["\'](.*?)["\']', r.text)
                clean_files = [f for f in files if not f.startswith('.') and not f.endswith('/')]
                print(f"\n📡 Golem File List ({base_url}):")
                for f in clean_files:
                    print(f" - {f}")
        except:
            print(f"⚠️ Could not reach Golem at {base_url} to list files.")

    def fetch(self, golem_url, filename, target_folder, force_redownload):
        # Clean URL
        golem_url = golem_url.rstrip('/')
        
        # Determine Local Path
        local_path = self._get_local_path(target_folder, filename)
        
        # Check Exists
        if os.path.exists(local_path) and not force_redownload:
            print(f"✅ [Golem] File exists: {local_path}. Skipping download.")
            return (local_path,)

        remote_file_url = f"{golem_url}/{filename}"
        
        print(f"🚀 [Golem] Connecting to {remote_file_url}...")
        
        try:
            # Stream request to handle large files
            with requests.get(remote_file_url, stream=True, timeout=10) as r:
                
                # If 404, scan directory to help user
                if r.status_code == 404:
                    print(f"❌ [Golem] File not found: {filename}")
                    self._list_remote_files(golem_url)
                    raise ValueError(f"File '{filename}' not found on Satellite. Check console for list.")
                
                r.raise_for_status()
                
                total_size = int(r.headers.get('content-length', 0))
                block_size = 1024 * 1024 # 1MB chunks
                
                # Download to temp file first
                temp_path = local_path + ".download"
                
                with open(temp_path, 'wb') as f, tqdm(
                    desc=f"Downloading {filename}",
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in r.iter_content(chunk_size=block_size):
                        size = f.write(chunk)
                        bar.update(size)
                        
            # Rename on success
            if os.path.exists(local_path):
                os.remove(local_path)
            os.rename(temp_path, local_path)
            
            print(f"🏁 [Golem] Download finished: {local_path}")
            return (local_path,)

        except Exception as e:
            # Cleanup temp file on failure
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

NODE_CLASS_MAPPINGS = {
    "GolemSatellite": GolemSatellite
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GolemSatellite": "🛰️ Golem Satellite Downloader"
}
