"""CLI entry point for slidown."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from slidown import __version__
from slidown.builder import build_from_file
from slidown.server import serve_presentation


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="slidown",
        description="Convert Markdown to self-contained HTML presentation slides.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  slidown build slides.md                  # Generate slides.html
  slidown build slides.md -o talk.html     # Custom output name
  slidown build slides.md --theme dark     # Dark theme
  slidown serve slides.md                  # Live preview with auto-reload
  slidown serve slides.md --port 8080      # Custom port
        """.strip(),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # build command
    build_parser = subparsers.add_parser(
        "build",
        help="Build HTML presentation from markdown",
    )
    build_parser.add_argument(
        "input",
        type=Path,
        help="Path to markdown file",
    )
    build_parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output HTML file path (default: input.html)",
    )
    build_parser.add_argument(
        "--theme",
        choices=["light", "dark"],
        default="light",
        help="Presentation theme (default: light)",
    )

    # serve command
    serve_parser = subparsers.add_parser(
        "serve",
        help="Start live preview server with auto-reload",
    )
    serve_parser.add_argument(
        "input",
        type=Path,
        help="Path to markdown file",
    )
    serve_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)",
    )
    serve_parser.add_argument(
        "--theme",
        choices=["light", "dark"],
        default="light",
        help="Presentation theme (default: light)",
    )

    args = parser.parse_args(argv)

    if args.command == "build":
        if not args.input.exists():
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            return 1
        output = build_from_file(
            args.input,
            output_path=args.output,
            theme=args.theme,
        )
        print(f"Built: {output}")
        return 0

    if args.command == "serve":
        if not args.input.exists():
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            return 1
        serve_presentation(
            args.input,
            port=args.port,
            theme=args.theme,
        )
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
