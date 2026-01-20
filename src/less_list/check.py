import subprocess
import sys


def run_command(command, description):
    print(f"\n--- {description} ---")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"{description} failed.")
        sys.exit(1)


def main():
    run_command(["uv", "run", "ruff", "format", "."], "Formatting")
    run_command(["uv", "run", "ruff", "check", "--fix", "."], "Linting")
    run_command(["uv", "run", "ty", "check"], "Type Checking")
    run_command(["uv", "run", "pytest"], "Running tests")

    print("\nAll checks passed!")


if __name__ == "__main__":
    main()
