#!/usr/bin/env python3
"""Validate data/atlas.csv against data/schema/controlled_vocab.yaml.

Checks, per the schema contract:
  - header matches the schema column set and order
  - required fields are non-empty
  - enum fields hold an allowed value (NA / NR always permitted)
  - int / float fields parse (NA / NR permitted)
  - record_id is unique

Exit code 0 = clean, 1 = errors found. Intended for local runs and CI.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "data" / "schema" / "controlled_vocab.yaml"
ATLAS = ROOT / "data" / "atlas.csv"

SENTINELS = {"", "NA", "NR"}          # accepted everywhere except required-empty check
REQUIRED_SENTINELS = {"NA", "NR"}     # a required field may hold these, but not ""


def _norm(v):
    """Coerce YAML-magic values back to atlas strings (True->'yes', False->'no')."""
    if v is True:
        return "yes"
    if v is False:
        return "no"
    return str(v)


def load_spec() -> list[dict]:
    with open(VOCAB) as fh:
        cols = yaml.safe_load(fh)["columns"]
    for c in cols:
        if "values" in c:
            c["values"] = [_norm(v) for v in c["values"]]
    return cols


def is_number(val: str) -> bool:
    try:
        float(val)
        return True
    except ValueError:
        return False


def main() -> int:
    spec = load_spec()
    by_name = {c["name"]: c for c in spec}
    expected = [c["name"] for c in spec]

    if not ATLAS.exists():
        print(f"ERROR: {ATLAS} not found. Run scripts/00_seed_atlas.py first.", file=sys.stderr)
        return 1

    with open(ATLAS, newline="") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        rows = list(reader)

    errors: list[str] = []

    if header != expected:
        errors.append("HEADER mismatch with schema.")
        missing = [c for c in expected if c not in header]
        extra = [c for c in header if c not in expected]
        if missing:
            errors.append(f"  missing columns: {missing}")
        if extra:
            errors.append(f"  unexpected columns: {extra}")
        if set(header) == set(expected):
            errors.append("  columns present but ORDER differs from schema.")

    seen_ids: set[str] = set()
    for i, row in enumerate(rows, start=2):  # row 1 is the header
        rid = row.get("record_id", "").strip()
        if rid:
            if rid in seen_ids:
                errors.append(f"row {i}: duplicate record_id '{rid}'")
            seen_ids.add(rid)

        for col in header:
            if col not in by_name:
                continue
            c = by_name[col]
            val = (row.get(col) or "").strip()

            if c.get("required") and val == "":
                errors.append(f"row {i}: required field '{col}' is empty")
                continue
            if val in SENTINELS:
                continue

            ctype = c["type"]
            if ctype == "enum":
                allowed = set(c.get("values", [])) | REQUIRED_SENTINELS
                if val not in allowed:
                    errors.append(
                        f"row {i}: '{col}'='{val}' not in allowed {sorted(c.get('values', []))}"
                    )
            elif ctype == "int":
                if not (val.lstrip("-").isdigit()):
                    errors.append(f"row {i}: '{col}'='{val}' is not an integer")
            elif ctype == "float":
                if not is_number(val):
                    errors.append(f"row {i}: '{col}'='{val}' is not numeric")

    if errors:
        print(f"FAIL: {len(errors)} problem(s) in {ATLAS.relative_to(ROOT)}:")
        for e in errors:
            print("  " + e)
        return 1

    print(f"OK: {len(rows)} rows x {len(header)} columns validate against schema.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
