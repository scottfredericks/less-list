"""Check script for running formatting, linting, type checking, and tests."""

import subprocess
import sys


def run_command(command, description):
    """Run a shell command and exit if it fails."""
    print(f"\n--- {description} ---")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"{description} failed.")
        sys.exit(1)


def main():
    """Run all checks including formatting, linting, type checking, and tests."""
    run_command(["uv", "run", "ruff", "format", "."], "Formatting")
    run_command(["uv", "run", "ruff", "check", "--fix", "."], "Linting")
    run_command(["uv", "run", "ty", "check"], "Type Checking")
    run_command(["uv", "run", "pytest"], "Running tests")

    print("\nAll checks passed!")


if __name__ == "__main__":
    main()
