#!/usr/bin/env python3
"""First-pass title/abstract screening of unscreened records.

Applies deterministic rules from methods/protocol.md:
  - auto-exclude reviews, false-positive "priming" hits, and records with no
    conditioning language + no experimental priming design
  - auto-include high-confidence experimental priming / TGP / carryover studies
    in marine taxa (decision=include, screened_by=auto-screen)

Ambiguous records stay unscreened for human review. Re-running is safe: only
rows with decision=unscreened are touched.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening" / "screening.csv"
SEARCHDIR = ROOT / "data" / "search"

FIELDS = ["record_key", "doi", "first_author", "year", "title", "source",
          "decision", "exclude_reason", "maps_to_study_key", "screened_by", "notes"]

FALSE_POS = re.compile(
    r"(fertilization envelope|priming capacity|cytoplasmic DNA|PCR priming|"
    r"\bprimer\b|radiocarbon|intcal|age calibration)",
    re.I,
)
REVIEW = re.compile(
    r"\b(a review|systematic review|meta[- ]analysis|perspective|editorial|"
    r"commentary|this review|we review)\b|(^review\b|\breview$|: a review\b)",
    re.I,
)
STRONG = re.compile(
    r"\b(transgenerational plasticity|carry[- ]?over effects?|"
    r"parental effects?|maternal effects?|paternal effects?|"
    r"epigenetic memory|transgenerational (immune )?priming|"
    r"preconditioning|thermal priming|heat priming|"
    r"parental exposure|maternal exposure|induced (thermal )?tolerance|"
    r"stress hardening|developmental priming|positive carryover|"
    r"transgenerational exposure)\b",
    re.I,
)
MARINE = re.compile(
    r"\b(oyster|mussel|coral|bivalve|clam|scallop|abalone|urchin|fish|"
    r"stickleback|sea bass|cod|salmon|shrimp|prawn|lobster|crab|"
    r"gastropod|cephalopod|sea anemone|damselfish|reef[- ]building|"
    r"crassostrea|saccostrea|mytilus|pocillopora|stylophora|porites|"
    r"ostrea|mercenaria|argopecten|sparus|gadus|amphiprion|acropora|"
    r"psammechinus|marine invertebrate|marine organism)\b",
    re.I,
)
EXPERIMENT = re.compile(
    r"\b(expos(ed|ure)|treatment|experiment|factorial|broodstock|larva|"
    r"embryo|offspring|juvenile|F0|F1|F2|control|precondition)\b",
    re.I,
)


def load_hits() -> dict:
    by_key, by_doi = {}, {}
    for p in SEARCHDIR.glob("*.csv"):
        if p.name.startswith("all_hits"):
            continue
        with open(p, newline="") as fh:
            for r in csv.DictReader(fh):
                by_key[r["record_key"]] = r
                if r.get("doi") and r["doi"] != "NR":
                    by_doi[r["doi"].lower()] = r
    return by_key, by_doi


def study_key(r: dict) -> str:
    a = re.sub(r"[^a-z]", "", (r.get("first_author") or "").lower())
    return f"{a}{r.get('year') or ''}"


def decide(r: dict, hit: Optional[dict]) -> Tuple[str, str, str, str]:
    """Return (decision, exclude_reason, maps_to_study_key, notes)."""
    title = r.get("title") or ""
    abstract = (hit or {}).get("abstract") or ""
    text = f"{title} {abstract}"

    if FALSE_POS.search(title):
        return "exclude", "not-priming", "", "false-positive priming language"
    if REVIEW.search(title):
        return "exclude", "review", "", "title indicates review/perspective"

    strong_title = bool(STRONG.search(title))
    strong_abs = bool(STRONG.search(abstract))
    marine = bool(MARINE.search(text))
    experimental = bool(EXPERIMENT.search(abstract) or EXPERIMENT.search(title))

    if strong_title and marine and experimental:
        return "include", "", study_key(r), "auto: strong priming/TGP title + marine + experimental cues"
    if strong_title and marine and strong_abs:
        return "include", "", study_key(r), "auto: strong priming/TGP title+abstract + marine"

    # No conditioning language at all → exclude as not-priming
    if not strong_title and not strong_abs:
        return "exclude", "not-priming", "", "no priming/TGP/carryover/parental-effect language"

    # Has language but not marine → not-marine
    if not marine:
        return "exclude", "not-marine", "", "priming language but not marine taxon"

    # Ambiguous: leave for human
    return "unscreened", "", "", "ambiguous; needs human title/abstract screen"


def main() -> int:
    by_key, by_doi = load_hits()
    with open(SCREEN, newline="") as fh:
        rows = list(csv.DictReader(fh))

    stats = {"include": 0, "exclude": 0, "unscreened": 0, "untouched": 0}
    for r in rows:
        if r.get("decision") != "unscreened":
            stats["untouched"] += 1
            continue
        hit = by_key.get(r["record_key"]) or by_doi.get((r.get("doi") or "").lower())
        decision, reason, mapkey, notes = decide(r, hit)
        r["decision"] = decision
        r["exclude_reason"] = reason
        r["maps_to_study_key"] = mapkey
        if decision != "unscreened":
            r["screened_by"] = "auto-screen"
            r["notes"] = notes
        stats[decision if decision in stats else "unscreened"] += 1

    with open(SCREEN, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})

    print("screening pass complete:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    includes = [r for r in rows if r["decision"] == "include" and r.get("screened_by") == "auto-screen"]
    print(f"\nauto-included ({len(includes)}):")
    for r in includes:
        print(f"  {r['year']} {r['first_author']}: {r['title'][:90]}")
        print(f"    -> {r['maps_to_study_key']}  doi={r['doi']}")
    still = [r for r in rows if r["decision"] == "unscreened"]
    print(f"\nstill unscreened: {len(still)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
