"""Extract AppImage from .deb archive."""
import re
import subprocess
import tempfile
from pathlib import Path

from .config import Config, ExtractError


class DebExtractor:
    """Extract AppImage from a .deb package.

    .deb files are ar archives containing control.tar.* and data.tar.*
    The AppImage is usually in data.tar.xz under opt/pt/ or similar.
    """

    def __init__(self, deb_path):
        self.deb_path = Path(deb_path)
        if not self.deb_path.exists():
            raise ExtractError(f"Deb file not found: {deb_path}")

    def _validate_deb(self):
        """Check .deb magic bytes."""
        with open(self.deb_path, "rb") as f:
            magic = f.read(8)
        if magic != b"!<arch>\n":
            raise ExtractError(f"{self.deb_path} is not a valid .deb archive")

    def _extract_ar(self, workdir):
        """Extract .deb ar archive."""
        result = subprocess.run(
            ["ar", "x", str(self.deb_path)],
            cwd=workdir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise ExtractError(f"Failed to extract .deb: {result.stderr}")

    def _find_data_tar(self, workdir):
        """Find data.tar.* file."""
        candidates = list(Path(workdir).glob("data.tar.*"))
        if not candidates:
            raise ExtractError("No data.tar.* found in .deb")
        return candidates[0]

    def _extract_data(self, data_tar, workdir):
        """Extract data archive."""
        result = subprocess.run(
            ["tar", "-xf", str(data_tar)],
            cwd=workdir,
            capture_output=True,
        )
        if result.returncode != 0:
            raise ExtractError(f"Failed to extract data.tar: {result.stderr}")

    def _find_appimage(self, workdir):
        """Find .AppImage file in extracted data."""
        candidates = list(Path(workdir).rglob("*.AppImage"))
        if not candidates:
            raise ExtractError("No AppImage found in .deb")
        return candidates[0]

    def _validate_appimage(self, appimage_path):
        """Check AppImage ELF header."""
        with open(appimage_path, "rb") as f:
            magic = f.read(4)
        if magic != b"\x7fELF":
            raise ExtractError(f"AppImage does not have valid ELF header")

    def extract(self):
        """Extract AppImage from .deb and return path to it.

        Returns:
            Path to extracted AppImage (in temp directory)
        """
        self._validate_deb()

        with tempfile.TemporaryDirectory() as workdir:
            work_path = Path(workdir)

            # Extract ar archive
            self._extract_ar(work_path)

            # Find and extract data.tar
            data_tar = self._find_data_tar(work_path)
            self._extract_data(data_tar, work_path)

            # Find AppImage
            appimage = self._find_appimage(work_path)
            self._validate_appimage(appimage)

            # Move to a stable temp location (caller will move to final dest)
            temp_appimage = Path(tempfile.gettempdir()) / "packettracer.AppImage"
            appimage.rename(temp_appimage)

            return temp_appimage
