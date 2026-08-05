# Changelog

Format: newest first. One entry per maintenance pass. See README.md § "Updating the
atlas" for what a normal entry should record.

## 2026-08-04 — Initial build

- First extraction sweep: 4 parallel literature pulls (bivalve temperature/pH,
  coral/cnidarian, immune priming, hypoxia/salinity/pollutant/other-taxa) against
  PubMed, Consensus, and Scite. 110 raw rows, 131 screened-out papers.
- Merged and deduplicated to 109 experiments from 105 papers (one exact duplicate
  dropped: `Donelan_2023` had been independently pulled into two sweeps).
- Verification pass: 6 high-leverage rows re-checked line-by-line against full
  text. Found and fixed:
  - `Drury_2022` — `effect_magnitude` quoted an ANOVA statistic (F=2.498, p=0.042)
    that the source paper itself attributes to initial pre-ramp Fv/Fm and explicitly
    discounts as driven by a single pairwise comparison. Replaced with the actual
    ED10 comparisons that support the paper's claim, and softened an internally
    false superlative in `notes` ("longest persistence in this set") that was
    contradicted by four other rows in the same file.
  - `Klepac_2020b` — `direction` was coded `No effect`; the source reports a
    significant chlorophyll decline in transplanted vs. native colonies, so this
    was revised to `Mixed`.
  - `Lafont_2017a` — `challenge` contained an unresolved `10^n` placeholder (a
    superscript exponent lost when PMC full text was converted to plain text).
    Replaced with an explicit note that the titre needs the original PDF rather
    than shipping a fabricated number.
  - Added a `PERSISTENCE SEMANTICS` caveat to `notes` on `Klepac_2020a`,
    `Klepac_2020b`, and `Uthicke_2024`: these rows report an exposure/tracking
    window under continuous or repeated conditioning, not a post-conditioning
    recovery gap, and should not be ranked against clean-gap rows like
    `Drury_2022` or `Lafont_2017a`.
  - Confirmed (not changed): the counterintuitive `Klepac_2020a` finding — the
    *most* thermally variable source pool producing the *most* bleaching-susceptible
    corals — is correctly transcribed, not inverted. Confirmed `Parker_2015`'s
    ~426-day persistence value is derived from the paper's own 14-month
    common-garden period. Confirmed no `persistence_days` value over 365 is a
    weeks-recorded-as-days unit error.
- Built `Conditioning_Atlas.xlsx` (5 sheets: README, Atlas, Coverage gaps, Data
  dictionary, Screened out) and `Conditioning_Atlas_dashboard.html` (filterable,
  6 filters, coverage heatmap, persistence strip plot).
- Reconstructed the ad hoc build steps into `scripts/merge_rows.py`,
  `scripts/build_xlsx.py`, `scripts/recalc_xlsx.py`, `scripts/build_dashboard.py`
  so the pipeline is re-runnable rather than one-off.
