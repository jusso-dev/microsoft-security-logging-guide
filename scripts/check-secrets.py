#!/usr/bin/env python3
"""Secret and scope guard for CI and the nightly guidance refresh workflow.

Modes:
  --mode repo
      Scans all git-tracked files for forbidden secret/config files and
      high-confidence secret patterns (Anthropic API keys, GitHub PATs,
      AWS access keys, private keys).

  --mode working-tree [--enforce-refresh-scope]
      Scans all modified and untracked files reported by `git status` for
      forbidden paths, secret patterns, and (when CHECK_SECRET_VALUE is set
      in the environment) exact, base64, URL-encoded, hex, or reversed forms
      of the secret value.

Never prints secret values or matched line contents.
"""

from __future__ import annotations

import argparse
import base64
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

def resolve_repo_root() -> Path:
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.strip()
        if top:
            return Path(top)
    except (OSError, subprocess.CalledProcessError):
        pass
    return Path.cwd()


ROOT = resolve_repo_root()

FORBIDDEN_FILES_EXACT = {
    ".env",
    ".claude/settings.local.json",
    "CLAUDE.local.md",
}

FORBIDDEN_FILE_PATTERNS = [
    (re.compile(r"(^|/)\.env(\..+)?$"), "dotenv file"),
    (re.compile(r"(^|/)\.claude/settings\.local\.json$"), "Claude local settings file"),
    (re.compile(r"\.(pem|key|p12|pfx)$", re.IGNORECASE), "private key/certificate file"),
]

ALLOWED_ENV_TEMPLATES = re.compile(r"(^|/)\.env\.(example|sample|template)$", re.IGNORECASE)

REFRESH_FORBIDDEN_PREFIXES = (
    ".github/",
    "scripts/",
    ".claude/",
)

REFRESH_FORBIDDEN_EXACT = {
    "package.json",
    "package-lock.json",
    "mkdocs.yml",
    ".gitignore",
    ".markdownlint-cli2.yaml",
}

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Anthropic API key", re.compile(r"\bsk-ant-(?:api|oat|admin)?[0-9A-Za-z_-]{16,}\b")),
    ("GitHub classic PAT", re.compile(r"\bgh[pousr]_[0-9A-Za-z]{36,}\b")),
    ("GitHub fine-grained PAT", re.compile(r"\bgithub_pat_[0-9A-Za-z_]{22,}\b")),
    ("AWS access key ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    (
        "Private key block",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    ),
]


def git_output(*args: str) -> bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout


def list_tracked_files() -> list[str]:
    raw = git_output("ls-files", "-z")
    return [entry.decode("utf-8", errors="surrogateescape") for entry in raw.split(b"\0") if entry]


def list_working_tree_changes() -> list[str]:
    raw = git_output("status", "--porcelain=v1", "-z", "--untracked-files=all")
    entries = raw.split(b"\0")
    paths: list[str] = []
    i = 0
    while i < len(entries):
        item = entries[i]
        if not item:
            i += 1
            continue
        status = item[:2].decode("ascii", errors="replace")
        path = item[3:].decode("utf-8", errors="surrogateescape")
        paths.append(path)
        if status and (status[0] in ("R", "C") or status[1] in ("R", "C")):
            i += 2
        else:
            i += 1
    return sorted(set(paths))


def check_forbidden_path(rel_path: str, enforce_refresh_scope: bool) -> list[str]:
    errors: list[str] = []
    norm = rel_path.replace("\\", "/")
    while norm.startswith("./"):
        norm = norm[2:]

    if not ALLOWED_ENV_TEMPLATES.search(norm):
        if norm in FORBIDDEN_FILES_EXACT:
            errors.append(f"{norm}: forbidden file")
        else:
            for pattern, label in FORBIDDEN_FILE_PATTERNS:
                if pattern.search(norm):
                    errors.append(f"{norm}: forbidden {label}")
                    break

    if enforce_refresh_scope:
        if norm in REFRESH_FORBIDDEN_EXACT or norm.startswith(REFRESH_FORBIDDEN_PREFIXES):
            errors.append(f"{norm}: outside allowed nightly-refresh scope")

    return errors


def build_secret_needles(secret: str) -> list[tuple[str, bytes]]:
    if not secret or len(secret) < 12:
        return []
    raw = secret.encode("utf-8")
    needles: list[tuple[str, bytes]] = [
        ("raw", raw),
        ("base64", base64.b64encode(raw)),
        ("urlsafe-base64", base64.urlsafe_b64encode(raw)),
        ("hex", raw.hex().encode("ascii")),
        ("url-encoded", urllib.parse.quote(secret, safe="").encode("ascii")),
        ("reversed", raw[::-1]),
    ]
    # Also check unpadded base64 prefix (strip trailing '=') to catch partial padding variants.
    b64_nopad = base64.b64encode(raw).rstrip(b"=")
    if b64_nopad != base64.b64encode(raw):
        needles.append(("base64-unpadded", b64_nopad))
    return needles


def scan_file(rel_path: str, needles: list[tuple[str, bytes]]) -> list[str]:
    full_path = ROOT / rel_path
    if not full_path.is_file() or full_path.is_symlink():
        return []

    errors: list[str] = []
    try:
        data = full_path.read_bytes()
    except OSError as exc:
        return [f"{rel_path}: could not read file ({exc})"]

    for label, needle in needles:
        if needle and needle in data:
            errors.append(f"{rel_path}: detected secret value ({label} encoding)")

    # Skip binary files for regex line scanning.
    if b"\x00" in data[:8192]:
        return errors

    text = data.decode("utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), start=1):
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                errors.append(f"{rel_path}:{lineno}: matched {name} pattern")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Secret and scope guard")
    parser.add_argument(
        "--mode",
        choices=("repo", "working-tree"),
        required=True,
        help="Scan all tracked files ('repo') or modified/untracked files ('working-tree').",
    )
    parser.add_argument(
        "--enforce-refresh-scope",
        action="store_true",
        help="Reject edits to workflows, scripts, and tooling config during nightly refresh.",
    )
    args = parser.parse_args()

    files = list_tracked_files() if args.mode == "repo" else list_working_tree_changes()
    secret_value = os.environ.get("CHECK_SECRET_VALUE", "")
    needles = build_secret_needles(secret_value)

    findings: list[str] = []
    for rel_path in files:
        findings.extend(check_forbidden_path(rel_path, args.enforce_refresh_scope))
        findings.extend(scan_file(rel_path, needles))

    if findings:
        for finding in findings:
            print(f"::error::{finding}", file=sys.stderr)
        print(
            f"Secret/scope guard failed with {len(findings)} finding(s).",
            file=sys.stderr,
        )
        return 1

    print(f"Secret/scope guard passed ({len(files)} file(s) scanned in {args.mode} mode).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
