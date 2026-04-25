"""Tests for slidown server module."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from slidown.server import serve_presentation


class TestServePresentation:
    @patch("slidown.server.build_from_file")
    def test_watchdog_missing(self, mock_build, tmp_path: Path, capsys) -> None:
        """Test error when watchdog is not installed."""
        md = tmp_path / "slides.md"
        md.write_text("# Hello", encoding="utf-8")

        with patch.dict(sys.modules, {"watchdog": None}):
            with patch.object(
                sys, "exit", side_effect=SystemExit(1)
            ) as mock_exit:
                with pytest.raises(SystemExit):
                    serve_presentation(md)

    @patch("slidown.server.build_from_file")
    @patch("watchdog.observers.Observer")
    @patch("watchdog.events.FileSystemEventHandler")
    @patch("socketserver.TCPServer")
    def test_serve_basic(
        self, mock_tcp, mock_handler_cls, mock_observer_cls, mock_build, tmp_path: Path
    ) -> None:
        """Test basic serve functionality."""
        md = tmp_path / "slides.md"
        md.write_text("# Hello", encoding="utf-8")

        mock_observer = MagicMock()
        mock_observer_cls.return_value = mock_observer

        mock_server = MagicMock()
        mock_tcp.return_value.__enter__ = lambda s: mock_server
        mock_tcp.return_value.__exit__ = lambda *a: None

        # Simulate keyboard interrupt to exit server
        mock_server.serve_forever.side_effect = KeyboardInterrupt()

        serve_presentation(md, port=9999, theme="dark")

        mock_build.assert_called_once()
        assert mock_build.call_args[1]["theme"] == "dark"
        assert mock_build.call_args[1]["serve_mode"] is True
        mock_observer.schedule.assert_called_once()
        mock_observer.start.assert_called_once()
        mock_server.serve_forever.assert_called_once()
        mock_observer.stop.assert_called_once()

    @patch("slidown.server.build_from_file")
    @patch("watchdog.observers.Observer")
    @patch("watchdog.events.FileSystemEventHandler")
    @patch("socketserver.TCPServer")
    def test_serve_default_port(
        self, mock_tcp, mock_handler_cls, mock_observer_cls, mock_build, tmp_path: Path
    ) -> None:
        """Test serve uses default port 8000."""
        md = tmp_path / "slides.md"
        md.write_text("# Hello", encoding="utf-8")

        mock_observer = MagicMock()
        mock_observer_cls.return_value = mock_observer

        mock_server = MagicMock()
        mock_tcp.return_value.__enter__ = lambda s: mock_server
        mock_tcp.return_value.__exit__ = lambda *a: None
        mock_server.serve_forever.side_effect = KeyboardInterrupt()

        serve_presentation(md)

        mock_tcp.assert_called_once()
        # First positional arg is the handler, second is port tuple
        assert mock_tcp.call_args[0][0] == ("", 8000)

    @patch("slidown.server.build_from_file")
    @patch("watchdog.observers.Observer")
    @patch("watchdog.events.FileSystemEventHandler")
    @patch("socketserver.TCPServer")
    def test_rebuild_on_change(
        self, mock_tcp, mock_handler_cls, mock_observer_cls, mock_build, tmp_path: Path
    ) -> None:
        """Test that build_from_file is called for initial build."""
        md = tmp_path / "slides.md"
        md.write_text("# Hello", encoding="utf-8")

        mock_observer = MagicMock()
        mock_observer_cls.return_value = mock_observer

        mock_server = MagicMock()
        mock_tcp.return_value.__enter__ = lambda s: mock_server
        mock_tcp.return_value.__exit__ = lambda *a: None
        mock_server.serve_forever.side_effect = KeyboardInterrupt()

        serve_presentation(md)

        assert mock_build.call_count == 1
        expected_output = tmp_path / ".slides.slidown.html"
        assert mock_build.call_args[1]["output_path"] == expected_output
