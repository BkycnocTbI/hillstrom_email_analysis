# Hillstrom email experiment data

Original source: [Kevin Hillstrom / MineThatData, March 20, 2008](https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html).

Download locally with:

~~~bash
python scripts/download_data.py
~~~

The helper uses the mirror documented by the [scikit-uplift loader](https://www.uplift-modeling.com/en/latest/_modules/sklift/datasets/datasets.html), verifies compressed MD5 and SHA-256, and verifies the decompressed CSV SHA-256. It writes data/raw/hillstrom.csv. Raw data are ignored and excluded from the repository/distribution; consult the publisher's terms before use or redistribution. No dataset license is asserted.

The compressed MD5 is a68a81291f53a14f4e29002629803ba3. The CSV SHA-256 is 00a6a868e05a9ffe7382da51629f6d6dce88c5acfc945e79d314ebc78fd3a2c0. Full acquisition metadata are in [provenance.json](provenance.json).

| Role | Field | Meaning |
|---|---|---|
| Pretreatment | recency | Months since last purchase |
| Pretreatment | history | Prior-year spend |
| Pretreatment | history_segment | Prior-spend category |
| Pretreatment | mens, womens | Past purchases in each merchandise category; not gender |
| Pretreatment | zip_code | Rural, suburban or urban locality |
| Pretreatment | newbie | New-customer indicator |
| Pretreatment | channel | Prior purchasing channel |
| Assignment | segment | Mens E-Mail, Womens E-Mail or No E-Mail |
| Two-week outcome | visit | Website visit indicator |
| Two-week outcome | conversion | Purchase indicator |
| Two-week outcome | spend | Customer revenue, not profit |

There is no persistent customer ID or order count. Treat each row as one customer under the publisher's description; row numbers do not establish identity. Fully matching combinations are retained because they cannot be established as erroneous duplicate people.

The provenance flag saying no effects had been calculated describes the acquisition stage on 2026-10-26. Final results are separate in [results.json](../outputs/results.json), with the workflow recorded in [the decision log](../docs/decision_log.md). The [original plan](../analysis_plan.md) is retained unchanged.
