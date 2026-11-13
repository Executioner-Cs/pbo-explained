# Release-candidate status

This package is a working-paper candidate, not an assertion of journal readiness or external peer review.

| Gate | Current evidence |
|---|---|
| Exact industry input recovery | Capture 20261113053423 independently retrieved; frozen SHA-256 matches |
| Exact factor input recovery | Capture 20261030074337 independently retrieved; frozen SHA-256 matches |
| Clean environment | New isolated virtual environment; 283 tests passed with 2 data skips, then all 285 passed with independently retrieved data |
| Full experiment reproduction | Running in the isolated candidate; final receipt will distinguish exact matches from historical exceptions |
| Three 2026 full texts | Not obtained: public SSRN delivery returns 403; no matching local PDFs found yet. Abstract/metadata scope remains explicit |
| Version of record | Candidate source and documentation versions will be recorded separately to avoid a self-referential commit hash |
| Public release decision | Prepare a draft release candidate; hold final publication approval until remaining source-review work is complete |

See data-recovery.json, full-text-access.json and reproducibility.md. Archival availability does not grant
permission to redistribute the raw inputs under the project's software licence. The ZIPs and third-party
paper PDFs are excluded from the release assets.
