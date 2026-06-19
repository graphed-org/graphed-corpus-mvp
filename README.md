# graphed-corpus

Ground-truth **requirements + runnable canonical-analysis fixtures** for `graphed` (milestone
M0.5), distilled from the A.8 reference corpus. Part of the
[`graphed-org`](https://github.com/graphed-org) project; see
[`graphed-project`](https://github.com/graphed-org/graphed-project-mvp) for root guidance and the plan.

This repository deliberately contains **no framework code**. It is *requirements made executable*:
the catalog of operations a real HEP analysis needs, the canonical analyses written in **plain
awkward** (the semantics oracle), a deterministic synthetic dataset to run them on, and stored
reference histograms with content fingerprints so "reproduces bit-for-bit" is a checkable claim
rather than a slogan. When a frozen test elsewhere asserts "graphed must equal awkward here",
*here* is this package.

## What's here

- **Required Operations Catalog** — `docs/requirements/ops_catalog.md`: every array op / selection /
  systematic / correction / ML pattern the frontend must support, tagged with its corpus source and
  the milestone that must deliver it. Ops that can't reasonably land in the MVP are recorded as
  Phase 2 with a rationale rather than silently dropped.
- **Canonical analyses** — `src/graphed_corpus/analyses/`:
  - `adl.py` — the eight ADL benchmark queries (`ADL_QUERIES["q1"]` … `["q8"]`): MET, jet
    kinematics with cuts, an opposite-sign dimuon Z-window, trijet combinatorics, ΔR lepton-jet
    isolation, and an SFOS + transverse-mass selection — the graded functionality ladder.
  - `systematics.py` — AGC-ttbar-style and TTGamma-style slices (`ttbar_region`, `ttgamma_region`,
    `TTBAR_FIXTURES`, `TTGAMMA_FIXTURES`) that stress *graph structure*: many shared-substructure
    variations of the kind that historically produced graph bloat and O(N²) optimization. They
    exercise both **weight systematics** (a per-event reweighting that leaves the selection
    unchanged, e.g. a b-tag scale factor) and **kinematic systematics** (a JES shift that re-runs
    the selection and the observable).
- **Reference histograms** — `corpus/references/*.json`: 23 committed fixtures (8 ADL queries,
  10 ttbar regions = 2 regions × 5 variations, 5 ttgamma variations), each stored as bin contents
  plus a content fingerprint so later milestones assert reproduction against exact, committed counts.
- **Graph-bloat note** — `docs/graph_bloat_note.md`: the node-count explosion (dask-awkward vs
  virtual arrays) that M4's reduction targets must avoid.

```python
from graphed_corpus import make_events, ADL_QUERIES, ttbar_region
events = make_events()                       # deterministic synthetic NanoAOD-like data
h = ADL_QUERIES["q5"](events)                # opposite-sign dimuon Z-window MET, real awkward
ht = ttbar_region(events, region="4j1b", variation="jes_up")   # kinematic systematic
```

## Reproducibility design

`make_events(n_events=20_000, seed=1234)` builds a NanoAOD-shaped jagged record array
(Muon/Electron/Jet/Photon collections plus MET) from a seeded generator. **Synthetic over real**
is an argument, not a shortcut: the contract `graphed` must satisfy is "same answer as plain
awkward on the same input", which a deterministic synthetic input exercises fully while staying
network-free, license-free, and CI-portable.

Histogram fills round derived float quantities to a fixed precision (`graphed_corpus.histograms.stable`)
*before* every cut and fill, so a last-ULP difference between platforms cannot flip a value across a
bin edge. References then compare as **exact integer counts** — no tolerances anywhere — and carry a
SHA-256 `fingerprint` over the canonical record.

> **Data provenance.** Fixtures use a deterministic *synthetic* dataset, not real CMS Open Data.
> A reduced real AGC/NanoAOD slice + a CMS-published reference is a tracked Phase-2 follow-up
> (recorded in the ops catalog); the synthetic oracle stays regardless.

## Develop

```bash
pip install -e ".[dev,docs]"
ruff check . && ruff format --check . && mypy
pytest --cov=graphed_corpus --cov-branch
python scripts/gen_references.py        # regenerate stored references (deterministic)
sphinx-build -W -b html docs docs/_build/html
```

The API reference (`docs/api.rst`) is generated recursively by `sphinx.ext.autosummary`, so it
always tracks the package source; the generated pages live under `docs/generated/` (gitignored).

Status: **M0 spine + M0.5 content built and DONE; 60 frozen tests green (23 fixtures reproduce
their stored references).** See `.graphed/state.json` for live milestone state, `CLAUDE.md` for the
distilled spec, and `docs/design.rst` for the engineering walkthrough.
