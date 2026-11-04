---
title: Data Analysis 9-10 — Descriptive Analysis (caso Etiopia)
date: 2026-10-09
session: 9
wispr: https://notes.wisprflow.ai/shared/Msyom_F0qStmIgsomQ6uwMLNxPR-DlpcAJV7-r1Ufgg
---
Descriptive analysis for econometrics: distributions, central tendency, dispersion, outliers, correlation, and common pitfalls, illustrated with an Ethiopia technology-adoption study.

### Course Format and Exam
- **Exam questions will focus on theory covered in the first part of each session and on the slides.**
- Second part of each session uses a continuing case developed across classes with different methodologies.
- Project must show descriptive patterns and key variable distributions before any regression.

### Distributions and Summary Metrics
- Descriptive analysis summarizes central tendency, variability, and correlations; it is the first step of any analysis.
- Distribution types: normal, skewed (e.g. funding is right skewed), uniform, and bimodal (signals subgroups).
    - Mean below median in negative skew, above in positive skew; gap signals outliers
- Rule of thumb: need more than 100 observations for a simple linear regression.
- No variability means no information: regressions cannot uncover relationships without variation in X or Y.
    - Highly skewed variables can be log-transformed to plot more readably

### Outliers and Use of AI Tools
- Outliers can be data errors (e.g. negative R&D), rare real phenomena, or data manipulation and fabrication.
- Dropping or recoding outliers is an assumption that must be justified; dropping top-funded firms distorts results.
- Scatter plots reveal outliers better than histograms.
- Students must be able to verify and correct AI analysis; undeclared fabricated data is an ethical and legal issue.

### Correlation and Common Mistakes
- Correlation can be positive, negative, or none; only statistically significant correlations are credible.
- Cross-tabulation example: most tech startups founded by males, with variation by industry.
- Pitfalls: truncated axes, outlier-driven analysis, pie charts not summing to 100, and **confusing correlation with causality**.

### Ethiopia Technology Adoption Case
- UN-funded panel of about 1,000 rural households in Ethiopia, surveyed every two years from 2013 to 2021.
- 65% adopted new technologies, but mostly crop changes; water harvesting adoption was below 5%.
- Newborn gender acted as a natural experiment: families with sons were about 3 to 3.5% more likely to adopt.
- Mechanism: daughters expected to marry and relocate, so families avoided long-term investments without a male heir.
