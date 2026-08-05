# The Conditioning Atlas

Priming windows, doses, and persistence of induced environmental memory in
marine invertebrates. A structured, filterable extraction of the sublethal
environmental-conditioning / parental-priming literature — one row per
experiment, not per paper — built for the Roberts Lab's environmental memory
/ predictive phenotyping framework.

This directory is a **future standalone git repository**. It currently lives
inside a Cowork session working folder; everything below assumes it will be
`git init`'d and pushed somewhere durable (lab GitHub org, OSF, etc.) rather
than left in a session that eventually gets reclaimed. See
["Becoming its own repo"](#becoming-its-own-repo) for the concrete steps.

## What's here

| File | What it is | Edit by hand? |
|---|---|---|
| `SCHEMA.md` | The 27-column extraction schema, inclusion criteria, and field-by-field instructions. The contract every row must satisfy. | Yes — this is the spec |
| `rows_*.tsv` | Raw extracted rows, one file per literature sweep, 27 tab-separated fields, no header. **This is the actual source of truth.** | Yes — this is where new studies get added |
| `excluded_*.tsv` | Papers that were screened and rejected, with a one-line reason. Kept so screening is auditable and isn't repeated. | Yes |
| `merged.json` | All `rows_*.tsv` combined, deduplicated, as a JSON list. | **No — generated** by `scripts/merge_rows.py` |
| `conditioning_atlas.tsv` | Same data as `merged.json`, flat TSV with header. The single-file hand-off format. | **No — generated** |
| `Conditioning_Atlas.xlsx` | The lab-facing deliverable: Atlas sheet + live Coverage-gaps formulas + data dictionary + screened-out log. | **No — generated** |
| `dashboard_template.html` | The dashboard's actual HTML/CSS/JS, with `__DATA__` / `__FOOT__` placeholders. | Yes — this is where chart/filter/layout changes go |
| `Conditioning_Atlas_dashboard.html` | `dashboard_template.html` with data injected. Self-contained, opens in any browser. | **No — generated** |
| `CHANGELOG.md` | One entry per maintenance pass: what was added, what was corrected, and why. | Yes — append, don't rewrite history |
| `scripts/` | The four-step build pipeline (below). | Yes |

The rule of thumb: if a file's row above says "generated," don't hand-edit it —
your edit will be silently overwritten the next time someone runs the
pipeline. Fix the *source* (a `rows_*.tsv` line, or `dashboard_template.html`)
and regenerate.

## The pipeline

```
rows_*.tsv  ──┐
              ├──▶ scripts/merge_rows.py ──▶ merged.json, conditioning_atlas.tsv
excluded_*.tsv┘                                    │
                                                    ├──▶ scripts/build_xlsx.py ──▶ Conditioning_Atlas.xlsx
                                                    │        └──▶ scripts/recalc_xlsx.py (computes the formula sheet)
                                                    │
                                                    └──▶ scripts/build_dashboard.py ──▶ Conditioning_Atlas_dashboard.html
                                                              (combines with dashboard_template.html)
```

Run the whole thing after any change to `rows_*.tsv` or `excluded_*.tsv`:

```bash
python3 scripts/merge_rows.py
python3 scripts/build_xlsx.py
python3 scripts/recalc_xlsx.py Conditioning_Atlas.xlsx
python3 scripts/build_dashboard.py
```

Dependencies: `openpyxl` (`pip install openpyxl --break-system-packages` if
missing) and a LibreOffice install (`soffice`/`libreoffice` on PATH) for the
recalculation step — without it, the workbook still opens fine, but the
"Coverage gaps" sheet's formulas won't show cached values until you open and
save the file once yourself in Excel or LibreOffice.

## Updating the atlas

### Adding new studies (the common case)

1. Find the right `rows_*.tsv` file for the study's taxon/stressor (or start a
   new `rows_<topic>.tsv` if it's a genuinely new category — `merge_rows.py`
   picks up any `rows_*.tsv` file automatically; add its display name to the
   `cluster_name_from_filename()` map in `scripts/merge_rows.py` and the
   `labels` dict in `scripts/build_xlsx.py` so it gets a readable cluster/sweep
   label instead of falling back to the filename stem).
2. Re-read `SCHEMA.md` before extracting — the 27 fields, their allowed
   values, and the "never infer, `not reported` is a finding" rule are not
   optional. Pull full text where possible; abstracts routinely omit exposure
   duration and the persistence window, the two fields the whole atlas exists
   to capture.
3. Append one tab-separated line per **experiment** (a paper testing two
   stressors, or two species, is two rows — use an `a`/`b` suffix on the
   study_id, same DOI).
4. Check the new DOI for retractions/corrections (Scite `search_literature`
   with the DOI, no `term`, read `editorialNotices`) and record the result in
   column 26.
5. If a paper was found but didn't qualify, add it to the matching
   `excluded_*.tsv` instead, with a one-line reason — don't just drop it
   silently, the next person who finds it will re-do the work otherwise.
