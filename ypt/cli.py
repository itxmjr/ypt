#!/usr/bin/env python3
"""CLI entry point for ypt."""
import argparse
import sys
from pathlib import Path

from .config import Config
from .deb_extractor import DebExtractor
from .appimage_installer import AppImageInstaller
from .desktop_integration import DesktopIntegration
from .browser_detector import BrowserDetector
from .launcher_generator import LauncherGenerator
from .debug import DebugDiagnostics


def main(argv=None):
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="ypt",
        description="Install Cisco Packet Tracer from .deb on any Linux distro",
    )
    parser.add_argument(
        "deb_file",
        nargs="?",
        type=Path,
        help="Path to the .deb file (auto-discovers if not provided)",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove Packet Tracer from user home",
    )
    parser.add_argument(
        "--test-browser",
        action="store_true",
        help="Test browser detection and launch",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--browser",
        metavar="BIN",
        help="Force specific browser binary",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done, don't execute",
    )
    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="Collect diagnostic information",
    )

    args = parser.parse_args(argv)

    if args.uninstall:
        uninstall()
        return 0

    if args.test_browser:
        test_browser(args.browser)
        return 0

    if args.diagnose:
        diag = DebugDiagnostics()
        report = diag.collect()
        print(report)
        save_path = diag.save_report()
        print(f"\nSaved to: {save_path}")
        return 0

    # Auto-discover .deb if not provided
    deb_file = args.deb_file
    if deb_file is None:
        deb_file = auto_discover_deb()
        if deb_file is None:
            print("Error: No .deb file found. Provide path or place .deb in current directory.")
            sys.exit(1)

    if not deb_file.exists():
        print(f"Error: File not found: {deb_file}")
        sys.exit(1)

    if args.dry_run:
        print(f"Would install from: {deb_file}")
        print(f"Would install to: {Config.PT_HOME}")
        return 0

    # Run installation
    try:
        install(deb_file, args.browser, args.debug)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    return 0


def auto_discover_deb():
    """Find first .deb in current directory."""
    import glob
    candidates = glob.glob("*.deb")
    if not candidates:
        return None
    return Path(candidates[0])


def install(deb_file, force_browser=None, debug=False):
    """Run full installation."""
    print(f"Installing from: {deb_file}")
    print(f"Target directory: {Config.PT_HOME}")
    print()

    # Step 1: Extract AppImage from .deb
    print("[1/5] Extracting AppImage from .deb...")
    extractor = DebExtractor(deb_file)
    appimage_path = extractor.extract()
    print(f"      ✓ Extracted to: {appimage_path}")

    # Step 2: Install AppImage
    print("[2/5] Installing AppImage...")
    appimage_installer = AppImageInstaller(appimage_path)
    appimage_installer.install()
    print(f"      ✓ Installed to: {Config.APPIMAGE_PATH}")

    # Step 3: Detect browser
    print("[3/5] Detecting browser...")
    detector = BrowserDetector()
    browser = detector.find_browser(force_browser)
    print(f"      ✓ Detected: {browser}")

    # Step 4: Generate launcher (with URL shim for login fix)
    print("[4/5] Creating launcher with URL handler shim...")
    launcher = LauncherGenerator(browser, debug=debug)
    launcher.create_launcher()
    print(f"      ✓ Created: {Config.LAUNCHER_PATH}")
    print(f"      ✓ URL shim installed (fixes login button)")

    # Step 5: Desktop integration
    print("[5/5] Creating desktop integration...")
    desktop = DesktopIntegration()
    desktop.create_desktop_entry()
    print(f"      ✓ Created: {Config.DESKTOP_FILE}")

    print()
    print("=" * 60)
    print("✓ Installation complete!")
    print("=" * 60)
    print(f"  Launch from terminal: {Config.LAUNCHER_PATH}")
    print(f"  Or search: 'Packet Tracer' in your app menu")
    print()
    print("The login button browser issue is now FIXED.")
    print("When you click login, it will open your browser properly.")
    print()
    print("If you have issues, check the debug log:")
    print(f"  {Config.DEBUG_LOG}")
    print()
    print("To uninstall: ypt --uninstall")


def uninstall():
    """Remove installed files."""
    import shutil
    print("Uninstalling Packet Tracer...")

    paths_to_remove = [
        Config.PT_HOME,
        Config.LAUNCHER_PATH,
        Config.DESKTOP_FILE,
    ]

    for path in paths_to_remove:
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"  Removed: {path}")

    print("\n✓ Uninstallation complete")


def test_browser(force_browser=None):
    """Test browser detection and launch."""
    import subprocess
    print("Testing browser detection...")

    detector = BrowserDetector()
    browser = detector.find_browser(force_browser)
    print(f"Detected: {browser}")

    print("\nTesting browser launch (opening https://www.netacad.com)...")
    subprocess.Popen([browser, "https://www.netacad.com"],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    print("Browser should have opened (check your browser window).")


if __name__ == "__main__":
    sys.exit(main())
