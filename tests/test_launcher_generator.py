"""Tests for launcher generation."""

import os
from pathlib import Path

import pytest

from ypt.config import Config
from ypt.launcher_generator import LauncherGenerator


def test_is_kde(monkeypatch: pytest.MonkeyPatch) -> None:
    """KDE desktop detection should be case-insensitive."""
    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "kde")
    gen = LauncherGenerator("/usr/bin/firefox")
    assert gen._is_kde() is True


def test_get_qt_platform_wayland(monkeypatch: pytest.MonkeyPatch) -> None:
    """Wayland sessions should prefer wayland;xcb."""
    monkeypatch.setenv("XDG_SESSION_TYPE", "wayland")
    gen = LauncherGenerator("/usr/bin/firefox")
    assert gen._get_qt_platform() == "wayland;xcb"
