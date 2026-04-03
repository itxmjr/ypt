"""ypt - Your Packet Tracer Installer

Installs Cisco Packet Tracer from .deb on any Linux distro.
Fixes login button browser opening on Wayland.
"""

__version__ = "1.0.0"
__all__ = [
    "DebExtractor",
    "AppImageInstaller",
    "DesktopIntegration",
    "BrowserDetector",
    "LauncherGenerator",
    "UrlHandlerShim",
]
