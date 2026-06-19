# Parse-x: A Literature Review for the Deep Benchmark Framework

A NeurIPS-style academic literature review (~39 pages, 159 references) surveying prior art for each of the nine measurement dimensions defined by the Parse-x Deep Benchmark Framework. Researcher-not-advocate stance: prior work is named for what it measures AND what it does not measure relative to the framework.

## Versions

The review went through four independent revision passes; all are preserved in `docs/`.

| Version | What it adds | Verdict from reviewers |
|---|---|---|
| v1 | First draft (12 parallel research agents) | n/a |
| v2 | ICML + CTO + ABM-GTM + style-auditor review applied (104 em-dash + 30 tone fixes; 12 metadata-mismatch citation corrections) | ICML reviewer: REWORK; CTO + ABM-GTM: ACCEPT-WITH-CHANGES |
| v3 | All 7 deferred items cleared (corpus consolidation, Chandra dedup, foundational works added, LayoutLMv3 + OCRBench v2 reconciled, customer-name scan, HITL scan) | n/a (no fresh review pass) |
| **v4** | **Deep citation re-verification** (5 verifier agents covering 55 verifications); senior-academic critique documented but not auto-applied | Senior academic: REWORK with material methodological findings preserved verbatim in audit trail |

## Audit trail

Full audit trail with all reviewer findings: [`docs/audit-trail.md`](docs/audit-trail.md).

## Discipline

- Researcher-not-advocate; no winner pre-picked.
- Apples-to-apples scoring or labeled apples-to-oranges.
- Fine-tune-vs-zero-shot disclosure per cell.
- `results.zip` is HyperAPI deployed output and is never used as ground truth.
- Internal corpora numbers are not externalized.

## License

Content licensed under CC-BY-4.0. Code (synthesis scripts) under MIT.
