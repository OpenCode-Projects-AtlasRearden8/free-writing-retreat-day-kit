#!/usr/bin/env python3
"""Verification for the Free-Writing-Retreat-Day Kit.

Checks that every promised file exists, that each HTML page is well-formed
enough to print, that Markdown printables contain their key sections, and
that the kit contains no secrets, API keys, or personal data.
Run:  python3 tests/verify.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FAILURES = []
CHECKS = 0


def check(label, condition, detail=""):
    global CHECKS
    CHECKS += 1
    if condition:
        print(f"  ok  - {label}")
    else:
        FAILURES.append(f"{label} {detail}".strip())
        print(f"  FAIL - {label} {detail}".strip())


REQUIRED_MD = [
    "README.md",
    "LICENSE",
    "docs/retreat-guide.md",
    "printables/retreat-day-schedule.md",
    "printables/warm-up-prompts.md",
    "printables/goal-setting-one-pager.md",
    "printables/snack-hydration-tent-cards.md",
    "printables/end-of-day-reflection.md",
    "printables/invite-one-friend-planner.md",
]

REQUIRED_HTML = [
    "print/index.html",
    "print/style.css",
    "print/retreat-day-schedule.html",
    "print/warm-up-prompts.html",
    "print/goal-setting-one-pager.html",
    "print/snack-hydration-tent-cards.html",
    "print/end-of-day-reflection.html",
    "print/invite-one-friend-planner.html",
]

# Void and inline HTML5 tags that never need a closing tag.
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

SECRET_PATTERNS = [
    r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_\-]{8,}",
    r"(?i)secret\s*[:=]\s*['\"][A-Za-z0-9_\-]{8,}",
    r"(?i)password\s*[:=]\s*['\"]\S{4,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"(?i)aws_access_key_id\s*=\s*['\"][A-Za-z0-9/+]{10,}",
    r"\bAKIA[0-9A-Z]{16}\b",
    r"gh[pousr]_[A-Za-z0-9]{20,}",
    r"(?i)Bearer\s+[A-Za-z0-9_\-\.]{20,}",
]

PERSONAL_DATA_PATTERNS = [
    r"\b[A-Za-z0-9._%+-]+@(?!(?:users\.)?noreply\.github\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    r"\b(?:\d[ -]*){12,16}\b",
    r"\b\d{3}-\d{2}-\d{4}\b",
]


def well_formed_html(path: Path) -> list[str]:
    """Return a list of structural problems (empty list = fine)."""
    problems = []
    stack = []
    text = path.read_text(encoding="utf-8")
    if not text.lstrip().lower().startswith("<!doctype html"):
        problems.append("missing doctype")
        return problems

    # Strip comments first so we don't match tags inside them.
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for m in re.finditer(r"<(/?)([a-zA-Z][a-zA-Z0-9-]*)((?:\"[^\"]*\"|'[^']*'|[^><\"'])*?)(/?)>", text):
        closing, tag, _, selfclose = m.groups()
        if tag.lower() in VOID_TAGS or selfclose:
            continue
        if closing:
            if not stack or stack[-1][0] != tag.lower():
                got = stack[-1][0] if stack else "nothing"
                problems.append(f"</{tag}> closes {got}; stack={stack[-3:]}")
                if stack and stack[-1][0] == tag.lower():
                    stack.pop()
            else:
                stack.pop()
        else:
            stack.append((tag.lower(), m.start()))

    if stack:
        problems.append(f"unclosed tags: {[t for t, _ in stack]}")
    return problems


def main() -> int:
    print("== Free-Writing-Retreat-Day Kit verification ==")

    # --- files exist ---
    print("\n[1/5] Required files")
    for rel in REQUIRED_MD + REQUIRED_HTML:
        path = ROOT / rel
        check(f"{rel} exists", path.is_file())

    # --- LICENSE exact line ---
    print("\n[2/5] LICENSE")
    lic = ROOT / "LICENSE"
    if lic.is_file():
        text = lic.read_text(encoding="utf-8")
        check(
            "copyright line exact",
            "Copyright (c) 2026 Asdale Dynamics, LLC" in text,
        )
        check("MIT license present", "MIT License" in text)
    else:
        check("LICENSE exists", False, "(missing)")

    # --- README credits ---
    print("\n[3/5] README + privacy")
    readme_path = ROOT / "README.md"
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        check("README credits Asdale Dynamics, LLC", "Asdale Dynamics, LLC" in readme)
        check("README mentions no data collection", "collects nothing" in readme)
        check("README is distinct from marketing kit",
              "free-author-marketing-kit" in readme and "selling" in readme)

    # --- printable content sanity ---
    print("\n[4/5] Printable content")
    expected_sections = {
        "printables/retreat-day-schedule.md": ["Sprint 1", "Break", "Lunch", "Reflection"],
        "printables/warm-up-prompts.md": ["Prompt menu", "Warm-up rules"],
        "printables/goal-setting-one-pager.md": ["main goal", "Sprint tracker"],
        "printables/snack-hydration-tent-cards.md": ["Hydration" if False else "WATER FIRST", "SNACK O'CLOCK", "fold"],
        "printables/end-of-day-reflection.md": ["Three questions", "Tomorrow's first line"],
        "printables/invite-one-friend-planner.md": ["Pick the person", "The message", "Response plan"],
    }
    for rel, keys in expected_sections.items():
        path = ROOT / rel
        if not path.is_file():
            check(f"{rel} content", False, "(missing)")
            continue
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        for key in keys:
            needle = key.lower()
            if needle in lower:
                check(f"{rel} contains '{key}'", True)
            else:
                found = needle.casefold() in text.casefold()
                check(f"{rel} contains '{key}'", found or needle in lower or key in text)

    # --- HTML structure ---
    print("\n[5/5] HTML structure + privacy scan")
    html_only = [f for f in REQUIRED_HTML if f.endswith(".html")]
    all_text_paths = list((ROOT / "print").glob("*.html")) + [ROOT / f for f in REQUIRED_MD]
    for rel in html_only:
        path = ROOT / rel
        if not path.is_file():
            continue
        problems = well_formed_html(path)
        check(f"{rel} well-formed", not problems, "; ".join(problems[:2]))
    for rel in html_only:
        path = ROOT / rel
        if path.is_file():
            t = path.read_text(encoding="utf-8")
            check(f"{rel} links print stylesheet", 'href="style.css"' in t)
            check(f"{rel} credits kit/LLC",
                  "Asdale Dynamics" in t or "Free-Writing-Retreat-Day Kit" in t)

    # --- secrets / personal data sweep across the whole kit ---
    seen = 0
    for path in ROOT.rglob("*"):
        if path.is_dir() or path.name.startswith(".") or path.suffix not in {
            ".md", ".html", ".css", ".py",
        }:
            continue
        body = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, body):
                check(f"{rel} free of secrets ({pattern[:24]})", False, "match found")
            else:
                seen += 1
        for pattern in PERSONAL_DATA_PATTERNS:
            if re.search(pattern, body):
                check(f"{rel} free of personal data ({pattern[:24]})", False, "match found")
            else:
                seen += 1
    check(f"privacy sweep ran ({seen} pattern scans)", seen > 50)

    # --- summary ---
    print("\n== Result ==")
    if FAILURES:
        print(f"{CHECKS - len(FAILURES)}/{CHECKS} checks passed; {len(FAILURES)} failed:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print(f"All {CHECKS} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
