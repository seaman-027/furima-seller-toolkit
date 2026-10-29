#!/usr/bin/env python3
"""Furima Seller Toolkit - reply template renderer for individual sellers.

A small, dependency-free CLI that lists, shows and renders Japanese
reply templates for flea-market / EC sellers (Mercari and similar).

Templates live in the ``templates/`` folder as Markdown files. Variables
are written as ``{name}`` and filled with ``--set name=value``.

Examples:
    python seller_templates.py list
    python seller_templates.py show out_of_stock
    python seller_templates.py render out_of_stock \
        --set item_name=シルクスカーフ --set alt_item=ウールスカーフ
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
VAR_PATTERN = re.compile(r"\{([a-zA-Z0-9_]+)\}")


def load_template(name: str) -> str:
    """Return the raw text of template *name* (without the .md suffix)."""
    path = TEMPLATE_DIR / f"{name}.md"
    if not path.is_file():
        available = ", ".join(list_templates()) or "(none)"
        raise SystemExit(f"Template not found: {name}\nAvailable: {available}")
    return path.read_text(encoding="utf-8")


def list_templates() -> list[str]:
    """Return the names of all available templates, sorted."""
    if not TEMPLATE_DIR.is_dir():
        return []
    return sorted(p.stem for p in TEMPLATE_DIR.glob("*.md"))


def template_variables(text: str) -> list[str]:
    """Return variable names used in *text*, in first-use order."""
    seen: list[str] = []
    for match in VAR_PATTERN.finditer(text):
        name = match.group(1)
        if name not in seen:
            seen.append(name)
    return seen


def render(text: str, values: dict[str, str]) -> str:
    """Replace ``{var}`` placeholders in *text* using *values*.

    Placeholders without a supplied value are left as-is so the seller
    can spot what still needs editing before sending.
    """
    def _sub(match: re.Match[str]) -> str:
        return values.get(match.group(1), match.group(0))

    return VAR_PATTERN.sub(_sub, text)


def parse_set_args(pairs: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise SystemExit(f"--set expects key=value, got: {pair}")
        key, value = pair.split("=", 1)
        values[key.strip()] = value
    return values


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render reply templates for flea-market sellers."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List available templates")

    show = sub.add_parser("show", help="Show a template and its variables")
    show.add_argument("name")

    rend = sub.add_parser("render", help="Render a template with values")
    rend.add_argument("name")
    rend.add_argument(
        "--set",
        dest="pairs",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Fill a {KEY} placeholder; repeatable",
    )

    args = parser.parse_args(argv)

    if args.command == "list":
        for name in list_templates():
            text = load_template(name)
            variables = ", ".join(template_variables(text)) or "-"
            print(f"{name}\t(vars: {variables})")
        return 0

    text = load_template(args.name)

    if args.command == "show":
        print(text)
        variables = template_variables(text)
        if variables:
            print("\n--- variables ---")
            for var in variables:
                print(f"{{{var}}}")
        return 0

    if args.command == "render":
        values = parse_set_args(args.pairs)
        output = render(text, values)
        print(output)
        missing = [v for v in template_variables(text) if v not in values]
        if missing:
            print(
                "\n[note] Unfilled placeholders: "
                + ", ".join(f"{{{m}}}" for m in missing),
                file=sys.stderr,
            )
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
