How to use this Updated Node

    Launch your Cloud Golem: Make sure it's running (Port 8000 exposed). Note the IP (e.g., 24.56.78.90).

    Launch Local ComfyUI:

        Add Node > Golem > 🛰️ Golem Satellite Downloader.

    Configure:

        golem_url: http://24.56.78.90:8000 (Use your cloud IP).

        filename: flux1-dev-fp8.safetensors (Must match the file inside your Golem /workspace).

        target_folder: checkpoints.

    Connect Output: Connect the local_path string output to a Load Checkpoint node (optional, or just use it as a standalone download step).

    Run:

        It will pull the file over HTTP.

        Check your local console/terminal to see the tqdm progress bar:
        Downloading flux1-dev.sft: 45%|████▌ | 4.50G/10.0G [02:30<03:15, 28.5MB/s]
