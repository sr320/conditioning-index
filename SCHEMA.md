# Conditioning Atlas — extraction schema

One row per **experiment** (not per paper). If a paper runs two stressors or two
species in separate experiments, emit two rows with the same DOI.

Output format: **tab-separated**, no header row (the merge step adds it), one row
per line, exactly 27 fields in this order. Never use a literal tab inside a
field. Use `; ` to separate items within a field. Use `not reported` when the
source does not state it. **Never infer or estimate a value the source does not
give** — `not reported` is a finding, not a failure.

| # | field | allowed values / format |
|---|-------|------------------------|
| 1 | study_id | `Lastname_Year` (e.g. `Wang_2023`); add `a`/`b` suffix if two rows from same first author + year differ |
| 2 | doi | bare DOI, no `https://` prefix. `not reported` only if truly absent |
| 3 | pmid | PubMed ID, or `not reported` |
| 4 | year | publication year |
| 5 | species | full Latin binomial(s) |
| 6 | taxon | `Bivalve` \| `Coral/cnidarian` \| `Gastropod` \| `Echinoderm` \| `Crustacean` \| `Polychaete/other` \| `Multiple` |
| 7 | stressor | free text, specific (e.g. `elevated temperature`, `reduced pH (elevated pCO2)`, `poly(I:C)`, `18-pesticide mixture`) |
| 8 | stressor_category | `Temperature` \| `pH/OA` \| `Hypoxia` \| `Salinity` \| `Pollutant` \| `Pathogen/immune` \| `Multiple` |
| 9 | conditioning_stage | `Broodstock/adult` \| `Gamete` \| `Embryo` \| `Larva` \| `Juvenile` \| `Multiple` — the stage the PRIMING exposure was applied to |
| 10 | dose_treatment | quantitative, WITH the control value. e.g. `pH 7.4 vs control pH 8.0`; `18 C (MHW) vs 13 C`; `2.85 ug/L nominal sum` |
| 11 | duration | conditioning exposure length with units; describe cycling regimes (e.g. `diel 3 C fluctuation, 28 d`) |
| 12 | generations | `F0` \| `F0-F1` \| `F0-F1-F2` \| `F1 only` etc., using the paper's labels |
| 13 | transmission | `Maternal` \| `Paternal` \| `Both parents` \| `Route not resolved` \| `Within-generation only` |
| 14 | challenge | the later stress the conditioned animals (or offspring) were tested against; `none (baseline only)` if no challenge |
| 15 | persistence_days | numeric days from END of conditioning to the assessment/challenge; `not reported` if unstated. Prefix `~` if approximate from the paper's own numbers |
| 16 | multiple_timepoints | `Yes` \| `No` — did the paper assess at more than one post-conditioning time? |
| 17 | decay | `Persisted` \| `Decayed` \| `Strengthened` \| `Not tested` |
| 18 | readouts | organismal/physiological outcomes measured |
| 19 | direction | `Improved` \| `No effect` \| `Worsened` \| `Mixed` \| `Not assessable` — effect of conditioning on performance under challenge vs naive controls |
| 20 | effect_magnitude | quoted numbers with statistic (e.g. `larval arm length -21.4%`; `LT50 +1.2 C, p<0.05`) |
| 21 | molecular_layers | `Methylation (WGBS)` \| `Methylation (methylRAD)` \| `Methylation (MBD-BS)` \| `Transcriptome (RNA-seq)` \| `Targeted qPCR` \| `ncRNA` \| `Chromatin` \| `None`; combine with `; ` |
| 22 | concordance | `Concordant` \| `Discordant` \| `Partial` \| `Not evaluated`; append any quantitative overlap (e.g. `Partial (42.8% of F0 DMGs retained to F2)`) |
| 23 | applied_framing | `Aquaculture` \| `Restoration` \| `Both` \| `Biomonitoring` \| `None` |
| 24 | replication | tanks/biological replicates per treatment; n families; n individuals |
| 25 | evidence_source | `Abstract only` \| `Full text` \| `Abstract + citations` |
| 26 | editorial_notice | `None found` \| `Retracted` \| `Correction` \| `Concern` \| `Not checked` |
| 27 | notes | anything a lab would want flagged — caveats, trade-offs, mismatch/maladaptive findings, why a field is unreported |

## Inclusion criteria (all must hold)

1. Marine or estuarine **invertebrate** (bivalve, coral/cnidarian, gastropod,
   echinoderm, crustacean, polychaete, bryozoan). Exclude fish, freshwater-only,
   terrestrial, cell-culture-only.
2. A deliberate **sublethal / sub-optimal / priming exposure** applied before a
   later assessment. Natural-history contrasts (e.g. intertidal vs subtidal
   provenance carried into common garden) DO count — tag them in notes as
   `natural conditioning contrast`.
3. A **later-life or offspring outcome** is measured (performance and/or
   molecular).
4. **Primary empirical study.** Exclude reviews, meta-analyses, perspectives,
   methods-only papers.

Studies that fail criteria go in a separate `excluded` file with a one-line reason.

## Priority fields

`persistence_days`, `multiple_timepoints`, `decay`, `dose_treatment`, and
`concordance` are the point of the whole exercise. Spend your effort there.
Where a paper is open access, pull the full text (PubMed `get_full_text_article`
with the PMC ID, or Scite `search_literature` with the DOI plus a `term` like
"exposure duration temperature control") rather than guessing from the abstract.
