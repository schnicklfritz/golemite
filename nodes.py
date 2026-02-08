import requests
import os

class GolemController:
    """
    Controls the Satellite Golem Docker container.
    """
    def __init__(self):
        # Default local docker address
        self.golem_url = "http://localhost:6080/vnc.html"
        self.api_url = "http://localhost:6080/api" # If you add a python server later

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "action": (["open_satellite", "sync_from_cloud"],),
            },
            "optional": {
                "download_url": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "Golem"

    def execute(self, action, download_url=""):
        if action == "open_satellite":
            # Returns the URL to open in your local browser to see the Golem
            return (f"Control Satellite here: {self.golem_url}",)
        
        if action == "sync_from_cloud":
            # Logic to run 'rclone sync' locally to pull files from Backblaze
            # that the Golem uploaded
            # os.system("rclone sync b2:my-bucket/models /comfyui/models")
            return ("Syncing from Backblaze...",)
            
        return ("Action complete",)

# Node Export
NODE_CLASS_MAPPINGS = {
    "GolemController": GolemController
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "GolemController": "Golem Satellite Controller"
}
