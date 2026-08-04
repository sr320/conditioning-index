#!/usr/bin/env python3
"""Bootstrap data/atlas.csv from the anchor papers we hold locally.

This is a ONE-TIME bootstrap. After the file exists, edit data/atlas.csv directly
(or append rows produced by the extraction step); re-running requires --force.

Column order is taken from data/schema/controlled_vocab.yaml so the CSV can never
drift out of alignment with the schema. Missing fields are written as "".

Grain: one row = one experimental contrast (stressor x dose x generation x assay x outcome).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "data" / "schema" / "controlled_vocab.yaml"
OUT = ROOT / "data" / "atlas.csv"

TODAY = "2026-08-04"
EXTRACTOR = "atlas-bootstrap"

# ---------------------------------------------------------------------------
# Seed rows. Extracted from the local anchor set (00_anchor_index.md + the PDFs
# in the project folder). Numeric doses/effect sizes taken from the anchor index
# summaries; extraction_confidence=med reflects that these came from the lab's own
# structured summary rather than page-verified re-reading. The systematic search
# (scripts 01-02) extends this seed.
# ---------------------------------------------------------------------------
SEED: list[dict] = [
    # ===== Sol Dourdin et al. 2024 — C. gigas, transgenerational pesticide priming =====
    {
        "record_id": "soldourdin2024-01", "study_key": "soldourdin2024", "doi": "NR",
        "first_author": "Sol Dourdin", "year": 2024,
        "short_title": "Parental early pesticide exposure drives oyster offspring phenotype",
        "species": "Crassostrea gigas", "common_name": "Pacific oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "embryo",
        "life_stage_assayed": "pediveliger-larva",
        "priming_window_text": "embryo-larval 0-48 hpf exposure in F0",
        "stressor_category": "pollutant", "stressor_specific": "18-pesticide environmental mixture",
        "dose_value": 2.85, "dose_unit": "ug/L",
        "dose_text": "nominal sum concentration of 18-pesticide mixture",
        "exposure_duration_value": 48, "exposure_duration_unit": "hours",
        "environmentally_realistic": "yes",
        "assay_type": "metamorphosis-competency", "outcome_metric": "epinephrine-induced metamorphosis rate",
        "effect_direction": "mixed", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "metamorphosis-competent pediveliger (MCP)",
        "persisted_past_metamorphosis": "not-tested",
        "persistence_notes": "assay measured AT metamorphosis; persistence beyond captured in survival row",
        "methylation_measured": "yes", "methylation_method": "RRBS-Methyl-seq",
        "transcriptome_measured": "yes", "ncRNA_measured": "no",
        "study_design": "full-factorial parental(F0) x direct(F1)",
        "source_location": "00_anchor_index.md #1", "extraction_confidence": "med",
        "extractor": EXTRACTOR, "extraction_date": TODAY,
        "notes": "parental exposure effect exceeded direct offspring exposure",
    },
    {
        "record_id": "soldourdin2024-02", "study_key": "soldourdin2024", "doi": "NR",
        "first_author": "Sol Dourdin", "year": 2024,
        "short_title": "Parental early pesticide exposure drives oyster offspring phenotype",
        "species": "Crassostrea gigas", "common_name": "Pacific oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "embryo",
        "life_stage_assayed": "spat-juvenile",
        "priming_window_text": "embryo-larval 0-48 hpf exposure in F0",
        "stressor_category": "pollutant", "stressor_specific": "18-pesticide environmental mixture",
        "dose_value": 2.85, "dose_unit": "ug/L",
        "dose_text": "nominal sum concentration of 18-pesticide mixture",
        "exposure_duration_value": 48, "exposure_duration_unit": "hours",
        "environmentally_realistic": "yes",
        "assay_type": "survival", "outcome_metric": "field survival after settlement",
        "effect_direction": "mixed", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "post-settlement field survival",
        "persisted_past_metamorphosis": "yes",
        "persistence_notes": "carryover of F0 exposure detectable in post-metamorphic field survival",
        "methylation_measured": "yes", "methylation_method": "RRBS-Methyl-seq",
        "transcriptome_measured": "yes", "ncRNA_measured": "no",
        "study_design": "full-factorial parental(F0) x direct(F1)",
        "source_location": "00_anchor_index.md #1", "extraction_confidence": "med",
        "extractor": EXTRACTOR, "extraction_date": TODAY,
        "notes": "flagship: bivalve, embryo-primed, effect persists past metamorphosis",
    },
    {
        "record_id": "soldourdin2024-03", "study_key": "soldourdin2024", "doi": "NR",
        "first_author": "Sol Dourdin", "year": 2024,
        "short_title": "Parental early pesticide exposure drives oyster offspring phenotype",
        "species": "Crassostrea gigas", "common_name": "Pacific oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "embryo",
        "life_stage_assayed": "pediveliger-larva",
        "priming_window_text": "embryo-larval 0-48 hpf exposure in F0",
        "stressor_category": "pollutant", "stressor_specific": "18-pesticide environmental mixture",
        "dose_value": 2.85, "dose_unit": "ug/L",
        "dose_text": "nominal sum concentration of 18-pesticide mixture",
        "exposure_duration_value": 48, "exposure_duration_unit": "hours",
        "environmentally_realistic": "yes",
        "assay_type": "methylation", "outcome_metric": "differentially methylated genes (Methyl-seq), incl Calm, Myd88",
        "effect_direction": "mixed", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "gastrula + MCP larvae",
        "persisted_past_metamorphosis": "not-tested",
        "persistence_notes": "methylome assayed at gastrula and MCP; not re-assayed post-metamorphosis",
        "methylation_measured": "yes", "methylation_method": "RRBS-Methyl-seq",
        "transcriptome_measured": "yes", "ncRNA_measured": "no",
        "study_design": "full-factorial parental(F0) x direct(F1)",
        "source_location": "00_anchor_index.md #1", "extraction_confidence": "med",
        "extractor": EXTRACTOR, "extraction_date": TODAY,
        "notes": "F1:F0 interaction candidates flagged (shell secretion, immunity)",
    },
    {
        "record_id": "soldourdin2024-04", "study_key": "soldourdin2024", "doi": "NR",
        "first_author": "Sol Dourdin", "year": 2024,
        "short_title": "Parental early pesticide exposure drives oyster offspring phenotype",
        "species": "Crassostrea gigas", "common_name": "Pacific oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "embryo",
        "life_stage_assayed": "pediveliger-larva",
        "priming_window_text": "embryo-larval 0-48 hpf exposure in F0",
        "stressor_category": "pollutant", "stressor_specific": "18-pesticide environmental mixture",
        "dose_value": 2.85, "dose_unit": "ug/L",
        "dose_text": "nominal sum concentration of 18-pesticide mixture",
        "exposure_duration_value": 48, "exposure_duration_unit": "hours",
        "environmentally_realistic": "yes",
        "assay_type": "transcriptome", "outcome_metric": "differentially expressed genes (RNA-seq), F1:F0 interaction",
        "effect_direction": "mixed", "effect_size_type": "log2FC", "significance": "sig",
        "latest_timepoint_assayed": "gastrula + MCP larvae",
        "persisted_past_metamorphosis": "not-tested",
        "methylation_measured": "yes", "methylation_method": "RRBS-Methyl-seq",
        "transcriptome_measured": "yes", "ncRNA_measured": "no",
        "study_design": "full-factorial parental(F0) x direct(F1)",
        "source_location": "00_anchor_index.md #1", "extraction_confidence": "med",
        "extractor": EXTRACTOR, "extraction_date": TODAY,
        "notes": "",
    },

    # ===== Liew et al. 2018 — Stylophora pistillata, within-generation OA acclimatization =====
    {
        "record_id": "liew2018-01", "study_key": "liew2018", "doi": "10.1126/sciadv.aar8028",
        "first_author": "Liew", "year": 2018,
        "short_title": "Epigenome-associated phenotypic acclimatization to OA in a coral",
        "species": "Stylophora pistillata", "common_name": "smooth cauliflower coral",
        "taxon_group": "coral", "taxon_class": "Anthozoa",
        "generation_primed": "F0", "generation_assayed": "F0",
        "transmission_channel": "somatic-within-gen", "life_stage_primed": "adult",
        "life_stage_assayed": "adult",
        "priming_window_text": "~2 year cultivation across four seawater pH set-points",
        "stressor_category": "OA-low-pH", "stressor_specific": "sustained low pH (7.2/7.4/7.8/8.0)",
        "dose_text": "pH 7.2, 7.4, 7.8, 8.0 (four levels)",
        "exposure_duration_value": 2, "exposure_duration_unit": "years",
        "environmentally_realistic": "yes",
        "assay_type": "calcification", "outcome_metric": "calyx size, porosity, calcification, cell size",
        "effect_direction": "beneficial", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "adult after ~2 yr sustained exposure",
        "persisted_past_metamorphosis": "NA",
        "persistence_notes": "within-generation acclimatization; no metamorphic transition in design",
        "methylation_measured": "yes", "methylation_method": "WGBS",
        "transcriptome_measured": "yes", "ncRNA_measured": "no",
        "study_design": "same-genet fragments distributed across pH treatments",
        "source_location": "00_anchor_index.md #7", "extraction_confidence": "med",
        "extractor": EXTRACTOR, "extraction_date": TODAY,
        "notes": "continued calcification under low carbonate saturation",
    },
    {
        "record_id": "liew2018-02", "study_key": "liew2018", "doi": "10.1126/sciadv.aar8028",
        "first_author": "Liew", "year": 2018,
        "short_title": "Epigenome-associated phenotypic acclimatization to OA in a coral",
        "species": "Stylophora pistillata", "common_name": "smooth cauliflower coral",
        "taxon_group": "coral", "taxon_class": "Anthozoa",
        "generation_primed": "F0", "generation_assayed": "F0",
        "transmission_channel": "somatic-within-gen", "life_stage_primed": "adult",
        "life_stage_assayed": "adult",
        "priming_window_text": "~2 year cultivation across four seawater pH set-points",
        "stressor_category": "OA-low-pH", "stressor_specific": "sustained low pH (7.2/7.4/7.8/8.0)",
        "dose_text": "pH 7.2, 7.4, 7.8, 8.0 (four levels)",
        "exposure_duration_value": 2, "exposure_duration_unit": "years",
        "environmentally_realistic": "yes",
        "assay_type": "methylation", "outcome_metric": "gene body methylation shifts tracking pH (WGBS)",
        "effect_direction": "mixed", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "adult after ~2 yr sustained exposure",
        "persisted_past_metamorphosis": "NA",
        "persistence_notes": "methylation state tracks sustained-stressor acclimatization",
        "methylation_measured": "yes", "methylation_method": "WGBS",
        "transcriptome_measured": "yes", "ncRNA_measured": "no",
        "study_design": "same-genet fragments distributed across pH treatments",
        "source_location": "00_anchor_index.md #7", "extraction_confidence": "med",
        "extractor": EXTRACTOR, "extraction_date": TODAY,
        "notes": "gbM interpreted as noise-reduction / transcriptional fidelity",
    },
    {
        "record_id": "liew2018-03", "study_key": "liew2018", "doi": "10.1126/sciadv.aar8028",
        "first_author": "Liew", "year": 2018,
        "short_title": "Epigenome-associated phenotypic acclimatization to OA in a coral",
        "species": "Stylophora pistillata", "common_name": "smooth cauliflower coral",
        "taxon_group": "coral", "taxon_class": "Anthozoa",
        "generation_primed": "F0", "generation_assayed": "F0",
        "transmission_channel": "somatic-within-gen", "life_stage_primed": "adult",
        "life_stage_assayed": "adult",
        "priming_window_text": "~2 year cultivation across four seawater pH set-points",
        "stressor_category": "OA-low-pH", "stressor_specific": "sustained low pH (7.2/7.4/7.8/8.0)",
        "dose_text": "pH 7.2, 7.4, 7.8, 8.0 (four levels)",
        "exposure_duration_value": 2, "exposure_duration_unit": "years",
        "environmentally_realistic": "yes",
        "assay_type": "transcriptome", "outcome_metric": "RNA-seq expression change with pH",
        "effect_direction": "mixed", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "adult after ~2 yr sustained exposure",
        "persisted_past_metamorphosis": "NA",
        "methylation_measured": "yes", "methylation_method": "WGBS",
        "transcriptome_measured": "yes", "ncRNA_measured": "no",
        "study_design": "same-genet fragments distributed across pH treatments",
        "source_location": "00_anchor_index.md #7", "extraction_confidence": "med",
        "extractor": EXTRACTOR, "extraction_date": TODAY,
        "notes": "",
    },
]


def load_columns() -> list[str]:
    with open(VOCAB) as fh:
        spec = yaml.safe_load(fh)
    return [c["name"] for c in spec["columns"]]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="overwrite an existing atlas.csv")
    args = ap.parse_args()

    if OUT.exists() and not args.force:
        print(f"refusing to overwrite existing {OUT} (use --force)", file=sys.stderr)
        return 1

    columns = load_columns()
    with open(OUT, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="raise")
        writer.writeheader()
        for row in SEED:
            writer.writerow({c: row.get(c, "") for c in columns})

    print(f"wrote {len(SEED)} rows x {len(columns)} columns -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
