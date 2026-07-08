# Moody-s-Fitch-Rating-Replica-

### Moody's (April 2026 → June 2026 RfC) and Fitch (prior criteria → June 1, 2026 final) replication plan level 1

**Status of the methodologies as of July 8, 2026.** Fitch's updated *CLOs and Corporate CDOs Rating Criteria* is final and effective (published ~June 1, 2026; Fitch estimates 5–15% of CLO note ratings affected, all changes positive). Moody's June 5, 2026 update is a **Request for Comment** — the comment period closed July 4, 2026 and the final methodology is pending. Everything on the Moody's side must therefore be parameterized so the final tables are a config swap, not a rebuild. Moody's last *final* methodology is the April 24, 2026 publication, which is the correct "old" baseline for the Moody's diff.

**Known headline changes (verify against primary documents before use):**

| Item | Old | New / proposed | Source status |
|---|---|---|---|
| Moody's Aaa default-probability stress multiplier | 1.95 (unchanged since ≥2019) | 1.81 (RfC) | Third-party replication of the RfC; **verify in RfC Exhibit** |
| Moody's collateral basis | Covenanted attributes (rate to the matrix/covenants) | Actual portfolio attributes | RfC; **verify scope and conditions** |
| Moody's recovery rate table | 2019-era table | Unchanged in RfC | Third-party comparison |
| Moody's correlation / diversity assumptions | — | Unchanged in RfC | Third-party comparison |
| Moody's projected impact | — | 1–3 notch upgrades on ~1/3 of outstanding classes | Moody's own estimate, quoted in commentary |
| Fitch parameter changes | Prior *CLOs and Corporate CDOs Rating Criteria* | Not itemized in public commentary — **requires the criteria redline** | Pull both versions from fitchratings.com |
| Fitch projected impact | — | 5–15% of note ratings change, all positive | Fitch's own estimate |
| Independent AAA impact estimate (Moody's multiplier alone) | — | ≈5% reduction in required Aaa credit support | Third-party BET replication; treat as sanity check, not truth |

---

## Phase 0 — Document acquisition and the parameter diff table

**Documents (all obtainable without scraping; registered access or desk copies):**
1. Moody's, *Global Approach to Rating Collateralized Loan Obligations*, April 24, 2026 (ratings.moodys.com — free registration).
2. Moody's, *Proposed Update — Request for Comment*, June 5, 2026 (same portal).
3. Fitch, *CLOs and Corporate CDOs Rating Criteria*, June 2026 (fitchratings.com — free registration; ask the desk for the redline vs. prior version, agencies usually circulate one).
4. Fitch, prior version of the same criteria (the superseded report remains downloadable; the July 2023 vintage is filed publicly as an exhibit to Fitch's NRSRO annual certification on EDGAR if the Fitch portal only shows current).
5. Desk-licensed tools as reconciliation targets: Moody's CDOROM, Intex, Fitch PCM (PCM is publicly downloadable — confirm with Anshu before installing anything on a firm machine).

**Diff table template.** One row per parameter; fill from primary documents with page cites. This table *is* the audit trail — every engine config value must trace to a row.

| # | Parameter | Moody's Apr-2026 (final) | Moody's Jun-2026 (RfC) | Δ | Fitch prior | Fitch Jun-2026 (final) | Δ | Binding for | Page cite (old / new) | Verified by |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DP stress multiplier, by target rating (Aaa…B3 / AAAsf…B-sf) | | | | n/a (Fitch stresses via PCM percentiles) | n/a | | Tranche sizing | | |
| 2 | Rating benchmark (expected loss table / RDR percentile mapping) | | | | | | | All | | |
| 3 | Recovery rate assumptions, by seniority × jurisdiction × target rating | | | | | | | Mezz/junior sizing | | |
| 4 | Correlation framework (diversity score construction / PCM inter- and intra-industry, regional, global) | | | | | | | AAA sizing | | |
| 5 | Collateral basis: covenanted vs. actual; matrix treatment | | | | | | | Manager flexibility, matrix design | | |
| 6 | WARF / IDR mapping, credit estimates, Caa/CCC treatment | | | | | | | OC haircuts | | |
| 7 | Cash-flow stress assumptions (default timing curves, interest-rate stresses, prepay/reinvestment) | | | | | | | Coverage cushions | | |
| 8 | Amortization / WAL treatment post-reinvestment | | | | | | | Senior WAL, spread duration | | |
| 9 | Concentration limit treatment / obligor granularity adjustments | | | | | | | Tail risk | | |
| 10 | Surveillance vs. new-issue application; transition provisions and effective dates | | | | | | | Outstanding book upgrades | | |

Add rows as the redlines reveal them. The "Binding for" column forces every diff to state which structuring decision it touches — if a row can't fill that column, it doesn't matter for the desk deliverable.

---

## Phase 1 — Moody's engine: BET, old and new as configs

**Design principle (same as the MVOC refactor):** pure functions, no I/O inside the math, assumption tables as versioned YAML configs, golden regression tests, reconciliation harness against CDOROM output. Two configs, one engine: `moodys_2026_04.yaml` and `moodys_2026_06_rfc.yaml`. When the final methodology publishes, add `moodys_2026_final.yaml` and rerun everything.

**Module layout**

```
clo_ratings/
  configs/
    moodys_2026_04.yaml        # stress multipliers, EL benchmarks, recovery table, WARF map
    moodys_2026_06_rfc.yaml
    fitch_prior.yaml
    fitch_2026_06.yaml
  moodys/
    warf.py          # portfolio -> WARF, weighted avg recovery, WAL
    diversity.py     # issuer/industry exposures -> diversity score (needs entity-resolution output)
    bet.py           # BET core: binomial loss distribution over D independent credits
    waterfall.py     # simplified sequential-pay loss allocation (or hook to Intex for full)
    rate.py          # expected loss per tranche -> rating vs. EL benchmark table
  fitch/
    pcm_io.py        # build PCM XML input from the resolved loan tape; parse PCM output (RDR/RRR)
    cashflow.py      # Fitch matrix-point cash flow layer over PCM outputs
  reconcile/
    golden/          # frozen deal snapshots + agency-published outputs (presale RDRs, CDOROM runs)
    harness.py       # replica vs. target, tolerance report, per-deal notch diff
  impact/
    restructure.py   # hold portfolio fixed, resize tranches to minimum CE per rating under each config
    arb.py           # liability WACC + equity arb delta between configs
```

**Core function signatures (pure, retypable):**

```python
def warf(exposures: pd.DataFrame, rf_map: dict) -> float: ...
def diversity_score(exposures: pd.DataFrame, industry_col: str) -> float:
    # requires canonical issuer + industry — direct consumer of the
    # entity-resolution pipeline output (resolved_entity_id, sp_industry)
def stressed_pd(warf: float, wal: float, multiplier: float, idealized: pd.DataFrame) -> float: ...
def bet_loss_dist(d_score: float, p_stressed: float, recovery: float) -> np.ndarray:
    # Binomial(D, p): P(k defaults), loss_k = k/D * (1 - recovery) * par
def tranche_el(loss_dist: np.ndarray, attach: float, detach: float) -> float: ...
def rating_from_el(el: float, wal: float, benchmark: pd.DataFrame) -> str: ...
```

The BET math is closed-form (binomial over the diversity-equivalent independent credits), so the whole Moody's engine is deterministic and fast — no Monte Carlo needed until you want the full cash-flow treatment, at which point Intex/CDOROM is the right tool and your engine's job is to *predict and explain* their output, not replace it.

**Covenanted vs. actual (the structurally interesting change).** Implement collateral basis as an input mode, not a code path: the engine takes an `exposures` frame either built from covenant/matrix points (old basis) or from the actual resolved loan tape (new basis). The delta between the two runs on the *same deal* isolates how much rating cushion comes purely from the portfolio being cleaner than its covenants — that number, per deal, is Phase-5 analysis (3).

**Golden tests.** Freeze 5–8 recent deals with known Moody's outputs (desk deals with CDOROM runs are best; otherwise new-issue reports). Test: old-config replica reproduces old ratings within one notch on every tranche *before* any new-config number is quoted. A replica that hasn't passed calibration produces deltas that are noise. Never attribute a discrepancy to the methodology change until the baseline reconciles.

---

## Phase 2 — Fitch engine: run PCM where possible, replicate only the gaps

Fitch differs from Moody's in kind: PCM is a Gaussian-copula Monte Carlo producing rating default rates (RDR) and rating recovery rates (RRR) per stress level, and Fitch's cash-flow model then tests each point of the WARF/WAS/WARR matrix. PCM itself is downloadable, so the priority order is:

1. **Run official PCM** (new version) on the resolved portfolios. If the prior PCM version is still installed anywhere on the desk, old-vs-new RDR curves come straight from official tooling — the strongest possible evidence, zero replication risk.
2. **Replicate the cash-flow layer** over PCM outputs: sequential waterfall, OC/IC diversion, Fitch default-timing curves per the criteria, at each tested matrix point. This is the piece with no public tool.
3. **Only if old PCM is unobtainable:** replicate the copula engine (single-factor Gaussian with Fitch's correlation tiers — global, regional, industry) using the prior criteria's published assumptions. Monte Carlo with fixed seed, ≥1M paths per Fitch's own convergence guidance.

Ground truth for golden tests: Fitch presale reports publish PCM RDRs, break-even default rate cushions, and tested matrix points per deal — public, citable, no licensing issue.

---

## Phase 3 — Portfolio feed

Input is the entity-resolution pipeline output: `resolved_entity_id → facility → industry classification`, joined to ratings (Moody's CFR / Fitch IDR or credit opinion), seniority, jurisdiction, spread, maturity. Reuse the Layer-5 enrichment join. Missing agency ratings get the criteria's prescribed treatment (credit estimate haircuts / CCC buckets) — a diff-table row of its own (#6).

## Phase 4 — Discrepancy measurement

Two runs per deal per agency: old config, new config. Report per tranche: model rating old, model rating new, actual rating, notch deltas. Report per deal: minimum credit enhancement per rating level under each config (the structuring inverse). Per the reporting doctrine: publish the misses alongside the hits — where the replica misses old ratings by more than a notch, the deliverable is the diagnosis (usually a criteria feature not yet implemented), not a tuned number.

## Phase 5 — Structuring impact deliverables

1. **New-issue re-optimization.** Representative BSL portfolio; solve for the max-AAA stack clearing each agency's new criteria; report Δattachment points, Δliability WACC (at current tranche spreads), Δequity arb. Sanity anchor: independent estimate of ≈5% Aaa credit-support reduction from the Moody's multiplier change alone.
2. **Binding-constraint map.** For dual-rated structures, which agency binds at each tranche pre/post. Fitch moving first and Moody's following changes agency-selection economics on new mandates.
3. **Covenanted→actual cushion.** Per deal: rating cushion attributable to actual portfolio quality vs. covenants; implications for matrix design and manager trading flexibility under the Moody's proposal.
4. **Outstanding book screen.** Apply new-config engines to inventory/axe-relevant deals; flag tranches in the upgrade-likely set (Fitch: 5–15% of notes; Moody's: 1–3 notches on ~1/3 of classes) with secondary positioning and refi/reset-candidate implications.

## Guardrails

- All parameter values trace to a diff-table row with a page cite; no value enters a config from secondary commentary alone.
- Moody's June numbers carry an `rfc_provisional: true` flag in config and a watermark in every output until the final methodology publishes.
- No scraping; documents via registered portals or desk copies. PCM installation cleared with Anshu first.
- Engines deterministic end to end (fixed seeds where MC is unavoidable); no LLM calls in firm code.
- Code sized for retypability: short pure functions, configs as data, no framework overhead.

