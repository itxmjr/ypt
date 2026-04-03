"""Lightweight integration tests for CLI flows."""

from pathlib import Path

import pytest

from ypt import cli


def test_install_pipeline_calls_components(monkeypatch: pytest.MonkeyPatch) -> None:
    """Install should call extractor, installer, detector, launcher, desktop."""
    called = {"extract": False, "install": False, "browser": False, "launcher": False, "desktop": False}

    class FakeExtractor:
        def __init__(self, deb):
            self.deb = deb

        def extract(self):
            called["extract"] = True
            return Path("/tmp/packettracer.AppImage")

    class FakeInstaller:
        def __init__(self, path):
            self.path = path

        def install(self):
            called["install"] = True

    class FakeDetector:
        def find_browser(self, force=None):
            called["browser"] = True
            return "/usr/bin/firefox"

    class FakeLauncher:
        def __init__(self, browser, debug=False):
            self.browser = browser

        def create_launcher(self):
            called["launcher"] = True

    class FakeDesktop:
        def create_desktop_entry(self):
            called["desktop"] = True

    monkeypatch.setattr(cli, "DebExtractor", FakeExtractor)
    monkeypatch.setattr(cli, "AppImageInstaller", FakeInstaller)
    monkeypatch.setattr(cli, "BrowserDetector", FakeDetector)
    monkeypatch.setattr(cli, "LauncherGenerator", FakeLauncher)
    monkeypatch.setattr(cli, "DesktopIntegration", FakeDesktop)

    cli.install(Path("sample.deb"))
    assert all(called.values())
