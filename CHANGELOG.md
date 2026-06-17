# Changelog

All notable changes to this literature review. Each version is a self-contained PDF/HTML preserved in `docs/`.

## v8 — 2026-06-16 (current)
**AAAI / NeurIPS-style academic copy-edit**: 136 verbatim (old, new) replacements applied across the document. Top categories: first-person-plural overuse (9), colloquialisms (8), informal phrasing (7), comma splices (7), filler removal (6), promotional adjectives (5), informal connectives (5), heading-punctuation consistency (5). Reference formatting harmonised to `[N, M]` and `[N]-[M]`. No content additions. v8.1 sub-pass restored verified arXiv ID for [6] PaddleOCR-VL-1.5 and rephrased [136] Microsoft Azure release-cadence footnote.

## v7 — 2026-06-16
**MUST-ADD content + NeurIPS-shape**: added Extend Parse 2.0 + RealDoc-Bench [188, 189]; xAI Grok 4/4.3 [190]; Meta Llama 4 Scout / Maverick / Behemoth [191]; invoice IDPs Mindee / Veryfi / Affinda / Klippa [192-195]; reading-order metric named explicitly (Spearman footrule) with field alternatives (Kendall tau, REDS, LOER) and citations [196, 197]. Added §1.1 Contributions list, §4 Limitations promoted from §3 subsections, §5 Broader Impact. Definitions: GTRM flagged as Parse-x convention; 7 first-use acronym glosses (VLM, VRD, MoE, KIE, NED, HTR, IAA).

## v6 — 2026-06-16
**Coverage extension** (4 dedicated coverage agents): table-recognition + VLM-era doc-AI surveys (Shi 2023; Ding 2024 / 2025; Barboule 2025; Somvanshi 2024); industrial IDP landscape (UiPath, Hyperscience, Rossum, ABBYY, Microsoft 365 doc processing, Google Document AI, AWS Textract); handwritten document recognition (IAM, TrOCR, 2024-25 HTR surveys); math formula extraction (Im2Latex, CROHME, LaTeX-OCR) + document classification (RVL-CDIP, Tobacco-3482). 4 new mini-sections (§2.5.1, §2.8, §2.9, §2.10), 21 new references [167]-[187].

## v5 — 2026-06-16
**Senior-academic critique applied**: MECE re-framing (9 dimensions → 7 measurement dimensions + 2 stratification overlays); contribution claim repositioned as industrial framework + curated dataset registry, citing HELM, BIG-bench, DUE, Cui 2021, Subramani 2020; D-LAYOUT first-framework claim softened with PaIRS provenance note; D-DOWNSTREAM novelty acknowledged with Dror 2018 and Ragas 2024 prior art; D-BBOX overlap with D-LAYOUT acknowledged; new §3 subsections: Scope limitations, Reproducibility caveats, Statistical floor (n=10 → ±0.15 CI95), Evaluator-LLM bias, Cross-engine fairness. 8 new bibliography entries [159]-[166].

## v4 — 2026-06-16
**Deep citation re-verification** (5 verifier agents covering 55 verifications): 15 INACCESSIBLE re-fetched (14 confirmed, 1 corrected); 3 NOT-FOUND deep-searched (3 corrected, all real papers found); 5 v3-new refs revalidated (all confirmed); 20-ref CONFIRMED spot-check (all held); 12 META-correction recheck (9 confirmed, 2 corrected, 1 still-unverified). 6 further citation corrections applied. Senior-academic critique attached as documented residual.

## v3 — 2026-06-16
**All 7 deferred items cleared**: corpus consolidation (FUNSD / CORD / SROIE / SAVIOR into App B.1); Chandra description deduplicated; foundational works added (LayoutXLM, UDOP, TILT, Zhang-Shasha); LayoutLMv3 CORD F1 = 97.46 verified (Table 1, official 800/100 split), SROIE 95.24 reattributed to LayoutLM v1 [76b]; OCRBench v2 canonical counts harmonised (10,000 QA / 23 tasks / 31 scenarios; first author Fu); customer-name scan (Eskimo, CJ Logistics redacted to `[customer omitted]`); HITL scan (0 hits).

## v2 — 2026-06-16
**Multi-reviewer audit applied**: 4 reviewer roles (ICML-tier senior, CTO-org technical, ABM-GTM brand, copy-edit style auditor) + 4 citation cross-check batches. 154 references verified against arXiv, HuggingFace, GitHub, conference pages. 104 em-dashes + 30 tone fixes; 12 metadata-mismatch citation corrections applied to bibliography; 15 INACCESSIBLE tagged; 3 NOT-FOUND tagged; advocacy language softened; abstract overclaim about citations honest-framed; D-LAYOUT circular-novelty acknowledged; §3 Discussion audit-note paragraph added.

## v1 — 2026-06-16
**Initial draft**: 12-agent parallel research workflow produced first-pass coverage for the seven framework dimensions, the two stratification overlays (D-DOC-QUALITY, D-LANG), and three appendices (Model Lineage, Datasets & Contamination, Vendor & API Pins). 154 unique citations after deduplication of 190 agent-emitted references; NeurIPS-style HTML rendering with 154 numbered references; PDF via weasyprint.

---

See the full audit trail at [docs/audit-trail.md](docs/audit-trail.md) for the complete reviewer findings, methodology details, salvaged workflow outputs, and honest residuals at each revision.
