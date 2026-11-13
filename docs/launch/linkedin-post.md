# LinkedIn launch copy

My backtest looked great. Then I made it defend itself.

93 moving-average rules. About 54 years of US market data.
The winner: Sharpe 0.588 versus the market's 0.458. Deflated Sharpe Ratio: 0.998.

That makes a pretty convincing screenshot.

So I kept going: account for the search, compare against the right benchmark, allow for dependence, and make execution a little less generous.

The Sharpe advantage wasn't statistically established. Market-alpha evidence looked borderline under the baseline assumptions. Add one extra day of execution delay and the search-aware alpha test gives p = 0.084.

That sensitivity became one of the most useful findings in the project.

I've written up a replication and empirical stress test of PSR, DSR and CSCV/PBO, with the code, fixed seeds, saved results and correction history available for inspection.

The question running through it: what does a strong backtest statistic actually establish?

One-page brief + full working paper + reproducible code:
https://github.com/Executioner-Cs/pbo-explained

Built on research by David H. Bailey, Marcos López de Prado and their collaborators. Working paper; not externally peer reviewed.

I'd love a skeptical read from people who build or evaluate systematic strategies. What's the first test you use to try to kill a promising backtest?

#QuantitativeFinance #Backtesting #QuantResearch

---

Attach `docs/submission/research-brief.pdf` to the LinkedIn post. Put the release link in the post or first comment for the full paper and downloads.

Optional direct-credit mention: Marcos Lopez de Prado — https://www.linkedin.com/in/lopezdeprado/ . Select the actual profile in LinkedIn when entering the mention; pasted text alone is not a verified tag. ADIA Lab is a relevant optional organization mention: https://www.linkedin.com/company/adia-lab/ . Neither mention implies collaboration, review or endorsement. Keep the focus on credit to the cited researchers; no firm relationship is claimed.
