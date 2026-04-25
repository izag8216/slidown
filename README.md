![banner](https://capsule-render.vercel.app/api?type=wave&height=200&section=header&text=slidown&fontSize=60&fontAlignY=42&desc=Markdown%20to%20HTML%20Slides&descAlignY=62&descSize=20&color=0:0f172a,100:1e1b4b&fontColor=f8fafc)

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Coming%20Soon-blue?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/)

</div>

---

**slidown** converts Markdown files into self-contained HTML presentation slides. No frameworks, no dependencies, no build steps -- just write Markdown and present.

## Features

- **Simple syntax** -- Separate slides with `---`
- **Self-contained output** -- Single HTML file with embedded CSS and JS
- **Syntax highlighting** -- Code blocks highlighted at build time via Pygments
- **Keyboard navigation** -- Arrow keys, space, PageUp/Down, Home/End
- **Touch support** -- Swipe left/right on mobile
- **Speaker notes** -- Hidden presenter notes in HTML comments
- **Live preview** -- `slidown serve` with auto-reload
- **Themes** -- Light and dark built-in themes
- **Zero runtime dependencies** -- Output works offline in any browser

## Installation

```bash
pip install slidown
```

For live preview support:

```bash
pip install slidown[serve]
```

## Quick Start

Create a Markdown file:

```markdown
# My Presentation

Welcome to my talk!

---

## Code Example

```python
def greet(name):
    return f"Hello, {name}!"
```

---

## Thank You

Questions?

<!-- note: Leave 5 minutes for Q&A -->
```

Build it:

```bash
slidown build slides.md
```

Open `slides.html` in your browser.

## Commands

### `slidown build`

Generate a self-contained HTML presentation.

```bash
slidown build slides.md                    # Default output: slides.html
slidown build slides.md -o talk.html       # Custom output name
slidown build slides.md --theme dark       # Dark theme
```

### `slidown serve`

Start a live-reload development server.

```bash
slidown serve slides.md                    # Serves on http://localhost:8000
slidown serve slides.md --port 3000        # Custom port
slidown serve slides.md --theme dark       # Dark theme preview
```

Edit your Markdown file and the browser refreshes automatically.

## Markdown Syntax

### Slide Separators

Use three dashes on their own line to separate slides:

```markdown
# Slide 1

Content here

---

# Slide 2

More content
```

### Speaker Notes

Add hidden speaker notes using HTML comments:

```markdown
# My Slide

Visible content

<!-- note: This is a speaker note -->
```

Press `N` during the presentation to toggle notes visibility.

### Supported Markdown

- Headings (`#` to `######`)
- Paragraphs and text formatting
- Unordered and ordered lists
- Code blocks with language highlighting
- Tables
- Blockquotes
- Images
- Inline code

## Navigation

| Key | Action |
|-----|--------|
| `Right`, `Down`, `Space`, `PageDown` | Next slide |
| `Left`, `Up`, `PageUp` | Previous slide |
| `Home` | First slide |
| `End` | Last slide |
| `N` | Toggle speaker notes |

Touch/swipe is also supported on mobile devices.

## Themes

- `light` (default) -- Clean white background with blue accents
- `dark` -- GitHub-dark inspired with high contrast

## Example

See [`examples/demo.md`](examples/demo.md) for a full example presentation.

## Development

```bash
git clone https://github.com/izag8216/slidown.git
cd slidown
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT License -- see [LICENSE](LICENSE).

## Acknowledgments

- [Python-Markdown](https://python-markdown.github.io/) -- Markdown parsing
- [Pygments](https://pygments.org/) -- Syntax highlighting
