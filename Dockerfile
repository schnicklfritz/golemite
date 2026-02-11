# ==========================================
# Golem Satellite (CPU Optimized)
# ==========================================
FROM archlinux:latest AS base

# 1. Optimize Pacman
RUN echo 'NoExtract = usr/share/help/* usr/share/doc/* usr/share/man/* usr/share/locale/*' > /etc/pacman.d/noextract.conf && \
    echo 'Include = /etc/pacman.d/noextract.conf' >> /etc/pacman.conf

# 2. Install Deps (Fixed Missing novnc)
RUN pacman-key --init && \
    pacman-key --populate archlinux && \
    pacman -Sy --noconfirm archlinux-keyring && \
    pacman -Su --noconfirm && \
    pacman -S --noconfirm \
    xorg-server xorg-server-xvfb x11vnc \
    chromium ttf-liberation ttf-dejavu \
    python python-pip git \
    supervisor \
    openbsd-netcat \
    && pacman -Scc --noconfirm

# 3. Manually Install noVNC (The Missing Piece)
RUN git clone --depth 1 https://github.com/novnc/noVNC.git /usr/share/novnc && \
    git clone --depth 1 https://github.com/novnc/websockify /usr/share/novnc/utils/websockify && \
    chmod +x /usr/share/novnc/utils/novnc_proxy

# 4. Setup User & Dirs
RUN useradd -m -G video golem
WORKDIR /home/golem
ENV DISPLAY=:0 \
    RESOLUTION=1280x720 \
    DOWNLOAD_DIR=/workspace \
    WM_COMMAND=fluxbox \
    VNC_AUTH_FLAG=""

# Create the ACTUAL download directory
RUN mkdir -p /home/golem/.config/chromium \
    /home/golem/scripts \
    /home/golem/logs \
    /workspace && \
    chown -R golem:golem /home/golem /workspace

# 5. Copy Scripts
COPY --chown=golem:golem scripts/entrypoint.sh /home/golem/scripts/
COPY --chown=golem:golem scripts/start_chromium.sh /home/golem/scripts/
COPY --chown=golem:golem supervisord.conf /etc/supervisord.conf
RUN chmod +x /home/golem/scripts/*.sh

# ==========================================
# BUILD: KIOSK
# ==========================================
FROM base AS kiosk
RUN pacman -S --noconfirm openbox && pacman -Scc --noconfirm
ENV DESKTOP_ENV=openbox WM_COMMAND=openbox

# Fix: QuickPod usually runs as root, but we can drop to user if desired.
# For simplicity in file permissions, running as root is often easier on rental pods,
# but if you use 'golem', ensure /workspace is writable (which we did above).
USER golem
EXPOSE 6080 5900 8000
ENTRYPOINT ["/home/golem/scripts/entrypoint.sh"]
