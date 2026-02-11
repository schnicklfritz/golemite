# ==========================================
# 1. SHARED BASE (The Engine)
# ==========================================
FROM archlinux:latest AS base

# Optimization: Diet Arch (No Docs)
RUN echo 'NoExtract = usr/share/help/* usr/share/doc/* usr/share/man/* usr/share/locale/*' > /etc/pacman.d/noextract.conf && \
    echo 'Include = /etc/pacman.d/noextract.conf' >> /etc/pacman.conf

# Core Dependencies + git for noVNC
RUN pacman-key --init && \
    pacman-key --populate archlinux && \
    pacman -Sy --noconfirm archlinux-keyring && \
    pacman -Su --noconfirm && \
    pacman -S --noconfirm \
    xorg-server xorg-server-xvfb x11vnc \
    chromium ttf-liberation ttf-dejavu \
    python python-pip \
    supervisor \
    openbsd-netcat \
    git \
    && pacman -Scc --noconfirm

# INSTALL noVNC MANUALLY
RUN git clone --depth 1 https://github.com/novnc/noVNC.git /usr/share/novnc && \
    git clone --depth 1 https://github.com/novnc/websockify /usr/share/novnc/utils/websockify && \
    chmod +x /usr/share/novnc/utils/novnc_proxy

# Common Setup
RUN useradd -m -G video golem
WORKDIR /home/golem
ENV DISPLAY=:0 \
    RESOLUTION=1280x720 \
    DOWNLOAD_DIR=/workspace \
    WM_COMMAND=fluxbox \
    VNC_AUTH_FLAG="" \
    DESKTOP_ENV=fluxbox

# Structure
RUN mkdir -p /home/golem/.config/chromium \
    /home/golem/scripts \
    /home/golem/logs \
    /workspace && \
    chown -R golem:golem /home/golem /workspace

# Copy Shared Scripts
COPY --chown=golem:golem scripts/entrypoint.sh /home/golem/scripts/
COPY --chown=golem:golem scripts/start_chromium.sh /home/golem/scripts/
COPY --chown=golem:golem scripts/configure_chromium.py /home/golem/scripts/
COPY --chown=golem:golem scripts/landing.html /home/golem/scripts/
COPY --chown=golem:golem supervisord.conf /etc/supervisord.conf

RUN chmod +x /home/golem/scripts/*.sh && chmod +x /home/golem/scripts/*.py

# ==========================================
# 2. BUILD A: GOLEM KIOSK (Zero Config)
# ==========================================
FROM base AS kiosk
RUN pacman -S --noconfirm openbox && pacman -Scc --noconfirm
ENV DESKTOP_ENV=openbox SETUP_WIZARD=false WM_COMMAND=openbox
USER golem
EXPOSE 6080 5900 8000
ENTRYPOINT ["/home/golem/scripts/entrypoint.sh"]

# ==========================================
# 3. BUILD B: GOLEM DESKTOP (The "Gentoo" Build)
# ==========================================
FROM base AS desktop

# Install Power User Tools
RUN pacman -S --noconfirm \
    fluxbox \
    rclone \
    zenity \
    unzip \
    wget \
    python-setuptools \
    xterm \
    && pacman -Scc --noconfirm

# Install Watchdog
RUN pip install --break-system-packages uv watchdog

# Set Envs for Advanced Mode
ENV DESKTOP_ENV=fluxbox \
    SETUP_WIZARD=true \
    WM_COMMAND=fluxbox

# Add Desktop Scripts
COPY --chown=golem:golem scripts/panic_button.sh /home/golem/scripts/
COPY --chown=golem:golem scripts/setup_wizard.sh /home/golem/scripts/
RUN chmod +x /home/golem/scripts/*.sh

USER golem
EXPOSE 6080 5900 8000
ENTRYPOINT ["/home/golem/scripts/entrypoint.sh"]

