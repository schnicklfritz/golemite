# Golem Satellite 🛰️

**One Tool, Two Flavors.**
Stop fighting slow internet. Use a data-center satellite browser to download models directly to your cloud workspace, or act as a high-speed "Sidecar" browser for your local ComfyUI.

## 📦 Choose Your Version

### 🟢 1. The "Zero Config" Kiosk (Recommended)
**Docker Image:** `schnicklbob/golem-kiosk:latest`
*   **Best for:** 90% of users. 
*   **Interface:** Fullscreen Browser (No windows, no OS).
*   **Behavior:** Downloads automatically go to `/workspace`.

### 🔴 2. The "Power User" Desktop
**Docker Image:** `schnicklbob/golem-desktop:latest`
*   **Best for:** Tinkerers, Python devs, Data Hoarders.
*   **Interface:** Full Desktop (Fluxbox) with taskbar and windows.
*   **Features:** Cloud Sync Wizard (Rclone), Panic Button, `uv` (fast python), Terminal.

---

## ☁️ Cloud Quick Start (RunPod / QuickPod / Vast)

1. **Deploy Pod:** Select one of the images above.
2. **Ports:** Ensure Port `6080` (HTTP) is exposed.
3. **Launch.**
4. **Click Connect (HTTP/6080):** 
   *   Browse to any site (Civitai, Tensor.art).
   *   Click Download.
   *   Files appear instantly in `/workspace`.

**Using with ComfyUI?** 
If your Cloud GPU is running ComfyUI on the same pod, the files are already there!

---

## 🏠 Running Locally (The "Universal Downloader")

You can run this container on your home computer (Windows or Linux) to map your local models folder to the Satellite browser. When you click download in the Satellite, the file saves directly to your hard drive without moving or renaming files.

### 🐧 For Linux Users

**Prerequisite:** [Docker Installed](https://docs.docker.com/engine/install/).

1. **Determine your Models Path:**
   Find where your ComfyUI models are stored (e.g., `~/ComfyUI/models`).

2. **Run the Command:**
   ```bash
   docker run -d \
     --name golem-sidecar \
     -p 6080:6080 \
     -v ~/ComfyUI/models:/workspace \
     schnicklbob/golem-kiosk:latest
    Browse:

        Open your regular browser to http://localhost:6080.

        Navigate to a site and click download.

        The file will appear in your actual ~/ComfyUI/models folder on your Linux machine.

(Note: If files don't appear, ensure your local user has write permissions to that directory).


🪟 For Windows Users

Prerequisite: Docker Desktop.

    Open PowerShell.

    Run the Command:
    (Replace the path C:\ComfyUI\models with your actual folder location).
docker run -d `
  --name golem-sidecar `
  -p 6080:6080 `
  -v "C:\ComfyUI\models:/workspace" `
  schnicklbob/golem-kiosk:latest

    Browse: Open http://localhost:6080 and start downloading directly into your folders.

🔌 Using the GolemFetch Node

If you want to pull files from a Remote Satellite to your Local ComfyUI (over slow internet):

    On Satellite: Deploy golem-kiosk in the cloud. Note the IP.

    On Local ComfyUI: Install the Golem Custom Nodes (separate repo).

    In ComfyUI:

        Add the Golem Satellite Downloader node.

        Set Address to http://YOUR-CLOUD-IP:8000 (Note port 8000).

        Enter the filename you downloaded on the satellite.

        Queue Prompt.

The node will reliably pull the file to your computer.
