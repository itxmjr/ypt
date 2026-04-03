"""Tests for .deb extraction prechecks."""

from pathlib import Path

import pytest

from ypt.config import ExtractError
from ypt.deb_extractor import DebExtractor


def test_invalid_magic_raises(tmp_path: Path) -> None:
    """Invalid archive header should be rejected."""
    bad = tmp_path / "bad.deb"
    bad.write_bytes(b"NOT_A_DEB")
    extractor = DebExtractor(bad)
    with pytest.raises(ExtractError):
        extractor._validate_deb()


def test_missing_file_raises(tmp_path: Path) -> None:
    """Non-existing .deb path should raise at construction."""
    missing = tmp_path / "missing.deb"
    with pytest.raises(ExtractError):
        DebExtractor(missing)
