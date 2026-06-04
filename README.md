# graphed-corpus

Ground-truth **requirements + runnable canonical-analysis fixtures** for `graphed` (milestone
M0.5), distilled from the A.8 reference corpus. Part of the
[`graphed-org`](https://github.com/graphed-org) project; see
[`graphed-project`](https://github.com/graphed-org/graphed-project) for root guidance and the plan.

## What's here

- **Required Operations Catalog** — `docs/requirements/ops_catalog.md`: every array op / selection /
  systematic / correction / ML pattern the frontend must support, tagged with its corpus source and
  the milestone that must deliver it.
- **Canonical analyses** — `src/graphed_corpus/analyses/`: ADL queries 1–8 and AGC-ttbar-style /
  TTGamma-style systematics slices, as plain awkward, each with a **stored reference histogram**
  (`corpus/references/`) so later milestones assert `graphed` reproduces them bit-for-bit.
- **Graph-bloat note** — `docs/graph_bloat_note.md`: the node-count explosion M4 must avoid.

```python
from graphed_corpus import make_events, ADL_QUERIES, ttbar_region
events = make_events()                       # deterministic synthetic NanoAOD-like data
h = ADL_QUERIES["q5"](events)                # dimuon-Z-window MET, real awkward
ht = ttbar_region(events, region="4j1b", variation="jes_up")   # kinematic systematic
```

> **Data provenance.** Fixtures use a deterministic *synthetic* dataset, not real CMS Open Data —
> sufficient for `graphed`'s "same answer as plain awkward" contract and network-free. A reduced
> real AGC/NanoAOD slice + CMS-published reference is a tracked Phase-2 follow-up.

## Develop

```bash
pip install -e ".[dev,docs]"
ruff check . && ruff format --check . && mypy
pytest --cov=graphed_corpus --cov-branch
python scripts/gen_references.py        # regenerate stored references (deterministic)
sphinx-build -W -b html docs docs/_build/html
```

Status: **M0 spine + M0.5 content built; 60 frozen tests green (23 fixtures reproduce references).**
See `.graphed/state.json` for live milestone state and `CLAUDE.md` for the distilled spec.
