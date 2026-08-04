#!/usr/bin/env python3
"""Merge search hits into the screening log, deduplicating and preserving decisions.

Reads all data/search/*_*.csv (produced by 01_search.py), deduplicates by DOI then by
normalized title, and updates data/screening/screening.csv:
  - records already in the log keep their human decision untouched
  - genuinely new records are appended with decision = "unscreened"

Then prints how many records are unscreened so the human knows what is left to do.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEARCHDIR = ROOT / "data" / "search"
SCREEN = ROOT / "data" / "screening" / "screening.csv"

SCREEN_FIELDS = ["record_key", "doi", "first_author", "year", "title", "source",
                 "decision", "exclude_reason", "maps_to_study_key", "screened_by", "notes"]


def norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def load_screen() -> list[dict]:
    if not SCREEN.exists():
        return []
    with open(SCREEN, newline="") as fh:
        return list(csv.DictReader(fh))


def load_hits() -> list[dict]:
    hits = []
    for p in sorted(SEARCHDIR.glob("*_*.csv")):
        if p.name.startswith("all_hits_"):
            continue
        with open(p, newline="") as fh:
            hits.extend(csv.DictReader(fh))
    return hits


def main() -> int:
    existing = load_screen()
    by_doi = {r["doi"].lower(): r for r in existing if r.get("doi") and r["doi"] != "NR"}
    by_title = {norm_title(r["title"]): r for r in existing if r.get("title")}
    by_key = {r["record_key"]: r for r in existing if r.get("record_key")}

    hits = load_hits()
    if not hits:
        print("no search hits found in data/search/. Run scripts/01_search.py first.")
    added = 0
    for h in hits:
        doi = (h.get("doi") or "").lower()
        nt = norm_title(h.get("title", ""))
        if (doi and doi != "nr" and doi in by_doi) or (nt and nt in by_title) \
           or h.get("record_key") in by_key:
            continue  # already known — do not touch its decision
        row = {
            "record_key": h.get("record_key", ""), "doi": h.get("doi", "NR"),
            "first_author": h.get("first_author", ""), "year": h.get("year", ""),
            "title": h.get("title", ""), "source": h.get("source", ""),
            "decision": "unscreened", "exclude_reason": "", "maps_to_study_key": "",
            "screened_by": "", "notes": "",
        }
        existing.append(row)
        if doi and doi != "nr":
            by_doi[doi] = row
        if nt:
            by_title[nt] = row
        by_key[row["record_key"]] = row
        added += 1

    SCREEN.parent.mkdir(parents=True, exist_ok=True)
    with open(SCREEN, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=SCREEN_FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in existing:
            w.writerow({k: r.get(k, "") for k in SCREEN_FIELDS})

    unscreened = sum(1 for r in existing if r.get("decision") == "unscreened")
    print(f"merged {len(hits)} hits: +{added} new, {len(existing)} total in screening log")
    print(f"unscreened awaiting human title/abstract decision: {unscreened}")
    print("next: screen in data/screening/screening.csv, then scripts/05_prisma.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
