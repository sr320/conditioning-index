#!/usr/bin/env python3
"""Emit PRISMA-style counts and a flow diagram from the screening log + atlas.

Reads data/screening/screening.csv and data/atlas.csv and writes:
  - data/screening/prisma_counts.csv   (identified / screened / excluded / included)
  - docs/prisma.svg                     (a simple self-contained flow diagram)
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening" / "screening.csv"
ATLAS = ROOT / "data" / "atlas.csv"
COUNTS = ROOT / "data" / "screening" / "prisma_counts.csv"
SVG = ROOT / "docs" / "prisma.svg"


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> int:
    screen = load(SCREEN)
    atlas = load(ATLAS)

    identified = len(screen)
    unscreened = sum(1 for r in screen if r.get("decision") == "unscreened")
    screened = identified - unscreened
    included = sum(1 for r in screen if r.get("decision") == "include")
    excluded_rows = [r for r in screen if r.get("decision") == "exclude"]
    excluded = len(excluded_rows)
    reasons = Counter(r.get("exclude_reason", "unspecified") or "unspecified" for r in excluded_rows)
    contrasts = len(atlas)
    included_studies = len({r.get("maps_to_study_key") for r in screen
                            if r.get("decision") == "include" and r.get("maps_to_study_key")})

    with open(COUNTS, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["stage", "n"])
        w.writerow(["identified", identified])
        w.writerow(["screened", screened])
        w.writerow(["unscreened_remaining", unscreened])
        w.writerow(["excluded", excluded])
        for reason, n in sorted(reasons.items()):
            w.writerow([f"excluded:{reason}", n])
        w.writerow(["included_studies", included_studies])
        w.writerow(["extracted_contrasts", contrasts])

    reason_lines = "".join(
        f'<tspan x="470" dy="16">{reason}: {n}</tspan>' for reason, n in sorted(reasons.items())
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="720" height="470" font-family="-apple-system,Segoe UI,Roboto,Arial,sans-serif" font-size="14">
  <style>
    .box {{ fill:#17212b; stroke:#2b3a49; }}
    .t {{ fill:#e8eef4; }} .m {{ fill:#93a4b3; }} .a {{ stroke:#4cc4b0; stroke-width:2; marker-end:url(#arrow); }}
  </style>
  <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
    <path d="M0,0 L6,3 L0,6 Z" fill="#4cc4b0"/></marker></defs>
  <rect width="720" height="470" fill="#0f1720"/>
  <rect class="box" x="60" y="20" width="320" height="60" rx="8"/>
  <text class="t" x="76" y="45">Records identified</text>
  <text class="m" x="76" y="66">n = {identified} (OpenAlex + Europe PMC + anchors)</text>

  <rect class="box" x="60" y="130" width="320" height="60" rx="8"/>
  <text class="t" x="76" y="155">Screened (title / abstract)</text>
  <text class="m" x="76" y="176">n = {screened}   ({unscreened} awaiting screening)</text>

  <rect class="box" x="60" y="240" width="320" height="60" rx="8"/>
  <text class="t" x="76" y="265">Included studies</text>
  <text class="m" x="76" y="286">n = {included_studies}</text>

  <rect class="box" x="60" y="350" width="320" height="70" rx="8"/>
  <text class="t" x="76" y="375">Extracted contrasts (atlas rows)</text>
  <text class="m" x="76" y="396">n = {contrasts}</text>

  <rect class="box" x="440" y="240" width="240" height="{60 + 16 * max(len(reasons),1)}" rx="8"/>
  <text class="t" x="456" y="265">Excluded  n = {excluded}</text>
  <text class="m" x="456" y="286">{reason_lines}</text>

  <line class="a" x1="220" y1="80" x2="220" y2="128"/>
  <line class="a" x1="220" y1="190" x2="220" y2="238"/>
  <line class="a" x1="220" y1="300" x2="220" y2="348"/>
  <line class="a" x1="380" y1="160" x2="438" y2="250"/>
</svg>"""
    SVG.parent.mkdir(parents=True, exist_ok=True)
    SVG.write_text(svg)

    print(f"identified={identified} screened={screened} unscreened={unscreened} "
          f"excluded={excluded} included_studies={included_studies} contrasts={contrasts}")
    print(f"wrote {COUNTS.relative_to(ROOT)} and {SVG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
