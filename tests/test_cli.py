"""Tests for CLI behavior."""

from pathlib import Path

import pytest

from ypt import cli


def test_auto_discover_deb_none(monkeypatch: pytest.MonkeyPatch) -> None:
    """No .deb files should return None."""
    monkeypatch.setattr("glob.glob", lambda pattern: [])
    assert cli.auto_discover_deb() is None


def test_auto_discover_deb_found(monkeypatch: pytest.MonkeyPatch) -> None:
    """First .deb should be returned as Path."""
    monkeypatch.setattr("glob.glob", lambda pattern: ["a.deb", "b.deb"])
    assert cli.auto_discover_deb() == Path("a.deb")


def test_main_dry_run(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """Dry run should return success without installation."""
    fake_deb = Path("fake.deb")
    monkeypatch.setattr(cli, "auto_discover_deb", lambda: fake_deb)
    monkeypatch.setattr(Path, "exists", lambda self: True)
    rc = cli.main(["--dry-run"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Would install from" in out
