#!/usr/bin/env python3
"""
Recalculate formulas in an .xlsx file using headless LibreOffice.

openpyxl writes formulas as strings with no cached value — until something
recalculates the workbook, every formula cell (all of "Coverage gaps") reads
back as blank/None to pandas, openpyxl(data_only=True), and most previewers,
even though the formula is correct and will compute fine once opened by hand
in a real spreadsheet app. This script forces that computation via a small
LibreOffice macro (ThisComponent.calculateAll()) and rewrites the file in
place, so the delivered .xlsx already shows correct numbers everywhere.

Plain `soffice --convert-to xlsx` does NOT reliably force a full recalculation
of every formula — LibreOffice may just resave cached (blank) values — which is
why this script drives it through a macro instead.

Usage:
    python3 scripts/recalc_xlsx.py Conditioning_Atlas.xlsx [timeout_seconds]

Requires libreoffice/soffice on PATH (apt install libreoffice-calc, or
brew install --cask libreoffice on macOS). If soffice is not available, this
script exits non-zero with instructions rather than silently skipping —
opening the file in Excel or LibreOffice once by hand and saving it has the
same effect.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MACRO = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="Module1" script:language="StarBasic">
    Sub RecalculateAndSave()
      ThisComponent.calculateAll()
      ThisComponent.store()
      ThisComponent.close(True)
    End Sub
</script:module>"""


def find_soffice():
    for name in ("soffice", "libreoffice"):
        path = shutil.which(name)
        if path:
            return path
    return None


def recalc(xlsx_path, timeout=60):
    soffice = find_soffice()
    if not soffice:
        print(
            "No 'soffice' or 'libreoffice' binary found on PATH.\n"
            "Install LibreOffice (e.g. `apt install libreoffice-calc` or "
            "`brew install --cask libreoffice`), or simply open the workbook once in "
            "Excel/LibreOffice and save it — either recalculates every formula.",
            file=sys.stderr,
        )
        return 2

    xlsx_path = str(Path(xlsx_path).resolve())

    with tempfile.TemporaryDirectory() as tmp:
        profile_dir = Path(tmp) / "profile"
        profile_url = profile_dir.as_uri()

        # Step 1: launch once headless so LibreOffice creates the profile directory
        # (including user/basic/Standard), then install the recalculation macro into it.
        try:
            subprocess.run(
                [soffice, "--headless", "--terminate_after_init", f"-env:UserInstallation={profile_url}"],
                capture_output=True, timeout=min(timeout, 30),
            )
        except subprocess.TimeoutExpired:
            print("LibreOffice timed out creating its profile.", file=sys.stderr)
            return 3

        macro_dir = profile_dir / "user" / "basic" / "Standard"
        if not macro_dir.exists():
            print("LibreOffice did not create a usable profile directory.", file=sys.stderr)
            return 4
        (macro_dir / "Module1.xba").write_text(MACRO)

        # Step 2: open the file and invoke the macro, which recalculates every
        # formula and overwrites the file with cached values baked in.
        macro_uri = f"macro:///Standard.Module1.RecalculateAndSave"
        cmd = [
            soffice, "--headless", "--norestore",
            f"-env:UserInstallation={profile_url}",
            xlsx_path,
            f"vnd.sun.star.script:Standard.Module1.RecalculateAndSave?language=Basic&location=application",
        ]
        # The reliable invocation form varies by LibreOffice version; try the
        # documented one first, fall back to passing the macro as an argument.
        try:
            result = subprocess.run(
                [soffice, "--headless", "--norestore", f"-env:UserInstallation={profile_url}",
                 f"vnd.sun.star.script:Standard.Module1.RecalculateAndSave?language=Basic&location=application",
                 xlsx_path],
                capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            print(f"soffice did not finish within {timeout}s.", file=sys.stderr)
            return 5

        if result.returncode != 0:
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return result.returncode

    print(f"Recalculated and rewrote {xlsx_path}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/recalc_xlsx.py <path.xlsx> [timeout_seconds]", file=sys.stderr)
        sys.exit(1)
    t = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    sys.exit(recalc(sys.argv[1], t))
