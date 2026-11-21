#!/usr/bin/env python3
"""Build the site-src tree for MkDocs.

Copies the guide Markdown into site-src/, the MkDocs docs directory, so the
published GitHub Pages site mirrors the repository structure:

- every folder's README.md becomes that folder's index.md
- links pointing at README.md are rewritten to index.md
- everything else (.github, scripts, packaging files) is skipped

Run "mkdocs build" after this script. Both site-src and _site are generated
and git-ignored.
"""

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "site-src"

SKIP_DIRS = {
    ".git",
    ".github",
    "scripts",
    "node_modules",
    "site-src",
    "_site",
}

# Match the target of an inline Markdown link that ends in README.md,
# optionally with an anchor. Group 1 is the part before README.md.
README_LINK_RE = re.compile(r"(\]\([^)#\s]*?)README\.md(\)|#[^)]*\))")


def markdown_files():
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts[:-1]):
            continue
        yield path


def destination_for(path: Path) -> Path:
    relative = path.relative_to(ROOT)
    parts = list(relative.parts)
    if parts[-1] == "README.md":
        parts[-1] = "index.md"
    return DEST.joinpath(*parts)


def rewrite_links(text: str) -> str:
    return README_LINK_RE.sub(r"\1index.md\2", text)


def main() -> None:
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()

    for path in markdown_files():
        target = destination_for(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rewrite_links(path.read_text(encoding="utf-8")))
        print(f"copied {path.relative_to(ROOT)} -> {target.relative_to(ROOT)}")

    queries_dir = ROOT / "queries"
    if queries_dir.exists():
        for path in sorted(queries_dir.rglob("*.kql")):
            target = DEST / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            print(f"copied {path.relative_to(ROOT)} -> {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
