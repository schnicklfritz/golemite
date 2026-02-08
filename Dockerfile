# ==========================================
# 1. SHARED BASE (The Engine)
# ==========================================
FROM archlinux:latest AS base

# Optimization: Diet Arch (No Docs/Locales) to save space
RUN sed -i 's/#NoExtract/NoExtract/' /etc/pacman.conf && \
    sed -i '/NoExtract/ s/$/ usr\/share\/help\/* usr\/share\/doc\/* usr\/share\/man\/* usr\/share\/locale\/*/' /etc/pacman.conf

# Core Dependencies (Corrected)
# 1. Initialize keyring (Fixes "no secret key" error)
# 2. Update keyring specifically first
# 3. Update system (-Su)
# 4. Install packages using Arch-specific names
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
    && pacman -Scc --noconfirm
# Common Setup
RUN useradd -m -G video golem
WORKDIR /home/golem
ENV DISPLAY=:0 \
    RESOLUTION=1280x720 \
    DOWNLOAD_DIR=/workspace

# Structure
RUN mkdir -p /home/golem/.config/chromium \
    /home/golem/scripts \
    /home/golem/logs \
    /workspace

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

# Install ONLY Kiosk window manager
RUN pacman -S --noconfirm matchbox-window-manager && pacman -Scc --noconfirm

# Set Envs for Zero Config
ENV DESKTOP_ENV=matchbox-window-manager \
    SETUP_WIZARD=false

USER golem
# 6080=VNC-Web, 5900=Raw-VNC, 8000=FileServer
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
    git \
    python-setuptools \
    xterm \
    && pacman -Scc --noconfirm

# Install UV (fast python) and Watchdog
RUN pip install --break-system-packages uv watchdog

# Set Envs for Advanced Mode
ENV DESKTOP_ENV=fluxbox \
    SETUP_WIZARD=true \
    VNC_PASSWORD=""

# Add Desktop Scripts
COPY --chown=golem:golem scripts/panic_button.sh /home/golem/scripts/
COPY --chown=golem:golem scripts/setup_wizard.sh /home/golem/scripts/
RUN chmod +x /home/golem/scripts/*.sh

USER golem
EXPOSE 6080 5900 8000
ENTRYPOINT ["/home/golem/scripts/entrypoint.sh"]
