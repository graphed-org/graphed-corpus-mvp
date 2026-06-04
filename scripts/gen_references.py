"""Generate the stored reference histograms for every canonical analysis.

Run once by the strong/human role to materialize the reference outputs the frozen tests compare
against. Deterministic: same dataset seed -> same references.
"""

from __future__ import annotations

from pathlib import Path

from graphed_corpus import (
    ADL_QUERIES,
    TTBAR_FIXTURES,
    TTGAMMA_FIXTURES,
    make_events,
    ttbar_region,
    ttgamma_region,
    write_reference,
)

REF_DIR = Path(__file__).resolve().parent.parent / "corpus" / "references"


def main() -> None:
    events = make_events()
    for name, fn in ADL_QUERIES.items():
        write_reference(REF_DIR / f"adl_{name}.json", fn(events))
    for name, (region, var) in TTBAR_FIXTURES.items():
        write_reference(REF_DIR / f"{name}.json", ttbar_region(events, region=region, variation=var))
    for name, var in TTGAMMA_FIXTURES.items():
        write_reference(REF_DIR / f"{name}.json", ttgamma_region(events, variation=var))
    print(f"wrote {len(ADL_QUERIES) + len(TTBAR_FIXTURES) + len(TTGAMMA_FIXTURES)} references to {REF_DIR}")


if __name__ == "__main__":
    main()
