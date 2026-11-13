# Literature review and novelty assessment

Access levels: **Full** = full text read by the project (local PDF in `.local/literature/` or hosted copy), with page-level
locators recorded in `docs/paper-checks.md` or `PROGRESS.md`. **Partial** = specific pages or sections read.
**Abstract** = abstract, index record or secondary description only. **Metadata** = bibliographic record only.
All DOIs, volumes and pages were checked against Crossref on 2026-11-12 unless noted.

## 1. Sources and what they establish

| Source | Access | Relevant content | Locator used |
|---|---|---|---|
| Bailey, Borwein, Lopez de Prado, Zhu (2014), Notices AMS 61(5) 458-471, doi 10.1090/noti1105 | Full (author copy 2014-04-01) | Expected max of N Normals (Prop 2.1, Eq 2.4); MinBTL (Thm 3.1, Eq 3.2) | pp.7-11 |
| Bailey, Borwein, Lopez de Prado, Zhu (2017), J. Comput. Finance 20(4), doi 10.21314/JCF.2016.322 | Full (author copy 2015-02-27) | CSCV Algorithm 2.3; PBO definition (Def 2.2, Sec 3.1); "customary" PBO <= 0.05; 12,780 typo | pp.9-14, 22 |
| Bailey, Lopez de Prado (2012), J. Risk 15(2) 3-44, doi 10.21314/JOR.2012.255 | Full (author copy July 2012) | PSR Eq 11, MinTRL Eq 13, variance Eq 8; claim of validity under stationary ergodic returns citing Opdyke | pp.4, 8-12 |
| Bailey, Lopez de Prado (2014), JPM 40(5) 94-107, doi 10.3905/jpm.2014.40.5.094 | Full (author copy 2014-07-31) | DSR Eq 2; implied N Eqs 8-9; "pointless" regime p.15 | pp.7-15 |
| Lo (2002), FAJ 58(4) 36-52, doi 10.2469/faj.v58.n4.2453 | Partial (pp.39-40, App. A p.47) | IID and GMM/HAC standard errors; annualization under autocorrelation | pp.39-40, 47 |
| Ledoit, Wolf (2008), JEF 15(5) 850-859, doi 10.1016/j.jempfin.2008.03.002 | Partial (Jan 2008 working paper) | Delta method Eqs 1-5; HAC; Remark 3.1 on Opdyke | pp.3-6, 11 |
| Opdyke (2007), J. Asset Mgmt 8(5) 308-336, doi 10.1057/palgrave.jam.2250084 | Full (preprint, local) | Equates Christie's closed form with Mertens'; claims validity under serial correlation | abstract p.1, p.4, fn 9 |
| Christie (2005), MAFC working paper, SSRN 720801 | Full (local) | GMM with autocorrelation-consistent S; lag-0 closed form (App. B) | pp.7, 10, 22-23, 33-35 |
| White (2000), Econometrica 68(5) 1097-1126, doi 10.1111/1468-0262.00152 | Metadata | Reality Check | none used |
| Hansen (2005), JBES 23(4) 365-380, doi 10.1198/073500105000000063 | Metadata; method as implemented | Consistent SPA, recentring g_c | none used |
| Sullivan, Timmermann, White (1999), JF 54(5) 1647-1691, doi 10.1111/0022-1082.00163 | Partial (hosted copy, conclusion read 2026-11-12) | Best DJIA rule survives Reality Check 1897-1986, not repeated 1987-1996 | p.37 |
| Romano, Wolf (2005), Econometrica 73(4) 1237-1282 | Metadata | StepM | none |
| Harvey, Liu, Zhu (2016), RFS 29(1) 5-68; Harvey, Liu (2014, 2015), JPM | Metadata | Multiple-testing haircuts | none |
| Politis, Romano (1994), JASA 89(428) 1303-1313 | Metadata; method as implemented | Stationary bootstrap | none |
| Politis, Romano (1992), circular block bootstrap, in LePage and Billard (eds) | Metadata NOT confirmed (no registry record found) | Circular block bootstrap | none |
| Kunsch (1989), Ann. Stat. 17(3) 1217-1241 | Metadata | Block bootstrap | none |
| Newey, West (1987, 1994) | Metadata | Bartlett HAC; lag rule | none |
| Kiefer, Vogelsang (2005); Politis, White (2004) | Metadata | Fixed-b HAC; automatic block length (cited as untried alternatives) | none |
| Jobson, Korkie (1981); Memmel (2003); Mertens (2002) | Metadata (Memmel, Mertens not verified) | IID Sharpe variance | none |
| Lo, MacKinlay (1988, 1990) | Metadata | Positive autocorrelation, nonsynchronous trading | none |
| Lopez de Prado, Lewis (2018), SSRN, doi 10.2139/ssrn.3167017 | Metadata | Effective trials by clustering | none |
| Lopez de Prado, Lipton, Zoonekynd (2026), JPM 52(6) 6-50, doi 10.3905/jpm.2026.1.837 | Full (working-paper version, ADIA Lab RPS No. 19, 7 March 2026, SSRN 5520741; local PDF read 2026-11-13) | Closed-form Sharpe variance for non-Normal AR(1) returns, factor (1+rho)/(1-rho) at SR = 0; DSR in location-and-scale form with Monte Carlo FWER check under serial correlation; effective trials by clustering or eigenvalues | Eq. 2 p.9; pp.4-6; Remarks 1-2 p.20; p.23; App. A.3 pp.40-41 |
| Lopez de Prado, Porcu (2026), JPM 53(1) 70-120, doi 10.3905/jpm.2026.070 | Full (SSRN 7198158, version of 24 August 2026, supplement 12 August 2026; local PDF read 2026-11-13; proofs not checked) | DSR-L / DSR-LS / DSR-EO; location-only analogue strongly conservative under independent Gaussian search (0.1643% at K = 100); Gumbel-reference LS rule asymptotically calibrated; independent-search results do not automatically extend to effective K | Exhibit 3 p.11; p.5 fn.1; Supplement App. B.5 |
| Lopez de Prado, Porcu, Zoonekynd, Engle (2026), SSRN, doi 10.2139/ssrn.6568702 | Full (undated SSRN version, local PDF read 2026-11-13; proofs not checked) | Sharpe variance under GARCH(1,1); clustering terms vanish when the mean is zero; root-n inference fails with infinite fourth moment | Props 4.7-4.8 pp.14-15; Sec. 5 |
| Pav (2021), CRC Press, doi 10.1201/9781003181057 | Metadata | Survey | none |

