"""Install AppImage to user directory."""
import shutil
import subprocess
from pathlib import Path

from .config import Config, InstallError


class AppImageInstaller:
    """Install AppImage and dependencies."""

    def __init__(self, appimage_source):
        self.source = Path(appimage_source)

    def install(self):
        """Install AppImage to PT_HOME."""
        # Create target directory
        Config.PT_HOME.mkdir(parents=True, exist_ok=True)

        # Copy AppImage
        shutil.copy2(self.source, Config.APPIMAGE_PATH)

        # Set executable (chmod +x)
        Config.APPIMAGE_PATH.chmod(0o755)

        # Verify it's runnable
        self._verify_appimage()

    def _verify_appimage(self):
        """Quick verification that AppImage works."""
        result = subprocess.run(
            [str(Config.APPIMAGE_PATH), "--appimage-version"],
            capture_output=True,
            timeout=10,
        )
        if result.returncode != 0:
            # Not fatal, just warn
            print(f"Warning: AppImage --appimage-version check failed")
