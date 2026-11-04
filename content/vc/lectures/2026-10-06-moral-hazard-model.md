---
title: VC 6-10 — Modello di moral hazard (Holmström-Tirole)
date: 2026-10-06
wispr: https://notes.wisprflow.ai/shared/vPzsI47MPWpcUDY_Q0AxJj3_DW7e0K_pckexYvbi5ok
---
Lecture on VC contracting via a single moral hazard model (likely Holmström and Tirole): incentive and investor constraints, why Europe needs more founder assets than the US, and why VC contracts are equity-based.

### Course Admin and Study Approach
- Class 8 contract lecture notes are released only after class so students work actively and build the model together
- ChatGPT and lecture notes are fine if used actively; passive study leads to far more mistakes
- Class 7 graph with inverted entrepreneurial activity axis has been corrected; students should recheck it

### Why VC Contracts Matter
- Contracts align entrepreneur and VC objectives when moral hazard arises; debt and equity alone cannot do this
- Contracts must also set monitoring and control, VC effort incentives, return split, and the liquidity event exit
    - Exit is regulated since a founder or VC leaving right after an IPO sends a bad market signal
- VC deals are conditional contracting: they must cover all possible outcomes, unlike a standard bank loan

### Single Moral Hazard Model
- Project costs I; entrepreneur has assets A < I, borrows I − A, protected by limited liability (no collateral)
- Return R with probability P, else 0; shirking lowers P from PH to PL but gives private benefit B
    - B and PL are independent and exogenous; higher B only raises the reward needed
- NPV must be positive only when behaving: PH·R − I > 0, while PL·R − I + B < 0
- IC constraint: (PH − PL)·R_B ≥ B; IR constraint: PH·R_L ≥ I − A, equality under perfect investor competition
    - Investor only breaks even, so the entrepreneur captures the full NPV as the price of incentives

### Required Founder Assets and US vs Europe
- Solving for A: A ≥ I − PH·(R − B/(PH − PL)); higher I needs more A, higher R needs less
- If PH equals PL, A goes to infinity: investors cannot distinguish behavior, so no one lends
- Higher B raises required assets; slow courts and opaque, unreliable economies raise B (e.g. Argentina 2001)
- Explains why US founders get funding with little capital while in Europe it relies on private savings
    - Example: US students borrowing from banks for MIT tuition, education debt not dischargeable in bankruptcy

### Debt vs Equity
- With zero payoff on failure, debt and equity are indistinguishable since there is no downside protection
- If value remains on failure, give the leftover (debt) to the investor and equity to the entrepreneur for upside incentive
- Under double moral hazard both need upside incentives, so VC contracts are typically all-equity

### Next Steps
- (Speaker 1) Upload class 8 lecture notes on contract after class
- (Speaker 1) Post a sample VC contract online to show its complexity
- (Students) Review the slides on VC selection and governance and send questions by email
