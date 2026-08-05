# Contributing

Thank you for helping maintain the Conditioning Atlas. Before changing data,
read [`README.md`](README.md) and [`SCHEMA.md`](SCHEMA.md). The schema and the
`rows_*.tsv` files are the source of truth; generated JSON, TSV, workbook, and
dashboard files should never be edited directly.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

LibreOffice is also needed to populate cached values for the workbook's
formulas. Install it with your system package manager, or open and save the
generated workbook once in Excel or LibreOffice.

## Making a change

1. Update the appropriate `rows_*.tsv`, `excluded_*.tsv`, `SCHEMA.md`, or
   `dashboard_template.html` source file.
2. Run the complete build:

   ```bash
   python3 scripts/merge_rows.py
   python3 scripts/build_xlsx.py
   python3 scripts/recalc_xlsx.py Conditioning_Atlas.xlsx
   python3 scripts/build_dashboard.py
   ```

3. Record data additions or corrections in `CHANGELOG.md`, including enough
   detail to explain why the change was made.
4. Review `git diff` and confirm that both dashboard outputs are identical:

   ```bash
   cmp Conditioning_Atlas_dashboard.html docs/index.html
   ```

5. Commit source changes together with their regenerated deliverables and open
   a pull request. The validation workflow must pass before merging.

Use a GitHub Issue to discuss schema changes or larger literature sweeps before
starting work, especially when they affect existing rows or inclusion criteria.

## Contribution license

By submitting a contribution, you agree that it may be distributed under the
repository's [Creative Commons Attribution 4.0 International License](LICENSE).
