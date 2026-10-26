"""Check the executed project against its data contract and frozen walkthrough."""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

import nbformat
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from sklearn.model_selection import train_test_split
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.policy import high_history_policy

checks = []


def check(name, passed):
    checks.append({"name": name, "passed": bool(passed)})


results = json.loads((ROOT / "outputs/results.json").read_text(encoding="utf-8"))
provenance = json.loads((ROOT / "data/provenance.json").read_text(encoding="utf-8"))
raw = ROOT / "data/raw/hillstrom.csv"
check("source CSV checksum", hashlib.sha256(raw.read_bytes()).hexdigest() == provenance["csv_sha256"])
data = pd.read_csv(raw)
check("source schema and dimensions", data.shape == (64000, 12) and list(data.columns) == provenance["columns"])
check("no missing source values", int(data.isna().sum().sum()) == 0)
check("matching combinations retained", len(data) == 64000 and int(data.duplicated().sum()) == 6562)
check("outcome coherence", all(value == 0 for value in results["coherence_flags"].values()))
check("input paths excluded from Git", "/data/raw/" in (ROOT / ".gitignore").read_text())
check("allocation diagnostic", abs(results["srm_p"] - 0.903693) < 0.00000051)

nb = nbformat.read(ROOT / "hillstrom_email_analysis.ipynb", as_version=4)
nbformat.validate(nb)
code = [cell for cell in nb.cells if cell.cell_type == "code"]
check("all 36 code cells executed", len(code) == 36 and all(c.execution_count is not None for c in code))
check("no notebook execution errors", not any(
    output.output_type == "error" for cell in code for output in cell.outputs
))
check("English explanations included", sum(c.cell_type == "markdown" for c in nb.cells) == 37)
check("portable notebook source", not any(
    re.search(r"[A-Za-z]:[\\/]", cell.source) for cell in code
))
for script in list((ROOT / "scripts").glob("*.py")) + list((ROOT / "src").glob("*.py")):
    ast.parse(script.read_text(encoding="utf-8"), filename=script.name)
check("Python helper syntax", True)

development, test = train_test_split(data, test_size=0.20, random_state=42, stratify=data["segment"])
train, validation = train_test_split(development, test_size=0.25, random_state=43, stratify=development["segment"])
manifest = pd.read_csv(ROOT / "outputs/split_manifest.csv", index_col=0)["split"]
check("split sizes", manifest.value_counts().to_dict() == {"train": 38400, "validation": 12800, "test": 12800})
check("unique complete record coverage", manifest.index.is_unique and set(manifest.index) == set(data.index))
check("split reproducibility", all(set(manifest.index[manifest == name]) == set(frame.index)
    for name, frame in [("train", train), ("validation", validation), ("test", test)]))
check("split disjointness", not (set(train.index) & set(validation.index) or
    set(train.index) & set(test.index) or set(validation.index) & set(test.index)))

full = pd.read_csv(ROOT / "outputs/full_primary_revenue.csv", index_col=0)
control = data.loc[data["segment"] == "No E-Mail", "spend"]
expected_rows = []
for action in ["Mens E-Mail", "Womens E-Mail"]:
    treatment = data.loc[data["segment"] == action, "spend"]
    result = ttest_ind(treatment, control, equal_var=False, alternative="two-sided")
    interval = result.confidence_interval()
    expected_rows.append([treatment.mean() - control.mean(), interval.low, interval.high, result.pvalue])
expected_rows = np.asarray(expected_rows)
check("full primary contrasts reproduce", np.allclose(
    full.loc[["Mens E-Mail", "Womens E-Mail"], ["effect", "ci_low", "ci_high", "p_raw"]],
    expected_rows, atol=1e-12, rtol=1e-10))
check("full primary Holm family", len(full) == 2 and np.allclose(
    full["p_holm"], multipletests(full["p_raw"], alpha=0.05, method="holm")[1]))
summary = pd.read_csv(ROOT / "outputs/full_campaign_summary.csv", index_col=0)
check("full cohort denominator", int(summary["customers"].sum()) == 64000)
check("full buyer counts", summary["buyers"].to_dict() ==
      {"Mens E-Mail": 267, "No E-Mail": 122, "Womens E-Mail": 189})
check("primary conclusions", (full["p_holm"] < 0.05).all() and (full["ci_low"] > 0).all())

secondary = pd.read_csv(ROOT / "outputs/development_secondary_tests.csv", index_col=0)
check("secondary seven-test BH family", len(secondary) == 7 and np.allclose(
    secondary["p_bh"], multipletests(secondary["p_raw"], alpha=0.05, method="fdr_bh")[1]))
interactions = pd.read_csv(ROOT / "outputs/development_interaction_tests.csv", index_col=0)
check("three exploratory interaction tests", len(interactions) == 3 and
      set(interactions.index) == {"newbie", "recent_buyer", "high_history"} and
      (interactions["p_holm"] >= 0.05).all())
dev = pd.read_csv(ROOT / "outputs/development_campaign_summary.csv", index_col=0)
check("development cohort labelled separately", int(dev["customers"].sum()) == 51200)

values = pd.read_csv(ROOT / "outputs/validation_policy_values.csv", index_col=0)
expected_policy_lifts = {
    "No email": 0.000, "Random Mens E-Mail": 0.156, "Random Womens E-Mail": 0.058,
    "High-history Mens": 0.246, "Ridge T-learner": 0.069, "HGB T-learner": -0.117
}
check("all six candidate values reproduce displayed walkthrough", set(values.index) == set(expected_policy_lifts)
      and all(abs(values.loc[k, "increment_vs_no_email"] - v) <= 0.00051
              for k, v in expected_policy_lifts.items()))
