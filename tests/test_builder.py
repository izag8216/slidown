"""Tests for slidown builder module."""

from __future__ import annotations

import pytest
from pathlib import Path

from slidown.builder import (
    _convert_slide,
    _extract_speaker_notes,
    _split_slides,
    build_from_file,
    build_presentation,
)


class TestExtractSpeakerNotes:
    def test_no_notes(self) -> None:
        text = "# Slide 1\n\nSome content"
        cleaned, notes = _extract_speaker_notes(text)
        assert cleaned == text
        assert notes is None

    def test_single_note(self) -> None:
        text = "# Slide 1\n\n<!-- note: remember to smile -->"
        cleaned, notes = _extract_speaker_notes(text)
        assert "remember to smile" in notes
        assert "<!--" not in cleaned

    def test_multiple_notes(self) -> None:
        text = "Content\n<!-- note: first -->\n<!-- note: second -->"
        cleaned, notes = _extract_speaker_notes(text)
        assert "first" in notes
        assert "second" in notes

    def test_speaker_alias(self) -> None:
        text = "<!-- speaker: say hello -->"
        cleaned, notes = _extract_speaker_notes(text)
        assert "say hello" in notes

    def test_notes_alias(self) -> None:
        text = "<!-- notes: extra info -->"
        cleaned, notes = _extract_speaker_notes(text)
        assert "extra info" in notes


class TestSplitSlides:
    def test_single_slide(self) -> None:
        text = "# Title\n\nContent"
        slides = _split_slides(text)
        assert len(slides) == 1
        assert slides[0][1] is None  # no notes

    def test_two_slides(self) -> None:
        text = "# Slide 1\n\n---\n\n# Slide 2"
        slides = _split_slides(text)
        assert len(slides) == 2

    def test_three_slides(self) -> None:
        text = "A\n\n---\n\nB\n\n---\n\nC"
        slides = _split_slides(text)
        assert len(slides) == 3

    def test_empty_sections_ignored(self) -> None:
        text = "\n\n---\n\n# Real\n\n---\n\n"
        slides = _split_slides(text)
        assert len(slides) == 1
        assert "# Real" in slides[0][0]

    def test_notes_preserved_per_slide(self) -> None:
        text = "# A\n<!-- note: noteA -->\n\n---\n\n# B\n<!-- note: noteB -->"
        slides = _split_slides(text)
        assert len(slides) == 2
        assert slides[0][1] == "noteA"
        assert slides[1][1] == "noteB"


class TestConvertSlide:
    def test_heading(self) -> None:
        html = _convert_slide("# Hello")
        assert "<h1>Hello</h1>" in html

    def test_paragraph(self) -> None:
        html = _convert_slide("Some text")
        assert "<p>Some text</p>" in html

    def test_list(self) -> None:
        html = _convert_slide("- a\n- b")
        assert "<ul>" in html
        assert "<li>a</li>" in html

    def test_code_block(self) -> None:
        html = _convert_slide("```python\nprint(1)\n```")
        assert "<pre>" in html
        assert "print" in html
        assert "1" in html

    def test_table(self) -> None:
        html = _convert_slide("| a | b |\n|---|---|\n| 1 | 2 |")
        assert "<table>" in html
        assert "<td>1</td>" in html


class TestBuildPresentation:
    def test_basic_structure(self) -> None:
        html = build_presentation("# Title\n\n---\n\n## Second")
        assert "<!DOCTYPE html>" in html
        assert '<section class="slide"' in html
        assert "<h1>Title</h1>" in html
        assert "<h2>Second</h2>" in html

    def test_light_theme(self) -> None:
        html = build_presentation("# T", theme="light")
        assert "--bg: #ffffff" in html

    def test_dark_theme(self) -> None:
        html = build_presentation("# T", theme="dark")
        assert "--bg: #0d1117" in html

    def test_invalid_theme_defaults_light(self) -> None:
        html = build_presentation("# T", theme="nonexistent")
        assert "--bg: #ffffff" in html

    def test_title_from_first_h1(self) -> None:
        html = build_presentation("# My Talk", title="My Talk")
        assert "<title>My Talk</title>" in html

    def test_speaker_notes_in_html(self) -> None:
        html = build_presentation("# T\n<!-- note: hello -->")
        assert "speaker-note" in html
        assert "hello" in html

    def test_serve_mode_injects_reload(self) -> None:
        html = build_presentation("# T", serve_mode=True)
        assert "true" in html  # the JS variable is set to true

    def test_no_slides_single_section(self) -> None:
        html = build_presentation("Just content")
        assert '<section class="slide"' in html

    def test_progress_bar(self) -> None:
        html = build_presentation("# A\n\n---\n\n# B")
        assert 'id="progress"' in html

    def test_counter(self) -> None:
        html = build_presentation("# A")
        assert 'id="counter"' in html


class TestBuildFromFile:
    def test_build_output(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Hello\n\nWorld", encoding="utf-8")
        out = build_from_file(md)
        assert out.exists()
        assert out.name == "test.html"
        content = out.read_text(encoding="utf-8")
        assert "<h1>Hello</h1>" in content

    def test_custom_output(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Hello", encoding="utf-8")
        out = tmp_path / "custom.html"
        result = build_from_file(md, output_path=out)
        assert result == out
        assert out.exists()

    def test_title_from_filename(self, tmp_path: Path) -> None:
        md = tmp_path / "my-talk.md"
        md.write_text("No heading", encoding="utf-8")
        out = build_from_file(md)
        content = out.read_text(encoding="utf-8")
        assert "<title>My Talk</title>" in content

    def test_theme_parameter(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# T", encoding="utf-8")
        out = build_from_file(md, theme="dark")
        content = out.read_text(encoding="utf-8")
        assert "--bg: #0d1117" in content
