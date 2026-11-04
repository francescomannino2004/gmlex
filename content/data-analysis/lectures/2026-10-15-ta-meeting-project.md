---
title: Data Analysis 15-10 — 2° TA meeting progetto (syndication e failure)
date: 2026-10-15
session: project
wispr: https://notes.wisprflow.ai/shared/wLIahloStk6b0AoTuVOfpm5-aJfaXUuvJlI0sRoig8U
---
TA check-in on the group's VC syndication project: the research question was reframed around startup survival, and the TA gave guidance on round comparison, failure definition, missing data, and dataset construction.

### Research Question
- Question: among VC-backed US startups, is syndicate size (number of investors) related to failure after early rounds?
- "Risk perception" is unmeasurable; reframe as startup survival or likelihood of going out of business.

### Comparing Financing Rounds
- Compare startups by deal type stage (Seed, early, later), not by chronological round number.
    - PitchBook only records raises above about 10k, so earlier rounds may be missing
- Syndication expected to matter more in early stages; later stages carry less risk.

### Failure Definition and Missing Data
- Business status date and ownership status date may not reflect actual failure dates, but no better option exists.
- Open question: measure failure within a fixed window (24 or 36 months) via survival analysis.
- About 18% of completed VC rounds lack a deal ID and cannot be merged across files; selection bias handled through controls.
- 26% of deals lack investor info, 10% lack financing dates.

### Dataset Construction and Regression
- Start from the company file (founded year, industry, number of founders, HQ country), then merge deals on company ID.
- Don't restrict the sample upfront: define non-negotiable variables, build a general dataset, and cut later.
- Syndication is the independent variable, failure the dependent; other variables enter as controls.

### Decisions Made
- Failure = bankruptcy or out of business in either ownership status or business status.
- Rounds without a deal ID are dropped; deals missing financing dates are excluded.
