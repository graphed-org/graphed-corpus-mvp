# CLAUDE.md — graphed-corpus

Defers to the root **`graphed-project/CLAUDE.md`**; the **project plan
(`graphed-project-plan-gated.md`) always wins.** This file distills **milestone M0.5** and **§A.8**.

## What this repo is

The **ground-truth requirements + functional fixtures** for `graphed`, distilled from real HEP
analyses. This is a **decompose / strong-model milestone** — output is **documents + runnable
fixtures, not framework code.** Every later test-author step consumes what lives here. **Extract
from the corpus; do NOT invent** the op surface or the tests from imagination.

> Guardrail: **no `graphed` implementation here** — requirements + reference data only.

## Deliverables (M0.5 Acceptance Contract)

1. **Required Operations Catalog** — `docs/requirements/ops_catalog.md`. Enumerate every array
   operation, selection/weight/category construct, systematic pattern (**weight vs kinematic**),
   correction type (correctionlib), and ML-inference pattern (ONNX/Triton) observed across the
   corpus. **Tag each entry** with (a) the corpus analysis it came from and (b) the milestone that
   must support it. If an op can't reasonably be supported in the MVP, record it as **"Phase 2"
   with a rationale** — never silently drop it.
2. **Canonical Analyses** — `tests/corpus/`. At minimum:
   - **ADL queries 1–8** (graded: simple column histogram → MET cuts → object selection →
     jet/lepton combinatorics → dilepton+MET+combinatorics);
   - a **reduced AGC ttbar slice** (fewer files);
   - a **TTGamma-style** selection + scale-factor + systematics slice.
   Each expressed **first as plain coffea/awkward** (the reference) producing a **stored reference
   histogram**, so later milestones assert `graphed` reproduces it **bit-for-bit**.
3. **Graph-bloat note** — compare the coffea-benchmark `coffea_2023_postrelease` (dask-awkward) vs
   `master` (virtual arrays) branches; **quantify the node-count explosion** `graphed` must avoid.
   This feeds **M4's reduction targets** (the O(10000)-node case, super-linear benchmark).

Fixtures live in a **dev-only shared location importable by all packages' test suites** (e.g.
`tests/corpus/`); **no published package**.

## Reference corpus (§A.8) — extract, do not imagine

- **ADL benchmarks** — `iris-hep/adl-benchmarks-index`; coffea impls in `CoffeaTeam/coffea-benchmarks`
  (branches `coffea_2023_postrelease` = dask-awkward, `master` = virtual arrays). 8 graded query
  tasks → the functional-test ladder for M3/M4/M5; the branch diff documents the bloat to avoid.
- **AGC CMS Open Data ttbar** — `iris-hep/analysis-grand-challenge` (`analyses/cms-open-data-ttbar`).
  The primary end-to-end fixture: ~9 processes × two regions (4j1b, 4j2b), process×variation axis,
  **weight systematics, JES/JER kinematic systematics that change selection AND observables,
  b-tagging scale factors, optional ONNX/Triton ML inference**, explicit preservation goal. Drives
  M7 + M9.
- **CMSDAS TTGamma long exercise** — `nsmith-/TTGamma_LongExercise` (with solutions). Teaching-grade
  full CMS ttbar+photon: photon/lepton selection, scale factors, systematics.
- **PocketCoffea** — `PocketCoffea/PocketCoffea` (+ Tutorials). Declarative skim → object
  calibration → preselection → categorization → weights → histograms; **shape variations re-run
  after skimming** (motivates systematics-as-axis, Phase 2). Note memory tactics (per-chunk parquet
  dumping; CartesianSelection beyond coffea's 64-category PackedSelection limit) as executor
  constraints.
- **boostedhiggs** — `cmantill/boostedhiggs`. Production boosted H→bb: large-R jets, substructure,
  triggers, corrections — jet-substructure + production-scale processor reference.

## Standards (bind the whole project)

Align with HEP standards, **invent no formats**: corrections via **correctionlib** (JSON), models
via **ONNX**, histograms via **UHI**, statistical models via **HS3**, environment via container
digest, datasets via IDs + content hashes. Determinism is the prerequisite for reproduction.

## Definition of Done (M0.5)

Coverage/benchmark gates are **N/A** (no framework code). The gate is **reviewer sign-off** that the
Catalog is **faithful to the actual repos** (spot-checked, not imagined), the **reference histograms
actually run and reproduce**, and **every catalog entry is mapped to a milestone** so nothing real is
left untested. Budget: iterations ≤ 6.
