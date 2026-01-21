# LessList

An AI-assisted job search app focused on finding high-alignment results using natural language reasoning.

Built using Python and [PySide6](https://pypi.org/project/PySide6/) with [Qt Widgets](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html).

## Dependencies

All Python dependencies are handled via [`uv`](https://docs.astral.sh/uv/#installation).

## Pre-Commit Checks

Before each commit, run:

```shell
uv run check
```

This will run:

- formatting ([`ruff`](https://docs.astral.sh/ruff/))
- linting (`ruff`)
- type checking ([`ty`](https://docs.astral.sh/ty/))
- tests ([`pytest`](https://docs.pytest.org/en/stable/))
