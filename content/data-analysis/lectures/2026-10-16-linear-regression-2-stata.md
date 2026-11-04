---
title: Data Analysis 16-10 — Linear regression (2): log, quadratici, interazioni + Stata
date: 2026-10-16
session: 11
wispr: https://notes.wisprflow.ai/shared/QAs3R5fhN0wN5igojMSVKCv9y572wrtpP-b4XCjzSqM
---
Modeling nonlinearities (logs, quadratic terms) and interaction terms, followed by a Stata crash course on the PitchBook startup database.

### Using AI Coding Tools
- Don't fully outsource analysis to AI; use it alongside Stata for support and validation.
- In a past exercise an AI tool silently cut about 300 observations, invalidating a student's regressions.
    - Always check observation counts and be able to trace each step of the code

### Logarithmic Transformations
- Nonlinearities are added via variable transformations or extra terms, keeping the model linear in parameters.
- **Interpretation: log-log = elasticity (% change in y for 1% change in x); log-level: multiply β by 100 (% change in y for a unit change in x); level-log: divide β by 100 (unit change in y for 1% change in x).**
    - Example: level-log food model coefficient 132 means 1% more income adds about 1.32 in food spending
- Use logs for skewed continuous or many-valued integer variables; avoid for few-value units, percentages, negatives.
    - With meaningful zeros (e.g. total raised), use log(1 + x)
- **Interpretation of transformed coefficients will be on the exam**; always use the natural log.

### Quadratic and Interaction Terms
- Quadratic terms test U-shaped or inverted U-shaped relations; the linear term must always be included.
    - Turning point: x* = −β1 / (2·β2)
- Housing price vs. square meters is usually U-shaped in data, driven by the luxury segment after the turning point.
- Interaction terms test moderation by a third variable; baseline variables must stay in the regression.
- With an interaction, each baseline coefficient is the effect when the other interacted variable equals zero.
    - Wage example: education 9.4%, experience 0.6%, negative interaction term

### Stata Crash Course (PitchBook Database)
- Data checks: describe, count, list, codebook, duplicates, tabulate with missing; company ID has no missings or duplicates.
    - Accelerator dummy missings recoded to 0, keeping about 57,000 firms instead of 22,000
- Descriptives: summarize (detail), bysort, histograms, kernel density, box plots, scatter plots, encode, bar and pie charts.
- Regressions: robust SE, estimates store, residual plots, test, log specs, quadratic turning point, margins.
    - Use `##` to include interaction plus baseline terms automatically; `#` adds only the interaction
