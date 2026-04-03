"""Shared pytest fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def temp_deb_file(tmp_path: Path) -> Path:
    """Create a minimal fake .deb-like file header."""
    deb_path = tmp_path / "sample.deb"
    deb_path.write_bytes(b"!<arch>\n")
    return deb_path
