"""Detect system browser for URL handling."""
import subprocess
import shutil
from pathlib import Path

from .config import Config, BrowserNotFoundError


class BrowserDetector:
    """Find the best browser for opening URLs.

    Priority:
    1. User's $BROWSER environment variable
    2. xdg-settings default-web-browser
    3. Check common browser binaries
    4. Fail with error
    """

    def find_browser(self, force_browser=None):
        """Find browser binary path.

        Args:
            force_browser: Optional specific browser to use

        Returns:
            Path to browser executable

        Raises:
            BrowserNotFoundError: If no browser found
        """
        if force_browser:
            return self._validate_browser(force_browser)

        # 1. Check $BROWSER env var
        env_browser = self._check_env_browser()
        if env_browser:
            return env_browser

        # 2. Check xdg-settings
        xdg_browser = self._check_xdg_default()
        if xdg_browser:
            return xdg_browser

        # 3. Check common browsers
        for browser in Config.BROWSER_CANDIDATES:
            path = shutil.which(browser)
            if path:
                return path

        raise BrowserNotFoundError(
            "No browser found. Set $BROWSER or install firefox/chromium."
        )

    def _validate_browser(self, browser):
        """Validate forced browser exists."""
        path = shutil.which(browser)
        if path:
            return path
        raise BrowserNotFoundError(f"Specified browser not found: {browser}")

    def _check_env_browser(self):
        """Check $BROWSER environment variable."""
        import os
        browser = os.environ.get("BROWSER")
        if browser:
            path = shutil.which(browser)
            if path:
                return path
        return None

    def _check_xdg_default(self):
        """Check xdg-settings for default browser."""
        try:
            result = subprocess.run(
                ["xdg-settings", "get", "default-web-browser"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                desktop_file = result.stdout.strip()
                # e.g., "firefox.desktop" -> "firefox"
                browser_name = desktop_file.replace(".desktop", "")
                path = shutil.which(browser_name)
                if path:
                    return path
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return None

    def test_browser(self, browser_path):
        """Test that browser can open URLs.

        Args:
            browser_path: Path to browser executable

        Returns:
            True if browser launches successfully
        """
        import subprocess
        try:
            # Try to start browser (don't wait for it to finish)
            subprocess.Popen(
                [browser_path, "about:blank"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception:
            return False
