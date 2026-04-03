"""Tests for configuration constants."""

from ypt.config import Config


def test_config_paths_are_path_objects() -> None:
    """Core config entries should be pathlib Paths."""
    assert hasattr(Config.PT_HOME, "exists")
    assert hasattr(Config.BIN_DIR, "exists")
    assert hasattr(Config.DESKTOP_DIR, "exists")


def test_browser_candidates_non_empty() -> None:
    """Browser candidate list should include common browsers."""
    assert "firefox" in Config.BROWSER_CANDIDATES
    assert len(Config.BROWSER_CANDIDATES) > 3
