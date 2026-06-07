# Contributing to graphed-corpus

Part of the `graphed` project, governed by the gated three-role pipeline. The root
[`graphed-project/CLAUDE.md`](https://github.com/graphed-org/graphed-project-mvp) and the project plan
(`graphed-project-plan-gated.md`) are authoritative; the plan always wins.

## What this repo is

The **ground-truth requirements + runnable fixtures** (milestone M0.5). Output is **documents +
deterministic fixtures with stored reference outputs**, not framework code. Extract from the A.8
corpus — do **not** invent the op surface or the tests.

## Integrity rules — NON-NEGOTIABLE (plan A.7 / B.6)

Violations are severe and PAUSE the entire run. **Never**:

- edit, delete, `skip`, `xfail`, or weaken any test under `tests/frozen/**`;
- hand-edit a stored reference in `corpus/references/**` to make a test pass — references are
  regenerated only by `scripts/gen_references.py` from the analysis code;
- relax CI gate config;
- blanket-apply `# type: ignore` / `except: pass`.

If a frozen test or reference looks wrong, **do not route around it** — file a Test Dispute under
`.graphed/<Mx>/disputes/<test_id>.md` and stop.

## The catalog and the fixtures stay in lock-step

`docs/requirements/ops_catalog.md` must keep mapping every fixture family and required op to a
milestone; `tests/frozen/m05/test_catalog.py` enforces this. Anything the corpus needs but the MVP
can't support is recorded as **Phase-2 with a rationale**, never silently dropped.

## Local gates (run before pushing)

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev,docs]"
ruff check . && ruff format --check .
mypy
pytest --cov=graphed_corpus --cov-branch --cov-report=term-missing
python scripts/gen_references.py            # must produce NO diff (deterministic fixtures)
sphinx-build -W -b html docs docs/_build/html
```

CI re-runs these on the plan A.5 matrix; the matrix is the gate of record. Reference equality is
checked per-platform by `tests/frozen/m05/test_fixtures_reproduce.py`.
