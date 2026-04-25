# Contributing to slidown

Thank you for your interest in contributing!

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

```bash
pytest
```

Tests must maintain 80%+ coverage.

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
ruff check src/
ruff format src/
```

## Pull Request Process

1. Ensure tests pass and coverage is maintained
2. Update documentation if needed
3. Keep changes focused and atomic

## Reporting Issues

Please include:
- Python version
- slidown version
- Steps to reproduce
- Expected vs actual behavior