6. Run the four pipeline commands above. `merge_rows.py` will print a warning
   if your new DOI collides with an existing `study_id` (a real duplicate) or
   merely shares a DOI with a different `study_id` (expected when a paper has
   multiple experiments — just make sure that's actually true).
7. Add an entry to `CHANGELOG.md` (see format below) and re-send the two
   deliverables (`Conditioning_Atlas.xlsx`, `Conditioning_Atlas_dashboard.html`).

### Correcting an existing row

Never patch `merged.json`, `conditioning_atlas.tsv`, or the `.xlsx`/`.html`
outputs directly — `merge_rows.py` will blow away any such edit on the next
run, silently, because it rebuilds those files from `rows_*.tsv` every time.
**Fix the line in the source `rows_*.tsv` file**, then re-run the pipeline.
This bit the initial build once already (see `CHANGELOG.md`, 2026-08-04) — a
verification pass's corrections were applied to `merged.json` only, then lost
the next time the merge script ran. Don't repeat it.

### Periodic re-verification

This atlas was built by automated extraction against explicit inclusion
criteria, not as a registered systematic review — no PRISMA flow, no dual
independent extraction, no formal risk-of-bias assessment (see the workbook's
README sheet). Treat any given row as provisional until it's been checked
once against the primary source. A reasonable maintenance cadence:

- Before citing a specific row's numbers in a manuscript or grant, verify that
  row against the full text yourself — don't assume a prior extraction pass
  got it right.
- Periodically (e.g., quarterly, or whenever a new grant/manuscript draws on
  the atlas) spot-check a handful of high-leverage rows the way the
  2026-08-04 build did: pull full text, compare every quoted number and
  statistic, and check that a stated superlative ("longest," "first," "only
  study to...") isn't contradicted by another row in the same file.
- If you find an error, fix the `rows_*.tsv` source, note the correction in
  `CHANGELOG.md` with enough detail that someone can see *why* the old value
  was wrong (not just what the new value is), and regenerate.

### Extending the schema

If a new field is needed, add it to `SCHEMA.md` first (with its allowed
values), then to the `HDR` list in **all three** of `scripts/merge_rows.py`,
`scripts/build_xlsx.py`, and (if the dashboard should filter/display it)
`dashboard_template.html`. Every existing line in every `rows_*.tsv` needs a
value inserted at the new column position, in order — a length mismatch will
make `merge_rows.py` raise immediately (it validates field count per line), so
you'll find out fast if a file was missed.

## Becoming its own repo

To promote this from a session working folder into a real, durable repository:

1. `git init`, add a `.gitignore` for `__pycache__/`, `*.pyc`, and any local
   LibreOffice temp/profile directories.
2. Commit everything in this directory as the first commit. Suggested message:
   `Initial import: 109 experiments, 105 papers, verification pass complete`.
3. Add a `LICENSE` — check with the lab on preference (CC-BY-4.0 is a common
   choice for a data resource like this, MIT/Apache-2.0 if the scripts are the
   more reusable part).
4. Consider splitting `scripts/` dependencies into a `requirements.txt`
   (`openpyxl`) so a fresh clone's setup is `pip install -r requirements.txt`.
5. Optional CI (GitHub Actions or equivalent): on every push, run
   `scripts/merge_rows.py` and fail the build if it raises (catches field-count
   mismatches and schema drift before they reach `main`). A second job could
   run `scripts/build_xlsx.py` + `scripts/build_dashboard.py` and upload the
   two generated files as build artifacts, so there's always a downloadable
   up-to-date deliverable attached to the latest commit without checking
   generated binaries into git history.
6. Decide whether `Conditioning_Atlas.xlsx` and `Conditioning_Atlas_dashboard.html`
   themselves belong in version control. Two reasonable models:
   - **Generated-only artifacts**: `.gitignore` them, rebuild locally or via CI
     whenever needed. Keeps the repo's diff history clean (source rows only).
   - **Committed deliverables**: check them in so anyone can grab the latest
     without running Python, at the cost of noisy binary diffs on every
     regeneration. If you go this route, regenerate and commit them as a
     dedicated step, not bundled into an unrelated content commit.
7. Point new contributors at this README and `SCHEMA.md` as the two required
   reads before touching any `rows_*.tsv` file.
8. If the atlas grows enough to want issue tracking (e.g., "verify the
   remaining 100 rows," "add crustacean salinity studies"), GitHub Issues
   against this repo is a natural fit — the `excluded_*.tsv` reasons and the
   "Structural gaps" list on the workbook's Coverage-gaps sheet are a
   ready-made backlog.

## Provenance and known limitations

- Sourced from PubMed, Consensus, and Scite (full-text retrieval where
  available). Elicit's systematic-review pipeline was the original intended
  tool but requires a Pro-tier API plan not available at build time — if that
  changes, Elicit's screening/extraction stages could replace or supplement
  the current PubMed/Consensus/Scite sweep.
- Every included DOI was checked via Scite for retractions, corrections, and
  expressions of concern at the time of extraction; recheck periodically,
  since a clean result then doesn't guarantee one later.
- 34 of the original 109 rows are sourced from abstracts alone (see the
  `evidence_source` column) — verify against full text before citing.
- This is a lab working resource and the scaffold for a real systematic
  review, not a substitute for one.