## 2. Comparison table

| Existing work | Established finding | Our replication | Our extension | Novelty limitation |
|---|---|---|---|---|
| Bailey and Lopez de Prado (2012) | PSR and MinTRL with skew/kurtosis under IID | All printed PSR and MinTRL examples | Zero-Sharpe PSR rejection rates under AR, GARCH, t, correlation | Only SR* = 0; GARCH/t cells are uninformative at SR* > 0 |
| Lo (2002); Ledoit and Wolf (2008) | IID Sharpe variance is wrong under serial dependence; Opdyke's time-series formulas reduce to IID | AR(1) rate 11.85% vs predicted 11.37% | Two-directional, period-dependent PSR error on daily industry data; block-bootstrap variance factor | Mechanism is textbook long-run variance; the real-data result is conditional on one history and fixed blocks |
| Bailey and Lopez de Prado (2014) | DSR location benchmark; implied N interpolation | Printed DSR and SR0 | Null rates of the operational procedure under AR, GARCH, t, correlation and 4 bootstrap designs; trial-count sensitivity | IID conservatism already shown by Lopez de Prado and Porcu (2026, Exhibit 3); 2026 recommends clustered effective trials, not Eq. 9; DSR-LS/EO not tested |
| Bailey et al. (2014, 2017) | Expected max approximation; MinBTL; PBO via CSCV | Printed constants; exact-quadrature check of Eq 2.4 | PBO under non-IID zero-edge nulls; mean PBO with a planted edge | Tie-free exchangeable nulls with independent halves imply mean 1/2; dependent halves only approximately follow this reference; power not measured |
| White (2000); Hansen (2005); Romano and Wolf (2005) | Search-aware benchmark tests | SPA implemented and applied | Juxtaposition of DSR 0.998 with SPA p 0.50 and power analysis | Standard method; one market and one rule family |
| Sullivan, Timmermann and White (1999); Brock et al. (1992) | MA rules on DJIA: in-sample superiority survives snooping adjustment, fails out of sample | Not replicated (different data) | MA rules on CRSP market factor, 1972-2026: no established standalone Sharpe superiority; baseline alpha is exploratory and execution-sensitive; walk-forward shortfall is within noise | Weaker in-sample evidence than STW; idealized execution |

