"""Debug and diagnostic tools for troubleshooting."""
import os
import subprocess
from pathlib import Path

from .config import Config


class DebugDiagnostics:
    """Collect diagnostic information about the environment."""

    def __init__(self):
        self.report = []

    def collect(self):
        """Collect all diagnostic information."""
        self.report = []
        self._collect_system_info()
        self._collect_environment()
        self._collect_browser_info()
        self._collect_installation()
        return "\n".join(self.report)

    def _collect_system_info(self):
        """Collect system information."""
        self.report.append("=" * 50)
        self.report.append("SYSTEM INFORMATION")
        self.report.append("=" * 50)

        # OS info
        if Path("/etc/os-release").exists():
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith(("NAME=", "VERSION=", "ID=")):
                        self.report.append(line.strip())

        # Session type
        self.report.append(f"XDG_SESSION_TYPE: {os.environ.get('XDG_SESSION_TYPE', 'not set')}")
        self.report.append(f"XDG_CURRENT_DESKTOP: {os.environ.get('XDG_CURRENT_DESKTOP', 'not set')}")
        self.report.append(f"WAYLAND_DISPLAY: {os.environ.get('WAYLAND_DISPLAY', 'not set')}")
        self.report.append(f"DISPLAY: {os.environ.get('DISPLAY', 'not set')}")

    def _collect_environment(self):
        """Collect relevant environment variables."""
        self.report.append("")
        self.report.append("=" * 50)
        self.report.append("ENVIRONMENT")
        self.report.append("=" * 50)

        keys = [
            "PATH",
            "HOME",
            "XDG_DATA_HOME",
            "XDG_CONFIG_HOME",
            "DBUS_SESSION_BUS_ADDRESS",
            "BROWSER",
            "QT_QPA_PLATFORM",
        ]

        for key in keys:
            value = os.environ.get(key, "not set")
            # Truncate long values
            if len(value) > 100:
                value = value[:100] + "..."
            self.report.append(f"{key}: {value}")

    def _collect_browser_info(self):
        """Collect browser information."""
        self.report.append("")
        self.report.append("=" * 50)
        self.report.append("BROWSER DETECTION")
        self.report.append("=" * 50)

        import shutil
        for browser in Config.BROWSER_CANDIDATES[:5]:  # Check first 5
            path = shutil.which(browser)
            self.report.append(f"{browser}: {path or 'not found'}")

    def _collect_installation(self):
        """Check installation status."""
        self.report.append("")
        self.report.append("=" * 50)
        self.report.append("INSTALLATION STATUS")
        self.report.append("=" * 50)

        paths = [
            ("PT_HOME", Config.PT_HOME),
            ("AppImage", Config.APPIMAGE_PATH),
            ("Launcher", Config.LAUNCHER_PATH),
            ("Desktop entry", Config.DESKTOP_FILE),
        ]

        for name, path in paths:
            status = "exists" if path.exists() else "NOT FOUND"
            self.report.append(f"{name} ({path}): {status}")

    def save_report(self, path=None):
        """Save report to file."""
        report_path = path or (Config.PT_HOME / "diagnostic.log")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(self.collect())
        return report_path
