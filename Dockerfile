FROM archlinux:latest AS base

# Optimization
RUN echo 'NoExtract = usr/share/help/* usr/share/doc/* usr/share/man/* usr/share/locale/*' > /etc/pacman.d/noextract.conf && \
    echo 'Include = /etc/pacman.d/noextract.conf' >> /etc/pacman.conf

# Dependencies (Added xorg-xhost for wizard display fix)
RUN pacman-key --init && \
    pacman-key --populate archlinux && \
    pacman -Sy --noconfirm archlinux-keyring && \
    pacman -Su --noconfirm && \
    pacman -S --noconfirm \
    xorg-server xorg-server-xvfb xorg-xdpyinfo xorg-xhost x11vnc \
    chromium ttf-liberation ttf-dejavu \
    python python-pip \
    supervisor \
    openbsd-netcat \
    git \
    && pacman -Scc --noconfirm

RUN git clone --depth 1 https://github.com/novnc/noVNC.git /usr/share/novnc && \
    git clone --depth 1 https://github.com/novnc/websockify /usr/share/novnc/utils/websockify && \
    chmod +x /usr/share/novnc/utils/novnc_proxy

# Setup
RUN useradd -m -G video golem
WORKDIR /home/golem
ENV DISPLAY=:0 RESOLUTION=1280x720 DOWNLOAD_DIR=/workspace
RUN mkdir -p /home/golem/.config/chromium /home/golem/scripts /home/golem/logs /workspace && \
    chown -R golem:golem /home/golem /workspace

# COPY SCRIPTS (Make sure server.py is in your local folder)
COPY --chown=golem:golem scripts/ /home/golem/scripts/
COPY --chown=golem:golem supervisord.conf /etc/supervisord.conf
RUN chmod +x /home/golem/scripts/*.sh && chmod +x /home/golem/scripts/*.py

# KIOSK Build
FROM base AS kiosk
RUN pacman -S --noconfirm openbox && pacman -Scc --noconfirm
ENV DESKTOP_ENV=openbox WM_COMMAND=openbox
USER golem
EXPOSE 6080 5900 8000
ENTRYPOINT ["/home/golem/scripts/entrypoint.sh"]

# DESKTOP Build
FROM base AS desktop
RUN pacman -S --noconfirm fluxbox rclone zenity unzip wget python-setuptools xterm && pacman -Scc --noconfirm
RUN pip install --break-system-packages uv watchdog
ENV DESKTOP_ENV=fluxbox WM_COMMAND=fluxbox SETUP_WIZARD=true
USER golem
EXPOSE 6080 5900 8000
ENTRYPOINT ["/home/golem/scripts/entrypoint.sh"]
