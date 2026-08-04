#!/usr/bin/env python3
"""Append curated extractions for newly included studies to data/atlas.csv.

Idempotent: skips record_ids that already exist. Column order follows the schema.
"""
from __future__ import annotations

import csv
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "data" / "schema" / "controlled_vocab.yaml"
ATLAS = ROOT / "data" / "atlas.csv"

TODAY = "2026-08-04"
EX = "search-extract-v1"

NEW: list[dict] = [
    # ===== Parker et al. 2011 — S. glomerata parental OA =====
    {
        "record_id": "parker2011-01", "study_key": "parker2011",
        "doi": "10.1111/j.1365-2486.2011.02520.x", "first_author": "Parker", "year": 2011,
        "short_title": "Adult OA exposure influences oyster offspring response",
        "species": "Saccostrea glomerata", "common_name": "Sydney rock oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "gamete-broodstock",
        "life_stage_assayed": "veliger-larva",
        "priming_window_text": "adult reproductive conditioning under elevated PCO2",
        "stressor_category": "OA-low-pH", "stressor_specific": "elevated PCO2 during reproductive conditioning",
        "dose_text": "elevated PCO2 (OA treatment vs ambient)", "environmentally_realistic": "yes",
        "assay_type": "growth-size", "outcome_metric": "larval growth and developmental rate",
        "effect_direction": "beneficial", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "larvae", "persisted_past_metamorphosis": "not-tested",
        "persistence_notes": "positive carryover assayed at larval stage only in this paper",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "adult OA conditioning then offspring reared at elevated/ambient PCO2; wild + selectively bred lines",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY,
        "notes": "foundational Sydney rock oyster parental OA priming paper",
    },
    {
        "record_id": "parker2011-02", "study_key": "parker2011",
        "doi": "10.1111/j.1365-2486.2011.02520.x", "first_author": "Parker", "year": 2011,
        "short_title": "Adult OA exposure influences oyster offspring response",
        "species": "Saccostrea glomerata", "common_name": "Sydney rock oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "gamete-broodstock",
        "life_stage_assayed": "veliger-larva",
        "priming_window_text": "adult reproductive conditioning under elevated PCO2",
        "stressor_category": "OA-low-pH", "stressor_specific": "elevated PCO2 during reproductive conditioning",
        "dose_text": "elevated PCO2 (OA treatment vs ambient)", "environmentally_realistic": "yes",
        "assay_type": "survival", "outcome_metric": "larval survival under elevated PCO2",
        "effect_direction": "beneficial", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "larvae", "persisted_past_metamorphosis": "not-tested",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "adult OA conditioning then offspring reared at elevated/ambient PCO2",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY, "notes": "",
    },

    # ===== Parker et al. 2015 — persistence of OA carryover past metamorphosis =====
    {
        "record_id": "parker2015-01", "study_key": "parker2015",
        "doi": "10.1371/journal.pone.0132276", "first_author": "Parker", "year": 2015,
        "short_title": "Persistence of positive OA carryover effects in S. glomerata",
        "species": "Saccostrea glomerata", "common_name": "Sydney rock oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "gamete-broodstock",
        "life_stage_assayed": "adult",
        "priming_window_text": "transgenerational exposure of adults to elevated CO2; F1 tracked to adulthood",
        "stressor_category": "OA-low-pH", "stressor_specific": "elevated CO2 / ocean acidification",
        "dose_text": "elevated CO2 vs ambient", "environmentally_realistic": "yes",
        "assay_type": "physiology-other",
        "outcome_metric": "positive carryover performance into adulthood under OA",
        "effect_direction": "beneficial", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "F1 adulthood", "persisted_past_metamorphosis": "yes",
        "persistence_notes": "explicit test that larval/juvenile positive carryover persists into adulthood",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "transgenerational OA; F1 followed to adulthood; subsequent generation also tested",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY,
        "notes": "flagship: bivalve broodstock-primed OA effect persists past metamorphosis into adulthood",
    },
    {
        "record_id": "parker2015-02", "study_key": "parker2015",
        "doi": "10.1371/journal.pone.0132276", "first_author": "Parker", "year": 2015,
        "short_title": "Persistence of positive OA carryover effects in S. glomerata",
        "species": "Saccostrea glomerata", "common_name": "Sydney rock oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0-F1", "generation_assayed": "F2",
        "transmission_channel": "biparental", "life_stage_primed": "gamete-broodstock",
        "life_stage_assayed": "spat-juvenile",
        "priming_window_text": "subsequent transgenerational exposure of F1 adults; F2 larvae/juveniles assayed",
        "stressor_category": "OA-low-pH", "stressor_specific": "elevated CO2 / ocean acidification",
        "dose_text": "elevated CO2 vs ambient", "environmentally_realistic": "yes",
        "assay_type": "survival", "outcome_metric": "F2 larval/juvenile performance under OA",
        "effect_direction": "beneficial", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "F2 larvae/juveniles", "persisted_past_metamorphosis": "not-tested",
        "persistence_notes": "tests whether adaptive responses appear in the next generation after F1 adult re-exposure",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "multi-generation OA exposure",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY, "notes": "",
    },

    # ===== Parker et al. 2021 — habitat-dependent TGP =====
    {
        "record_id": "parker2021-01", "study_key": "parker2021",
        "doi": "10.1242/jeb.239269", "first_author": "Parker", "year": 2021,
        "short_title": "Oyster OA TGP differs with intertidal vs subtidal habitat",
        "species": "Saccostrea glomerata", "common_name": "Sydney rock oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "gamete-broodstock",
        "life_stage_assayed": "veliger-larva",
        "priming_window_text": "parental OA exposure under emersion (intertidal) vs continuous immersion (subtidal)",
        "stressor_category": "OA-low-pH", "stressor_specific": "elevated CO2 with/without tidal emersion",
        "dose_text": "elevated CO2; habitat = emersion vs immersion", "environmentally_realistic": "yes",
        "assay_type": "physiology-other", "outcome_metric": "TGP magnitude/direction depends on parental habitat",
        "effect_direction": "mixed", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "larvae/juveniles", "persisted_past_metamorphosis": "not-tested",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "parental habitat (emersion/immersion) x elevated CO2 TGP design",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY,
        "notes": "shows TGP to OA is habitat-context dependent",
    },

    # ===== Lafont et al. 2018/2019 — poly(I:C) maternal immune priming =====
    {
        "record_id": "lafont2018-01", "study_key": "lafont2018",
        "doi": "10.1016/j.dci.2018.09.022", "first_author": "Lafont", "year": 2018,
        "short_title": "Maternal poly(I:C) priming improves larval OsHV-1 survival",
        "species": "Crassostrea gigas", "common_name": "Pacific oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "maternal", "life_stage_primed": "gamete-broodstock",
        "life_stage_assayed": "veliger-larva",
        "priming_window_text": "adult injection of poly(I:C) 3 or 10 days prior to strip-spawning",
        "stressor_category": "pathogen-immune", "stressor_specific": "poly(I:C) viral mimic (OsHV-1 priming)",
        "dose_value": 5, "dose_unit": "mg/ml",
        "dose_text": "100 uL poly(I:C) at 5 mg/ml injected into adductor muscle",
        "exposure_duration_value": 3, "exposure_duration_unit": "days",
        "environmentally_realistic": "no",
        "assay_type": "immune-challenge",
        "outcome_metric": "larval cumulative mortality 48 h post OsHV-1 inoculation",
        "effect_direction": "beneficial", "effect_size_value": 14.4, "effect_size_type": "percent-change",
        "significance": "sig",
        "persistence_value": 3, "persistence_unit": "days",
        "latest_timepoint_assayed": "larvae 48 h post-challenge",
        "persisted_past_metamorphosis": "not-tested",
        "persistence_notes": "3-day pre-spawn maternal priming reduced larval mortality to 14.4% vs 45.3% control; 10-day priming weaker/ns",
        "methylation_measured": "no", "transcriptome_measured": "yes", "ncRNA_measured": "no",
        "study_design": "maternal vs paternal poly(I:C); time-to-spawn factorial; RNA-seq on unchallenged larvae",
        "sample_size": "up to 6 pair-mated families per treatment",
        "source_location": "Lafont et al. DCI manuscript methods/results", "extraction_confidence": "high",
        "extractor": EX, "extraction_date": TODAY,
        "notes": "framework Section-6 precedent: poly(I:C) broodstock priming → herpesvirus-resistant offspring",
    },
    {
        "record_id": "lafont2018-02", "study_key": "lafont2018",
        "doi": "10.1016/j.dci.2018.09.022", "first_author": "Lafont", "year": 2018,
        "short_title": "Maternal poly(I:C) priming improves larval OsHV-1 survival",
        "species": "Crassostrea gigas", "common_name": "Pacific oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "paternal", "life_stage_primed": "gamete-broodstock",
        "life_stage_assayed": "veliger-larva",
        "priming_window_text": "paternal poly(I:C) injection prior to spawning",
        "stressor_category": "pathogen-immune", "stressor_specific": "poly(I:C) viral mimic (OsHV-1 priming)",
        "dose_value": 5, "dose_unit": "mg/ml",
        "dose_text": "100 uL poly(I:C) at 5 mg/ml injected into adductor muscle",
        "environmentally_realistic": "no",
        "assay_type": "immune-challenge",
        "outcome_metric": "larval survival after OsHV-1 challenge",
        "effect_direction": "none", "effect_size_type": "NR", "significance": "ns",
        "latest_timepoint_assayed": "larvae", "persisted_past_metamorphosis": "not-tested",
        "persistence_notes": "paternal priming had no significant effect; maternal channel only",
        "methylation_measured": "no", "transcriptome_measured": "yes", "ncRNA_measured": "no",
        "study_design": "maternal vs paternal cross design",
        "source_location": "Lafont et al. DCI results", "extraction_confidence": "high",
        "extractor": EX, "extraction_date": TODAY, "notes": "",
    },
    {
        "record_id": "lafont2018-03", "study_key": "lafont2018",
        "doi": "10.1016/j.dci.2018.09.022", "first_author": "Lafont", "year": 2018,
        "short_title": "Maternal poly(I:C) priming improves larval OsHV-1 survival",
        "species": "Crassostrea gigas", "common_name": "Pacific oyster",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "maternal", "life_stage_primed": "gamete-broodstock",
        "life_stage_assayed": "veliger-larva",
        "priming_window_text": "adult poly(I:C) prior to spawning",
        "stressor_category": "pathogen-immune", "stressor_specific": "poly(I:C) viral mimic (OsHV-1 priming)",
        "dose_value": 5, "dose_unit": "mg/ml",
        "dose_text": "100 uL poly(I:C) at 5 mg/ml",
        "environmentally_realistic": "no",
        "assay_type": "transcriptome",
        "outcome_metric": "antiviral gene expression in unchallenged larvae (RNA-seq)",
        "effect_direction": "none", "effect_size_type": "NR", "significance": "ns",
        "latest_timepoint_assayed": "unchallenged larvae", "persisted_past_metamorphosis": "not-tested",
        "persistence_notes": "no evidence parental poly(I:C) reconfigures constitutive antiviral transcriptome; maternal provisioning hypothesized",
        "methylation_measured": "no", "transcriptome_measured": "yes", "ncRNA_measured": "no",
        "study_design": "RNA-seq of unchallenged larvae from primed vs control mothers",
        "source_location": "Lafont et al. DCI abstract/results", "extraction_confidence": "high",
        "extractor": EX, "extraction_date": TODAY, "notes": "",
    },

    # ===== Griffith & Gobler 2017 — costly TGP in clams/scallops =====
    {
        "record_id": "griffith2017-01", "study_key": "griffith2017",
        "doi": "10.1038/s41598-017-11442-3", "first_author": "Griffith", "year": 2017,
        "short_title": "Parental OA makes clam/scallop offspring more vulnerable",
        "species": "Mercenaria mercenaria", "common_name": "hard clam",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "gamete-broodstock",
        "life_stage_assayed": "veliger-larva",
        "priming_window_text": "adults under high vs low pCO2 during gametogenesis",
        "stressor_category": "OA-low-pH", "stressor_specific": "elevated pCO2 during gametogenesis",
        "dose_text": "high vs ambient pCO2", "environmentally_realistic": "yes",
        "assay_type": "survival",
        "outcome_metric": "larval vulnerability to low pH and additional stressors",
        "effect_direction": "costly", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "larvae under low pH + thermal/food/HAB stress",
        "persisted_past_metamorphosis": "not-tested",
        "persistence_notes": "no beneficial TGP; offspring of high-pCO2 adults more vulnerable",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "parental pCO2 x offspring pH x additional stressors",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY,
        "notes": "important counterexample: parental OA priming can be maladaptive",
    },
    {
        "record_id": "griffith2017-02", "study_key": "griffith2017",
        "doi": "10.1038/s41598-017-11442-3", "first_author": "Griffith", "year": 2017,
        "short_title": "Parental OA makes clam/scallop offspring more vulnerable",
        "species": "Argopecten irradians", "common_name": "bay scallop",
        "taxon_group": "bivalve", "taxon_class": "Bivalvia",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "gamete-broodstock",
        "life_stage_assayed": "veliger-larva",
        "priming_window_text": "adults under high vs low pCO2 during gametogenesis",
        "stressor_category": "OA-low-pH", "stressor_specific": "elevated pCO2 during gametogenesis",
        "dose_text": "high vs ambient pCO2", "environmentally_realistic": "yes",
        "assay_type": "survival",
        "outcome_metric": "larval vulnerability to low pH and additional stressors",
        "effect_direction": "costly", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "larvae", "persisted_past_metamorphosis": "not-tested",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "parental pCO2 x offspring pH x additional stressors",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY, "notes": "",
    },

    # ===== Putnam et al. 2015 — coral parental preconditioning =====
    {
        "record_id": "putnam2015-01", "study_key": "putnam2015",
        "doi": "10.1242/jeb.123018", "first_author": "Putnam", "year": 2015,
        "short_title": "Pocillopora parental temp+OA preconditioning and larval TGP",
        "species": "Pocillopora damicornis", "common_name": "cauliflower coral",
        "taxon_group": "coral", "taxon_class": "Anthozoa",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "maternal", "life_stage_primed": "adult",
        "life_stage_assayed": "veliger-larva",
        "priming_window_text": "adult exposure during larval brooding period",
        "stressor_category": "multiple",
        "stressor_specific": "elevated temperature + OA (28.9C, 805 uatm PCO2)",
        "dose_text": "28.9C + 805 uatm vs ambient 26.5C + 417 uatm",
        "environmentally_realistic": "yes",
        "assay_type": "physiology-other",
        "outcome_metric": "larval performance / parental-effects evidence under future climate",
        "effect_direction": "mixed", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "released larvae", "persisted_past_metamorphosis": "not-tested",
        "persistence_notes": "adult performance negatively affected; larvae show parental effects (TGP potential)",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "adult high vs ambient temp+OA during brooding; larval assays",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY, "notes": "",
    },

    # ===== Bellantuono et al. 2011 — coral thermal preconditioning =====
    {
        "record_id": "bellantuono2011-01", "study_key": "bellantuono2011",
        "doi": "10.1098/rspb.2011.1780", "first_author": "Bellantuono", "year": 2011,
        "short_title": "Short-term thermal preconditioning confers coral bleaching resistance",
        "species": "Acropora millepora", "common_name": "staghorn coral",
        "taxon_group": "coral", "taxon_class": "Anthozoa",
        "generation_primed": "F0", "generation_assayed": "F0",
        "transmission_channel": "somatic-within-gen", "life_stage_primed": "adult",
        "life_stage_assayed": "adult",
        "priming_window_text": "10-day preconditioning at 3C below bleaching threshold",
        "stressor_category": "thermal",
        "stressor_specific": "sub-bleaching thermal preconditioning",
        "dose_text": "temperature 3C below experimentally determined bleaching threshold",
        "exposure_duration_value": 10, "exposure_duration_unit": "days",
        "environmentally_realistic": "yes",
        "assay_type": "physiology-other",
        "outcome_metric": "symbiosis stability / bleaching resistance under subsequent thermal stress",
        "effect_direction": "beneficial", "effect_size_type": "NR", "significance": "sig",
        "persistence_value": 10, "persistence_unit": "days",
        "latest_timepoint_assayed": "adult under acute thermal stress",
        "persisted_past_metamorphosis": "NA",
        "persistence_notes": "within-generation acquired thermal tolerance; no symbiont community shift",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "short-term thermal preconditioning then heat challenge; symbiont/bacterial genotyping",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY,
        "notes": "restoration-relevant within-gen thermal hardening",
    },

    # ===== Clark et al. 2019 — urchin TGP transcriptome =====
    {
        "record_id": "clark2019-01", "study_key": "clark2019",
        "doi": "10.1038/s41598-018-37255-6", "first_author": "Clark", "year": 2019,
        "short_title": "Molecular mechanisms of low-pH TGP in green sea urchin",
        "species": "Psammechinus miliaris", "common_name": "green sea urchin",
        "taxon_group": "echinoderm", "taxon_class": "Echinoidea",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "adult",
        "life_stage_assayed": "embryo",
        "priming_window_text": "adult pre-acclimation to low pH; larvae spawned into low pH",
        "stressor_category": "OA-low-pH", "stressor_specific": "low pH adult preconditioning",
        "dose_text": "low pH vs ambient", "environmentally_realistic": "yes",
        "assay_type": "transcriptome",
        "outcome_metric": "larval RNA-seq; antioxidant pre-loading signature",
        "effect_direction": "beneficial", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "larvae under low pH", "persisted_past_metamorphosis": "not-tested",
        "persistence_notes": "adult conditioning pre-loads embryonic transcriptional pool with antioxidants",
        "methylation_measured": "no", "transcriptome_measured": "yes", "ncRNA_measured": "no",
        "study_design": "adult low-pH acclimation then offspring RNA-seq under low pH",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY, "notes": "",
    },

    # ===== Donelson et al. 2016 — reef fish warming TGP =====
    {
        "record_id": "donelson2016-01", "study_key": "donelson2016",
        "doi": "10.1111/eva.12386", "first_author": "Donelson", "year": 2016,
        "short_title": "Gradual warming across generations improves reproductive TGP",
        "species": "Acanthochromis polyacanthus", "common_name": "spiny chromis",
        "taxon_group": "fish", "taxon_class": "Actinopterygii",
        "generation_primed": "F0-F1", "generation_assayed": "F1",
        "transmission_channel": "biparental", "life_stage_primed": "whole-lifecycle",
        "life_stage_assayed": "adult",
        "priming_window_text": "+1.5C in F0 then +3.0C in F1 (gradual) vs abrupt warming",
        "stressor_category": "thermal", "stressor_specific": "ocean warming across generations",
        "dose_text": "+1.5C then +3.0C vs controls/abrupt", "environmentally_realistic": "yes",
        "assay_type": "reproduction",
        "outcome_metric": "reproductive output and offspring quality",
        "effect_direction": "beneficial", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "F1 adults / their offspring",
        "persisted_past_metamorphosis": "NA",
        "persistence_notes": "gradual warming over two generations yielded greater reproductive plasticity than abrupt",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "multi-generation thermal acclimation rate experiment",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY, "notes": "",
    },

    # ===== Shama et al. 2014 — stickleback maternal warming =====
    {
        "record_id": "shama2014-01", "study_key": "shama2014",
        "doi": "10.1111/1365-2435.12280", "first_author": "Shama", "year": 2014,
        "short_title": "Maternal TGP mediates stickleback offspring size under warming",
        "species": "Gasterosteus aculeatus", "common_name": "three-spined stickleback",
        "taxon_group": "fish", "taxon_class": "Actinopterygii",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "maternal", "life_stage_primed": "adult",
        "life_stage_assayed": "spat-juvenile",
        "priming_window_text": "maternal acclimation to 17C or 21C; offspring reared at matching/mismatching temps",
        "stressor_category": "thermal", "stressor_specific": "maternal warming acclimation",
        "dose_value": 21, "dose_unit": "degC",
        "dose_text": "maternal 17C vs 21C; offspring cross-factored",
        "environmentally_realistic": "yes",
        "assay_type": "growth-size",
        "outcome_metric": "offspring body size to 30 days (and beyond)",
        "effect_direction": "beneficial", "effect_size_type": "NR", "significance": "sig",
        "persistence_value": 30, "persistence_unit": "days",
        "latest_timepoint_assayed": "offspring >=30 days",
        "persisted_past_metamorphosis": "NA",
        "persistence_notes": "maternal TGP benefits on size stronger/longer under warmer conditions",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "TGP x quantitative genetics; mitochondrial respiration mechanism",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY, "notes": "marine stickleback population",
    },

    # ===== Marshall 2008 — bryozoan copper maternal effects =====
    {
        "record_id": "marshall2008-01", "study_key": "marshall2008",
        "doi": "10.1890/07-0449.1", "first_author": "Marshall", "year": 2008,
        "short_title": "Context-dependent maternal copper effects across life history",
        "species": "Bugula neritina", "common_name": "brown bryozoan",
        "taxon_group": "other", "taxon_class": "Gymnolaemata",
        "generation_primed": "F0", "generation_assayed": "F1",
        "transmission_channel": "maternal", "life_stage_primed": "adult",
        "life_stage_assayed": "whole-lifecycle",
        "priming_window_text": "maternal colonies exposed to copper pollution stress in lab",
        "stressor_category": "pollutant", "stressor_specific": "copper",
        "dose_text": "copper exposure of maternal colonies", "environmentally_realistic": "yes",
        "assay_type": "survival",
        "outcome_metric": "offspring performance across life-history stages (context-dependent)",
        "effect_direction": "mixed", "effect_size_type": "NR", "significance": "sig",
        "latest_timepoint_assayed": "multiple post-settlement stages",
        "persisted_past_metamorphosis": "yes",
        "persistence_notes": "maternal effects can increase performance in one stage and reduce it in another; assayed across life history incl. post-metamorphosis",
        "methylation_measured": "no", "transcriptome_measured": "no", "ncRNA_measured": "no",
        "study_design": "maternal copper exposure; offspring tracked across life history",
        "source_location": "abstract + OpenAlex", "extraction_confidence": "med",
        "extractor": EX, "extraction_date": TODAY,
        "notes": "classic marine TGP / maternal-effects paper; taxon_group=other (bryozoan)",
    },
]


def columns() -> list[str]:
    with open(VOCAB) as fh:
        return [c["name"] for c in yaml.safe_load(fh)["columns"]]


def main() -> int:
    cols = columns()
    existing_ids = set()
    rows = []
    if ATLAS.exists():
        with open(ATLAS, newline="") as fh:
            rows = list(csv.DictReader(fh))
            existing_ids = {r["record_id"] for r in rows}

    added = 0
    for row in NEW:
        if row["record_id"] in existing_ids:
            continue
        rows.append({c: row.get(c, "") for c in cols})
        added += 1

    with open(ATLAS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    print(f"appended {added} new contrasts; atlas now {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
