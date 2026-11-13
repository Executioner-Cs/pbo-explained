# Frozen input manifest

Source of truth for archive names and expected hashes: `src/pbo/french.py`. This manifest describes the
snapshots used in the saved results; it does not provide an immutable download service.

## Snapshot identity

RECOMPUTED repository record: both archives were downloaded on 2026-11-12 and identify the 202609 CRSP release.
Store the original ZIP bytes under the repository's ignored `data/` directory.

| Input | Local archive | SHA-256 |
|---|---|---|
| French 49 Industry Portfolios, daily | `data/49_Industry_Portfolios_daily_CSV.zip` | `b9d36d571e968d71f7b03207e7fed6398554f953719b8c1bf3ee3ad8d00e7520` |
| Fama/French research factors, daily | `data/F-F_Research_Data_Factors_daily_CSV.zip` | `96c23b88e651cbfff3740a53f8225e59ee39893371e96385a1d8125ec2cd9c89` |

Original acquisition endpoints (rolling, not immutable):

- [Daily 49-industry ZIP](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_daily_CSV.zip).
- [Daily factor ZIP](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip).
- [Official data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).
- [Official factor construction](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html).

The exact archive hashes, not just their calendar endpoints, identify the inputs. A newly downloaded archive
can contain revised history even when overlapping dates appear unchanged. The loader refuses a mismatch;
changing its expected hash would define a new dataset and would require a new provenance record and rerun.

## Windows and transformations

The following are RECOMPUTED dataset dimensions or recorded modeling choices, not paper-derived constants.

- Common source window: 1971-07-01 through 2026-09-30, inclusive; 13,929 daily observations.
- Industry panel: 49 columns from `Average Value Weighted Returns -- Daily`. Values are converted from percent
  to decimal and each column is demeaned over the full source window for the full-window zero-edge bootstrap.
- Corrected G6: split at 1999-01-01, then demean each industry separately within each period. Full-window
  demeaning alone does not impose a zero mean within those periods. The original uncentered G6 output is
  historical evidence with its earlier calibration interpretation withdrawn.
- Market panel: `Mkt-RF` and `RF`, converted from percent to decimal and not demeaned. The MA signal uses the
  compounded total-return research index from `Mkt-RF + RF`; strategy performance is measured in excess returns.
- MA evaluation: the longest slow window is removed and leading rows are trimmed to complete CSCV blocks.
  The saved evaluation spans 1972-07-18 through 2026-09-30, with 13,664 observations. Positions and turnover
  costs are calculated before trimming. This is an idealized factor-index experiment, not an identified
  executable instrument with demonstrated real-time fills.
- Loaders check archive SHA-256, increasing dates, window/schema, and missing/nonfinite values. Tests and code
  provide the exact conditions; this is not a claim to audit every original vendor data construction step.

## Reproduction status

Both exact ZIPs have timestamped recovery routes independently downloaded and verified on 2026-11-13 UTC:

- [Industry capture, 20261113053423](https://web.archive.org/web/20261113053423id_/https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_daily_CSV.zip).
- [Factor capture, 20261030074337](https://web.archive.org/web/20261030074337id_/https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip).

The industry capture was requested for the existing public provider URL under the owner's preservation request.
Both returned ZIPs match the hashes and byte lengths listed in [reproducibility.md](reproducibility.md).
This establishes verified retrieval at that time, not perpetual availability or data redistribution rights.
The ZIPs remain excluded from Git and from the software licence. A fresh-environment reproduction record is
maintained in docs/reproducibility.md; keep identity verification separate from execution evidence.

The manuscript's paper PDFs are also excluded from Git. References and the page-check record document their
identity and verification scope; local PDF availability should not be confused with immutable data provisioning.
