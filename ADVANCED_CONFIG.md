**File:** `ADVANCED_CONFIG.md`

```markdown
# Advanced Configuration 🔧

This guide is for users of `schnicklfritz/golem-desktop` or those creating custom orchestrations.

### Environment Variables
You can override these in your Docker Template (Docker Options `-e KEY=VALUE`).

| Variable | Default | Description |
|----------|---------|-------------|
| `RESOLUTION` | `1280x720` | Screen size (e.g., `1920x1080`). |
| `VNC_PASSWORD` | *(Empty)* | Protect your session with a password. |
| `DOWNLOAD_DIR` | `/workspace` | Target path on the container. |
| `DESKTOP_ENV` | `fluxbox` | Switch desktop (Desktop image only). |

### Cloud Sync (Backblaze/S3/Drive)
*Only available in Desktop Edition.*

1. **Launch Wizard:** On first startup, the desktop will prompt you to configure Rclone.
2. **Setup:** Follow the prompts (e.g., select Backblaze B2, enter keys).
3. **Panic Button:** Once configured, a "Panic Upload" icon appears on the desktop. Clicking this will immediately sync `/workspace` to your configured Cloud Storage.

### Rclone Automation
If you have an existing `rclone.conf`, you can mount it directly to skip the wizard:
` -v ./my-rclone.conf:/home/golem/.config/rclone/rclone.conf`

### HTTP File Server
The container exposes **Port 8000** as a direct HTTP file server.
*   **URL:** `http://ip:8000/`
*   **Purpose:** Allows ComfyUI nodes to scrape/pull files.
*   **Security Warning:** This port has no password. Anyone with the IP can download your files. Use firewall rules if running publicly.
