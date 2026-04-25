"""Theme CSS definitions for slidown presentations."""

from __future__ import annotations

THEME_CSS: dict[str, str] = {
    "light": """
:root {
  --bg: #ffffff;
  --fg: #1a1a2e;
  --accent: #3a6b8c;
  --accent-light: #e8f4f8;
  --code-bg: #f6f8fa;
  --code-border: #d0d7de;
  --slide-border: #e1e4e8;
  --shadow: rgba(0,0,0,0.08);
  --note-bg: #fff8dc;
  --note-border: #f0e68c;
}
""",
    "dark": """
:root {
  --bg: #0d1117;
  --fg: #c9d1d9;
  --accent: #58a6ff;
  --accent-light: #1c2128;
  --code-bg: #161b22;
  --code-border: #30363d;
  --slide-border: #21262d;
  --shadow: rgba(0,0,0,0.3);
  --note-bg: #2d2a1e;
  --note-border: #5a5330;
}
""",
}

COMMON_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  width: 100%; height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background: var(--bg); color: var(--fg);
  overflow: hidden;
}
#slides {
  width: 100%; height: 100%;
  position: relative;
}
.slide {
  position: absolute; top: 0; left: 0;
  width: 100%; height: 100%;
  display: none;
  padding: 4rem 5rem;
  overflow-y: auto;
  background: var(--bg);
  border-bottom: 1px solid var(--slide-border);
}
.slide.active { display: flex; flex-direction: column; justify-content: center; }
.slide h1 { font-size: 3rem; margin-bottom: 1rem; color: var(--accent); }
.slide h2 { font-size: 2.2rem; margin-bottom: 0.8rem; color: var(--accent); }
.slide h3 { font-size: 1.6rem; margin-bottom: 0.6rem; }
.slide p { font-size: 1.3rem; line-height: 1.7; margin-bottom: 1rem; }
.slide ul, .slide ol {
  font-size: 1.2rem; line-height: 1.8;
  margin-left: 2rem; margin-bottom: 1rem;
}
.slide li { margin-bottom: 0.4rem; }
.slide code {
  background: var(--code-bg); border: 1px solid var(--code-border);
  border-radius: 4px; padding: 0.15em 0.4em; font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 0.9em;
}
.slide pre {
  background: var(--code-bg); border: 1px solid var(--code-border);
  border-radius: 8px; padding: 1rem; overflow-x: auto;
  margin: 1rem 0;
}
.slide pre code { background: none; border: none; padding: 0; }
.slide blockquote {
  border-left: 4px solid var(--accent); padding-left: 1rem;
  margin: 1rem 0; font-style: italic; color: var(--fg); opacity: 0.85;
}
.slide table {
  width: 100%; border-collapse: collapse; margin: 1rem 0;
}
.slide th, .slide td {
  border: 1px solid var(--code-border); padding: 0.6rem 0.8rem;
  text-align: left;
}
.slide th { background: var(--accent-light); font-weight: 600; }
.slide img { max-width: 100%; max-height: 60vh; object-fit: contain; }

/* Speaker notes */
.notes {
  display: none;
  position: fixed; bottom: 0; left: 0; right: 0;
  background: var(--note-bg); border-top: 2px solid var(--note-border);
  padding: 1rem 2rem; font-size: 1rem; z-index: 100;
}
.notes.visible { display: block; }

/* Navigation hints */
.nav-hint {
  position: fixed; bottom: 1rem; right: 1.5rem;
  font-size: 0.8rem; color: var(--fg); opacity: 0.4;
  pointer-events: none; z-index: 50;
}

/* Progress bar */
#progress {
  position: fixed; top: 0; left: 0; height: 3px;
  background: var(--accent); width: 0%;
  transition: width 0.3s ease; z-index: 100;
}

/* Slide counter */
#counter {
  position: fixed; top: 1rem; right: 1.5rem;
  font-size: 0.85rem; color: var(--fg); opacity: 0.35;
  z-index: 50;
}

/* Print styles */
@media print {
  .slide { display: block !important; position: static; page-break-after: always; }
  .nav-hint, #counter, #progress, .notes { display: none !important; }
}

/* Responsive */
@media (max-width: 768px) {
  .slide { padding: 2rem; }
  .slide h1 { font-size: 2rem; }
  .slide h2 { font-size: 1.6rem; }
  .slide p, .slide ul, .slide ol { font-size: 1rem; }
}
"""

NAVIGATION_JS = """
(function() {
  const slides = document.querySelectorAll('.slide');
  const total = slides.length;
  let current = 0;
  const progress = document.getElementById('progress');
  const counter = document.getElementById('counter');
  const notes = document.querySelector('.notes');

  function show(idx) {
    if (idx < 0) idx = 0;
    if (idx >= total) idx = total - 1;
    slides.forEach((s, i) => s.classList.toggle('active', i === idx));
    current = idx;
    progress.style.width = ((current + 1) / total * 100) + '%';
    counter.textContent = (current + 1) + ' / ' + total;
    updateNotes();
  }

  function updateNotes() {
    if (!notes) return;
    const active = slides[current];
    const noteEl = active.querySelector('.speaker-note');
    notes.textContent = noteEl ? noteEl.textContent : '';
    notes.classList.toggle('visible', noteEl && notes.classList.contains('visible'));
  }

  function next() { show(current + 1); }
  function prev() { show(current - 1); }

  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ' || e.key === 'PageDown') {
      e.preventDefault(); next();
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'PageUp') {
      e.preventDefault(); prev();
    } else if (e.key === 'Home') {
      e.preventDefault(); show(0);
    } else if (e.key === 'End') {
      e.preventDefault(); show(total - 1);
    } else if (e.key === 'n') {
      if (notes) notes.classList.toggle('visible');
    }
  });

  let touchStartX = 0;
  document.addEventListener('touchstart', function(e) {
    touchStartX = e.changedTouches[0].screenX;
  });
  document.addEventListener('touchend', function(e) {
    const dx = e.changedTouches[0].screenX - touchStartX;
    if (dx < -50) next();
    else if (dx > 50) prev();
  });

  // Auto-reload polling for serve mode
  if (window.__SLIDOWN_SERVE__) {
    let lastEtag = '';
    setInterval(function() {
      fetch(location.href, { method: 'HEAD', cache: 'no-store' })
        .then(r => {
          const etag = r.headers.get('etag') || r.headers.get('last-modified');
          if (lastEtag && etag !== lastEtag) location.reload();
          lastEtag = etag;
        })
        .catch(() => {});
    }, 1000);
  }

  show(0);
})();
"""
