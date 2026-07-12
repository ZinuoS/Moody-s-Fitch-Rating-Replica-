# References

Companion citation list for `clo_methodology_change_2026.ipynb`. Items (1)-(4)
and (8) are primary sources: obtain via the registered agency portal (or SEC
EDGAR for the NRSRO exhibit); do not scrape.

1. Moody's, *Global Approach to Rating Collateralized Loan Obligations*,
   Apr 24, 2026. **Primary — obtain via registered Moody's portal; do not
   scrape.**

2. Moody's, *Proposed Methodology Update — Request for Comment*, Jun 5,
   2026. Comment period closed Jul 4, 2026; final methodology pending as of
   this notebook's date. **Primary — obtain via registered Moody's portal;
   do not scrape.**

3. Fitch, *CLOs and Corporate CDOs Rating Criteria*, Jun 2026 (final,
   effective ~Jun 1, 2026). **Primary — obtain via registered Fitch Ratings
   portal; do not scrape.**

4. Fitch, prior version of *CLOs and Corporate CDOs Rating Criteria* (via
   fitchratings.com, or the NRSRO certification exhibit on SEC EDGAR).
   **Primary — obtain via registered portal or EDGAR; do not scrape.**

5. Dubitsky, R., "Moody's and Fitch Engage in Dangerous Competitive CLO
   Relaxation Pas de Deux," Rod's Substack, Jul 2026. Source of the
   1.95 -> 1.81 Aaa default-probability stress multiplier figure, the
   recovery-table comparison against the 2019 vintage table, and the
   timeline critique of the Apr/Jun 2026 sequencing used in Sections 2 and 3
   of the notebook. Cited throughout as commentary, not as agency-confirmed
   fact.

6. Fitch, *Portfolio Credit Model User Guide* — reference for the PCM
   mechanics (Gaussian-copula Monte Carlo, RDR/RRR derivation) described in
   Section 1.

7. Cordell, L., Roberts, G., and Schwert, M., *CLO Performance* — background
   on realized tranche and equity performance, referenced in the desk-impact
   synthesis in Section 6.

8. S&P, *Global Methodology and Assumptions for CLOs and Corporate CDOs*,
   Jun 21, 2019. **Primary — obtain via registered S&P RatingsDirect portal;
   do not scrape.**

9. S&P, *CLO Spotlight: All You Need to Know About CDO Monitor*, Mar 2020 —
   source for the CDO Monitor (CDOM) reinvestment-test mechanics described in
   Section 2.4.

10. S&P, CDO Suite of Models product documentation (CDO Evaluator, Cash Flow
    Evaluator, CDO Monitor) — reference for the SDR/BDR mechanics described in
    Section 2.4 and the copula engine framing in Section 3b.

11. S&P, earlier Request for Comment describing rating-quantile calibration
    for CDO Evaluator (e.g. the 1.829% SDR quantile example) — referenced in
    Section 2.4.

12. FINRA, CLO secondary-market pricing tables (`cdn.finra.org/trace/FINRA_IDS_PXTABLES.xlsx`),
    scraped via the companion clo-atlas project's `src/official/scrape_trace.py`
    (`git@github.com:ZinuoS/CLO_Atlas.git`), 2026-07-08 snapshot. Public, unlicensed,
    no "do not scrape" restriction — used in Section 7 as a real-data anchor for the
    notebook's illustrative spread assumptions. See `data_reuse_assessment.md` for the
    full recheck of what clo-atlas data can and cannot feed into this notebook.

## Notes on sourcing status

- Items (1)-(4) are the primary criteria/RfC texts. As of this notebook's
  date they were not available locally in `docs/criteria/`; every figure and
  table in the notebook that would otherwise depend on them runs in an
  explicitly labeled ILLUSTRATIVE mode instead of fabricating parameter
  values.
- Item (5) is third-party commentary and is the sole source for the specific
  multiplier values (1.95, 1.81) and the recovery-table-unchanged claim used
  in this notebook; both are tagged TO-VERIFY against the actual RfC exhibit
  once available.
- Fitch's parameter-level changes (as opposed to the aggregate 5-15% note
  impact estimate) were not itemized in public commentary as of this
  notebook's date and are not sourced here; Section 5 of the notebook
  documents the comparison harness to apply once the redline is available.
- S&P's current global CLO criteria (item 8) date to Jun 21, 2019; no 2026
  update was identified in public sources as of this notebook's date. This
  is stated in Section 2.4 as "no update identified — confirm with desk /
  RatingsDirect" and tagged TO-VERIFY; if confirmed, S&P functions as the
  notebook's control group. Specific S&P correlation and recovery-tier
  values (item 8's appendices) are not reproduced here and are tagged
  TO-VERIFY wherever the notebook references them.
- Item 12 (FINRA TRACE, via clo-atlas) is real, current data, not commentary
  or a placeholder — it is a single-day snapshot, so it anchors Section 7's
  spread context but does not yet test methodology impact against realized
  pricing. See `data_reuse_assessment.md` for the full check of which
  clo-atlas outputs can and cannot feed this notebook's engines.
