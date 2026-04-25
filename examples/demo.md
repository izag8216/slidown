# Welcome to slidown

A lightweight tool that turns Markdown into beautiful HTML presentations.

---

## Features

- **Simple syntax**: Use `---` to separate slides
- **Self-contained output**: Single HTML file, no dependencies
- **Keyboard navigation**: Arrow keys, space, home/end
- **Speaker notes**: Hidden notes for presenters
- **Live preview**: Auto-reload development server
- **Syntax highlighting**: Code blocks with Pygments

---

## Markdown Support

### Lists

- Bullet points
- Numbered lists
- Nested items

### Code Blocks

```python
def hello(name: str) -> str:
    return f"Hello, {name}!"
```

### Tables

| Feature | Status |
|---------|--------|
| Slides | Done |
| Themes | Done |
| Serve | Done |

---

## Speaker Notes

This slide has hidden speaker notes!

<!-- note: Remind the audience that slidown is open source and accepts contributions -->

---

## Thank You

Try it today:

```bash
pip install slidown
slidown build slides.md
slidown serve slides.md
```
