#!/usr/bin/env python3
"""Systematic search for marine priming / conditioning experiments.

Queries OpenAlex and Europe PMC (both free, no key) with the concept blocks from
methods/protocol.md and writes one CSV per source to data/search/, plus a combined
data/search/all_hits_<date>.csv. Re-runnable and datable.

Usage:
  scripts/01_search.py --max 300 --mailto you@example.org
  scripts/01_search.py --source europepmc --max 100

Network access is required. Failures are reported but do not crash the other source.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "data" / "search"

CONDITIONING = [
    "priming", "conditioning", "transgenerational plasticity", "carryover effect",
    "developmental programming", "hardening", "acclimatization", "parental effect",
    "epigenetic memory", "preconditioning", "transgenerational immune priming",
]
MARINE = [
    "marine", "ocean", "estuarine", "oyster", "mussel", "clam", "scallop", "coral",
    "abalone", "sea urchin", "bivalve", "mollusc",
]

FIELDS = ["source", "record_key", "doi", "first_author", "year", "title", "abstract", "url", "query"]


def _key(author: str, year, doi: str) -> str:
    a = re.sub(r"[^a-z]", "", (author or "").lower())
    if a and year:
        return f"{a}{year}"
    if doi and doi != "NR":
        return re.sub(r"[^a-z0-9]", "", doi.lower())[:24]
    return re.sub(r"[^a-z0-9]", "", (author or "anon").lower())[:16] + str(year or "")


def _reconstruct_abstract(inv_index) -> str:
    if not inv_index:
        return ""
    positions = []
    for word, idxs in inv_index.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions)[:1200]


def boolean_query() -> str:
    cond = " OR ".join(f'"{t}"' if " " in t else t for t in CONDITIONING)
    mar = " OR ".join(f'"{t}"' if " " in t else t for t in MARINE)
    return f"({cond}) AND ({mar})"


def search_openalex(max_records: int, mailto: str) -> list[dict]:
    rows, seen = [], set()
    base = "https://api.openalex.org/works"
    query = boolean_query()
    params = {
        "search": query,
        "per-page": 200,
        "select": "title,doi,publication_year,authorships,abstract_inverted_index,primary_location",
    }
    if mailto:
        params["mailto"] = mailto
    cursor = "*"
    while len(rows) < max_records:
        params["cursor"] = cursor
        r = requests.get(base, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        for w in data.get("results", []):
            doi = (w.get("doi") or "").replace("https://doi.org/", "") or "NR"
            auths = w.get("authorships") or []
            first = ""
            if auths:
                first = (auths[0].get("author") or {}).get("display_name", "").split()[-1:]
                first = first[0] if first else ""
            key = _key(first, w.get("publication_year"), doi)
            if key in seen:
                continue
            seen.add(key)
            loc = w.get("primary_location") or {}
            rows.append({
                "source": "openalex", "record_key": key, "doi": doi, "first_author": first,
                "year": w.get("publication_year") or "", "title": (w.get("title") or "").strip(),
                "abstract": _reconstruct_abstract(w.get("abstract_inverted_index")),
                "url": loc.get("landing_page_url", "") or "", "query": query,
            })
            if len(rows) >= max_records:
                break
        cursor = (data.get("meta") or {}).get("next_cursor")
        if not cursor:
            break
        time.sleep(0.3)
    return rows


def search_europepmc(max_records: int) -> list[dict]:
    rows, seen = [], set()
    base = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    query = boolean_query()
    page_size = 100
    cursor = "*"
    while len(rows) < max_records:
        params = {"query": query, "format": "json", "pageSize": page_size,
                  "cursorMark": cursor, "resultType": "core"}
        r = requests.get(base, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        results = (data.get("resultList") or {}).get("result", [])
        if not results:
            break
        for w in results:
            doi = w.get("doi") or "NR"
            first = (w.get("authorString") or "").split(",")[0].split()[-1:] or [""]
            first = first[0]
            key = _key(first, w.get("pubYear"), doi)
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "source": "europepmc", "record_key": key, "doi": doi, "first_author": first,
                "year": w.get("pubYear") or "", "title": (w.get("title") or "").strip(),
                "abstract": (w.get("abstractText") or "")[:1200],
                "url": f"https://doi.org/{doi}" if doi != "NR" else "", "query": query,
            })
            if len(rows) >= max_records:
                break
        nxt = data.get("nextCursorMark")
        if not nxt or nxt == cursor:
            break
        cursor = nxt
        time.sleep(0.3)
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max", type=int, default=300, help="max records per source")
    ap.add_argument("--source", choices=["openalex", "europepmc", "both"], default="both")
    ap.add_argument("--mailto", default="", help="contact email for the OpenAlex polite pool")
    args = ap.parse_args()

    OUTDIR.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    combined: list[dict] = []

    runners = []
    if args.source in ("openalex", "both"):
        runners.append(("openalex", lambda: search_openalex(args.max, args.mailto)))
    if args.source in ("europepmc", "both"):
        runners.append(("europepmc", lambda: search_europepmc(args.max)))

    for name, fn in runners:
        try:
            rows = fn()
            write_csv(OUTDIR / f"{name}_{today}.csv", rows)
            combined.extend(rows)
            print(f"{name}: {len(rows)} records -> data/search/{name}_{today}.csv")
        except Exception as e:  # noqa: BLE001 - report and continue with other source
            print(f"{name}: FAILED ({e})", file=sys.stderr)

    if combined:
        write_csv(OUTDIR / f"all_hits_{today}.csv", combined)
        print(f"combined: {len(combined)} records -> data/search/all_hits_{today}.csv")
        print("next: scripts/02_dedupe_screen.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
