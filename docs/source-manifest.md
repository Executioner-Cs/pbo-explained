# Source manifest

Exact versions of the source papers held locally for this project. One copy of each PDF is kept in the Git-ignored
`.local/literature/`. **None is redistributed.** No redistribution permission has been recorded for any of them;
unknown permission is treated as no permission. Obtain each paper from the link given, then compare SHA-256 to confirm
the same version.

Access levels follow the [literature review](literature-review.md): **Full** = full text read; **Selected pages** =
only the stated pages read. Sources cited in the paper without a local copy (for example White 2000, Hansen 2005,
Romano and Wolf 2005, Politis and Romano 1994) are listed there with their actual access level and are not held here.
Page-level checks of printed values are in [paper checks](paper-checks.md).

Paths are relative to `.local/literature/`. Hashes were computed from the files on 2026-11-13.

## Backtest overfitting (`backtest-overfitting/`)

| File | Authors, title, year | Version | DOI / acquisition | SHA-256 | Access and limits | Secondary topics |
|---|---|---|---|---|---|---|
| `backtest-overfitting/backtest-pseudo.pdf` | Bailey, Borwein, López de Prado, Zhu. "Pseudo-Mathematics and Financial Charlatanism." Notices AMS 61(5), 2014 | Author copy, 1 April 2014 | doi [10.1090/noti1105](https://doi.org/10.1090/noti1105); [author copy](https://www.davidhbailey.com/dhbpapers/backtest-pseudo.pdf) | `6e790c4185bf393272f89af5a2668b6b12203aa87fa7d5914fbeadc7c9ba0f3e` | Full. Author copy, not the typeset journal version | Expected maximum Sharpe (best-of-N), MinBTL |
| `backtest-overfitting/backtest-prob.pdf` | Bailey, Borwein, López de Prado, Zhu. "The Probability of Backtest Overfitting." J. Comput. Finance 20(4), 2017 | Author copy, 27 February 2015 | doi [10.21314/JCF.2016.322](https://doi.org/10.21314/JCF.2016.322); [author copy](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf) | `d8bfbadaaedb430d9dec929646d92f3580fdf18238f34121ae7738fa1c69a63d` | Full. Author copy predates the journal version | CSCV |
| `backtest-overfitting/deflated-sharpe.pdf` | Bailey, López de Prado. "The Deflated Sharpe Ratio." J. Portfolio Management 40(5), 2014 | Author copy, 31 July 2014 | doi [10.3905/jpm.2014.40.5.094](https://doi.org/10.3905/jpm.2014.40.5.094); [author copy](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf) | `ca4a1e834a2954b84eb560776e903329cd9cef318d458aadf6d67bc8166d10b5` | Full | Sharpe inference, multiple testing |
| `backtest-overfitting/lopez-de-prado-porcu-2026.pdf` | López de Prado, Porcu. Unified DSR framework (DSR-L, DSR-LS, DSR-EO). J. Portfolio Management 53(1), 2026 | SSRN 7198158, version of 24 August 2026; supplement 12 August 2026 | doi [10.3905/jpm.2026.070](https://doi.org/10.3905/jpm.2026.070) | `7786aab27ffc89fa9c66ee01de4ee2ac5febffa39b71b34647282bbefc34922e` | Full, read 2026-11-13. Supplementary proofs not checked. Its procedures were not tested in this study | Multiple testing, Sharpe inference |
| `backtest-overfitting/overfit-tools.pdf` | Bailey, Borwein, Salehipour, López de Prado, Zhu. "Online tools for demonstration of backtest overfitting." Report, 2015 | Dated 29 November 2015 | [author copy](https://www.davidhbailey.com/dhbpapers/overfit-tools.pdf) | `42cbced57a0b1d1ddf22ac9519587cf269dec40bec08609395fa27023bc45d1b` | Selected pages (p.2 only, in an earlier internal check). Not cited in the paper | None |

## Sharpe inference (`sharpe-inference/`)

| File | Authors, title, year | Version | DOI / acquisition | SHA-256 | Access and limits | Secondary topics |
|---|---|---|---|---|---|---|
| `sharpe-inference/sharpe-frontier.pdf` | Bailey, López de Prado. "The Sharpe Ratio Efficient Frontier." J. Risk 15(2), 2012 | Author copy, July 2012 | doi [10.21314/JOR.2012.255](https://doi.org/10.21314/JOR.2012.255); [author copy](https://www.davidhbailey.com/dhbpapers/sharpe-frontier.pdf) | `7a756315dc645e343f9b619a727adbd10fde7347af14ae7000bdf3c99397b0e5` | Full | PSR, MinTRL |
| `sharpe-inference/christie-2005.pdf` | Christie. "Is the Sharpe Ratio Useful in Asset Allocation?" MAFC working paper, 2005 | Working paper | doi [10.2139/ssrn.720801](https://doi.org/10.2139/ssrn.720801) (SSRN 720801) | `c20abab84fa9c7e5e6e5b09338ce20cf856c1a109cabfb62a8e0b5a67a5f6319` | Full | Serial dependence (GMM) |
| `sharpe-inference/opdyke-2007.pdf` | Opdyke. "Comparing Sharpe Ratios: So Where Are the p-Values?" J. Asset Management 8(5), 2007 | Preprint (SSRN 886728), not the journal version | doi [10.1057/palgrave.jam.2250084](https://doi.org/10.1057/palgrave.jam.2250084) | `5595798b92c9ca39335652a7b03bed59b4bd037cfc5004d911af5515138a8331` | Full (preprint) | Serial dependence |
| `sharpe-inference/lopez-de-prado-lipton-zoonekynd.pdf` | López de Prado, Lipton, Zoonekynd. "How to Use the Sharpe Ratio." J. Portfolio Management 52(6), 2026 | ADIA Lab Research Paper Series No. 19, 7 March 2026 (SSRN 5520741) | doi [10.3905/jpm.2026.1.837](https://doi.org/10.3905/jpm.2026.1.837) | `89d6a986441d8955ae4636a4bc051654fde013bc1a84b2ed006a8c870131a972` | Full (working-paper version), read 2026-11-13 | Serial dependence, DSR, effective trials |
| `sharpe-inference/lopez-de-prado-porcu-zoonekynd-engle-2026.pdf` | López de Prado, Porcu, Zoonekynd, Engle. Sharpe-ratio inference under GARCH(1,1), 2026 | Undated SSRN version | doi [10.2139/ssrn.6568702](https://doi.org/10.2139/ssrn.6568702) | `d1bc63828532d7c9901e5774b0ebb02bddba4e1085572f5d3ffd8a5c909692ac` | Full, read 2026-11-13. Proofs not checked | GARCH |

## Bootstrap and multiple testing

No local copies exist. The bootstrap and data-snooping references were used at metadata level or as standard method
descriptions; see the [literature review](literature-review.md) for the exact access level of each.
