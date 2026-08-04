# Conditioning Atlas — Data Dictionary

The machine-readable contract lives in [`controlled_vocab.yaml`](controlled_vocab.yaml).
This document is the human-facing companion. If the two ever disagree, the YAML wins —
the validator (`scripts/04_validate_schema.py`), the spreadsheet builder
(`scripts/03_build_xlsx.py`), and the dashboard (`docs/atlas.js`) all read the YAML.

## The unit of a row

**One row = one experimental contrast.** A contrast is a single combination of
`stressor × dose × generation × assay × outcome`. A study that primes at two doses,
tracks two generations, and runs three assays produces up to `2 × 2 × 3` rows. This is
deliberate: Section 6 of the lab framework asks us to *"identify the windows, identify the
doses, and characterize persistence"*, and none of those are answerable at paper
granularity.

`NA` (not applicable) and `NR` (not reported) are accepted in any field. Prefer `NR` when
the study could have reported a value but did not; prefer `NA` when the field is
structurally meaningless for that row (e.g. metamorphosis persistence for an adult coral).

## Columns

### Identity
| column | type | required | notes |
|---|---|---|---|
| `record_id` | string | yes | Unique row id, e.g. `soldourdin2024-01` |
| `study_key` | string | yes | Author+year, shared across a study's rows |
| `doi` | string | no | Bare DOI, no `https://doi.org/` prefix |
| `first_author` | string | yes | First author surname |
| `year` | int | yes | Publication year |
| `short_title` | string | no | Short human-readable title |

### Organism
| column | type | required | allowed |
|---|---|---|---|
| `species` | string | yes | Latin binomial |
| `common_name` | string | no | |
| `taxon_group` | enum | yes | bivalve, coral, fish, gastropod, crustacean, echinoderm, cephalopod, macroalgae, other |
| `taxon_class` | string | no | e.g. Bivalvia, Anthozoa |

### Priming design
| column | type | required | allowed |
|---|---|---|---|
| `generation_primed` | enum | yes | F0, F1, F2, F0-F1, F0-F1-F2, multi |
| `generation_assayed` | enum | yes | F0, F1, F2, F0-F1, F0-F1-F2, multi |
| `transmission_channel` | enum | yes | maternal, paternal, biparental, somatic-within-gen, unclear |
| `life_stage_primed` | enum | yes | gamete-broodstock, embryo, veliger-larva, pediveliger-larva, spat-juvenile, adult, whole-lifecycle |
| `life_stage_assayed` | enum | yes | embryo, veliger-larva, pediveliger-larva, spat-juvenile, adult, whole-lifecycle |
| `priming_window_text` | string | no | Free-text exposure window |

### Stressor / dose
| column | type | required | allowed / notes |
|---|---|---|---|
| `stressor_category` | enum | yes | thermal, OA-low-pH, hypoxia, salinity, pathogen-immune, pollutant, nutrition, UV, multiple, other |
| `stressor_specific` | string | yes | Specific agent, e.g. `poly(I:C)`, `18-pesticide mixture`, `+4C` |
| `dose_value` | float | no | Numeric dose if scalar |
| `dose_unit` | string | no | e.g. `ug/L`, `pH`, `degC`, `ppt` |
| `dose_text` | string | no | Dose when non-scalar / multi-level |
| `exposure_duration_value` | float | no | |
| `exposure_duration_unit` | enum | no | hours, days, weeks, months, years |
| `environmentally_realistic` | enum | no | yes, no, unclear |

### Outcome / assay
| column | type | required | allowed / notes |
|---|---|---|---|
| `assay_type` | enum | yes | survival, growth-size, metamorphosis-competency, calcification, immune-challenge, methylation, transcriptome, lncRNA, reproduction, physiology-other, behavior |
| `outcome_metric` | string | yes | Specific metric, e.g. `% metamorphosed` |
| `effect_direction` | enum | yes | beneficial, costly, none, mixed (primed vs control) |
| `effect_size_value` | float | no | |
| `effect_size_type` | enum | no | percent-change, cohens-d, log2FC, survival-diff, odds-ratio, correlation, hedges-g, other, NR |
| `significance` | enum | yes | sig, ns, NR |

### Persistence (the Section-6 payload)
| column | type | required | allowed / notes |
|---|---|---|---|
| `persistence_value` | float | no | Time from priming to last observation of the effect |
| `persistence_unit` | enum | no | hours, days, weeks, months, years, generations |
| `latest_timepoint_assayed` | string | no | Latest stage/time checked |
| `persisted_past_metamorphosis` | enum | yes | yes, no, not-tested, NA |
| `persistence_notes` | string | no | Decay / persistence free text |

### Molecular
| column | type | required | allowed |
|---|---|---|---|
| `methylation_measured` | enum | yes | yes, no |
| `methylation_method` | enum | no | WGBS, RRBS-Methyl-seq, MBD-seq, amplicon-BS, EPIC-array, other, NA |
| `transcriptome_measured` | enum | no | yes, no |
| `ncRNA_measured` | enum | no | yes, no |

### Provenance
| column | type | required | allowed / notes |
|---|---|---|---|
| `study_design` | string | no | e.g. `full-factorial F0xF1` |
| `sample_size` | string | no | n / replication |
| `source_location` | string | no | Page/figure/table |
| `extraction_confidence` | enum | yes | high, med, low |
| `extractor` | string | yes | Who/what extracted the row |
| `extraction_date` | string | yes | YYYY-MM-DD |
| `notes` | string | no | |

## The flagship query

> *"Has anyone primed at this stage in a bivalve, and did it stick past metamorphosis?"*

is answered by three columns with zero interpretation:

```
taxon_group == "bivalve"
AND life_stage_primed == <stage of interest>
AND persisted_past_metamorphosis IN ("yes", "no")   # i.e. it was actually tested
```

The dashboard ships this as a one-click preset.
