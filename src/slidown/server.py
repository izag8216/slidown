"""Live preview server with auto-reload."""

from __future__ import annotations

import contextlib
import http.server
import socketserver
import sys
import time
from pathlib import Path

from slidown.builder import build_from_file


def serve_presentation(input_path: Path, port: int = 8000, theme: str = "light") -> None:
    """Serve a markdown presentation with auto-rebuild and auto-reload.

    Builds the presentation into a temporary HTML file, serves it via
    HTTP, and watches the source file for changes.
    """
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError:
        print("Error: watchdog is required for 'serve'.", file=sys.stderr)
        print("  pip install slidown[serve]", file=sys.stderr)
        sys.exit(1)

    # Create temp output in same directory so relative assets resolve
    output_path = input_path.parent / f".{input_path.stem}.slidown.html"

    def rebuild() -> None:
        try:
            build_from_file(
                input_path,
                output_path=output_path,
                theme=theme,
                serve_mode=True,
            )
        except Exception as e:
            print(f"Build error: {e}", file=sys.stderr)

    # Initial build
    rebuild()

    # File watcher
    class RebuildHandler(FileSystemEventHandler):
        def __init__(self) -> None:
            self.last_modified = 0.0

        def on_modified(self, event) -> None:
            if event.is_directory:
                return
            if Path(event.src_path).resolve() == input_path.resolve():
                now = time.time()
                if now - self.last_modified > 0.3:  # debounce
                    self.last_modified = now
                    print(f"Change detected: {input_path.name}")
                    rebuild()

    handler = RebuildHandler()
    observer = Observer()
    observer.schedule(handler, str(input_path.parent), recursive=False)
    observer.start()

    # HTTP server
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, directory=str(input_path.parent), **kwargs)

        def do_GET(self) -> None:
            # Serve the generated HTML for root path
            if self.path == "/":
                self.path = f"/{output_path.name}"
            super().do_GET()

        def log_message(self, format: str, *args) -> None:
            # Suppress default logging
            pass

    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"Serving at http://localhost:{port}")
            print(f"Watching: {input_path}")
            print("Press Ctrl+C to stop")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        observer.stop()
        observer.join()
        # Clean up temp file
        with contextlib.suppress(OSError):
            output_path.unlink()
