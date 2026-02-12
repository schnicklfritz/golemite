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
