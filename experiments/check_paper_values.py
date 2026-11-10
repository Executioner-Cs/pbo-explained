"""Check that every constant in src/pbo/paper_values.py really appears on its cited PDF page.

Local only: needs the PDFs in papers/ (not in git). Exit code 1 if any check fails.
Run: .venv/Scripts/python.exe experiments/check_paper_values.py
"""
import pathlib
import sys
import unicodedata

from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pbo import paper_values as pv  # noqa: E402

PSEUDO, DSR, PBO = "backtest-pseudo.pdf", "deflated-sharpe.pdf", "backtest-prob.pdf"

# constant name -> (pdf, page, text that must appear on that page). Text is built from the constant, not retyped.
TEXT = {
    "EMAX_N": (PSEUDO, 9, f"N = {pv.EMAX_N} alternative"),
    "EMAX_N10": (PSEUDO, 9, f"Sharpe ratio IS of {pv.EMAX_N10}"),
    "MINBTL_YEARS": (PSEUDO, 11, f"only {pv.MINBTL_YEARS} years of data"),
    "MINBTL_MAX_N": (PSEUDO, 11, f"no more than {pv.MINBTL_MAX_N} independent"),
    "MINBTL_TARGET": (PSEUDO, 11, f"fixed at {pv.MINBTL_TARGET}. For instance"),
    "PERIODS_PER_YEAR": (DSR, 10, f"{pv.PERIODS_PER_YEAR} observations per year"),
    "PBO_RANK_EX_R_IS": (PBO, 9, str(pv.PBO_RANK_EX_R_IS)),
    "PBO_RANK_EX_RANK_IS": (PBO, 9, str(pv.PBO_RANK_EX_RANK_IS)),
    "PBO_RANK_EX_R_OOS": (PBO, 9, str(pv.PBO_RANK_EX_R_OOS)),
    "PBO_RANK_EX_RANK_OOS": (PBO, 9, str(pv.PBO_RANK_EX_RANK_OOS)),
    "PBO_S16": (PBO, 11, f"if S = {pv.PBO_S16}"),
    "PBO_S16_PRINTED": (PBO, 11, f"{pv.PBO_S16_PRINTED:,} combinations"),
    "PBO_EX_T": (PBO, 25, f"{pv.PBO_EX_T:,} daily prices"),
}

# Printed inside an equation image or a figure. Text extraction cannot see them. Checked by eye by Mayo on 2026-11-10.
MANUAL = {
    "DSR_EX_N": "DSR p.9, last line, and p.10 SR0 equation",
    "DSR_EX_V_ANNUAL": "DSR p.9, last line (printed as 1/2)",
    "DSR_EX_SR0": "DSR p.10, equation for SR0",
    "PBO_FIG1_S": "PBO p.13, Figure 1",
    "PBO_FIG1_SPLITS": "PBO p.13, Figure 1",
}

# Not quoted from a paper: tolerances and aliases.
DERIVED = {"EMAX_N10_TOL", "DSR_EX_SR0_TOL", "DSR_EX_PPY"}


def norm(s):
    # NFKC turns ligatures like "fi" into plain letters. Drop all whitespace: extraction spacing is unreliable.
    return "".join(unicodedata.normalize("NFKC", s).split())


pages = {}
failed = False
for name, (pdf, page, needle) in TEXT.items():
    key = (pdf, page)
    if key not in pages:
        pages[key] = norm(PdfReader(ROOT / "papers" / pdf, strict=False).pages[page - 1].extract_text())
    ok = norm(needle) in pages[key]
    failed |= not ok
    print(f"{'PASS' if ok else 'FAIL'}    {name:22s} {pdf} p.{page}: {needle!r}")

for name, where in MANUAL.items():
    print(f"MANUAL  {name:22s} {where} (checked by eye 2026-11-10)")

names = {n for n in vars(pv) if n.isupper()}
unknown = names - TEXT.keys() - MANUAL.keys() - DERIVED
for name in sorted(unknown):
    failed = True
    print(f"FAIL    {name:22s} not listed in this script. Add a check for it.")

print("SOME FAIL" if failed else "ALL TEXT CHECKS PASS")
sys.exit(1 if failed else 0)
