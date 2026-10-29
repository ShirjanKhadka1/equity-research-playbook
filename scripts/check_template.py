"""Template-completeness checker for the equity research playbook.

Stdlib only, deterministic, dependency-free.

A filled template passes when every required section heading for its
template type is present and has non-empty content beneath it. A heading
with nothing but blank lines (or table separators) under it counts as
empty, not present. Output order follows the template definition order,
never set order, so repeated runs on the same file are identical.

Usage:
    python scripts/check_template.py <file.md> [--template initiation]
    python scripts/check_template.py --list-templates

Exit code 0 means complete; exit code 1 means missing or empty sections.
This checker verifies structure only. It does not verify that any
figure is sourced, correct, or a valuation, and it never recommends
any security.
"""

import argparse
import re
import sys
from pathlib import Path

TEMPLATES = {
    "initiation": (
        "Thesis in one paragraph",
        "Business",
        "Industry",
        "Financials",
        "Valuation",
        "Risks",
        "What would change this thesis",
        "Open questions / unverified items",
    ),
    "earnings": (
        "Headline vs reality",
        "What actually moved",
        "Quality check",
        "Questions for management / next check",
        "Thesis impact",
    ),
    "forensic": (
        "Revenue and cash",
        "Profit quality",
        "Balance sheet",
        "Governance and disclosure",
        "Verdict",
    ),
    "valuation-sanity": (
        "Implied assumptions at the current price",
        "Peer check",
        "Downside case",
        "Method fit",
        "The one-sentence test",
    ),
    "data-first": (
        "Question and scope",
        "Source, licence, and freshness check",
        "Every number: source + period",
        "Confirmation before pattern",
        "Downside and falsifier",
        "Labelling",
    ),
    "structured-debate": (
        "Study + as-of date",
        "Analyst reports landed",
        "Bull case",
        "Bear case",
        "Answered vs unanswered",
        "Risk scenarios",
        "Risk Veto verdict",
        "Falsifier + downside",
    ),
    "ledger-control": (
        "Frozen input list",
        "Cut-off check",
        "Restatement log",
        "Completeness verdict",
        "Falsifier",
    ),
    "research-to-use-case": (
        "Finding, stated plainly",
        "Proposed use case",
        "Evidence gate",
        "Kill criteria",
        "What it is not",
    ),
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def normalize(text):
    """Lowercase, strip numbering, collapse punctuation to spaces."""
    text = text.strip().lower()
    text = re.sub(r"^\d+\.\s*", "", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_sections(text):
    """Return a list of (heading, body) in file order.

    Only level-2 and deeper headings start a section, so the
    level-1 document title is never mistaken for a section.
    """
    sections = []
    current_heading = None
    current_lines = []
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) >= 2:
            if current_heading is not None:
                sections.append((current_heading, "\n".join(current_lines)))
            current_heading = match.group(2)
            current_lines = []
        elif current_heading is not None:
            current_lines.append(line)
    if current_heading is not None:
        sections.append((current_heading, "\n".join(current_lines)))
    return sections


def _has_content(body):
    """True when a section body holds anything beyond blanks."""
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if set(stripped) <= set("|-: "):
            continue
        return True
    return False


def check_text(text, template):
    """Return (missing, empty) section names, in definition order."""
    required = TEMPLATES[template]
    sections = parse_sections(text)
    normalized = [(normalize(h), body) for h, body in sections]
    missing = []
    empty = []
    for wanted in required:
        key = normalize(wanted)
        found = None
        for heading, body in normalized:
            if key in heading:
                found = body
                break
        if found is None:
            missing.append(wanted)
        elif not _has_content(found):
            empty.append(wanted)
    return missing, empty


def detect_template(text):
    """Pick the template with the most matched sections.

    Ties break by template definition order, so detection is
    deterministic. Falls back to 'initiation' when nothing matches.
    """
    best = "initiation"
    best_score = 0
    for name, required in TEMPLATES.items():
        missing, empty = check_text(text, name)
        matched = len(required) - len(missing) - len(empty)
        if matched > best_score:
            best = name
            best_score = matched
    return best


def check_file(path, template="auto"):
    """Check one file. Return (template_used, missing, empty)."""
    text = Path(path).read_text(encoding="utf-8")
    chosen = detect_template(text) if template == "auto" else template
    missing, empty = check_text(text, chosen)
    return chosen, missing, empty


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check a filled playbook template for "
        "missing or empty required sections."
    )
    parser.add_argument("file", nargs="?", help="Markdown file to check")
    parser.add_argument(
        "--template",
        default="auto",
        choices=["auto", *TEMPLATES],
        help="Template type (default: auto-detect).",
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List supported template types and exit.",
    )
    args = parser.parse_args(argv)
    if args.list_templates:
        for name in TEMPLATES:
            print(name)
        return 0
    if not args.file:
        parser.error("a file is required unless --list-templates is given")
    chosen, missing, empty = check_file(args.file, args.template)
    if not missing and not empty:
        print(f"PASS: {args.file} ({chosen}) — all required sections present.")
        return 0
    parts = []
    if missing:
        parts.append("missing: " + ", ".join(missing))
    if empty:
        parts.append("empty: " + ", ".join(empty))
    print(f"FAIL: {args.file} ({chosen}) — " + "; ".join(parts))
    return 1


if __name__ == "__main__":
    sys.exit(main())
