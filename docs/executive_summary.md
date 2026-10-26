# Executive summary

## Questions and evidence

Analyze whether historical email campaigns increase two-week revenue per assigned customer, then whether targeting improves a fixed mailing capacity. The published benchmark has 64,000 source-described customers randomized in thirds. It is an educational reanalysis of an already-studied experiment.

## Average campaign results

| Campaign vs no email | Revenue difference per customer (USD) | Individual 95% CI | Relative change | Holm p-value |
|---|---:|---:|---:|---:|
| Mens E-Mail | +0.770 | [+0.485, +1.055] | +117.9% | 2.33e-07 |
| Womens E-Mail | +0.424 | [+0.169, +0.680] | +65.0% | 0.00113 |


The primary outcome includes zeros. Two fixed comparisons use Welch inference and Holm-adjusted p-values; the intervals above are separate 95% intervals. Full-sample reporting followed the policy-selection lock.

## Targeting decision

Fit models only on 38,400 train rows. Use 12,800 validation rows for policy selection. Development diagnostics also used validation; the independent final confirmation is the separate 12,800-row test set.

At 2,000 emails per evaluation cohort, validation selected High-history Mens: mail Mens to the largest pretreatment histories. Its validation increment was USD 0.246 per eligible customer. The two fitted T-learners had lower validation point estimates than this heuristic.

Freeze the rule and two comparisons, then evaluate once on test:

| Frozen comparison | Difference per eligible customer (USD) | 97.5% interval per comparison |
|---|---:|---:|
| High-history vs No email | +0.131 | [-0.265, +0.482] |
| High-history vs Random Mens | +0.047 | [-0.300, +0.361] |


These separate 97.5% percentile intervals provide approximate joint 95% coverage for the two frozen comparisons. Both include zero. Added targeting value is not established; neither a zero effect nor equivalence is established.

## Recommendation

The experiment supports a positive average campaign effect, while the tested capacity-constrained targeting rule requires further evidence. Do not represent the personalization models as a demonstrated business improvement. A new randomized comparison of the frozen high-history rule against random Mens would address the targeting question directly.

Profit cannot be measured from this dataset. The included scenarios use explicitly assumed margins and per-email costs; their wide transformed intervals preserve the underlying uncertainty.

## Important limits

The horizon is two weeks in a historical benchmark. Persistent customer IDs, delivery records, timestamps and the original randomization implementation are unavailable. All customer rows and genuine zero outcomes are retained; matching recorded combinations do not prove duplicate people.

No individual causal effects or causal spend-per-buyer effects are observed. Policy intervals are approximate, condition on the recorded observations and fixed recommendations, and do not refit models. Exploratory stages have separate multiplicity families; no project-wide 5% error guarantee is claimed.
