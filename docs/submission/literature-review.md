# Literature review and novelty assessment

Access levels: **Full** = full text read by the project (local PDF in `papers/` or hosted copy), with page-level
locators recorded in `docs/paper_check.md` or `PROGRESS.md`. **Partial** = specific pages or sections read.
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
| Lopez de Prado, Lipton, Zoonekynd (2026), JPM 52(6) 6-50, doi 10.3905/jpm.2026.1.837 | Metadata | PSR/MinTRL/DSR as reporting standards | none |
| Lopez de Prado, Porcu (2026), JPM 53(1) 70-120, doi 10.3905/jpm.2026.070 | Abstract | DSR-L, DSR-LS, DSR-EO; calibration results linking approximation error to false-positive distortion | none |
| Lopez de Prado, Porcu, Zoonekynd, Engle (2026), SSRN, doi 10.2139/ssrn.6568702 | Metadata and secondary descriptions | Closed-form Sharpe inference under GARCH | none |
| Pav (2021), CRC Press, doi 10.1201/9781003181057 | Metadata | Survey | none |

## 2. Comparison table

| Existing work | Established finding | Our replication | Our extension | Novelty limitation |
|---|---|---|---|---|
| Bailey and Lopez de Prado (2012) | PSR and MinTRL with skew/kurtosis under IID | All printed PSR and MinTRL examples | Zero-Sharpe PSR rejection rates under AR, GARCH, t, correlation | Only SR* = 0; GARCH/t cells are uninformative at SR* > 0 |
| Lo (2002); Ledoit and Wolf (2008) | IID Sharpe variance is wrong under serial dependence; Opdyke's time-series formulas reduce to IID | AR(1) rate 11.85% vs predicted 11.37% | Two-directional, period-dependent PSR error on daily industry data; block-bootstrap variance factor | Mechanism is textbook long-run variance; the real-data result is conditional on one history and fixed blocks |
| Bailey and Lopez de Prado (2014) | DSR location benchmark; implied N interpolation | Printed DSR and SR0 | Null acceptance rates across 9 synthetic and 4 bootstrap designs; trial-count sensitivity | Lopez de Prado and Porcu (2026) derive general calibration results for DSR variants; not read beyond the abstract |
| Bailey et al. (2014, 2017) | Expected max approximation; MinBTL; PBO via CSCV | Printed constants; exact-quadrature check of Eq 2.4 | PBO under non-IID zero-edge nulls; mean PBO with a planted edge | Exchangeable nulls guarantee mean 1/2; power not measured |
| White (2000); Hansen (2005); Romano and Wolf (2005) | Search-aware benchmark tests | SPA implemented and applied | Juxtaposition of DSR 0.998 with SPA p 0.50 and power analysis | Standard method; one market and one rule family |
| Sullivan, Timmermann and White (1999); Brock et al. (1992) | MA rules on DJIA: in-sample superiority survives snooping adjustment, fails out of sample | Not replicated (different data) | MA rules on CRSP market factor, 1972-2026: no in-sample superiority; walk-forward shortfall | Weaker in-sample evidence than STW; idealized execution |

## 3. Defensible contribution

1. A test-driven reimplementation with page-level provenance that reproduces the selected numerical examples listed in the paper, including one
   typographical error identified (12,780 vs 12,870) and the direction of the Eq 2.4 approximation error.
2. Quantified operating characteristics of the 2014 DSR as a decision rule under several null designs.
3. Evidence on real daily data that PSR's serial-dependence error depends on the period and can be below 5%, with a
   variance approximation that predicts both periods.
4. A worked contrast between a high selection-adjusted zero-skill statistic and a non-significant, low-power
   benchmark-relative test, with SPA and a walk-forward check.

Not defensible: a new statistic; first identification of the serial-correlation defect (Ledoit and Wolf 2008 and
Lo 2002 precede it); priority over Lopez de Prado and Porcu (2026) for DSR calibration findings; any trading edge.

## 4. Search limitations

No systematic database search (Scopus, Web of Science, SSRN full-text) was performed. Later literature was located
through Crossref bibliographic queries and web search on 2026-11-12. Papers that criticize SF's p.4 wording directly,
or that tabulate DSR null rates, may exist and were not found. The three 2026 Lopez de Prado papers are the most
important unread sources.
