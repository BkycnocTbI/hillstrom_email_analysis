# Hillstrom Email Experiment: Analysis Plan

Status: planned. This document is written before calculating the project's treatment effects or fitting its models. It is not a preregistration of the historical experiment.

## Business problem

Determine whether sending either email campaign increases two-week revenue per assigned customer, and whether customer targeting can improve the use of a limited mailing capacity.

According to [Kevin Hillstrom's original description](https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html), the data contains 64,000 customers randomly assigned in thirds to Mens E-Mail, Womens E-Mail and No E-Mail. Outcomes cover two weeks after the campaign. Pretreatment purchase history and customer characteristics are available.

This is an independent reanalysis of a historical public benchmark. Published solutions already exist.

## 1. Establish the data contract

- Verify provenance, available usage terms, file integrity, dimensions, schema and categories.
- Inspect missingness, binary fields, impossible values and consistency between Visit, Conversion and Spend.
- Preserve legitimate zero revenue and large purchases; investigate unusual records before changing anything.
- The documented schema does not include a persistent customer ID. Row numbers can identify analysis records but cannot prove that each record represents a unique person. Matching customer profiles are not automatically erroneous duplicate customers.
- Distinguish pretreatment fields from assignment and post-treatment outcomes. Never use Visit, Conversion or Spend as targeting features.

## 2. Experiment health

- Check observed allocation against the author's stated 1:1:1 ratio. Use a prespecified SRM diagnostic threshold of 0.001; a flag prompts investigation rather than an automatic correction of group sizes.
- Examine pretreatment balance with effect-size diagnostics as well as sample counts.
- Document what cannot be checked: the original randomization implementation, identity deduplication, delivery/noncompliance, interference, timestamps and complete follow-up.
- Analyze customers by assigned campaign, keeping the no-email control and all recorded zero outcomes.

## 3. Prespecified outcomes and comparisons

Immediately after structural checks, create and save an assignment-stratified 60% train / 20% validation / 20% test split. Reserve 20% as test with random_state=42, then reserve 25% of the remainder as validation with random_state=43, stratifying both operations by assignment. Use train and validation rows for outcome exploration, interim inference and segment discovery. Test outcomes are not used to choose features, models, thresholds or policies. Full-sample effect estimates are reported only after the policy and its held-out evaluation have been locked; they must not be fed back into policy selection.

**Primary outcome:** mean two-week Spend per assigned customer, including zeros.

**Primary comparisons:** Mens E-Mail minus No E-Mail; Womens E-Mail minus No E-Mail. Control the family-wise error rate at 0.05 with Holm adjustment across these two tests.

**Secondary exploratory family:** seven comparisons: each email versus control on conversion and visit (four), and Mens versus Womens on revenue, conversion and visit (three). Report Benjamini-Hochberg adjusted p-values with q = 0.05 for this separate family. This is not a claim of global 5% family-wise error across all reported analyses. Revenue among purchasers and average order value are descriptive conditional metrics, not substitutes for the randomized per-customer revenue comparison.

Do not select a winner by the smallest unadjusted p-value. The primary family remains the two revenue comparisons with the no-email control.

## 4. Estimate effects and uncertainty

- Report group sizes, outcome counts, rates, mean revenue, absolute differences and relative effects where the baseline permits them.
- Use mean-based inference appropriate to unequal variances, with a prespecified bootstrap analysis to assess uncertainty in the skewed revenue outcome.
- Keep ordinary per-comparison intervals distinct from family-wise conclusions. Add simultaneous intervals when making a simultaneous decision across campaigns.
- Use a fixed seed and bounded-memory resampling. Do not change methods or remove large purchases to obtain significance.
- Analyze sensitivity to extreme purchases transparently. Any trimming or winsorization changes the estimand and is not the primary result.
- Explain statistical uncertainty alongside the size and practical relevance of the revenue change.

## 5. Variance reduction and heterogeneity

- Assess an adjusted revenue analysis using pretreatment history, with appropriate robust uncertainty and separation from the unadjusted primary result.
- Preselect a small set of business-relevant segments, such as purchase recency, prior spend and new-customer status. Check sample support and use interaction tests rather than comparing which subgroup has a significant p-value.
- Treat broader segment searches as exploratory. Apply multiplicity control and validate promising patterns on held-out data.
- Do not claim individual causal effects are observed for each customer.

## 6. Targeting models and policy evaluation

- Use the fixed split defined before outcome exploration. Keep test outcomes out of the policy-selection process until the policy is chosen.
- Compare simple baselines with interpretable treatment-effect models; add more complex uplift methods only if they improve held-out decisions.
- Select between no email, the Mens campaign and the Womens campaign using pretreatment information only.
- Evaluate incremental revenue with methods compatible with the randomized assignment, such as inverse-probability or doubly robust policy evaluation.
- Assess a fixed-capacity scenario corresponding to 10,000 of 64,000 customers. On a test subset, evaluate the equivalent selection fraction rather than pretending it contains the whole population.
- Use held-out policy value as a decision criterion; predictive accuracy or conversion propensity alone does not establish that targeting creates incremental revenue.

## 7. Business scenarios and deliverables

- Separate revenue from profit. Actual email costs and margins are not provided; cost and break-even analyses must label their assumptions.
- Explain the two-week horizon and limits to generalization.
- Produce an executive summary, reproducible notebooks, figures, results tables, environment information and an English README.
- Publish only after reviewing the results and receiving approval for GitHub changes.

## Working rule

The scope is broad, but each method must serve a business question or a validation need. Freeze each stage's choices before seeing its results; document deviations instead of silently adding tests until a favorable finding appears.

## Plan history

- 2026-10-26: initial plan saved before the dataset download and before calculating treatment effects.
- 2026-10-26: after checking only the downloaded file's checksum, shape and column names, specified split seeds 42 and 43. No group outcome comparisons or models had been run. The acquisition record retains the earlier plan checksum and records the current revision separately.
