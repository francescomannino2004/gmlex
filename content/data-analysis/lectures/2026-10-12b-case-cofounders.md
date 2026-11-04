---
title: Data Analysis 12-10 — Caso: numero di co-founder e fondi raccolti
date: 2026-10-12
session: 10
wispr: https://notes.wisprflow.ai/shared/nRA1rRcqfv760NHURKcKtzjnLIjPKRXJkADqVk6h5ME
---
Class review of the co-founder team-size case: the founders effect on total raised is significant but explains little variation, and employees and deals are bad regressors to exclude.

### Case Goal and Sample
- Question: recommend a formal team-size bonus, no formal role, or a weak secondary role for applicants with more founders
- Co-founders lost significance once many other factors were added
- Sample limited to accelerator startups; about 1,507 observations after missings

### Theoretical Expectations
- Expected positive effect: more founders bring heterogeneous skills and competencies
- But theory is ambiguous: coordination, communication and conflict costs offset the benefits; data decides which dominates

### Simple Regression Results
- Intercept about 4.1 million: predicted funding for a startup with 0 founders
- Each additional founder raises average total raised by about 7.04 million, p-value 0.001, significant at 1%
- **R-squared is very low (about 0.88%)**: founders are significant but explain little of funding variation
- Estimates must report robust standard errors

### Multiple Regression and Controls
- Adding years since 2012 leaves the founders coefficient stable; its own coefficient is about −4
    - Likely captures liability of youth: younger firms had less time to raise money
- Toggling regressors on/off is normally the golden rule, but here employees and deals are **bad controls**:
    - Employees likely measured after funding: **reverse causality**
    - Deals determined simultaneously with total raised: **simultaneity bias**
