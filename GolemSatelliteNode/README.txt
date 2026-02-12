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

# 🔧 Golem Troubleshooting Guide

If things aren't working, follow this checklist in order.

### 🛑 Problem 1: "The Node Does Nothing"
**Symptom:** You press "Queue Prompt" in ComfyUI, the node turns green for a split second, but no file appears.

**Step 1: Verify the Satellite Connection**
The most common error is the wrong IP address or Port.
1. Open a new browser tab.
2. Go to: `http://YOUR_POD_IP:8000`
   *   **Result A:** You see a file directory listing? ✅ Connection Good.
   *   **Result B:** "Site cannot be reached"? ❌ Your Pod IP is wrong, or Port 8000 isn't mapped.
3. Go to: `http://YOUR_POD_IP:8000/api/latest`
   *   **Result A:** You see JSON `{ "filename": "model.safetensors" }`? ✅ API is working.
   *   **Result B:** `{ "error": "No files found..." }`? ⚠️ The Golem /workspace is empty. Download something first!

**Step 2: Check the Console**
ComfyUI prints the real errors to the **Black Console Window** (not the web UI).
*   Look for: `requests.exceptions.ConnectionError` -> Connection failed.
*   Look for: `HTTPError: 404 Client Error` -> The filename "auto" failed to find a file.

---

### 🛑 Problem 2: "Setup Wizard Crashes" (DRI / Machine ID Error)
**Symptom:** You try to run the wizard manually in the terminal and get `libGL error` or `machine-id` error.

**Fix 1: Generate Machine ID**
Run this command in the Pod Terminal:
```bash
dbus-uuidgen > /etc/machine-id

### Part 3: Node User Guide (Readme)

Include this section in the `ComfyUI-Golem` Node repository.

```markdown
# 🛰️ Golem ComfyUI Node

This node automatically fetches models from your Golem Satellite.

### The "Auto" Mode (Magic 🪄)
1. **Satellite:** Open the Golem Browser and download a file (e.g., `super_realism_xl.safetensors`).
2. **ComfyUI:**
   *   Add the **Golem Auto-Fetcher** node.
   *   Set `golem_url`: `http://YOUR_POD_IP:8000`.
   *   Set `filename`: `auto`.
3. **Queue Prompt.**
   *   The node asks the satellite: *"What is the newest file?"*
   *   Satellite replies: *"It's super_realism_xl.safetensors"*.
   *   The node downloads it to your `checkpoints` folder automatically.

### Manual Mode
If you want a specific file that isn't the newest:
*   Set `filename` to the exact name: `my_specific_lora.safetensors`.

### Config Checklist
*   [ ] Did you copy the IP from QuickPod correctly?
*   [ ] Is the port **8000**? (Not 6080).
*   [ ] Did you actually download a file to the satellite first?