check("validation capacity", (values["emails"] <= 2000).all() and
      (values.drop(index="No email")["emails"] == 2000).all())
check("selection follows frozen criterion", values["value_per_customer"].idxmax() == "High-history Mens")

for index, expected in [(27, {"No E-Mail": 10800, "Mens E-Mail": 1398, "Womens E-Mail": 602}),
                        (29, {"No E-Mail": 10800, "Mens E-Mail": 1017, "Womens E-Mail": 983})]:
    text = "\n".join(output.get("text", "") for output in code[index].outputs
                     if output.output_type == "stream")
    counts = {name: int(number) for name, number in re.findall(
        r"^(No E-Mail|Mens E-Mail|Womens E-Mail)\s+(\d+)\s*$", text, flags=re.M)}
    check("model allocation reproduces cell " + str(index), counts == expected)

protocol = json.loads((ROOT / "outputs/selected_policy.json").read_text())
check("frozen selected rule", protocol["selected_policy"] == "High-history Mens"
      and protocol["capacity_fraction"] == 10000 / 64000
      and protocol["no_test_outcome_based_retuning"] is True)
check("two frozen test contrasts and interval level", len(protocol["test_comparisons"]) == 2 and
      protocol["test_interval_level_per_comparison"] == 0.975 and
      protocol["bootstrap_replicates"] == 10000 and protocol["bootstrap_seed"] == 42)

recommendations = pd.read_csv(ROOT / "outputs/test_recommendations.csv", index_col=0)["recommendation"]
expected_recommendations = high_history_policy(test["history"])
check("exported rule matches held-out recommendations", recommendations.index.equals(test.index) and
      np.array_equal(recommendations.to_numpy(), expected_recommendations.to_numpy()))
check("held-out capacity and actions", recommendations.value_counts().to_dict() ==
      {"No E-Mail": 10800, "Mens E-Mail": 2000})

intervals = pd.read_csv(ROOT / "outputs/test_policy_intervals.csv", index_col=0)
expected_test = np.array([[0.131, -0.265, 0.482], [0.047, -0.300, 0.361]])
check("held-out estimates and intervals match displayed walkthrough", np.allclose(
    intervals.loc[protocol["test_comparisons"], ["difference", "ci_low", "ci_high"]],
    expected_test, atol=0.00051, rtol=0))
check("test conclusion retains uncertainty", (intervals["ci_low"] < 0).all()
      and (intervals["ci_high"] > 0).all())

scenarios = pd.read_csv(ROOT / "outputs/business_scenarios.csv", index_col=0)
check("cost scenarios explicitly assumed", len(scenarios) == 18 and scenarios["scenario_only"].all())
check("scenario population and capacity", (scenarios["eligible_customers"] == 64000).all()
      and (scenarios["target_emails"] == 10000).all())
scenario_ok = True
for _, row in scenarios.iterrows():
    source = intervals.loc[row["comparison"]]
    cost = 10000 * row["assumed_cost_per_email"] if row["comparison"].endswith("No email") else 0
    multiplier = 64000 * row["assumed_margin"]
    expected = source[["difference", "ci_low", "ci_high"]].to_numpy(dtype=float) * multiplier - cost
    actual = row[["projected_contribution_difference", "ci_low", "ci_high"]].to_numpy(dtype=float)
    scenario_ok &= np.allclose(expected, actual, atol=1e-8, rtol=1e-10)
check("scenario arithmetic and interval transformation", scenario_ok)
check("profitability uncertainty preserved", (scenarios["ci_low"] < 0).all()
      and (scenarios["ci_high"] > 0).all())

from PIL import Image
figures = ["development_revenue_effects.png", "full_campaign_effects.png",
           "test_policy_comparison.png", "validation_policy_comparison.png"]
for name in figures:
    with Image.open(ROOT / "outputs" / name) as image:
        image.verify()
    check("valid PNG " + name, True)

validation_path = ROOT / "outputs/validation.json"
validation_path.write_text(json.dumps({"status": "checking"}, indent=2), encoding="utf-8")
broken_links = []
for doc in ROOT.rglob("*.md"):
    if any(part in {".runtime", "raw", "__pycache__"} for part in doc.relative_to(ROOT).parts):
        continue
    for target in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", doc.read_text(encoding="utf-8")):
        if target.startswith(("http:", "https:", "#", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if target and not (doc.parent / target).resolve().exists():
            broken_links.append({"document": str(doc.relative_to(ROOT)), "target": target})
check("local documentation links resolve", not broken_links)
report = {
    "status": "passed" if all(item["passed"] for item in checks) else "failed",
    "checks": checks,
    "passed": sum(item["passed"] for item in checks),
    "total": len(checks),
    "broken_links": broken_links,
    "raw_data_in_distribution": False,
    "notes": "Fresh-kernel execution is performed separately by scripts/run_notebook.py. "
             "Intervals are approximate; numerical checks do not verify the original randomization or customer identity."
}
validation_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({"status": report["status"], "passed": report["passed"], "total": report["total"],
                  "failed": [item["name"] for item in checks if not item["passed"]]}))
if report["status"] != "passed":
    raise SystemExit(1)
