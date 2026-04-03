"""Create .desktop files and register MIME types."""
import subprocess
from pathlib import Path

from .config import Config, DesktopIntegrationError


class DesktopIntegration:
    """Integrate with desktop environment."""

    DESKTOP_ENTRY_TEMPLATE = """[Desktop Entry]
Version=1.0
Type=Application
Name=Cisco Packet Tracer
GenericName=Network Simulator
Comment=Cisco Packet Tracer network simulation tool
Exec={launcher} %U
Icon={icon}
Terminal=false
Categories=Education;Network;Science;
Keywords=cisco;networking;simulation;packet;tracer;
StartupNotify=true
StartupWMClass=PacketTracer
MimeType={mime_types};
"""

    def create_desktop_entry(self):
        """Create .desktop file for app menu."""
        # Ensure directory exists
        Config.DESKTOP_DIR.mkdir(parents=True, exist_ok=True)

        mime_types = ";".join(Config.MIME_TYPES)

        content = self.DESKTOP_ENTRY_TEMPLATE.format(
            launcher=Config.LAUNCHER_PATH,
            icon=Config.ICON_NAME,
            mime_types=mime_types,
        )

        # Write desktop entry
        Config.DESKTOP_FILE.write_text(content)
        Config.DESKTOP_FILE.chmod(0o755)

        # Update desktop database
        self._update_desktop_database()

    def _update_desktop_database(self):
        """Update desktop menu cache."""
        try:
            subprocess.run(
                ["update-desktop-database", str(Config.DESKTOP_DIR)],
                capture_output=True,
                timeout=10,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass  # Not critical

    def extract_icon(self, appimage_path):
        """Try to extract icon from AppImage.

        Args:
            appimage_path: Path to AppImage

        Returns:
            Path to extracted icon or None
        """
        import tempfile
        import shutil

        # Try to extract .png from AppImage using bsdtar or 7z
        extractors = []
        if shutil.which("bsdtar"):
            extractors.append(["bsdtar", "-xf", str(appimage_path), "*.png"])
        if shutil.which("7z"):
            extractors.append(["7z", "e", "-o.", str(appimage_path), "*.png"])

        with tempfile.TemporaryDirectory() as tmpdir:
            for cmd in extractors:
                try:
                    result = subprocess.run(
                        cmd,
                        cwd=tmpdir,
                        capture_output=True,
                        timeout=30,
                    )
                    if result.returncode == 0:
                        # Find extracted PNG
                        pngs = list(Path(tmpdir).glob("*.png"))
                        if pngs:
                            # Use largest by file size (usually highest res)
                            best = max(pngs, key=lambda p: p.stat().st_size)
                            Config.ICON_DIR.mkdir(parents=True, exist_ok=True)
                            dest = Config.ICON_DIR / f"{Config.ICON_NAME}.png"
                            shutil.copy2(best, dest)
                            return dest
                except (subprocess.TimeoutExpired, Exception):
                    continue

        return None
