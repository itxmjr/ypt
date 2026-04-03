"""URL handler shim template injected into Packet Tracer launcher PATH."""

SHIM_TEMPLATE = '''#!/usr/bin/env python3
# Auto-generated URL handler shim for Packet Tracer
# This intercepts xdg-open calls from the AppImage

import os
import sys
import subprocess
import urllib.parse
from pathlib import Path

def log_debug(msg):
    """Log to debug file."""
    log_file = Path.home() / ".local/share/PacketTracer/debug.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a") as f:
        import datetime
        ts = datetime.datetime.now().isoformat()
        f.write(f"[{ts}] [url-shim] {msg}\\n")

def get_browser():
    """Get browser from environment."""
    browser = os.environ.get("PT_BROWSER")
    if browser and Path(browser).exists():
        return browser
    import shutil
    for candidate in ["firefox", "firefox-wayland", "google-chrome-stable",
                      "chromium", "chromium-browser", "brave"]:
        path = shutil.which(candidate)
        if path:
            return path
    return None

def open_url(url):
    """Open URL in browser."""
    log_debug(f"Opening URL: {url}")
    browser = get_browser()
    if not browser:
        log_debug("ERROR: No browser found!")
        return 1

    # Direct browser launch
    try:
        subprocess.Popen(
            [browser, url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        log_debug(f"Launched: {browser}")
        return 0
    except Exception as e:
        log_debug(f"Failed: {e}")

    # Fallback to system xdg-open
    xdg = shutil.which("xdg-open")
    if xdg:
        try:
            subprocess.run([xdg, url], capture_output=True, timeout=30)
            return 0
        except:
            pass

    return 1

def main():
    if len(sys.argv) < 2:
        return 1
    url = sys.argv[1]
    if url.startswith("ptsa://"):
        log_debug(f"ptsa:// URL (handled internally): {url}")
        return 0
    return open_url(url)

if __name__ == "__main__":
    import shutil
    sys.exit(main())
'''
