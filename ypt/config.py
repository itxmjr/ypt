"""Configuration constants and paths."""
import os
from pathlib import Path


class Config:
    """Paths and constants for installation."""

    # XDG paths
    HOME = Path.home()
    XDG_DATA_HOME = Path(os.environ.get("XDG_DATA_HOME", HOME / ".local/share"))
    XDG_CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))

    # Installation paths
    PT_HOME = XDG_DATA_HOME / "PacketTracer"
    BIN_DIR = HOME / ".local/bin"
    DESKTOP_DIR = XDG_DATA_HOME / "applications"
    ICON_DIR = XDG_DATA_HOME / "icons/hicolor/256x256/apps"

    # AppImage and shims
    APPIMAGE_PATH = PT_HOME / "packettracer.AppImage"
    SHIMS_DIR = PT_HOME / "shims"
    DEBUG_LOG = PT_HOME / "debug.log"

    # Launcher
    LAUNCHER_PATH = BIN_DIR / "packettracer"

    # Desktop entry
    DESKTOP_FILE = DESKTOP_DIR / "cisco-packet-tracer.desktop"
    ICON_NAME = "cisco-packet-tracer"

    # URL schemes
    URL_SCHEMES = ["ptsa", "ptsb", "ptsc"]
    MIME_TYPES = [
        "application/x-pkt",
        "application/x-pka",
        "application/x-pkz",
        "application/x-pks",
        "application/x-pksz",
    ]

    # Known browser binaries to check
    BROWSER_CANDIDATES = [
        "firefox",
        "firefox-wayland",
        "google-chrome-stable",
        "google-chrome",
        "chromium",
        "chromium-browser",
        "brave",
        "brave-browser",
        "falkon",
        "epiphany",
        "konqueror",
    ]

    # Desktop environments
    DE_KDE = "KDE"
    DE_GNOME = "GNOME"
    DE_XFCE = "XFCE"
    DE_GENERIC = "GENERIC"


class InstallError(Exception):
    """Base exception for installer errors."""
    pass


class ExtractError(InstallError):
    """Failed to extract archive."""
    pass


class BrowserNotFoundError(InstallError):
    """No suitable browser found."""
    pass


class DesktopIntegrationError(InstallError):
    """Failed to create desktop entry."""
    pass
