"""Tests for slidown CLI module."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from slidown.cli import main


class TestCliBuild:
    def test_build_missing_file(self, capsys) -> None:
        result = main(["build", "nonexistent.md"])
        assert result == 1
        captured = capsys.readouterr()
        assert "File not found" in captured.err

    def test_build_success(self, tmp_path: Path, capsys) -> None:
        md = tmp_path / "slides.md"
        md.write_text("# Hello", encoding="utf-8")
        result = main(["build", str(md)])
        assert result == 0
        captured = capsys.readouterr()
        assert "Built:" in captured.out
        assert (tmp_path / "slides.html").exists()

    def test_build_custom_output(self, tmp_path: Path, capsys) -> None:
        md = tmp_path / "slides.md"
        md.write_text("# Hello", encoding="utf-8")
        out = tmp_path / "output.html"
        result = main(["build", str(md), "-o", str(out)])
        assert result == 0
        assert out.exists()

    def test_build_dark_theme(self, tmp_path: Path) -> None:
        md = tmp_path / "slides.md"
        md.write_text("# Hello", encoding="utf-8")
        result = main(["build", str(md), "--theme", "dark"])
        assert result == 0
        html = (tmp_path / "slides.html").read_text(encoding="utf-8")
        assert "--bg: #0d1117" in html

    def test_build_invalid_theme(self, tmp_path: Path) -> None:
        md = tmp_path / "slides.md"
        md.write_text("# Hello", encoding="utf-8")
        # argparse will reject invalid theme choices
        with pytest.raises(SystemExit):
            main(["build", str(md), "--theme", "blue"])


class TestCliServe:
    def test_serve_missing_file(self, capsys) -> None:
        result = main(["serve", "nonexistent.md"])
        assert result == 1
        captured = capsys.readouterr()
        assert "File not found" in captured.err

    @patch("slidown.cli.serve_presentation")
    def test_serve_success(self, mock_serve, tmp_path: Path, capsys) -> None:
        md = tmp_path / "slides.md"
        md.write_text("# Hello", encoding="utf-8")
        result = main(["serve", str(md)])
        assert result == 0
        mock_serve.assert_called_once()
        args = mock_serve.call_args
        assert args[1]["port"] == 8000
        assert args[1]["theme"] == "light"

    @patch("slidown.cli.serve_presentation")
    def test_serve_custom_port(self, mock_serve, tmp_path: Path) -> None:
        md = tmp_path / "slides.md"
        md.write_text("# Hello", encoding="utf-8")
        main(["serve", str(md), "--port", "3000"])
        assert mock_serve.call_args[1]["port"] == 3000


class TestCliGeneral:
    def test_version(self, capsys) -> None:
        with pytest.raises(SystemExit) as exc:
            main(["--version"])
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "slidown" in captured.out

    def test_no_command(self) -> None:
        with pytest.raises(SystemExit):
            main([])

    def test_help(self, capsys) -> None:
        with pytest.raises(SystemExit) as exc:
            main(["--help"])
        assert exc.value.code == 0
