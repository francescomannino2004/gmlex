---
title: VC 13-10 — Clausole contrattuali, SAFE, anti-dilution, staging
date: 2026-10-13
wispr: https://notes.wisprflow.ai/shared/oNaYZjzQS8t5ce-7xH-gffR1y6xi2xYz7j0a5DBecO8
---
Lecture on VC contract terms: preferred stock variants, SAFEs and convertible notes, anti-dilution clauses, other term sheet rights, and a stage financing example showing entrepreneurs can sell less equity.

### Preferred Stock Variants
- Straight preferred is paid first at liquidation (after debt); preferred term = investment × multiplier, plus possible cumulative dividends.
    - Multiplier was 1 in more than 90% of US cases in Q2 2026; higher in downturns
- Redeemable preferred (about 5% of deals) lets the VC demand money back, signaling very high VC bargaining power.
- Convertible preferred: the conversion share S reveals the minimum post-money valuation as I / S; a higher multiplier raises the conversion threshold.
    - Conversion is irreversible: once converted, there is no going back to preferred
- Participating preferred keeps PT plus a share of remaining returns, often capped; beyond the cap the investor must convert to common.

### Convertible Notes and SAFEs
- Convertible notes and SAFEs (simple agreement for future equity) are debt-like, used at pre-seed, giving little control.
    - Over 90% of pre-seed rounds in Q1 2026 used these; not used 10 years ago
- SAFE holders usually cannot demand anti-dilution: a 10% stake falls to 8% if a new investor takes 20%.

### Anti-Dilution Clauses
- Full ratchet resets conversion price to the new issue price, punishing the entrepreneur and signaling strong VC power.
    - Example: price drops from 1 dollar to 0.5, investor shares double to 2 million, stake above 50%
- Weighted average multiplies the old price by a ratio below 1; in the example new price is 0.988 and stake falls from 50% to about 49%.
- Common exam mistake: forgetting to multiply the ratio by the old price when it equals 1.

### Other Term Sheet Rights
- Covered pay to play, protection provisions, preemption, right of first refusal, tag along, drag along, co-sale, and lock-up periods.
- Drag along forces all shareholders to sell once the board majority decides, e.g. to liquidate a failing firm and limit liability.
- Also: information and visitation rights, key man insurance, jurisdiction choice, IP transfer, veto and affirmative rights, registration rights.
- Control rights: about 47% of US board seats held by VCs, rising above 50% when things go badly.

### Stage Financing and Grandstanding
- Example needs 30 (10 now, 20 later); good news (prob 2/3) yields 150, bad news yields 150 with prob 1/10, else 0.
- All money up front: stake is 30/105, about 28.5%; staged: 10% at time 0 plus 13.3% at time 1, total 23.3%.
    - Staged stakes use conditional expectation on good news, since VC won't fund after bad news
- Milestones (patent, sales, profit) gate later tranches; staging serves control, signaling, and screening.
- Young VCs push IPOs early to build reputation: grandstanding.

### Next Steps
- (Speaker 1) Add a computation for the case where the bad-news payoff is positive
- (Students) Work through the numerical examples on preferred stock and anti-dilution, emailing questions if stuck
