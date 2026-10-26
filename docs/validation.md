# Validation record

The prepared notebook completed all 36 code cells from a fresh local Python kernel with errors disallowed. Its outputs reproduce the user's completed walkthrough to the displayed precision, including both T-learner allocations, all six validation policy values and the independent test intervals.

The portable validation script checks:

- Source checksum, dimensions, schema, missingness and matching-combination count.
- Exact train/validation/test membership from the fixed split seeds, complete source-row coverage and disjointness.
- Full-sample campaign estimates and the two-test Holm correction.
- Development cohort sizes and the seven-test BH and three-test interaction families.
- All six policy point estimates and mailing capacities; the selection criterion and frozen test protocol.
- Exported recommendations against the outcome-free selected rule.
- Held-out interval levels, displayed test estimates and preservation of uncertainty.
- Explicit cost assumptions, projection arithmetic and transformed bounds.
- Python helper syntax, executable notebook outputs, PNG integrity and local documentation links.

The four exported figures were visually inspected. The original notebook and input CSV were read without modification. Their recorded checksums match the source snapshot and input provenance.

These are reproduction and implementation checks, not verification of the historical customer identities, original randomization, noncompliance, interference or follow-up. Approximate interval coverage is a statistical assumption, not something numerical checks prove.

Run:

~~~bash
python scripts/run_notebook.py
python scripts/validate_project.py
~~~

The detailed result is in [validation.json](../outputs/validation.json). The distributed file manifest records a packaging snapshot; executing the notebook can update cached-output metadata.
