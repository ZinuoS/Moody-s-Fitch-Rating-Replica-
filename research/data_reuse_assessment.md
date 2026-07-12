# Data validity recheck and clo-atlas reuse assessment

Date: 2026-07-12. Scope: (1) recheck whether the data underlying
`clo_methodology_change_2026.ipynb` is valid, (2) assess whether real data already
scraped by the companion clo-atlas project (`git@github.com:ZinuoS/CLO_Atlas.git`) can
feed the rating-replica engines described in `README.md` Phases 1-3, for both the
original (Moody's Apr-2026 / Fitch prior) replication and the new-methodology
(Moody's Jun-2026 RfC / Fitch Jun-2026) study.

## 1. Recheck: is the data in the notebook valid?

**Provenance scan (notebook cell 3, executed).** `docs/criteria/` and `docs/pcm_outputs/`
are both empty in this repo. The notebook's own self-report -- "no criteria PDFs found
locally; ALL figures below run in ILLUSTRATIVE mode" -- is accurate, not a false claim.
Every figure that depends on an unavailable primary source is tagged ILLUSTRATIVE or
TO-VERIFY, consistent with the guardrail "no value enters a config from secondary
commentary alone."

**The one load-bearing external claim** -- Moody's Aaa default-probability stress
multiplier moving 1.95 -> 1.81 -- traces to Rod Dubitsky's Substack (`references.md`
item 5), explicitly tagged TO-VERIFY, not agency-confirmed fact. A web search confirms
Dubitsky's article is real and the multiplier figures are corroborated by at least one
other independent aggregation of the same commentary. This is as far as validation can
go without the RfC exhibit itself: the notebook's TO-VERIFY tag is doing its job
correctly (grounded in a findable, real, but non-primary source), and should stay a
TO-VERIFY until the RfC exhibit or final methodology is obtained through the registered
Moody's portal per the guardrails.

**Everything else** (agency timeline dates, Fitch's 5-15% impact estimate, S&P's 2019
criteria date, the mechanism descriptions of BET/PCM/CDO Evaluator) is VERIFIED against
public agency announcements and methodology summaries, not third-party commentary.

**Conclusion: the data the notebook currently relies on is valid as far as it goes** --
the notebook does not fabricate anything, and its TO-VERIFY tags are attached to the
right claims. The gap is real primary-source parameter values (the full multiplier
ladder, the recovery table, correlation assumptions, Fitch's actual redline), which
remain genuinely unavailable without registered-portal access, per the guardrails.

## 2. clo-atlas data inventory (checked against the actual parquet files, not the plan)

| File | Rows | Real columns | What it actually is |
|---|---|---|---|
| `data/interim/bdc_soi_positions.parquet` | 12,708 | `fund, investment_identifier, company, instrument_type, coupon, spread, fair_value, amortized_cost, principal, period` | Per-position holdings scraped from BDC (e.g. ARCC) Schedule-of-Investments EDGAR filings. Company-level, instrument-level, real coupon/spread/fair-value. |
| `data/final/edgar_resolved_issuers.parquet` | 10,533 | `raw_name, canonical_id, canonical_name, method, score` | Entity-resolution output (`src/common/entity.py`) mapping raw filing names to canonical issuer IDs, with match method and confidence score. |
| `data/interim/trace_clo_pricing.parquet` | 166 | `date, rating_band, vintage, metric, value` | FINRA TRACE CLO secondary-market pricing (average/quartile price, volume, trade count) by rating band (AAA / non-AAA IG / non-IG) and vintage. **Single-day snapshot** as of 2026-07-08 -- clo-atlas's scraper had run once. |

## 3. What this can and cannot do for the rating-replica engines

**Cannot feed Phase 1 (Moody's BET) or Phase 2 (Fitch PCM) directly, for either the old
or new methodology study.** Both engines need per-obligor agency ratings (to build WARF
/ idealized PD) and an industry classification (for the diversity score / correlation
structure). Neither column exists in any clo-atlas output. Agency ratings are exactly
the kind of data the guardrails say must come from registered portals, not scraped --
so this is not a gap clo-atlas can close, by design.

**Partially usable for Phase 3 (Portfolio feed).** `edgar_resolved_issuers.parquet` +
`bdc_soi_positions.parquet` together already satisfy the *entity-resolution* half of
Phase 3's spec (`resolved_entity_id -> facility`, with real coupon/spread/fair-value
attached) -- this is real, not synthetic. But it is a **BDC's** loan book, not a CLO's:
useful as a same-universe proxy (BDCs and CLOs both hold broadly syndicated and
middle-market leveraged loans) for illustrating loan-level mechanics, not as a
substitute for an actual CLO's collateral tape. Using it to replace Section 4's 8
synthetic deals would trade one kind of illustrative placeholder for another and isn't
worth the complexity it would add; the honest labeling stays the same either way.

**Usable now, and used.** `trace_clo_pricing.parquet` is real, public, unlicensed,
and outside any "do not scrape" guardrail (it's FINRA TRACE, not a rating agency). It
does not test methodology impact (a single day can't show a before/after move around
the Apr/Jun 2026 announcement dates), but it is a legitimate real-data anchor for the
notebook's illustrative spread assumptions. **Wired into the notebook as new Section 7**
(`docs/market_context/trace_clo_pricing_2026-07-08.csv`, cell tagged VERIFIED with full
provenance sidecar) rather than left as an unused opportunity.

## 4. Recommendation

1. Keep Phase 1/2 blocked on registered-portal document acquisition, as the README
   already plans -- clo-atlas cannot and should not be used to route around that.
2. Re-run clo-atlas's `src/official/scrape_trace.py` periodically and re-export; once
   a real time series spans the Apr 24 / Jun 1 / Jun 5 2026 dates, Section 6's
   impact-summary claims become testable against real secondary pricing, not just
   mechanically reasoned. This is the one honestly promising cross-repo reuse path
   left open by this assessment.
3. Do not force bdc_soi_positions into the WARF/diversity-score pipeline; it lacks the
   ratings and industry-classification columns that pipeline needs, and mislabeling a
   proxy universe as replication input would violate the same discipline this notebook
   otherwise holds itself to.