## 3. Defensible contribution

1. A test-driven reimplementation with page-level provenance that reproduces the selected numerical examples listed in the paper, including one
   typographical error identified (12,780 vs 12,870) and the direction of the Eq 2.4 approximation error.
2. Quantified operating characteristics of the 2014 DSR as a decision rule under several null designs.
3. Evidence on real daily data that PSR's serial-dependence error depends on the period and can be below 5%, with a
   variance identity that checks the Normal approximation in both periods.
4. A worked contrast between a high selection-adjusted zero-skill statistic and a non-significant, low-power
   benchmark-relative test, with SPA and a walk-forward check.

Not defensible: a new statistic; first identification of the serial-correlation defect (Ledoit and Wolf 2008 and
Lo 2002 precede it); priority over Lopez de Prado and Porcu (2026) for DSR calibration findings; any trading edge.

## 4. Search limitations

No systematic database search (Scopus, Web of Science, SSRN full-text) was performed. Later literature was located
through Crossref bibliographic queries and web search on 2026-11-12. Papers that criticize SF's p.4 wording directly,
or that tabulate DSR null rates, may exist and were not found. The three 2026 Lopez de Prado papers were read in full on
2026-11-13 (versions above); their supplementary proofs were not checked.

## 5. Effect of the 2026 full texts on the contribution (2026-11-13)

| Manuscript claim | 2026 source | Consequence |
|---|---|---|
| AR(1) over-rejection of uncorrected PSR | Lopez de Prado, Lipton, Zoonekynd, Eq. 2: variance factor (1+rho)/(1-rho) at SR = 0 | Confirmation only; the parametric AR(1) correction is published and was not tested here |
| DSR far below 5% under IID search | Lopez de Prado and Porcu, Exhibit 3 (0.1643% at K = 100, location analogue) and App. B.5 | Confirmation for the operational 2014 procedure (0.05% [0.00, 0.28]); no priority |
| DSR acceptance rises with cross-strategy correlation; Eq. 9 interpolation | Lopez de Prado and Porcu, p.5 fn.1 (independent-search results do not extend automatically); LLZ App. A.3 (clustered effective K) | Still an extension, but about the 2014 interpolation that the 2026 papers no longer recommend |
| GARCH and Student-t leave zero-Sharpe PSR near 5% | Lopez de Prado et al. (GARCH), Props 4.7-4.8 | Consistent with theory; uninformative about SR* > 0 |
| PSR error on real daily data runs in both directions by period | none found | Remains the main empirical extension |
| DSR 0.998 against zero skill with distinct Sharpe/alpha conclusions | none found | Remains a worked illustration |

## 6. Access record for the 2026 papers

Read 2026-11-13 from owner-supplied PDFs in `.local/literature/` (not committed; third-party copyright). Supplementary proofs were
not checked.

| Paper | Version read | Local file SHA-256 |
|---|---|---|
| Lopez de Prado and Porcu, unified DSR framework (SSRN 7198158) | 24 August 2026; supplement 12 August 2026 | `7786aab27ffc89fa9c66ee01de4ee2ac5febffa39b71b34647282bbefc34922e` |
| Lopez de Prado, Lipton and Zoonekynd, "How to Use the Sharpe Ratio" (SSRN 5520741) | ADIA Lab Research Paper Series No. 19, 7 March 2026 | `89d6a986441d8955ae4636a4bc051654fde013bc1a84b2ed006a8c870131a972` |
| Lopez de Prado, Porcu, Zoonekynd and Engle, GARCH signal-to-noise inference (SSRN 6568702) | undated SSRN version | `d1bc63828532d7c9901e5774b0ebb02bddba4e1085572f5d3ffd8a5c909692ac` |
