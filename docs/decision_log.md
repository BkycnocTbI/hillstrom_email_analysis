# Analysis and selection record

This educational reanalysis follows the historical experiment; it is not its original preregistration. The original plan is retained unchanged in analysis_plan.md.

- 2026-10-26: acquisition and checksum verification, before project treatment-effect calculations; split seeds 42 and 43 fixed before outcome comparisons.
- Development: structural checks retained all 64,000 source-described customer rows; no ID-based independence audit is possible. Allocation and balance checks preceded effect exploration.
- The 60/20/20 assignment-stratified split preceded outcome comparisons. Train plus validation supported interim exploration. Validation was used for selection; it was not an independent confirmation sample.
- Full-sample primary campaign estimates were postponed until the policy and its held-out evaluation were locked.
- The secondary family remained seven development comparisons with BH at q=0.05. Three prespecified binary segment definitions used three omnibus interaction tests with Holm at 0.05.
- The upper-tail sensitivity fixed a shared 95th-percentile development-buyer cap before inspecting capped effects. Full, uncapped revenue remained primary.
- A pilot estimated one fixed random recipient lottery. The final random benchmark analytically averages over uniformly random fixed-capacity subsets, before model evaluation, avoiding arbitrary-lottery noise. Raw historical allocation is nominally 1/3; conditional IPW on each stratified evaluation split uses its fixed n_arm/N fractions.
- Candidate evaluation order: expected random benchmarks; Ridge T-learner (alpha=100); high-history Mens heuristic; one final HGB T-learner with fixed documented settings. No further models or parameter searches were added after the test result.
- Capacity is a hypothetical scenario: 10,000/64,000, equivalent to 2,000/12,800. Learned policies choose the best positive predicted email increment up to that limit. The high-history heuristic always fills the available capacity.
- Before test: freeze High-history Mens by maximum validation IPW mean; freeze two contrasts (no email and expected random Mens), 10,000 stratified paired bootstrap replicates, seed 42, and 97.5% intervals per contrast for approximate joint 95% coverage.
- Test evaluation did not establish superiority. The selected rule was not replaced or retuned after inspecting that result.
- 2026-10-27: source notebook copied for English explanations, portable paths, full-sample final campaign reporting, clearly assumed cost scenarios, plots and exports. Source computation choices and original files are preserved. The complete copy is checked from a fresh kernel.

The policy comparison is conditional on the recorded customer-level observations and fixed recommendations. Percentile intervals are approximate and do not refit models. Independent people, reported randomization, no interference and adequate follow-up remain assumptions. The project does not claim global 5% error control across exploratory stages.
