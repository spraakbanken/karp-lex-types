# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Transform the README.md to support a specific deployment target.

By default, we assume that our README.md will be rendered on GitHub. However, different
targets have different strategies for rendering light- and dark-mode images. This script
adjusts the images in the README.md to support the given target.
"""
# Copied from https://github.com/astral-sh/uv and adjusted to this project.

import argparse
import re
import urllib.parse
from pathlib import Path

import tomllib


def main(target: str) -> None:
    """Modify the README.md to support the given target."""
    # Replace the benchmark images based on the target.
    readme_path = Path("README.md")
    content = readme_path.read_text(encoding="utf8")

    if target != "pypi":
        msg = f"Unknown target: {target}"
        raise ValueError(msg)

    # Read the current version from the `pyproject.toml`.
    with Path("pyproject.toml").open(mode="rb") as fp:
        # Parse the TOML.
        pyproject = tomllib.load(fp)
        if "project" in pyproject and "version" in pyproject["project"]:
            version = pyproject["project"]["version"]
        else:
            raise ValueError("Version not found in pyproject.toml")

    # Replace the badges with versioned URLs.
    for existing, replacement in [
        (
            "https://img.shields.io/pypi/v/karp-lex-types.svg",
            f"https://img.shields.io/pypi/v/karp-lex-types/{version}.svg",
        ),
        (
            "https://img.shields.io/pypi/l/karp-lex-types.svg",
            f"https://img.shields.io/pypi/l/karp-lex-types/{version}.svg",
        ),
        (
            "https://img.shields.io/pypi/pyversions/karp-lex-types.svg",
            f"https://img.shields.io/pypi/pyversions/karp-lex-types/{version}.svg",
        ),
        (
            "https://img.shields.io/pypi/status/karp-lex-types.svg",
            f"https://img.shields.io/pypi/status/karp-lex-types/{version}.svg",
        ),
    ]:
        if existing not in content:
            raise ValueError(f"Badge not found in README.md: {existing}")
        content = content.replace(existing, replacement)

    # Replace any relative URLs (e.g., `[PIP_COMPATIBILITY.md`) with absolute URLs.
    def replace(match: re.Match) -> str:
        url = match.group(1)
        if not url.startswith("http"):
            url = urllib.parse.urljoin(
                f"https://github.com/spraakbanken/karp-lex-types/blob/v{version}/README.md",
                url,
            )
        return f"]({url})"

    content = re.sub(r"]\(([^)]+)\)", replace, content)

    readme_path.write_text(content, encoding="utf8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Modify the README.md to support a specific deployment target.",
    )
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        choices=("pypi", "mkdocs"),
    )
    args = parser.parse_args()

    main(target=args.target)
