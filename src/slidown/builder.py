"""Build Markdown into self-contained HTML presentation."""

from __future__ import annotations

import html
import re
from pathlib import Path

import markdown
from markdown.extensions import fenced_code, tables
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

from slidown.themes import COMMON_CSS, NAVIGATION_JS, THEME_CSS


def _extract_speaker_notes(text: str) -> tuple[str, str | None]:
    """Extract speaker notes from HTML comment blocks.

    Supports:
    <!-- note: speaker note text -->
    <!-- speaker: speaker note text -->
    <!-- notes: speaker note text -->
    """
    pattern = re.compile(
        r"<!--\s*(?:note|speaker|notes):?\s*(.*?)\s*-->",
        re.IGNORECASE | re.DOTALL,
    )
    notes = []

    def replacer(m: re.Match) -> str:
        note_text = m.group(1).strip()
        if note_text:
            notes.append(note_text)
        return ""

    cleaned = pattern.sub(replacer, text)
    combined = "\n\n".join(notes) if notes else None
    return cleaned, combined


def _split_slides(text: str) -> list[tuple[str, str | None]]:
    """Split markdown text into slides separated by '---' horizontal rules.

    Returns list of (slide_markdown, speaker_notes).
    """
    # Normalize line endings
    text = text.replace("\r\n", "\n")
    # Split on horizontal rule lines (--- on its own line)
    raw_slides = re.split(r"\n---\s*\n", text)
    slides = []
    for raw in raw_slides:
        raw = raw.strip()
        if not raw:
            continue
        cleaned, notes = _extract_speaker_notes(raw)
        slides.append((cleaned, notes))
    return slides


def _highlight_code(code: str, lang: str | None = None) -> str:
    """Highlight code block using Pygments."""
    try:
        lexer = get_lexer_by_name(lang, stripall=False) if lang else guess_lexer(code)
    except Exception:
        lexer = get_lexer_by_name("text")

    formatter = HtmlFormatter(
        style="github-dark",
        noclasses=True,
        prestyles="margin:0;padding:0;background:transparent;",
    )
    return highlight(code, lexer, formatter)


def _convert_slide(md_text: str) -> str:
    """Convert a single slide's markdown to HTML."""
    md = markdown.Markdown(
        extensions=[
            fenced_code.FencedCodeExtension(),
            tables.TableExtension(),
        ],
        extension_configs={
            "fenced_code": {"lang_prefix": "language-"},
        },
    )
    html_content = md.convert(md_text)

    # Post-process code blocks: Pygments highlighting
    # Python-Markdown fenced_code outputs <pre><code class="language-xxx">...</code></pre>
    def replace_code_block(m: re.Match) -> str:
        pre_attrs = m.group(1) or ""
        code_attrs = m.group(2) or ""
        code_text = html.unescape(m.group(3))

        # Extract language
        lang_match = re.search(r'class="[^"]*language-([^"\s]+)', code_attrs)
        lang = lang_match.group(1) if lang_match else None

        highlighted = _highlight_code(code_text, lang)
        # Pygments wraps in <div class="highlight"><pre>...</pre></div>
        # We want to keep our own <pre> styling, so extract inner
        inner_match = re.search(r"<pre[^>]*>(.*?)</pre>", highlighted, re.DOTALL)
        if inner_match:
            inner = inner_match.group(1)
            return f"<pre{pre_attrs}><code{code_attrs}>{inner}</code></pre>"
        return highlighted

    html_content = re.sub(
        r"<pre([^>]*)><code([^>]*)>(.*?)</code></pre>",
        replace_code_block,
        html_content,
        flags=re.DOTALL,
    )

    return html_content


def build_presentation(
    markdown_text: str,
    title: str = "Presentation",
    theme: str = "light",
    serve_mode: bool = False,
) -> str:
    """Build a complete HTML presentation from markdown text.

    Args:
        markdown_text: Raw markdown with --- slide separators.
        title: Presentation title (HTML <title>).
        theme: Theme name ('light' or 'dark').
        serve_mode: If True, injects auto-reload JavaScript.

    Returns:
        Self-contained HTML string.
    """
    if theme not in THEME_CSS:
        theme = "light"

    slides_data = _split_slides(markdown_text)
    if not slides_data:
        slides_data = [(markdown_text, None)]

    slide_html_parts = []
    for idx, (md_slide, notes) in enumerate(slides_data):
        body = _convert_slide(md_slide)
        note_html = ""
        if notes:
            escaped = html.escape(notes)
            note_html = f'<div class="speaker-note" style="display:none;">{escaped}</div>'
        slide_html_parts.append(
            f'<section class="slide" id="slide-{idx}">\n{body}\n{note_html}\n</section>'
        )

    theme_css = THEME_CSS[theme]
    nav_js = NAVIGATION_JS.replace(
        "window.__SLIDOWN_SERVE__",
        "true" if serve_mode else "false",
    )

    slides_html = "\n".join(slide_html_parts)
    html_doc = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"<title>{html.escape(title)}</title>\n"
        "<style>\n"
        f"{theme_css}\n"
        f"{COMMON_CSS}\n"
        "</style>\n"
        "</head>\n"
        "<body>\n"
        '<div id="progress"></div>\n'
        '<div id="counter"></div>\n'
        '<div id="slides">\n'
        f"{slides_html}\n"
        "</div>\n"
        '<div class="notes"></div>\n'
        '<div class="nav-hint">Arrow keys / swipe to navigate &middot; N for notes</div>\n'
        "<script>\n"
        f"{nav_js}\n"
        "</script>\n"
        "</body>\n"
        "</html>\n"
    )
    return html_doc


def build_from_file(
    input_path: Path,
    output_path: Path | None = None,
    theme: str = "light",
    serve_mode: bool = False,
) -> Path:
    """Build presentation from a markdown file.

    Args:
        input_path: Path to markdown source file.
        output_path: Path for output HTML. Defaults to input_path with .html extension.
        theme: Theme name.
        serve_mode: Enable auto-reload JS.

    Returns:
        Path to generated HTML file.
    """
    md_text = input_path.read_text(encoding="utf-8")
    title = input_path.stem.replace("-", " ").replace("_", " ").title()

    # Try to extract title from first H1
    first_h1 = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    if first_h1:
        title = first_h1.group(1).strip()

    html_output = build_presentation(
        md_text,
        title=title,
        theme=theme,
        serve_mode=serve_mode,
    )

    if output_path is None:
        output_path = input_path.with_suffix(".html")

    output_path.write_text(html_output, encoding="utf-8")
    return output_path
