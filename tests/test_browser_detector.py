"""Tests for browser detection."""

from types import SimpleNamespace

import pytest

from ypt.browser_detector import BrowserDetector
from ypt.config import BrowserNotFoundError


def test_force_browser_found(monkeypatch: pytest.MonkeyPatch) -> None:
    """Forced browser should be used when available."""
    monkeypatch.setattr("ypt.browser_detector.shutil.which", lambda b: "/usr/bin/firefox")
    detector = BrowserDetector()
    assert detector.find_browser("firefox") == "/usr/bin/firefox"


def test_no_browser_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """Missing browsers should raise BrowserNotFoundError."""
    monkeypatch.delenv("BROWSER", raising=False)
    monkeypatch.setattr("ypt.browser_detector.shutil.which", lambda b: None)
    monkeypatch.setattr(
        "ypt.browser_detector.subprocess.run",
        lambda *args, **kwargs: SimpleNamespace(returncode=1, stdout="", stderr=""),
    )
    detector = BrowserDetector()
    with pytest.raises(BrowserNotFoundError):
        detector.find_browser()
