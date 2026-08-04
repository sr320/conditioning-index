# The Conditioning Atlas

A structured, systematic extraction of **every priming / conditioning experiment in the
marine literature**, built to make one question answerable in a click:

> **Has anyone primed at this stage in a bivalve, and did it stick past metamorphosis?**

This operationalizes Section 6 of the lab conceptual framework — *"identify the windows,
identify the doses, and characterize how long the induced memory persists"* — as a real
spreadsheet plus a filterable dashboard, instead of prose.

The core design choice: **one row = one experimental contrast** (a single
`stressor × dose × generation × assay × outcome`), never one paper. That is the only grain at
which windows, doses, and persistence become queryable.

## What's here

| Path | What it is |
|---|---|
| `data/atlas.csv` | **Source of truth.** One row per experimental contrast. |
| `data/atlas.xlsx` | Generated spreadsheet: autofilter, dropdown validation, a pre-filtered `flagship` sheet, a `schema` sheet. |
| `data/schema/controlled_vocab.yaml` | The machine-readable schema + controlled vocabulary (single source of truth for columns/values). |
| `data/schema/data_dictionary.md` | Human-readable companion to the schema. |
| `data/screening/screening.csv` | PRISMA screening log (include/exclude + reasons). |
| `data/screening/prisma_counts.csv` | Generated PRISMA tallies. |
| `docs/` | The static dashboard (GitHub Pages): `index.html`, `atlas.js`, `atlas.csv`, `prisma.svg`. |
| `methods/protocol.md` | The systematic-review protocol (scope, search strings, eligibility). |
| `scripts/` | The pipeline (search → screen → validate → build). |

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# (first time only) bootstrap the seeded atlas from the anchor papers
python scripts/00_seed_atlas.py

# validate, build the xlsx, and publish data to the dashboard
scripts/build.sh
```

### View the dashboard locally
Browsers block `file://` fetches, so serve the folder:

```bash
cd docs && python3 -m http.server
# open http://localhost:8000/
```

The **★ Flagship** button applies `taxon_group = bivalve` and restricts to rows where
persistence past metamorphosis was actually tested. Facet counts update live; every row
expands to full provenance.

### Publish on GitHub Pages
Settings → Pages → Source: `main` / folder `/docs`. The dashboard is fully static
(no build step, no external dependencies).

## Growing the atlas (add papers systematically)

```bash
# 1. search the literature (OpenAlex + Europe PMC), datable + re-runnable
python scripts/01_search.py --max 300 --mailto you@example.org

# 2. merge hits into the screening log (preserves existing decisions)
python scripts/02_dedupe_screen.py

# 3. screen: in data/screening/screening.csv set decision = include | exclude
#    (+ exclude_reason), and maps_to_study_key for includes

# 4. extract: add rows to data/atlas.csv for each included study, one row per
#    experimental contrast, following data/schema/data_dictionary.md

# 5. refresh PRISMA + rebuild spreadsheet + dashboard
python scripts/05_prisma.py
scripts/build.sh
```

`scripts/04_validate_schema.py` (run by `build.sh`) rejects any row whose enum values, types,
or required fields violate the schema — so the atlas cannot silently drift out of vocabulary.

## The schema at a glance

Grouped columns (full definitions in `data/schema/data_dictionary.md`):

- **Identity** — `record_id`, `study_key`, `doi`, `first_author`, `year`, `short_title`
- **Organism** — `species`, `common_name`, `taxon_group`, `taxon_class`
- **Priming design** — `generation_primed` / `generation_assayed`, `transmission_channel`,
  `life_stage_primed` / `life_stage_assayed`, `priming_window_text`
- **Stressor / dose** — `stressor_category`, `stressor_specific`, `dose_value` / `dose_unit` /
  `dose_text`, `exposure_duration_*`, `environmentally_realistic`
- **Outcome / assay** — `assay_type`, `outcome_metric`, `effect_direction`, `effect_size_*`,
  `significance`
- **Persistence** — `persistence_*`, `latest_timepoint_assayed`,
  **`persisted_past_metamorphosis`**, `persistence_notes`
- **Molecular** — `methylation_measured`, `methylation_method`, `transcriptome_measured`,
  `ncRNA_measured`
- **Provenance** — `study_design`, `sample_size`, `source_location`, `extraction_confidence`,
  `extractor`, `extraction_date`, `notes`

## Current contents

**66 contrasts across 55 included studies** (OpenAlex search + curated bibliography).
Screening log: 485 records → 55 include / 430 exclude.

Major clusters now in the atlas:
- **Thermal hardening** — Clegg/Jackson oysters; Brun scallop; Aleng/Dunphy/Dong/Georgoulis/Moyen/Song/Zhang mussel & clam heat-hardening; Glass anemone heat priming.
- **Immune priming** — Green/Lafont/Morga poly(I:C) & OsHV-1 series; Cong/Yue/Wang scallop; Zhang/Li/Wang/Rey-Campos Vibrio priming; Fallet early-life microbial protection.
- **OA / carryover / TGP** — Parker OA TGP series; Hettinger/Spencer Olympia larval carryover (past metamorphosis); Putnam/Gurr geoduck; Rondón parental diuron methylome; Kozal paternal heat.
- **Anchors / other** — Sol Dourdin, Liew, Putnam coral parental, Bellantuono, Clark urchin, fish TGP, Marshall bryozoan.

Flagship filter (bivalve + persistence past metamorphosis tested) currently hits **8 contrasts**.
