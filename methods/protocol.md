# Systematic Review Protocol — The Conditioning Atlas

A PRISMA-informed, reproducible protocol for assembling every priming / conditioning
experiment in the marine literature into the Conditioning Atlas. The atlas operationalizes
Section 6 of the lab conceptual framework — *"identify the windows, identify the doses, and
characterize how long the induced memory persists"* — at the grain of a single experimental
contrast.

## 1. Objective and review question

**Primary question.** Across marine organisms, in which life-stage / generation windows,
at which stressor doses, has sub-lethal conditioning been applied; what was the direction and
size of the induced phenotypic effect; and how long did it persist — in particular, did it
survive metamorphosis?

**Design-level question the atlas must answer instantly.**
> Has anyone primed at *this* stage in a bivalve, and did it stick past metamorphosis?

## 2. Scope (eligibility criteria)

**Population.** Marine animals (all phyla; bivalves and reef-building corals are the anchor
systems but the search is not restricted to them). Macroalgae included where an animal-style
conditioning design is used.

**Exposure / intervention.** A *deliberate, sub-lethal conditioning / priming manipulation* —
a defined stressor applied during a defined window (gamete/broodstock, embryo, larva, spat, or
adult) with the intent (or effect) of biasing a later phenotype. Includes within-generation
hardening/acclimatization and trans-/multi-generational priming.

**Comparator.** An unprimed / ambient control (or a dose gradient with a reference level).

**Outcomes.** Any organismal, physiological, or molecular readout measured *after* the
conditioning window: survival, growth, metamorphosis competency, calcification, immune
challenge, reproduction, behavior, DNA methylation, transcriptome, non-coding RNA.

### Inclusion
- Primary empirical study with a conditioning manipulation and a post-exposure readout.
- Marine or estuarine organism.
- Control or dose-reference present.

### Exclusion (with the reason codes used in `data/screening/screening.csv`)
- `review` — review, perspective, or opinion with no new primary experiment.
- `not-priming` — observational / correlational only; no deliberate conditioning manipulation
  (e.g. field population contrasts, reciprocal transplants of wild genotypes).
- `not-marine` — freshwater/terrestrial system.
- `no-control` — no comparator or dose reference.
- `lethal-only` — exposure is acute-lethal toxicology, not sub-lethal conditioning.
- `no-outcome` — no measured post-exposure phenotype/molecular readout.

## 3. Information sources

Scripted, re-runnable queries (no login) against:
- **OpenAlex** (`https://api.openalex.org/works`)
- **Europe PMC** (`https://www.ebi.ac.uk/europepmc/webservices/rest/search`)

Crossref / Semantic Scholar may be used later for DOI and metadata enrichment. Hand-known
anchors (the seven-paper foundational set) are entered directly into the screening log so the
review is auditable from a non-empty baseline.

## 4. Search strategy

The concept blocks combined by the search script (`scripts/01_search.py`):

- **Conditioning block:** priming OR conditioning OR "transgenerational plasticity" OR
  "carryover effect" OR "developmental programming" OR hardening OR acclimation OR
  acclimatization OR "parental effect" OR "epigenetic memory" OR preconditioning
- **Marine block:** marine OR ocean OR estuarine OR oyster OR mussel OR clam OR scallop OR
  coral OR abalone OR "sea urchin" OR bivalve OR mollusc
- **Mechanism/outcome sharpeners (optional):** methylation OR epigenetic OR metamorphosis OR
  larva OR broodstock OR resilience OR tolerance

The exact query strings and result counts are written to `data/search/` on each run so a
search is fully reproducible and datable.

## 5. Selection process

1. `scripts/01_search.py` retrieves records → `data/search/<source>_<date>.csv`.
2. `scripts/02_dedupe_screen.py` merges sources, deduplicates by DOI (then normalized title),
   and updates `data/screening/screening.csv`, **preserving existing human decisions** and
   marking new records `unscreened`.
3. A human screens title/abstract in `screening.csv`, setting `decision` to `include` /
   `exclude` (+`exclude_reason`). Included records get a `maps_to_study_key`.
4. `scripts/05_prisma.py` reads the screening log and emits `data/screening/prisma_counts.csv`
   and a PRISMA flow diagram (`docs/prisma.svg`).

## 6. Data extraction

Included full texts are extracted into `data/atlas.csv` at **one row per experimental
contrast**, following [`data/schema/data_dictionary.md`](../data/schema/data_dictionary.md)
and the controlled vocabulary in
[`data/schema/controlled_vocab.yaml`](../data/schema/controlled_vocab.yaml). Every row records
provenance (`source_location`) and `extraction_confidence`. `scripts/04_validate_schema.py`
enforces the schema; `scripts/build.sh` regenerates the spreadsheet and dashboard data.

## 7. Data items

See the data dictionary. The load-bearing items for the framework's Section 6 program are:
`life_stage_primed`, `generation_primed` / `generation_assayed`, `stressor_category` + dose,
`exposure_duration_*`, `effect_direction` + `effect_size_*`, `persistence_*`,
`persisted_past_metamorphosis`, and `methylation_measured`.

## 8. Reproducibility

- `pip install -r requirements.txt`
- `scripts/01_search.py` → `scripts/02_dedupe_screen.py` → screen → extract → `scripts/build.sh`
- All intermediate artifacts are committed (except large raw API dumps, see `.gitignore`).
