"""Kenneth French daily data: 49 industry portfolios (step 4b) and market factors (step 5). Download once, check."""
import hashlib
import urllib.request
import zipfile
from pathlib import Path

import numpy as np

FTP = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
DATA = Path(__file__).resolve().parents[2] / "data"                  # git-ignored cache
INDUSTRIES = ("49_Industry_Portfolios_daily_CSV.zip", "b9d36d571e968d71f7b03207e7fed6398554f953719b8c1bf3ee3ad8d00e7520")
FACTORS = ("F-F_Research_Data_Factors_daily_CSV.zip", "96c23b88e651cbfff3740a53f8225e59ee39893371e96385a1d8125ec2cd9c89")
DOWNLOADED = "2026-11-12"                         # both frozen snapshots (202609 CRSP)
START, END = 19710701, 20260930                   # our choice: fixed window (YYYYMMDD), all 49 industries present

TABLE = "Average Value Weighted Returns -- Daily"


def parse_table(text):
    """Return (dates, values in percent) of the value-weighted daily table, the first in the file."""
    lines = text.splitlines()
    start = lines.index("  " + TABLE) + 2                  # skip the title and the column-name line
    end = lines.index("", start)                           # the table ends at the first blank line
    table = np.array([[float(v) for v in line.split(",")] for line in lines[start:end]])
    return table[:, 0].astype(int), table[:, 1:]


def prepare(dates, values, start, end):
    """Cut the window, reject bad values, convert percent to decimal, demean. Returns (dates, returns)."""
    if np.any(np.diff(dates) <= 0):
        raise ValueError("dates must be unique and increasing")
    keep = (dates >= start) & (dates <= end)
    dates, values = dates[keep], values[keep]
    if not np.isfinite(values).all() or (values <= -99.99).any():
        raise ValueError("missing-value markers (-99.99, -999) or non-finite values inside the window")
    returns = values / 100                                   # file is in percent
    return dates, returns - returns.mean(axis=0)             # zero average return for every industry


def ar_residuals(returns, order):
    """Per column: residuals of a least-squares AR(order) fit with intercept, demeaned (G2). Removes linear
    autocorrelation up to lag `order`; keeps everything else, e.g. volatility clustering. Our choice of method."""
    out = []
    for x in returns.T:
        lagged = np.column_stack([np.ones(len(x) - order)] + [x[order - k:len(x) - k] for k in range(1, order + 1)])
        coef, *_ = np.linalg.lstsq(lagged, x[order:], rcond=None)
        out.append(x[order:] - lagged @ coef)
    resid = np.column_stack(out)
    return resid - resid.mean(axis=0)


def read_snapshot(name, sha256):
    """Text of a frozen French zip: downloaded once to data/, then refused if its SHA-256 ever differs."""
    path = DATA / name
    if not path.exists():
        DATA.mkdir(exist_ok=True)
        part = path.with_suffix(".part")                     # an interrupted download never looks complete
        urllib.request.urlretrieve(FTP + name, part)
        part.replace(path)
    # Same bytes means same columns, dates and values. French revises history, so a new download must fail.
    if hashlib.sha256(path.read_bytes()).hexdigest() != sha256:
        raise ValueError(f"{name} is not the frozen snapshot (SHA-256 differs)")
    with zipfile.ZipFile(path) as z:
        return z.read(z.namelist()[0]).decode()


def load_returns():
    """49 industries: (dates, demeaned decimal returns, lines describing the data)."""
    text = read_snapshot(*INDUSTRIES)
    all_dates, values = parse_table(text)
    first, last = all_dates[0], all_dates[-1]
    dates, returns = prepare(all_dates, values, START, END)
    if returns.shape != (13929, 49) or dates[0] != START or dates[-1] != END:   # frozen schema (PROGRESS.md)
        raise ValueError(f"unexpected panel {returns.shape}, {dates[0]} to {dates[-1]}")
    facts = [
        f"Data: {FTP + INDUSTRIES[0]}",
        f"  downloaded {DOWNLOADED}, SHA-256 {INDUSTRIES[1]} (checked)",
        f"  table '{TABLE}' covers {first} to {last}; percent converted to decimal",
        f"  window {dates[0]} to {dates[-1]}: {returns.shape[0]} days x {returns.shape[1]} industries",
        "  no missing-value markers or non-finite values in the window; each industry demeaned",
    ]
    return dates, returns, facts


def load_market():
    """Market factors in the step 4 window: (dates, market excess return, risk-free rate), decimal, not demeaned."""
    rows = np.array([line.split(",") for line in read_snapshot(*FACTORS).splitlines() if line[:8].isdigit()], float)
    dates = rows[:, 0].astype(int)
    if np.any(np.diff(dates) <= 0):
        raise ValueError("dates must be unique and increasing")
    keep = (dates >= START) & (dates <= END)
    dates, mkt_rf, rf = dates[keep], rows[keep, 1] / 100, rows[keep, 4] / 100
    values = rows[keep, 1:]
    if dates[0] != START or dates[-1] != END or (values <= -99.99).any() or not np.isfinite(values).all():
        raise ValueError("unexpected window or missing values in the factors file")
    return dates, mkt_rf, rf
