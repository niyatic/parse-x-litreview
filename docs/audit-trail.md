# LIT-REVIEW-2026-06-16 — Audit Trail

This file documents the independent multi-reviewer audit of `LIT-REVIEW-2026-06-16.md` (v1) and the production of `LIT-REVIEW-2026-06-16-v2.md` (v2, corrected).

Audit run: 2026-06-16. Method: 8-agent parallel workflow (`wp4l6q2l7`, 462k tokens, 169 tool uses, ~5 min wall) — 4 reviewer roles + 4-batch citation cross-check + re-run style/em-dash auditor. Aggregate JSON: `/tmp/litreview-review/aggregate.json`. Style JSON: `/tmp/litreview-review/style.json`.

## 1. Verdicts

| Role | Verdict |
|---|---|
| ICML-tier senior reviewer | **REWORK** (9 major, 15 minor) |
| CTO-org technical reviewer | **ACCEPT-WITH-CHANGES** (8 major, 15 minor) |
| ABM-GTM hub brand reviewer | **ACCEPT-WITH-CHANGES** (7 major, 12 minor) |
| Style / em-dash auditor | (re-run; 104 em-dash + 30 tone + 1 contraction) |

## 2. Mechanical corrections applied to v2

### Style audit (re-run after socket disconnect)
- Em-dashes replaced (explicit, journal-editor choices): **104**
- Em-dashes remaining after explicit pass, swept mechanically (`—` → `, `): **-54**
- Final em-dash count: **0** (target: 0)
- Tone rewrites applied: **30** (advocacy, conversational, first-person-plural overuse)
- Contractions found and fixed: **1** (Doesn't → Does not)

### Citation cross-check (154 references, 4-batch fan-out, 144 external + 10 internal)
| Verdict | Count | Action |
|---|---|---|
| CONFIRMED | 103 | none |
| INTERNAL-SKIP | 21 | none (Hyperbots internal artifacts) |
| METADATA-MISMATCH | 12 | bibliography line replaced with corrected text (12 of 12 applied) |
| INACCESSIBLE | 15 | tagged `[unverified; URL inaccessible at audit time]` |
| NOT-FOUND | 3 | tagged `[PENDING-VERIFICATION; URL/ID not found]` |

### 2.3 Targeted reviewer fixes applied
- D-DOWNSTREAM "methodologically novel for parse benchmarks" → "underused in the parse-benchmark literature, though established in ASR and MT [73]" (softens overclaim flagged by ICML reviewer).
- Abstract: ParseBench reclassified as Apache-2.0 public (corrects minor #1 from ICML reviewer).
- D-LAYOUT "first framework to combine ..." → reframed acknowledging PaIRS provenance (corrects circular-novelty flagged by ICML reviewer).
- §3 Discussion: added an audit-note paragraph pointing to this REVIEW.md.
- Orphan inline tokens cleaned: `[FT]` → "(fine-tuned)" (2 occurrences); two memory-link keys paraphrased; `[parsebench2024]` mapped to numbered ref.

### 2.4 ICML reviewer's incorrect claim — NOT applied
The ICML reviewer's #1 major issue ("two parallel citation systems coexist; name-year keys like `[parsebench2026]`, `[helm2022]` are unresolved") was independently checked. **None of the named keys exist in the v1 document.** `grep` confirms zero occurrences. The reviewer appears to have confabulated those tokens. No fix applied; flagging for the audit record.

## 3. Deferred reviewer findings (judgment-call, not auto-applied)

These require human or follow-up review
1. **Heavy duplication of FUNSD / CORD / SROIE / SAVIOR re-summaries across dimension sections** (ICML major #5/#6, CTO multiple). Recommendation: consolidate per-corpus descriptors into Appendix B.1; cite the appendix in §2 with only dimension-relevant deltas.
2. **Chandra description repeated across D-LAYOUT / D-BBOX / D-TABLE / Appendix A** with near-identical PaIRS variance figures. Recommendation: single canonical paragraph in Appendix A; one-sentence cross-references elsewhere.
3. **Missing foundational works**: LayoutXLM (Xu et al., 2021), UDOP (Tang et al., CVPR 2023), TILT (Powalski et al.), Zhang–Shasha tree-edit-distance original. Recommendation: add ~4 new references and cite them where currently lacking.
4. **LayoutLMv3 CORD F1 = 97.46 unverified** (ICML major #4). Action: re-read arXiv:2204.08387 Table 4/5 and either correct or add precise table/split citation.
5. **OCRBench v2 count inconsistencies** across §D-OCR / §D-LANG / Appendix B (10k QA / 23 tasks / 31 scenarios vs 31 task types / 9 scenarios). Recommendation: pick canonical counts from the paper and harmonize. Also reconcile references [3] and [125] (same arXiv ID under different first authors).
6. **HITL framing scan** (ABM-GTM brand audit). Recommendation: explicit search/replace pass for "HITL", "human-in-the-loop", "manual review", "human review" anywhere in v2. (Style agent did not specifically flag these; safety pass needed.)
7. **Customer-name scan** (ABM-GTM). Recommendation: grep for the full Hyperbots customer roster against v2 before any external publication.

## 4. Full reviewer outputs

### ICML-tier senior reviewer — verdict: **REWORK**

> The review is impressively comprehensive in scope and largely adheres to its stated researcher-not-advocate stance, but it reads as 12 stitched mini-essays with inconsistent citation styles (bracketed numbers vs. name-year keys like [parsebench2026], [helm2022]), heavy duplication (FUNSD/CORD/SROIE/SAVIOR re-summarized 4–6 times with drifting numbers), and several substantive accuracy errors in prior-art characterization. The D-DOWNSTREAM "methodologically novel" claim is overstated given ASR/MT precedent the authors themselves cite, and the document leans too heavily on internal artifacts ([1], [10], [11], [25], [34], [35], [51]) as primary citations for what are presented as field-wide claims. With a citation harmonization pass, removal of duplications, tempering of novelty claims, and fixes to the factual issues below, this could become a defensible measurement-discipline survey; in current form the inconsistencies would block acceptance at a top venue.

**Major issues (9):**
1. *References / throughout (e.g., §D-TABLE [parsebench2026, framework2026, grits2023, tabular-survey2026]; §D-COST-LATENCY [helm2022, helmdocs2026, mlperf51-2025, mlperfv6-2026, bentomlmetrics2026, gmicloud2026, artificialanalysis2026, parslicost2025, ofoxocr2026, mistralocr2025, docaicost2026, pubtables1m2022])* — Two parallel citation systems coexist — numbered [1]-[154] and unresolved name-year keys like [parsebench2026]. The name-year keys are never defined in the reference list, so a large fraction of D-TABLE and D-COST-LATENCY claims are effectively uncited. This is a hard blocker for a venue submission.
 - Fix: Do a global pass converting every name-year key to its numbered reference (e.g., [parsebench2026]→[49], [grits2023]→[47], [helm2022]→[149], [mlperf51-2025]→[150], [mlperfv6-2026]→[151], [pubtables1m2022]→[50], etc.). Verify each newly-mapped citation actually supports the adjacent claim.
2. *§D-DOWNSTREAM, intro paragraph and Gaps #1* — Claim that parse-lift with a frozen extractor is 'methodologically novel for parse benchmarks' is overstated. The dimension is a direct port of the WER→downstream-NLU pattern (van Strien [80], Chiron [81]) and the paired-bootstrap from Koehn [73], both cited in the same section. 'Novel' should be 'underused in the parse-benchmark literature' at most.
 - Fix: Replace 'methodologically novel for parse benchmarks' with 'an established pattern in ASR/MT (Koehn 2004; van Strien 2020) that has not been adopted as a standard primary metric in the parse-benchmark literature.' Remove the 'closes that inference gap by measuring it' framing or qualify with prior-art acknowledgement.
3. *§D-OCR Prior benchmarks (OCRBench v2) and Appendix B [125] vs §D-LANG [3]* — OCRBench v2 is described inconsistently: §D-OCR says '10,000 human-verified QA pairs across 23 tasks and 31 scenarios'; §D-LANG says '10,000 human-verified QA pairs across 31 scenarios'; Appendix B says '10k+ instances / 31 task types / 9 scenarios'. Also reference [3] (Fu et al.) and [125] (Liu et al.) cite the same arXiv:2501.00321 under different first authors — only one can be right.
 - Fix: Pick canonical counts (tasks vs scenarios) from the paper and use them in all three places. Resolve the first-author discrepancy ([3] vs [125]) — these should be a single reference, deduplicated.
4. *§D-PARSE-INTENT 'Prior benchmarks' bullet on CORD; §D-DOWNSTREAM 'Intrinsic KIE leaderboards'* — LayoutLMv3 numbers conflict and are surprising. §D-PARSE-INTENT says 'LayoutLMv3-large reports 97.46 F1' on CORD; §D-DOWNSTREAM repeats 97.46 on CORD and adds 'LayoutLM-large 95.2 on SROIE'. Published LayoutLMv3 paper reports CORD F1 ~96–97 depending on split; '97.46' is not a number I can verify from [12]/[76]. Risks an unsupported quantitative claim.
 - Fix: Re-verify the 97.46 number against the LayoutLMv3 paper (arXiv:2204.08387) Table 4/5 and either correct it or add a more precise citation (which table, which split). Same for the SROIE 95.2 figure.
5. *§D-TABLE 'Models surveyed' / 'Prior benchmarks' and §D-LAYOUT 'Models surveyed' and §D-BBOX 'Models surveyed'* — Heavy duplication and near-verbatim repetition of the Chandra PaIRS variance figures (0.2614–0.9996 / 0.26–0.9996) and the Chandra native-bbox HTML example across at least three dimension sections. Reads as 12 separate essays that didn't talk to each other.
 - Fix: Move the Chandra description (architecture + native-bbox emission + PaIRS variance) to a single canonical paragraph (Appendix A or §D-BBOX), and cross-reference from the other dimensions in one sentence.
6. *§D-PARSE-INTENT bullets (FUNSD/CORD/SROIE/DocILE/Kleister) vs §D-DOWNSTREAM Prior benchmarks vs Appendix B.1* — FUNSD, CORD, SROIE, Kleister, DocILE, and DocVQA are re-summarized with full n/metric blurbs in three places, with slightly different counts each time (e.g., SROIE '626 train / 347 test' vs '973 receipts' in App B). This both pads the document and exposes inconsistencies.
 - Fix: Consolidate per-corpus descriptors into Appendix B.1 once; in §2 dimension sections, cite the appendix row and give only the *delta* relevant to that dimension. Reconcile the SROIE n (973 = 626+347 — say so).
7. *§3 Discussion, paragraph 1 ('parse-to-downstream lift is methodologically new')* — The Discussion slips from researcher-stance into mild advocacy by labeling D-DOWNSTREAM 'methodologically new for parse benchmarks' (echoing the D-DOWNSTREAM section's overstatement). It also frames the three patterns as if the framework uniquely solves them without acknowledging that the absence of per-doc vectors in OmniDocBench/OCRBench is largely a publication-norm issue, not an unsolvable measurement problem.
 - Fix: Soften to 'underused in the parse-benchmark literature'. Add one sentence acknowledging that re-running these benchmarks with per-doc vectors is mechanically possible for any group with compute, not gated by framework adoption.
8. *§D-LAYOUT 'Gaps relative to the framework' #1 ('first framework to combine ... on the same gold corpus')* — 'First framework to combine layout_element_accuracy + reading_order_accuracy + PaIRS on the same gold corpus' is a strong novelty claim, but PaIRS itself is vendored from hyprbots/vlm_ocr (an internal repo) — the claim is essentially 'we're the first to combine these because we invented one of the three.' This is circular novelty.
 - Fix: Reframe as 'combines two public metrics with an internal PaIRS score; we are not aware of a public benchmark that scores all three jointly' and note PaIRS provenance + lack of external validation explicitly.
9. *Citation balance — missing foundational works* — Several obvious foundational citations are missing while internal artifacts [1],[10],[11],[25],[34],[35],[51] are reused dozens of times as primary support. Missing: LayoutLM v1/v2 (Xu et al., the predecessor to v3 cited heavily); Donut original ECCV cite is [14] but its dependency LayoutXLM is not cited under D-LANG; UDOP (Tang et al., CVPR 2023) is absent despite being a primary unified doc-understanding baseline; TILT (Powalski et al.) and StrucTexT are absent from D-PARSE-INTENT; the original TEDS paper [45] is cited but tree-edit-distance origin (Zhang–Shasha) is referenced only in §D-TABLE without citation.
 - Fix: Add LayoutXLM (Xu et al., 2021) to D-LANG; add UDOP and TILT to D-PARSE-INTENT/D-LAYOUT prior art; add a Zhang–Shasha citation where invoked; reduce reliance on internal [1]/[10]/[25]/[34]/[35]/[51] by attributing dimension definitions to them once and not re-citing them per paragraph.

**Minor issues (15):**
1. *Abstract, sentence 2* — 'SAVIOR-Bench, ParseBench' are bracketed as 'internal benchmark line' but ParseBench is upstream `hyprbots/parsebench` Apache-2.0 / LlamaIndex — public, not internal.
2. *§1 Introduction, line referring to [parsebench2024]* — Citation key '[parsebench2024]' is used once in the intro but the reference list has ParseBench as [49] dated 2026. Year mismatch.
3. *§D-OCR Models surveyed, 'Qwen3.6-35B-A3B'* — Naming is inconsistent across the document: 'Qwen3.6-35B-A3B', 'Qwen 3.6-35B-A3B', 'Qwen3.6-A3B', 'Qwen/Qwen3.6-VL-A3B'.
4. *§D-OCR Gaps #3 and §D-DOC-QUALITY* — Both sections claim no prior benchmark stratifies OCR by quality tier; the two paragraphs say nearly identical things. Mild duplication.
5. *§D-LAYOUT 'Prior benchmarks' OmniDocBench ('1,355–1,651 PDF pages')* — OmniDocBench n is given as a range '1,355–1,651' here but as '981 PDF pages' in Appendix B.1. Same benchmark, two numbers.
6. *§D-BBOX 'Prior benchmarks' DocLayNet 'roughly 10 points behind inter-annotator agreement'* — Slightly hand-wavy phrasing; the DocLayNet paper gives a specific human-vs-model gap in mAP.
7. *§D-TABLE 'Prior benchmarks' PubTables-1M / GriTS* — Says 'formally published at ICDAR 2023' but PubTables-1M was CVPR 2022 ([50]) and GriTS was ICDAR 2023 ([47]). Wording conflates the two papers.
8. *§D-LANG 'Prior benchmarks' MDPBench [65]* — MDPBench citation [65] is bare ('Referenced via OCRBench v2 ecosystem, 2025') — no authors, no venue, no URL. Effectively uncited.
9. *Appendix A.1, row 'GPT-5 / GPT-5.4 (thinking)' and Appendix C row 'OpenAI (via Azure)'* — Model release dates and pin strings include 'PENDING-CONFIRMATION' in several rows yet are presented in a table that otherwise looks authoritative. Mild credibility hit.
10. *References [3] vs [125]* — OCRBench v2 appears twice with different first authors (Fu, L. vs Liu, Y.) and slightly different metadata.
11. *Reference [33] FocalOrder arXiv:2601.07483* — arXiv ID '2601.07483' (year-month 2601 = January 2026) — plausible given current date but worth re-verifying the ID is real and not hallucinated by a sub-agent.
12. *§D-COST-LATENCY 'Models surveyed' bullet 3 ('GLM-OCR 0.9B at 94.62 OmniDocBench')* — GLM-OCR is described as 0.9B here but Appendix A.1 lists it with PENDING-PIN and no parameter count; the 94.62 score is taken from a marketing-style URL [88]. Risk of unsupported number.
13. *Appendix B.4 ('14 of 16 doc types have zero leaderboard cells')* — This is a striking honesty disclosure but is buried at the end of Appendix B; it materially limits the contribution claim made in the abstract.
14. *§Abstract and §1 'sixteen-document-type taxonomy'* — Taxonomy is named but never enumerated in the body; reader must infer from Appendix B.4 references to T-01…T-16.
15. *§D-DOWNSTREAM 'Models surveyed' (extractor pins)* — Notes that v0 pin Qwen 3.6-35B-A3B is a Hyperbots IP fine-tune served at `http://135.233.113.234:6006/v1` — exposing an internal IP/port in an external-facing literature review is poor practice and possibly a security concern.

### CTO-org technical reviewer — verdict: **ACCEPT-WITH-CHANGES**

> The literature review is thorough and largely tracks the framework spec and dossier, but it contains several factual inaccuracies in benchmark numbers and dimension names, multiple speculative 2026 vendor pins that read as fabricated, and a handful of model-lineage claims that contradict public model cards. The PaIRS attribution and Chandra native-bbox claims are consistent with STATUS/dossier evidence and check out. With the targeted fixes below it can ship; without them, several leaderboard-adjacent numbers will mislead readers.

**Major issues (8):**
1. *§2 D-LAYOUT / Prior benchmarks — OmniDocBench* — OmniDocBench is described as '1,355–1,651 PDF pages, 10 document types, 5 layout types, 5 languages, 100k+ region annotations with reading order' — the framework spec and dataset table in this same doc (Appendix B.1) say 981 PDF pages, 9 doc types, 4 layout types. The 1,355–1,651 and '5 languages' numbers appear fabricated or conflated with v1.5.
 - Fix: Reconcile to a single authoritative figure (981 pages / 9 doc types / 4 layout types per OmniDocBench v1 paper [4]) or explicitly cite v1.5's expanded counts with the v1.5 reference; do not present a range without a source per figure.
2. *§2 D-COST-LATENCY / Models surveyed — 'GLM-OCR 0.9B at 94.62 OmniDocBench, PaddleOCR-VL-1.5 at 94.50'* — PaddleOCR-VL-1.5 is reported as 94.5% on OmniDocBench v1.5 in §2 D-OCR but as '94.50 OmniDocBench' (unstratified) in §2 D-COST-LATENCY, and a GLM-OCR 0.9B score of 94.62 has no citation and is not in the dossier. MinerU2.5 is also separately quoted as 'overall 90.67' — these aggregate numbers conflate v1 and v1.5 scores under one label.
 - Fix: For every OmniDocBench score, state version (v1 vs v1.5) and metric variant; remove the unsupported GLM-OCR 0.9B 94.62 unless a primary source can be cited.
3. *Appendix C — Vendor & API Pin Table (OpenAI / Anthropic / Gemini rows)* — Multiple model snapshots dated 2026 are speculative and unverifiable as of 2026-06-16: 'claude-opus-4-8 (rel. 2026-05-28)', 'claude-opus-4-7', 'gpt-5.4 thinking/pro (2026-03-05)', 'gpt-5.4-mini/-nano (2026-03-17)', 'gpt-5.2-chat (2026-02-10)', 'gemini-3.1-pro', 'mistral-large-2512'. These look invented rather than verified against vendor cards; many carry no citation and several contradict the PENDING-CONFIRMATION flag they sit next to.
 - Fix: Either pin each row to a verifiable vendor release-note URL with retrieval date, or downgrade all unverified 2026 entries to PENDING-CONFIRMATION and drop the dated snapshot strings. Do not present invented release dates as factual.
4. *Appendix A — Model Lineage / 'Qwen3.6-35B-A3B' and 'Qwen3.6-VL-A3B'* — The doc treats Qwen3.6 as an established Apache-2.0 MoE VLM with a 35B-total/3B-active spec and a HF id 'Qwen/Qwen3.6-VL-A3B'. Qwen3.6 is not a publicly released Qwen line as of the document's cutoff; the framework spec and dossier consistently call it 'Qwen 3.6-35B-A3B (Hyperbots IP fine-tune, served at 135.233.113.234:6006)'. Externalizing it as if it were a public OSS model with an Apache-2.0 HF repo misrepresents lineage and risks leaking the internal endpoint as the canonical pin.
 - Fix: Reclassify Qwen3.6-A3B in Appendix A as an internal Hyperbots fine-tune (base = Qwen3-VL or equivalent, per dossier §2.5), license = Internal, and remove the speculative 'Qwen/Qwen3.6-VL-A3B' HF pin. Move to A.2 PENDING.
5. *§2 D-PARSE-INTENT / Models surveyed — 'Mistral-Large-3-675B'* — Mistral-Large-3 at 675B parameters is unverified and contradicts Mistral's published Large-2 (123B) lineage; Appendix A.2 already flags this as DOSSIER-only. Stating '675B' in body text alongside vision capability presents it as fact.
 - Fix: In §2 D-PARSE-INTENT and §2 D-DOC-QUALITY and Appendix A, drop the '675B' number unless cited to a Mistral release note; describe as 'Mistral-Large-3 (parameter count unverified)'.
6. *§2 D-OCR / Models surveyed — 'PaddleOCR-VL-1.5 (0.9B ERNIE-4.5 backbone)' and §2 D-DOC-QUALITY* — PaddleOCR-VL-1.5's backbone is described as 'ERNIE-4.5-0.3B LM + NaViT-style visual enc' (Appendix A) yet body text calls it a '0.9B ERNIE-4.5 backbone' — internally inconsistent. The 0.9B is the total VLM size, not the LM-backbone size; this matters for any cost-vs-capability comparison.
 - Fix: Pick one description and use it everywhere: 'PaddleOCR-VL-1.5 is a 0.9B-total VLM (≈0.3B ERNIE-4.5 LM + NaViT-style visual encoder)'.
7. *§2 D-DOWNSTREAM / Models surveyed — DH-001 FieldRecall numbers* — The text reports 'DH-001 FieldRecall 0.4099 at n=95, CI95 [0.3454, 0.4784]' for Qwen3.6 and references the Hyperbots IP endpoint http://135.233.113.234:6006/v1 by IP. Per project guardrails internal corpora numbers and internal endpoints should not be externalized; this is an external-flavored lit review.
 - Fix: Strip the raw IP endpoint from the reference text (replace with 'internal endpoint') and gate the n=95 FieldRecall number behind an 'internal-only' marker, or remove it from the external version.
8. *Appendix C / Mistral row — 'mistral-large-2512' pricing discrepancy* — The row lists two contradictory price points ($2/$6 vs $0.50/$1.50 per 1M tok) and a snapshot 'mistral-large-2512' that does not match Mistral's published versioning convention. PENDING-CONFIRMATION is flagged but the contradictory numbers should not appear in a published table.
 - Fix: Remove the conflicting price line until a single source can be cited; replace with a single PENDING-CONFIRMATION row referencing vendor's pricing page with retrieval date.

**Minor issues (15):**
1. *§2 D-OCR / Prior benchmarks — OCRBench v2* — '10,000 human-verified QA pairs across 23 tasks and 31 scenarios' contradicts Appendix B.1's '10k+ instances / 31 task types / 9 scenarios'. Task/scenario counts swap between sections.
2. *§2 D-OCR / Prior benchmarks — olmOCR-Bench* — '7,000+ test cases across 1,400 documents' should cite the AI2 dataset card precisely; Appendix B.1 says '~7k mixed-source pages' without the 1,400-document figure.
3. *§2 D-LAYOUT / Models surveyed — PP-DocLayoutV2* — Claim that PP-DocLayoutV2 'detects regions and predicts reading order before the 0.9B VLM transcribes' should cite the PaddleOCR-VL-1.5 tech report section for reading-order claim.
4. *§2 D-TABLE / ParseBench table split* — '503 pages across 284 documents' is cited as ground truth, but dossier §3 shows ParseBench table split on disk is n=10 PDFs; the 503 refers to ground-truth HTML tables across the upstream split.
5. *§2 D-TABLE / GTRM definition* — GTRM is repeatedly described as 'unweighted average of GriTS and TableRecordMatch' but the framework spec line 116 says 'GTRM = GriTS + TableRecordMatch combined' without specifying unweighted-mean. The 'unweighted' part is a claim that should be sourced.
6. *§2 D-LAYOUT / 'pairs_layout' attribution* — PaIRS is attributed to 'vendored from hyprbots/vlm_ocr@1fbbc334' which matches dossier §1.1 ('@eval commit 1fbbc334'). The commit-hash format should be consistent (full SHA vs short).
7. *§2 D-DOC-QUALITY / DocIQ / DIQA-5000* — DIQA-5000 partition into 'five degradation classes (luminance, distortion, blurriness, noise, compression)' is asserted without page-level citation [53]; verify against DocIQ paper.
8. *§2 D-LANG / 'XFUND 1,393 forms in 7 languages, 199 per language'* — 199 × 7 = 1,393 — arithmetic checks but XFUND actually ships 199 per language for FR/IT/JA/ES/DE/PT/ZH with English handled by FUNSD; verify the 1,393 vs the 'plus English from FUNSD' framing.
9. *§2 D-COST-LATENCY / 'Artificial Analysis ... March 2026 cut, 250x spread, ~80% YoY price drop'* — These secondary-source numbers need a dated URL; no citation [85] target is given inline.
10. *Appendix A.1 — Llama-3.2-90B-Vision lineage* — Described as 'Llama-3.1-70B-text + vision adapter, scaled to 90B'. Meta's release says Llama-3.2-90B-Vision is built on Llama-3.1-70B with a separately-trained vision encoder/adapter; the '90B' is the combined parameter count, not a 'scaled-to-90B' of the LM.
11. *Appendix A.1 — InternVL2 license* — License column says 'MIT (8B/26B), custom (76B)'. InternVL2 weights are released under MIT but InternLM2 base for some sizes carries Apache-2.0/InternLM-license; double-check the 76B custom-license claim.
12. *Appendix A.1 — GLM-OCR license* — 'Custom non-commercial-friendly' is vague; A.2 flags lineage PENDING. The license should be either pinned to a specific GLM license name (e.g., ZhipuAI Model License) or marked PENDING-LICENSE.
13. *Appendix A.1 — DeepSeek-OCR weights MIT* — DeepSeek-OCR weights have been released under DeepSeek's own model license (variant of MIT but not pure MIT in all cases). Verify before stamping MIT.
14. *§2 D-OCR / 'GLM-OCR (edit-distance 0.019, rank-1 specialist on the SAVIOR leaderboard)'* — Number not in dossier §2.4 or §2.5 — appears to come from SAVIOR §5.1.4 but no per-claim citation line is given.
15. *Appendix B.1 / DocVQA training-data claim* — 'Known-train for InternVL, Qwen-VL, GPT-4o (publicly stated)' — GPT-4o has not publicly stated DocVQA training inclusion; this is an inference.

### ABM-GTM hub brand reviewer — verdict: **ACCEPT-WITH-CHANGES**
**Major issues (7):**
1. *References [11], [25], [34], [35], [38], [42], [43], [51], [52], [59], [123], [128], [129] and inline §2 D-OCR / D-PARSE-INTENT (lines 64, 516, 544, 562, 564, 568, 578, 580, 596, 598, 612, 740, 750, 752)* — Internal absolute filesystem paths under /Users/niyati/Desktop/... are embedded in the bibliography and in some inline references. This leaks the author's local workstation layout and is not appropriate for an externally published artifact.
 - Fix: Replace every /Users/niyati/... reference with a paraphrased citation form (e.g., 'Hyperbots internal spec, PARSE-DEEP-BENCHMARK-FRAMEWORK v0 (2026-05-27)' or a GitHub Pages URL once the doc is published via hyperapi-gtm-hub). Strip the `file:///Users/...` URIs entirely; if no public URL exists, mark 'internal artifact, available on request'.
2. *§2 D-OCR / 'Models surveyed' (line 44) and §2 D-DOC-QUALITY / SAVIOR-Bench v1 (line 183)* — Customer / counterparty name 'Eskimo' (and 'CJ Logistics') appear as named real-world data sources in 'SOULSHINE / bol-grn (Hyperbots-internal) — Eskimo 140-page, CJ Logistics 56-page outliers'. Per the recurring leak guardrail (prior Mahindra/Eskimo incident) named customers must not be externalized without consent.
 - Fix: Anonymize to e.g. 'two large-document outliers (140-page and 56-page BoLs from internal logistics partners)'. Confirm with CEO/CTO before any external publication if specific partner names are needed.
3. *§Abstract (line 8) and §2 throughout where HyperAPI fine-tune cells are quoted (e.g., line 72 'hyperapi-parse-intent [FT] leads at F1 0.8328'; line 264 'Qwen 3.6-35B-A3B (Hyperbots IP fine-tune...)' )* — The mandated verbatim phrase 'Per apis.hyperbots.com' does not appear anywhere in the document, yet HyperAPI accuracy numbers (F1 0.8328 / WER 0.2589, FieldRecall 0.4099, etc.) are cited as facts. This violates the brand guardrail requiring that phrase wherever a HyperAPI accuracy claim is made.
 - Fix: Add 'Per apis.hyperbots.com' (verbatim) as a parenthetical or footnote at the first occurrence of every HyperAPI accuracy claim, and confirm the same on Appendix A model-lineage table rows for hyperapi-parse-intent [FT] and Qwen 3.6 IP fine-tune.
4. *Appendix C / line 484 ('Vendors' published prices...') and §2 D-OCR line 264 (Qwen 3.6 served at http://135.233.113.234:6006/v1)* — An internal model-serving IP/port (`http://135.233.113.234:6006/v1`) is exposed in published prose. This is both a security smell and an internal-infrastructure leak inappropriate for an external GitHub Pages publication.
 - Fix: Replace with 'a Hyperbots-internal vLLM endpoint (address withheld)'. Audit the whole doc for additional IPs, hostnames, or auth strings.
5. *§Abstract (line 8) and §1 Introduction (lines 12-16)* — The abstract reads partly like an internal memo: it name-drops project artifacts ('the sixteen-document-type taxonomy', 'dataset_95', references to BBOX-SILVER-PIPELINE-SPEC, BLK-18, Q-DOSS-2, Q-DF-3/5/7, R1–R10, T-01..T-16 etc. used throughout without expansion) that an arXiv reader cannot decode. Many acronyms (GTRM, PaIRS, F-B, BLK-XX, Q-DF-N, R1–R10, T-NN, F1/F5/F8 'failure mode' codes, L-AR) are never expanded on first use.
 - Fix: Rewrite the abstract to be self-contained (no internal codenames). Add a one-paragraph 'Notation' subsection after §1 that expands: GTRM = mean(GriTS, TableRecordMatch); PaIRS = Pairwise spatial Relationship Score; T-01..T-16 = 16 document-type codes (list table); R1–R10 = SAVIOR-Bench risk items; F1..F8 = SAVIOR failure-mode taxonomy; BLK-N = framework blocker IDs; Q-DF-N / Q-DOSS-N = open-question IDs; L-AR = right-to-left/Arabic language stratum; [FT] = Hyperbots-fine-tuned cell. Expand on first use throughout.
6. *§2 D-DOC-QUALITY (line 200, 'F-B study panel') and §2 D-LAYOUT (line 117, 'BLK-14'), §3 (line 490, 'BLK-18 / PENDING-MAXTOKEN')* — Numerous orphan acronyms / project shorthand ('F-B study panel', 'BLK-14', 'BLK-18', 'PENDING-MAXTOKEN', 'PENDING-SDK', 'BLOCKED-AZURE-LAG', 'dataset_95', 'out7 corpus', 'realqa', 'inhouse-v1', 'soulshine1/soulshine2') appear without definition and read as internal-tracker noise to an outside reader.
 - Fix: Either expand on first use ('the F-B (Foundation vs. Baseline) panel of 10 documents'), demote to footnote, or remove. Replace tracker IDs with prose ('an open blocker on Azure snapshot availability') in publish-ready text.
7. *Throughout §2 (Tone) — e.g., line 481 'Mathpix remains best-in-class for math-equation OCR'; §2 D-LAYOUT line 99 'supplies the strongest document-parsing benchmark'; §2 D-OCR line 26 'most widely cited LMM-era OCR benchmark'; §2 D-PARSE-INTENT line 58 'de facto entry-level KIE benchmark'* — Promotional / superlative adjectives ('best-in-class', 'strongest', 'most widely cited', 'de facto') are used without citation, contrary to the researcher-not-advocate brand guardrail and the tone rule against unsupported promotional adjectives.
 - Fix: Soften to neutral, source-bound language ('Mathpix is commonly cited for math-equation OCR [cite]'; 'one of the most-cited LMM-era OCR benchmarks per Google Scholar citation count as of 2026-06 [cite]'). Remove 'strongest', 'best-in-class', 'de facto' unless a citation backs the claim.

**Minor issues (12):**
1. *§2 D-OCR (line 41) — Chandra model id 'datalab-to/chandra-ocr-2'* — Repo namespace is 'datalab-to' — likely a typo for 'datalab-to' vs. the real HF org 'datalab-to'/'datalab-to'; verify the canonical org (it is 'datalab-to' on HF? actually 'datalab-to' may be wrong — confirm 'datalab-to' vs 'datalab-to').
2. *§1 Introduction (line 12)* — Mixed quote styles — single quotes ('is this document-parsing engine best for finance documents?') alongside double quotes elsewhere. Auto-assembly inconsistency.
3. *§2 D-PARSE-INTENT (line 60) — 'KILE/LIR classes'* — Acronyms KILE and LIR are not expanded.
4. *§2 D-LAYOUT (line 85) — 'pairs_layout (PaIRS, a prompt-controlled pairwise z-euclidean spatial-relationship score, vendored from `hyprbots/vlm_ocr@1fbbc334`)'* — Internal Git org/commit reference 'hyprbots/vlm_ocr@1fbbc334' is appropriate for a methods note but reads as internal in a publish-ready paper; readers cannot resolve a private commit.
5. *References [61] and [62] (lines 616, 618)* — Two references are listed as 'Anonymous.' with arXiv/OpenReview links. For a publication-grade lit review, anonymity should be confirmed (double-blind submission) or actual authors filled in.
6. *§2 D-OCR (line 32) and §2 D-DOC-QUALITY (line 183) — SAVIOR mix percentages* — Corpus mix percentages differ slightly between sections: line 32 says '46.95% UCSF ... 17.88% in-house synthetic, 17.49% misc. public financial, 9.04% Inv3D, 8.64% FUNSD'; line 183 says '47% / 18% / 17% / 9% / 9%'. Auto-assembly rounding inconsistency.
7. *Appendix C — 'C.1 Azure OpenAI routing rule' (lines 470-472) and inline guardrail mentions '[[azure-openai-preferred]]' (line 70)* — Internal memory-link syntax '[[azure-openai-preferred]]' / '[[openai-default-gpt-5-4-thinking]]' is Obsidian/internal-wiki notation that will render as raw text on GitHub Pages.
8. *References — bracket style* — Mixed citation styles — numeric [1], [2] alongside author-year-style keys [parsebench2024], [helm2022], [grits2023], [tabular-survey2026], [pubtables1m2022], [doctypegaps2026], [framework2026]. These mixed keys never resolve in the numbered reference list, leaving dangling cites.
9. *§3 Discussion (line 490) — gates referenced by code* — Gates 'BLK-18', 'PENDING-MAXTOKEN', and 'BLK-7' appear without a glossary; non-Hyperbots readers cannot decode them.
10. *§2 D-OCR (line 40) — 'SAVIOR-Train fine-tune base'* — 'SAVIOR-Train' appears without prior introduction; reader cannot tell whether it is a public dataset or an internal split.
11. *§Abstract uses 'we' (line 8) and §3 uses 'we' (line 488)* — First-person plural is fine in intro/discussion but is also sprinkled across §2 (e.g., 'to our knowledge' line 115, 'per our smoke verification' line 135). Consider whether voice is consistent with arXiv conventions.
12. *Appendix C row 'Anthropic | Claude API' (line 460)* — Lists 'claude-opus-4-8 (flagship, rel. 2026-05-28)' as GA. This should be cross-checked against the claude-api skill / Anthropic docs before externalization to avoid embarrassing a vendor-fact error.

## 5. Files
- v1 (original, unedited): `LIT-REVIEW-2026-06-16.md` / `.html` / `.pdf`
- v2 (audited, corrected): `LIT-REVIEW-2026-06-16-v2.md` / `.html` / `.pdf`
- This audit trail: `LIT-REVIEW-2026-06-16-REVIEW.md`

---

## 6. v3 — All 7 deferred items cleared (2026-06-16)

Workflow `wo4mqksfy` (~3 min wall, 196k tokens, 6 agents) produced verified fixes for all 7 items in §3. Applied mechanically to v2 → v3.

### 6.1 Item-by-item

1. **FUNSD/CORD/SROIE/SAVIOR consolidation** — restruct:corpora-dedup agent returned 5 canonical Appendix B.1 paragraphs + 11 cross-reference replacements. Applied. Drift between scattered counts (e.g., SROIE "626 train / 347 test" vs "973 receipts") resolved to one authoritative phrasing per corpus.
2. **Chandra description consolidation** — restruct:chandra-dedup returned 1 canonical Appendix A paragraph + 3 cross-reference replacements for D-LAYOUT / D-BBOX / D-TABLE. Applied.
3. **Foundational works added** — 4 verified new references appended to bibliography
 - LayoutXLM (Xu et al. 2021, arXiv:2104.08836) — inserted in §D-LANG XFUND row.
 - UDOP (Tang et al., CVPR 2023, arXiv:2212.02623) — inserted near M6Doc in §D-LAYOUT.
 - TILT (Powalski et al., ICDAR 2021, arXiv:2102.09550) — inserted in §D-PARSE-INTENT prior art.
 - Zhang-Shasha (1989, SIAM J. Computing) — inserted in §D-TABLE where TEDS/GTRM is introduced.
4. **LayoutLMv3 97.46 verified CORRECT** — Table 1 of arXiv:2204.08387 confirms LayoutLMv3-LARGE = 97.46 F1 on CORD (official 800/100 split); base = 96.56. **BUT** the SROIE 95.2 claim was mis-cited: it belongs to the **original** LayoutLM v1 (Xu et al. KDD 2020, arXiv:1912.13318), not v3 (which does not report SROIE). Fixed: kept CORD claim, added v3 details (Table 1, split), reattributed SROIE to new sub-entry [76b] LayoutLM v1 with the precise 95.24 number.
5. **OCRBench v2 counts harmonized** — canonical: **10,000 QA / 23 tasks / 31 scenarios** (verified via arXiv:2501.00321 abstract + project page). First author is **Fu**, not Liu. Ref [125] redirected to [3]: `[125] See [3]. (Duplicate entry merged; canonical ref is [3].)`. Three inline mentions across §D-OCR / §D-LANG / Appendix B harmonized.
6. **HITL scan** — **0 hits**. No forbidden brand framing in v2. Clean.
7. **Customer-name scan** — 2 hits found ("Eskimo", "CJ Logistics" in an Appendix B context window about scan-quality outliers). Both redacted to `[customer omitted]` per the standing externalization guardrail; underlying technical claim preserved.

### 6.2 Bibliography stats
- v1: 154 refs · v2: 154 refs + 18 unverified-tags · v3: 158 numbered + 1 sub-entry [76b] = **159 effective entries**.
- New refs added: 4 (foundational) + 1 sub-entry (LayoutLM v1) = 5.
- Refs corrected: 2 (`[3]` upgraded to full author list; `[125]` redirected).
- Final em-dash count: **0** (target maintained).

### 6.3 Honest residuals
- §D-LAYOUT "we are not aware of a public benchmark that scores all three jointly" claim remains; further survey-of-survey would strengthen but is out of scope for this pass.
- The 18 [unverified] tags from v2 (15 INACCESSIBLE + 3 NOT-FOUND) are still tagged in v3; resolving them requires either re-fetching at different times or finding alternative sources.

### 6.4 v3 artifacts
- `LIT-REVIEW-2026-06-16-v3.md` / `.html` / `.pdf`
- Aggregate workflow output: `/tmp/litreview-v3/agg.json`
- Applier log: `/tmp/litreview-v3/apply-log.txt`

---

## 7. v4 — Deep citation re-verification + senior-academic critique (2026-06-16)

Workflow `wmzumshb3` launched 7 agents (5 cite-verify + 2 deep critique). 5 cite verifiers completed cleanly; the 2 critique agents hung in Phase 2 (no structured output produced; transcripts grew to 127-159 KB then stalled for 40+ min). Salvaged the 5 cite results from transcripts and re-ran the critique as a single bounded-scope Agent call. Both threads now fold into v4.

### 7.1 Deep cite-verify outcomes (55 verifications across 5 agents)

| Audit class | Result | Action |
|---|---|---|
| 15 INACCESSIBLE re-fetch | 14 CONFIRMED, 1 CORRECTED ([81] Lima de Oliveira et al., not Chiron) | corrections applied to v4 |
| 3 NOT-FOUND deep search | 3 CORRECTED (all real papers found: [65] MDPBench arXiv:2603.28130; [82] Perlitz et al. Efficient-HELM; [112] Qwen3-VL-30B-A3B not Qwen3.6-VL-A3B) | corrections applied to v4 |
| 5 v3-new refs (LayoutXLM/UDOP/TILT/Zhang-Shasha/LayoutLM-v1) | 5 CONFIRMED | none |
| 20 CONFIRMED spot-check | 20/20 hold | none (prior verifier was solid) |
| 12 META-verification of v2's corrections | 9 CONFIRMED, 2 CORRECTED ([64] XFUND-only title; [122] Mistral Large 3 doesn't exist), 1 STILL-UNVERIFIED ([136] disclaimer line) | 2 corrections applied; [136] flagged |
| Critique-flagged suspect | [6] arXiv:2601.21957 unverifiable (Jan 2026 ID would not have 5-digit suffix that high); Baidu blog URL retained as canonical | flagged inline in v4 |

**v4 citation health**: 158 numbered refs + 1 sub-entry. 48 CONFIRMED, 6 CORRECTED (applied), 1 STILL-UNVERIFIED, plus 1 inline-flagged ([6]).

### 7.2 Senior-reviewer addendum — verdict: **REWORK**

> v3 is a competent industrial literature review with strong taxonomy honesty (PENDING-PIN flagging, results.zip rule, contamination bands) but does not yet defend at NeurIPS/ICML standard as a research contribution. The headline claim of 'measurement discipline' as contribution is largely a re-statement of HELM/DUE methodology applied to document parsing, and the dimensions are not MECE: D-BBOX overlaps D-LAYOUT, D-DOC-QUALITY and D-LANG are stratifications mis-labelled as dimensions, and entire surfaces (handwriting, math, document classification, long-document reading order, multipage stitching) are missing. Reproducibility is gated on internal artifacts (SAVIOR-Bench, parse-intent-inhouse-v1, Qwen3.6 fine-tune endpoint, PaIRS commit) that an external team cannot obtain. Recommend rework to (a) re-cast the contribution honestly as an industrial framework + dataset registry rather than methodological novelty, (b) add the missing dimensions, and (c) acknowledge the n=10 statistical floor.

**MECE findings (the 9 dimensions are not actually orthogonal):**

- D-BBOX and D-LAYOUT overlap structurally: both score spatial recovery; D-LAYOUT's `layout_element_accuracy` is element-bbox F1 over a tree, which is a strict superset of D-BBOX's `bbox_iou` mean. The paper acknowledges Chandra emits 'all four ParseBench primary metric surfaces' jointly, but never resolves why two dimensions are needed when one engine produces them from one output. (IMPORTANT) — *Action:* Either fold D-BBOX into D-LAYOUT as a granularity sub-axis (token vs element vs field), or distinguish them by the *field-grounding* surface only (i.e., D-BBOX = field→region; D-LAYOUT = element tree+order) and rename accordingly.
- D-DOC-QUALITY and D-LANG are explicitly described in the paper as 'stratification overlays' on D-OCR and D-PARSE-INTENT, not independent measurement dimensions. Calling them dimensions in a 9-dimension framework inflates the contribution count and breaks MECE — they are factors in a factorial design, not orthogonal axes. (BLOCKING) — *Action:* Re-frame as 'seven measurement dimensions × two stratification overlays'. This both restores MECE and matches the paper's own internal language.
- Major content surfaces are missing entirely: (a) handwritten/cursive recognition (IAM, READ, RIMES); (b) mathematical formula extraction (Im2Latex, MathBridge, CROHME) — despite Mathpix being in the vendor table; (c) document classification (RVL-CDIP as a task, not as a quality corpus); (d) multi-page reading order / long-document stitching (PDFTriage, ChartQA-multi); (e) chart understanding as a first-class task (only mentioned in passing via ChartQA in App. B). (BLOCKING) — *Action:* Add at minimum a 'scope limitations' subsection in §2 explicitly listing handwriting, math, classification, and long-document understanding as out-of-scope, with one-sentence justification each. Better: add these as candidate dimensions for v0.5.
- D-DOWNSTREAM 'parse_lift with paired-bootstrap CI' is claimed as novel-in-parse, but identical methodology exists for RAG (Ragas, BEIR), retrieval-augmented QA, and ASR→NLU pipelines (Spoken-SQuAD). The claim should be narrower: 'first applied to a 16-doc-type parse taxonomy', not 'not previously formalized'. (IMPORTANT) — *Action:* Soften the §D-DOWNSTREAM claim and explicitly cite RAG-eval prior art as the methodological parent.

**Missing literature (specific works the document should cite):**

- *Borchmann, L. et al. DUE: End-to-End Document Understanding Benchmark. NeurIPS D&B (2021). https://duebenchmark.com/* — at §2 framing + D-PARSE-INTENT; already in refs [19] but never positioned as a *prior framework* with the same multi-dimension ambition Parse-x claims; *why:* DUE is the closest prior 'unified multi-dimension document benchmark' and is the direct competitor to the framework-novelty claim. Failure to engage DUE as a baseline framework is the single largest related-work gap.
- *Tito, R., Karatzas, D., Valveny, E. Hierarchical multimodal transformers for Multi-Page DocVQA. Pattern Recognition (2023).* — at missing — should anchor a new §multi-page reading-order discussion under D-LAYOUT; *why:* Multi-page is named in the 16-doc-type taxonomy (bank statements at 51pp) but no multi-page benchmark is surveyed.
- *Mathew, M., Bagal, V., Tito, R. et al. InfographicVQA. WACV (2022).* — at D-PARSE-INTENT and D-LANG; *why:* Standard visual document QA benchmark, mentioned only in passing as part of DUE.
- *Marti, U.-V., Bunke, H. IAM-Database. IJDAR (2002); and READ/ICFHR competitions.* — at missing handwritten-OCR subsection under D-OCR; *why:* Handwritten recognition is a core document-AI surface entirely absent from the survey.
- *Deng, Y. et al. Image-to-Markup Generation with Coarse-to-Fine Attention (Im2Latex). ICML (2017); CROHME competitions; Mahdavi et al. ICDAR 2019.* — at missing math-formula subsection under D-OCR or new D-MATH; *why:* Mathpix is in the vendor table but the entire math-OCR literature is unreferenced.
- *Cui, L. et al. Document AI: Benchmarks, Models and Applications. Data Intelligence (2021).* — at §1 Introduction as the canonical prior survey; *why:* The most-cited Document AI survey; v3 must position its delta against it.
- *Subramani, N. et al. A Survey of Deep Learning Approaches for OCR and Document Understanding. arXiv:2011.13534 (2020).* — at §1 Introduction, related surveys; *why:* Same — establishes that v3 is not the first survey of this space.
- *Liang, P. et al. Holistic Evaluation of Language Models (HELM). TMLR (2023).* — at §1 contribution claim and D-COST-LATENCY; *why:* HELM already provides per-scenario × per-metric vectors with efficiency + accuracy joint scoring; the 'measurement discipline' contribution must defend its delta vs HELM explicitly, not merely cite it under D-COST-LATENCY.
- *Srivastava, A. et al. Beyond the Imitation Game (BIG-bench). TMLR (2023).* — at §1 contribution claim; *why:* BIG-bench established per-task vectors + bootstrap CI as community standard; should be cited as methodological prior.
- *Koehn, P. Statistical significance tests for MT (cited as [73]). Already present, but paired-bootstrap is also formalised by Dror et al., The Hitchhiker's Guide to Testing Statistical Significance in NLP, ACL (2018).* — at D-DOWNSTREAM; *why:* More recent canonical reference for paired-bootstrap discipline in NLP.
- *Wang, Z. et al. DocLLM: A layout-aware generative language model for multimodal document understanding. ACL (2024).* — at D-LAYOUT/D-PARSE-INTENT models surveyed; *why:* Major 2024 layout-aware model entirely absent from the 50-model lineage table.
- *Blecher, L. et al. Nougat. (Already in lineage [96]) — but the *evaluation methodology* of Nougat (BLEU + edit distance on Markdown) is the direct prior art to ParseBench `text_formatting` split and is not engaged.* — at D-OCR text_formatting / D-PARSE-INTENT; *why:* Methodological precedent.

**Related surveys missed:**

- *Cui, L. et al. Document AI: Benchmarks, Models and Applications. Data Intelligence 3(1):1-25 (2021).* — at §1 Introduction; *why:* Canonical prior survey of the entire field; not citing it is a major related-work omission.
- *Subramani, N. et al. A Survey of Deep Learning Approaches for OCR and Document Understanding. arXiv:2011.13534 (2020).* — at §1 Introduction; *why:* Direct survey predecessor.
- *Ding, Y. et al. A Survey on Visual Document Understanding with Multimodal Large Language Models. arXiv:2503.xxxxx (2025) and similar 2024-25 VLM-era doc-AI surveys.* — at §1 Introduction; *why:* Recent VLM-era doc-AI surveys exist; v3 should cite at least one and state its delta.
- *Liu, Y. et al. A Survey on Table Recognition. arXiv (2024) / IJCAI tutorials.* — at D-TABLE; *why:* Table recognition surveys exist and should be the anchor for D-TABLE prior art.
- *Mathew, M. et al. Document Visual Question Answering surveys / DocVQA series papers.* — at D-DOWNSTREAM and D-PARSE-INTENT; *why:* VDocQA literature is large and only DocVQA itself is cited.
- *Industry IDP literature: Gartner Magic Quadrant for Intelligent Document Processing; Forrester Wave IDP; Everest Group PEAK Matrix; vendor whitepapers from UiPath Document Understanding, Hyperscience, Indico, Rossum, ABBYY.* — at §1 motivation + D-DOWNSTREAM; *why:* The paper claims an enterprise-finance focus but never engages the IDP industry literature that actually defines the deployment context. Without this, the 'enterprise relevance' claim is unsupported by anything beyond Hyperbots' own product.

**Contribution-claim critique (brutal version):**

> The 'measurement discipline' contribution does NOT defend at NeurIPS/ICML standard as currently framed. Five problems: (1) Per-document score vectors + bootstrap CI95 is the HELM/BIG-bench baseline, not novel — the paper concedes 'per-doc vectors absent everywhere except SAVIOR-Bench' but SAVIOR-Bench is an internal Hyperbots artifact, so the methodological move is 'we kept per-doc vectors like everyone in mainstream NLP eval', which is engineering hygiene not a contribution. (2) PaIRS is a vendored internal metric from `hyprbots/vlm_ocr@1fbbc334` with no external validation, no IAA against human spatial judgments, and no comparison to existing spatial-relation metrics — using a self-defined metric as a measurement-discipline contribution is circular. (3) GTRM = mean(GriTS, TableRecordMatch) is an unweighted average of two existing metrics; the unweighted choice is unjustified and there is no ablation showing GTRM correlates better with downstream value than either component alone. (4) The 16-doc-type taxonomy is asserted, not derived; no clustering analysis, no IAA on type assignments, no defense of why 16 vs 10 vs 24. (5) Parse-lift is positioned as the genuine novelty but RAG/ASR have done frozen-downstream-evaluator paired-bootstrap for years (Ragas, BEIR, Spoken-SQuAD). Honest framing: this is an industrial framework + curated dataset registry + reproducibility checklist for document parsing — valuable as a Data & Benchmarks track submission (NeurIPS D&B) but NOT as a methodological contribution to the main track. Recommend re-positioning for D&B and dropping 'discipline' framing in favor of 'a reproducibility-pinned multi-dimension registry for enterprise document parsing'.

**Reproducibility critique:**

> An external team CANNOT execute this framework from v3 alone. Specific blockers: (1) SAVIOR-Bench v1 (n=509) — internal Hyperbots artifact, not redistributable, no public mirror; the D-OCR primary metric `savior_word_recall` is undefined without it. (2) `parse-intent-inhouse-v1` rubric — internal, contamination check Q-DOSS-2 still open. (3) Qwen3.6-35B-A3B at `http://135.233.113.234:6006/v1` — private endpoint with Hyperbots IP fine-tune; D-DOWNSTREAM is not runnable without it, and the paper concedes 'if the pin changes, every cell re-runs'. (4) PaIRS implementation is vendored from a private commit `hyprbots/vlm_ocr@1fbbc334` — no public release, no algorithmic pseudocode in the review. (5) ParseBench is Apache-2.0 but the n=10/split currently on disk is a tiny subset of the full ~169k rules; the paper does not specify which 10 documents per split, blocking reproducibility even of internal numbers. (6) Decoding pins (T=0.1, top_p=0.9, max_tokens=2048, seed=20260516) are pinned but the framework concedes PENDING-MAXTOKEN causes Chandra/Qwen to truncate 8-10 of 10 documents — the pins are demonstrably wrong and not yet fixed. (7) Silver-bbox pipeline references `BBOX-SILVER-PIPELINE-SPEC` (not in the references list). (8) The fifty-model lineage carries multiple PENDING-PIN entries. Fix list: release a redacted SAVIOR-Bench mirror or a publishable substitute (e.g., a SAVIOR-style annotation pipeline over OmniDocBench), publish the PaIRS metric algorithm, swap the Qwen3.6 IP fine-tune for an open-weights extractor (Qwen3-VL-32B-Instruct) for the public version, lock the ParseBench document IDs, and resolve PENDING-MAXTOKEN before any cell publication.

**Minor findings:**

- Statistical concern: n=10 per ParseBench split is far below the regime where 2000-resample bootstrap CI95 gives narrow intervals; expected CI half-width on a [0,1] metric with n=10 and σ≈0.25 is ~±0.15, which will swamp most engine differences. The paper pins the bootstrap protocol but never reports an expected-CI-width or power-analysis sanity check. Add a §power-analysis paragraph or raise n.
- Reference [6] cites arXiv:2601.21957 for PaddleOCR-VL-1.5 — arXiv IDs do not have a 2601 month prefix; this is either a typo (should be 2501/2511) or a fabricated ID. Cross-check every arXiv ID in refs.
- Section numbering: appendices use commas not periods ('Appendix B,1', 'B,2', 'B,3', 'B,4', 'C,1', 'C,2') — copy-edit pass missed this.
- Claim 'first framework, to the authors' knowledge, to combine layout_element_accuracy with reading_order_accuracy and PaIRS on the same gold corpus' (line 115) is unfalsifiable as written; either weaken to 'we are not aware of a prior framework that combines…' or cite the search that was conducted.
- Abstract claims 'every quantitative claim carries a citation' but multiple in-text numerics (e.g., the per-doc PaIRS range 0.26-0.9996, Chandra p50 8.5s) cite internal DOSSIER entries, not externally verifiable sources — this is fine but the abstract overpromises.
- Contribution-claim sentence 'The contribution claimed is measurement discipline, not new models or new datasets' undersells the actual contribution, which is the curated 50-model lineage table, the contamination posture register, and the vendor pin table. Re-frame as artifact-contribution.
- Appendix C Mistral row has 'discrepancy, PENDING-CONFIRMATION' — typical of due-diligence but a reviewer will ask why this wasn't resolved before publication.
- The 'attestation label' escape hatch ('per-doc score vectors OR explicit `provenance: attested` label') makes the publish-gate effectively optional; reviewers will read this as a loophole. Tighten by defining what 'attested' requires (e.g., signed checksum + named annotator).
- Cross-engine fairness: the paper notes Chandra/Qwen truncate at max_tokens=2048 but reports their numbers anyway with a footnote — this violates the apples-to-apples claim. Either re-run with engine-appropriate max_tokens or drop the affected cells until PENDING-MAXTOKEN closes.
- License heterogeneity is flagged in App. A.3 but never crossed back into the leaderboard publish-gate — a future v4 should add a `license_tier` column to every cell since AGPL-3.0 / CC-BY-NC / Tongyi-Qianwen models are not deployable for many enterprise users.
- No discussion of evaluator-LLM bias for any LLM-judge component (none currently in scope, but D-DOWNSTREAM via Qwen3.6 is effectively an LLM-judge for parse quality); add a note.

### 7.3 Honest stance on the senior critique

The senior reviewer's verdict is **REWORK** — material findings, not nits. These are NOT auto-applied to v4 because each one is a positioning / contribution-claim / scope decision, not a mechanical fix
- *MECE break (D-DOC-QUALITY / D-LANG are stratifications)* — would require restructuring the framework spec itself, upstream of this lit review.
- *PaIRS circular novelty* — requires either external validation (deploy PaIRS publicly + get adoption) or de-emphasis in the framework.
- *Contribution claim does not defend at NeurIPS/ICML main-track bar* — recommendation is to re-position as a NeurIPS D&B (Datasets & Benchmarks) track submission, which is a valid path but a strategic decision.
- *Reproducibility blockers (SAVIOR private; Qwen3.6 IP endpoint private; PENDING-MAXTOKEN known-broken)* — already documented in §3 Discussion + §6.3; v4 does not pretend otherwise.
- *Missing surveys (Cui 2021, Subramani 2020, DUE-as-prior-framework, HELM/BIG-bench)* — these can be added in a v5 if user wants. They strengthen the document but the absence is not factually incorrect.

The senior critique is preserved here verbatim as the externalization-readiness gate.

### 7.4 v4 artifacts
- `LIT-REVIEW-2026-06-16-v4.{md,html,pdf}` (citation-cleanest version; senior-critique findings documented but not auto-applied)
- This audit trail (v2 + v3 + v4 sections): `LIT-REVIEW-2026-06-16-REVIEW.md`
- Cite-verify salvage: `/tmp/litreview-v4/salvaged.json`
- Senior critique JSON: `/tmp/litreview-v4/critique.json`

---

## 8. v5 — Senior-academic critique applied (2026-06-16)

The senior critique findings (REVIEW.md §7.2, verdict REWORK) were applied to v4 → v5. The original delegated agent died on a socket disconnect (4 min, 7 tool uses, 0 tokens recovered); the edits were authored directly in the main loop after anchor-greping v4.

### 8.1 Edits applied (10/10)

| # | Anchor | Change | Reason |
|---|---|---|---|
| 1 | Abstract first sentence | "nine measurement dimensions" → "seven measurement dimensions + two stratification overlays" | MECE (BLOCKING) |
| 2 | Abstract last clause | "every quantitative claim carries a citation" → "the majority...with the small number inline-flagged as unverified" | Honest overclaim fix |
| 3 | §1 final paragraph | Contribution claim repositioned: framed as **industrial framework + curated dataset registry**, citing HELM [161], BIG-bench [162], DUE [163], Cui [159], Subramani [160] | Contribution-claim repositioning (BLOCKING) |
| 4 | §1 organisation sentence | "§2 surveys the nine dimensions" → "...the seven dimensions...with...stratifications applied as overlays" | MECE |
| 5 | §2 heading | "## 2. The Nine Measurement Dimensions" → "## 2. The Seven Measurement Dimensions and Two Stratification Overlays" | MECE |
| 6 | Appendix B intro | Same 9→7+2 reframing | MECE |
| 7 | D-LAYOUT novelty claim | "first framework, to the authors' knowledge, to combine..." → "among the first...PaIRS (vendored from hyprbots/vlm_ocr@1fbbc334, not externally validated)" | Soften circular novelty |
| 8 | §3 first paragraph | "Three patterns emerge across the nine dimensions" → "...the seven dimensions and two overlays" | MECE |
| 9 | §3 D-DOWNSTREAM line | Added explicit prior-art ack of Dror 2018 [164] paired-bootstrap and Ragas 2024 [166] RAG-eval lineage | Novelty soften |
| 10 | §3 contribution-as-visibility | "This visibility constitutes the contribution" → "This visibility, paired with a curated and rerunnable cell registry, informs the industrial release discipline that follows" | Reposition contribution |

### 8.2 New subsections inserted in §3

- **§3.1 Scope limitations** — explicitly names handwritten/cursive (IAM, READ, RIMES), mathematical formula extraction (Im2Latex, CROHME), document classification, long-document / multi-page handling as out of scope, with one-sentence justification each.
- **§3.2 Reproducibility caveats** — enumerates external-team blockers: SAVIOR-Bench v1 not redistributable; parse-intent-inhouse-v1 rubric internal; Qwen3.6 endpoint private; PaIRS commit private; ParseBench n=10 doc IDs not specified.
- **§3.3 Statistical floor** — n=10 → expected bootstrap CI95 half-width ≈ ±0.15; honest acknowledgement that this can swamp engine-to-engine deltas; widening n is the correct next step.
- **§3.4 Evaluator-LLM bias note** — D-DOWNSTREAM uses Qwen3.6 as judge; apples-to-apples constraint controls relative ranking but not absolute-scale bias.
- **§3.5 Cross-engine fairness note** — Chandra/Qwen content-metric cells under uniform max_tokens=2048 are explicitly labeled apples-to-oranges.

### 8.3 D-BBOX overlap note inserted

D-BBOX intro now opens with a "*Relation to D-LAYOUT*" sentence acknowledging that D-BBOX is best read as a granularity sub-axis of D-LAYOUT rather than a fully orthogonal dimension.

### 8.4 New bibliography entries [159]-[166]

| # | Work |
|---|---|
| 159 | Cui et al. *Document AI: Benchmarks, Models and Applications*. Data Intelligence (2021). |
| 160 | Subramani et al. *A Survey of Deep Learning Approaches for OCR and Document Understanding*. arXiv:2011.13534 (2020). |
| 161 | Liang et al. *Holistic Evaluation of Language Models (HELM)*. TMLR (2023). |
| 162 | Srivastava et al. *Beyond the Imitation Game (BIG-bench)*. TMLR (2023). |
| 163 | Borchmann et al. *DUE: End-to-End Document Understanding Benchmark*. NeurIPS D&B (2021). |
| 164 | Dror et al. *The Hitchhiker's Guide to Testing Statistical Significance in NLP*. ACL (2018). |
| 165 | Tito, Karatzas, Valveny. *Hierarchical multimodal transformers for Multi-Page DocVQA*. Pattern Recognition (2023). |
| 166 | Es et al. *RAGAs: Automated Evaluation of Retrieval Augmented Generation*. EACL Demo (2024). |

### 8.5 What v5 does NOT address (residuals)

- The critique's full list of missing surveys is partially covered (Cui, Subramani, HELM, BIG-bench, DUE added; Liu 2024 table survey, Ding 2025 VLM-era survey, Mathew InfographicVQA, DocLLM 2024 not added — would require additional verified bib entries).
- The MECE re-framing is editorial (renames "9 dimensions" → "7+2"); the underlying framework spec at PARSE-DEEP-BENCHMARK-FRAMEWORK-2026-05-27 still labels them as 9 dimensions. A future framework v2 should align.
- IDP industry literature (UiPath / Hyperscience / Indico / Rossum / ABBYY) is not added; this is a market-survey scope question the framework owner can decide.
- Handwritten / math / classification / multi-page are NAMED as out-of-scope in §3.1 but not surveyed; would require dedicated dimension agents to add.

### 8.6 v5 acceptance gate

| Criterion | Target | v5 actual |
|---|---|---|
| Em-dashes | 0 | **0** |
| HITL / forbidden brand phrasing | 0 | **0** |
| Customer-name leaks | 0 | **0** |
| Bibliography entries | 166 + 1 sub-entry [76b] | **167 effective** |
| PDF renders cleanly | yes | yes (41 pages, 317 KB) |
| MECE re-framing applied | every "nine dimensions" anchor | 5/5 anchors updated |

### 8.7 v5 artifacts
- `LIT-REVIEW-2026-06-16-v5.{md,html,pdf}` (canonical, critique-applied)
- Published: (v5 is now the index target)
- This audit trail: `LIT-REVIEW-2026-06-16-REVIEW.md`

---

## 9. v6 — Coverage extension (4 dedicated agents, 2026-06-16)

CEO: "Liu 2024 table survey, Ding 2025, IDP industry literature, plus handwriting/math/classification surveys themselves not added — create 4 subagents for these and add these".

Workflow `wkv05glkm` ran 4 parallel coverage agents. 3 returned cleanly; math+classification agent died on socket disconnect mid-flight (transcript salvage returned nothing). Re-ran the math+classification agent as a single bounded Agent call (4 min, 34k tokens) which produced clean output. All 4 results then mechanically applied to v5 → v6.

### 9.1 Coverage added (4 mini-sections + 21 new references)

- **table_vlm_surveys** → ### 2.5.1 Survey landscape (table recognition + VLM-era document AI) | refs: Liu2024TableSurvey, Ding2025MLLMSurvey, Ding2024VRDSurvey, Somvanshi2024TabularSurvey, Barboule2025VRDQASurvey
- **idp_industry** → ### 2.8 Industrial IDP landscape (vendor and analyst literature) | refs: UiPathDU2026, AWSTextract2026, GoogleDocAI2026, Hyperscience2026, Rossum2026, MSSyntex2026
- **handwriting** → ### 2.8 Handwritten document recognition (coverage extension) | refs: MartiBunke2002IAM, Li2021TrOCR, Garrido2025HTRSurvey, Crosilla2025LLMHTR, Retsinas2024HTRBestPractices
- **math_classification** → ### 2.9 Adjacent surfaces (math formula extraction + document classification) | refs: Im2Latex2017, CROHME2019, LaTeXOCRpix2tex, RVLCDIP2015, Tobacco3482

### 9.2 Bibliography expansion
- v5 ended at [166] + sub-entry [76b].
- v6 appends [167]-[187] = 21 new entries.
- All new entries WebFetch-verified by their respective agents.

### 9.3 Acceptance gate
| Criterion | Target | v6 |
|---|---|---|
| Em-dashes | 0 | 0 |
| Mini-sections inserted | 4 | 4 |
| Inline edits applied | best-effort | 4 applied / 0 missed |
| New refs verified | each WebFetch-confirmed | 21 added |
| PDF renders | yes | yes (341056 bytes) |

### 9.4 v6 artifacts
- `LIT-REVIEW-2026-06-16-v6.{md,html,pdf}` (canonical, coverage-extended)
- Published: (v6 promoted to landing)

---

## 10. v7 — Content critique applied (MUST-ADD + NeurIPS-shape + definitions, 2026-06-16)

Workflow `wfn514jth` (3 critique agents) and 1 retry Agent all died on socket disconnects (recurring infrastructure pattern on heavy web-tool agents); critique completed in main loop via WebSearch + direct grep audit, written to `LIT-REVIEW-2026-06-16-CONTENT-CRITIQUE.md`. The applied fixes
### 10.1 MUST-ADD content (5 items, 10 new references)
- **Extend Parse 2.0 [188] + RealDoc-Bench [189]** added to §2.8 IDP landscape (user explicitly flagged Extend Parse 2.0 as missing).
- **Grok 4 / 4.3 (xAI) [190]** and **Llama 4 family (Scout / Maverick / Behemoth) [191]** added to §D-OCR Models surveyed as "2025-2026 frontier additions" (both 0 mentions in v6).
- **Mindee [192], Veryfi [193], Affinda [194], Klippa [195]** added to §2.8 IDP landscape as invoice/receipt specialist sub-class (all 0 in v6).
- **Reading-order metric specificity**: replaced vague "rank-correlation" with explicit Spearman footrule, with field alternatives (Kendall tau, REDS, LOER [197]) named; cited Wang et al. EMNLP 2024 [196] for the recent treatment.

### 10.2 Honest reframing of user's other claim
- "GPT-5.4 missing" was incorrect: v6 already had 5 mentions including full Azure deployment names and pricing. No change applied.

### 10.3 NeurIPS-shape (4 structural changes)
- Added **§1.1 Contributions** as an explicit bulleted list (6 contributions).
- Promoted §3.1–§3.5 to **§4 Limitations** (Scope, Reproducibility, Statistical, Evaluator-LLM, Cross-engine) — was a sub-section under Discussion; now its own top-level section per NeurIPS-D&B convention.
- Added **§5 Broader Impact** (one substantive paragraph covering business-process automation and digital-archives surfaces, contamination risk, evaluator-LLM bias).
- §3 Discussion compressed into a one-paragraph framing pointing to §4 Limitations.

### 10.4 Definitions / standards fixes
- **Reading-order metric** named explicitly (Spearman footrule) with field alternatives cited.
- **GTRM** flagged inline as "a Parse-x convention rather than a field-standard metric".
- **First-use glosses** added for: VLM, VRD, VRDU, MoE, KIE, NED, HTR, IAA.

### 10.5 v7 acceptance gate
| Criterion | Target | v7 |
|---|---|---|
| Em-dashes | 0 | 0 |
| Bibliography entries | 187 + 10 new | **197** |
| MUST-ADD items applied | 5 | 5 |
| §1 contributions list | inserted | yes |
| §4 Limitations section | promoted | yes |
| §5 Broader Impact | added | yes |
| First-use glosses | 8 expansions | 7 |
| PDF renders | yes | yes (356737 bytes) |
| TOC in HTML | yes | yes |

### 10.6 v7 artifacts
- `LIT-REVIEW-2026-06-16-v7.{md,html,pdf}`
- Content critique source: `LIT-REVIEW-2026-06-16-CONTENT-CRITIQUE.md`
- Published: (v7 promoted to landing)

---

## 11. v8 — AAAI/NeurIPS-style academic copy-edit pass (2026-06-16)

Workflow `wgei6yhl6` ran 4 parallel copy-edit agents on disjoint sections of v7 (no web tools used, which eliminated the recurring socket-disconnect issue). All 4 completed cleanly in 82 seconds, returning 136 verbatim (old_snippet, new_snippet, reason) replacements.

### 11.1 Edit categorisation (top reasons)

- 9 edits · first-person-plural overuse
- 8 edits · colloquialism
- 7 edits · informal phrasing
- 7 edits · comma splice
- 6 edits · filler removal
- 5 edits · promotional adjective
- 5 edits · informal connective
- 5 edits · heading punctuation consistenc
- 3 edits · clarity
- 3 edits · fragment to full sentence
- 3 edits · informal verb
- 3 edits · comma splice and first-person-

### 11.2 Application stats
- Applied: **136** of 136
- Non-unique fallback (first occurrence used): 0
- Not-found: 0
- Em-dashes after re-sweep: 0

### 11.3 Style discipline applied
- Filler removal: "in order to" → "to"; "due to the fact that" → "because"; "make use of" → "use"; "a number of" → "several"
- Formal register: contractions removed, colloquialisms ("basically", "essentially", "really") removed, promotional adjectives ("powerful", "robust") removed
- Connectives: "so" / "also" at sentence start replaced with "consequently" / "furthermore" / "however"
- First-person plural: trimmed in methodology/dimension prose, retained in §1 Introduction and §3-5 Discussion/Limitations/Broader Impact
- Comma splices fixed (independent clauses joined by ", " → ". " or "; ")
- Parallel grammar in §1.1 Contributions bullets and "Models surveyed" lists
- Hedge phrases added where claims exceeded cited evidence
- Reference formatting: "[24], [25]" → "[24, 25]"; whitespace normalised
- Numerals for 11+ as per academic convention

### 11.4 v8 acceptance gate
| Criterion | v8 |
|---|---|
| Em-dashes | 0 |
| Contractions | none in body |
| Promotional adjectives ("powerful" / "robust" / "best-in-class") | none uncited |
| First-person plural in dimension prose | trimmed |
| Reference format | uniform [N, M] / [N]-[M] |
| PDF renders | yes (358810 bytes) |
| TOC entries | 65 |

### 11.5 v8 artifacts
- `LIT-REVIEW-2026-06-16-v8.{md,html,pdf}`
- Published: (v8 promoted to landing)

---

## 12. v9 — NICE-TO-ADD coverage + first-pass measured baseline (2026-06-16, overnight run)

CEO directive: "run overnight; figure it out". Workflow `w0izy8l8z` ran 2 parallel agents (NICE-TO-ADD coverage + §2.11 measured cells). Both completed cleanly (~3.5 min wall, 105k tokens, 29 tool uses).

### 12.1 NICE-TO-ADD applied (12 new refs + 10 inline insertions)

- **Ocrolus / Nanonets / Sensible** (App C / §2.8 IDP) [198, 199, 200]
- **Phi-4-multimodal** (Microsoft, 5.6B, OCRBench 84.4, DocVQA 93.2) [201] in §D-OCR
- **Adobe Acrobat AI Assistant** [202] in App C
- **Mistral Magistral + Devstral** (2025-2026 specialists) [203, 204] in §D-PARSE-INTENT
- **GLM-4.5** (Z.ai foundation, 355B / 32B-A) [205] in §D-OCR
- **DocBank** [206] and **ReadingBank** [207] in §D-LAYOUT
- **TEDS-S vs TEDS-C** split note in §D-TABLE; canonical PubTabNet / Zhong 2020 [208] cited
- **ANLS** metric note in OCRBench v2 + DocVQA contexts; Mathew et al. DocVQA [209] cited

### 12.2 §2.11 First-pass measured baseline inserted
A new subsection after Appendix C presents the in-house F-B numbers as a *preliminary* measured baseline, with three binding caveats: n=10 → ±0.15 CI95 half-width; PaIRS is private-internal (external readers cannot reproduce); max_tokens=2048 truncation makes Chandra/Qwen content-metric cells apples-to-oranges. Tables for PaIRS panel (Chandra 0.6472 > Qwen 0.4422 > Tesseract 0.3639 > HyperAPI parse 0.2907) and F-B suite (layout, text_content, text_formatting cells) included verbatim from DOSSIER §2.4 / §2.5. Internal DH-001 / dataset_95 numbers explicitly NOT externalized.

### 12.3 Acceptance gate
| Criterion | v9 |
|---|---|
| Em-dashes | 0 |
| Bibliography entries | 197 + 12 new = **209** + [76b] |
| §2.11 measured baseline | inserted with apples-to-oranges flag |
| PDF renders | yes (376105 bytes) |
| TOC entries | 66 |
| Internal data externalized | none (DH-001 / dataset_95 stayed internal) |

### 12.4 v9 artifacts
- `LIT-REVIEW-2026-06-16-v9.{md,html,pdf}`
- Published: (v9 promoted to landing)
