# Content Critique of v6 — Models, Vendors, Definitions

Audit: 2026-06-16. Method: workflow `wfn514jth` (all 3 agents died on socket), single-Agent retry (also socket-died), then completed in main loop with WebSearch + targeted greps of v6.

User's two specific premises tested:

| User claim | Truth |
|---|---|
| "GPT-5.4 is missing" | **FALSE.** v6 already covers GPT-5.4 thinking/pro extensively (5 inline mentions at lines 280, 390, 490, 501, 508 incl. full Azure deployment names `gpt-5.4-thinking`, `gpt-5.4-mini`, `gpt-5.4-nano`, pricing, snapshot dates 2026-03-05/17, reasoning-token billing note). |
| "Extend AI's Parse 2.0 is missing" | **PARTIALLY TRUE.** Extend appears 5 times in v6 prose, but the specific product "Parse 2.0" (Extend's layout-first parsing API, 1M+ pages training, beats other providers on Extend's own RealDoc-Bench) is NOT named, and RealDoc-Bench is not in §3 (Datasets). Both should be added. |

---

## 1. MUST-ADD (real gaps with high reviewer impact)

| Gap | Category | Where it lands | Evidence |
|---|---|---|---|
| **Extend Parse 2.0** + **RealDoc-Bench** | Parse-specialist product + new benchmark | §1 motivation, App C vendor table, §3 Datasets (RealDoc-Bench: 1,500 samples, healthcare/financial-services/logistics/real-estate documents, measures layout accuracy + downstream agent performance) | [Extend Parse 2.0 launch](https://www.extend.ai/resources/parse-2-and-realdocbench-launch); [RealDoc-Bench](https://www.extend.ai/resources/realdocbench) |
| **Grok 4 / 4.1 / 4.3 (xAI)** with vision + OCR | Frontier VLM | §D-OCR Models surveyed, App C vendor row | [xAI Grok models 2026](https://www.lorka.ai/ai-models/xai); released July 2025; Grok 4.3 beta April 2026 with native multimodal video + 256k context |
| **Llama 4 family** (Scout 109B/10M-ctx, Maverick 400B/1M-ctx; Behemoth previewed) | Frontier VLM with native multimodality | §D-OCR / §D-PARSE-INTENT Models surveyed, App A lineage | [Meta Llama 4 explainer](https://medium.com/@simranjeetsingh1497/llama-4-herd-behemoth-maverick-scout-explained-946c9f996349); released April 2025, first Llama with native multimodality via early-fusion |
| **Mindee, Veryfi, Affinda, Klippa** (invoice/receipt-specialist IDPs) | IDP vendor sub-class | §2.8 Industrial IDP landscape | [Eden AI best receipt parsers](https://www.edenai.co/post/best-receipt-parser-apis); these are the canonical invoice-IDP comparison set; benchmarks at [Veryfi 2025 comparison](https://www.veryfi.com/ai-insights/invoice-ocr-competitors-veryfi/), [Mindee top-10 OCR](https://www.mindee.com/blog/leading-ocr-api-solutions) |
| **Reading-order metric specificity** | Definitional non-standardness | §D-LAYOUT — name whether `reading_order_accuracy` is Spearman footrule, Kendall tau, REDS (Reading Edit Distance Score), or LOER (Layout Ordering Error Rate); currently just "rank-correlation" | [Modeling Layout Reading Order, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.540/) — field uses Spearman footrule / Kendall tau / REDS / LOER; v6 must pick one |

## 2. NICE-TO-ADD (real but secondary)

| Gap | Where |
|---|---|
| **Ocrolus, Nanonets, Sensible.io, Documind, AryaXAI** (additional invoice/extract specialists) | §2.8 Industrial IDP (extends the existing vendor list) |
| **Phi-4-multimodal** (Microsoft's vision LM separate from the briefly-mentioned Phi-4-vision) | §D-OCR Models surveyed; Phi-3.5/Phi-4-vision is mentioned in passing but the 2025 Phi-4-multimodal release is not covered |
| **Adobe document AI** (Acrobat AI Assistant, Firefly Document) | App C vendor table — Adobe is absent |
| **Mistral 2026 specialists** (Magistral reasoning, Devstral code, possibly Mistral Vision 2) | App C; Mistral Large 3/Medium 3.5/Small 4 are present, but the specialist 2026 line is not |
| **GLM-4.5 / GLM-OCR-3** if released | §D-OCR Models surveyed; v6 has GLM-OCR but not the 4.5 generation |
| **TEDS-S vs TEDS-C split** for table eval | §D-TABLE metrics — v6 cites TEDS/GriTS but doesn't note the structure-only vs content variants which are now standard |
| **ANLS** (Average Normalized Levenshtein Similarity, the DocVQA metric) | §D-PARSE-INTENT or §D-OCR — field-standard metric, not glossed in v6 |
| **DocBank, ReadingBank** datasets | §D-LAYOUT prior art (datasets); v6 mentions ReadingBank in passing but does not catalogue properly |

## 3. INTENTIONAL-OMISSION / USER PREMISE INCORRECT

| Premise tested | Actual state in v6 |
|---|---|
| "GPT-5.4 missing" | GPT-5.4 thinking/pro, Mini, Nano all named with Azure deployment IDs + snapshot dates + pricing |
| "Claude 4.x missing" | Sonnet 4.6, Opus 4.7/4.8, Haiku 4.5 all in App C with pricing |
| "Gemini 2.5 / 3.x missing" | Gemini 2.5 Pro/Flash named; 3.1-pro and 3.5-flash flagged PENDING-CONFIRMATION |
| "Mistral missing" | Large-3, Medium 3.5, Small 4 all named |
| "Phi missing" | Phi-3.5 and Phi-4-vision named (briefly; could be expanded) |
| "LlamaParse / Reducto / Unstructured / Docling / Hyperscience / UiPath / Mathpix / Marker / Surya / ABBYY missing" | All present |

## 4. DEFINITIONS / STANDARDS AUDIT

### 4.1 Standard vs project-internal terminology

| Term | Status | Recommendation |
|---|---|---|
| **TEDS** (Tree-Edit-Distance Similarity) | Field-standard (Zhong et al. 2020) | Already correctly cited |
| **GriTS** | Field-standard (Smock et al. CVPR 2023) | Already correctly cited |
| **TableRecordMatch** | ParseBench-defined; not field-standard | v6 should note this once: "ParseBench-defined; not a field-standard metric" |
| **GTRM = mean(GriTS, TableRecordMatch)** | Project-defined composite | v6 should explain the composite formula and note "this is a Parse-x convention; readers may prefer to report GriTS and TableRecordMatch separately" |
| **PaIRS** (z-Euclidean Pairwise Spatial) | Project-internal, vendored from hyprbots/vlm_ocr@1fbbc334; v5 acknowledged | OK — already glossed in v5 |
| **`savior_word_recall`** | Project-internal (SAVIOR-Bench is internal) | OK — already glossed; could rename to "multiset word recall (SAVIOR-Bench gold)" for clarity |
| **`layout_element_accuracy`** | Tree F1 over layout elements — terminology is field-adjacent but the specific implementation should cite a source paper or define the tree-edit metric used | Add one-sentence definition |
| **`reading_order_accuracy`** "rank-correlation" | Non-specific; field uses **Spearman footrule**, **Kendall tau**, **REDS**, or **LOER** | **MUST-FIX**: specify which one |
| **D-OCR / D-PARSE-INTENT / D-LAYOUT / D-BBOX / D-TABLE / D-DOWNSTREAM / D-COST-LATENCY** | Project dimension labels (Parse-x framework taxonomy) | OK as project labels; v5 added the "7 + 2 overlays" reframing |
| **Q-HIGH / Q-MED / Q-LOW** doc-quality tiers | Project taxonomy; no field-standard for parse-quality stratification | Add a sentence: "Hyperbots-defined tiers; no field-standard equivalent" |
| **L-EN/DE/FR/ES/ZH/JA/AR** | Standard ISO 639-1 codes, lifted into project notation | OK |
| **F-B / BLK-15 / F11-DICT-LITERAL / R8/R9 / [FT] / PENDING-MAXTOKEN / PENDING-KEY / PENDING-SDK** | Internal project jargon | Already glossed appropriately for the audience; minor copy-edit recommendation: define on first use throughout each section so a reader entering at §D-X doesn't need to backtrack |

### 4.2 Missing definitions on first use

Terms used in v6 without an inline gloss the first time they appear:

- **IAA** (Inter-Annotator Agreement) — define once
- **NED** (Normalized Edit Distance) — define once
- **CER / WER** (Character / Word Error Rate) — assume reader knows but a one-line gloss is journal-conventional
- **HTR** (Handwritten Text Recognition) — defined in §2.9 but used earlier
- **VRD / VRDU** (Visually Rich Document Understanding) — used in §2.5.1 and §1; never expanded
- **MoE** (Mixture of Experts) — used for Qwen3-VL-30B-A3B and Llama 4; never defined
- **VLM** (Vision-Language Model) — used everywhere; never glossed on first use
- **KIE** (Key Information Extraction) — used in §D-DOWNSTREAM; never expanded

### 4.3 Field-convention drift

| Concept | v6 framing | Field standard | Severity |
|---|---|---|---|
| Reading order eval | "rank-correlation" | Spearman footrule (Wang 2024 EMNLP), Kendall tau, REDS, LOER (Coquenet 2022) | MUST-FIX |
| Apples-to-apples constraint | "uniform decoding pins per task family" | The field calls this "fixed-pin evaluation" or "frozen decoding protocol"; HELM uses "decontamination" + "pinned generation params" | Aligns; could harmonize vocabulary |
| Fine-tune vs zero-shot disclosure | `[FT]` tag | Field-standard is "FT" suffix in benchmark tables (e.g., LLaMA-7B-FT vs LLaMA-7B); could match | NICE-FIX |
| Per-doc vectors + bootstrap CI | Framed as Parse-x discipline | HELM and BIG-bench already do this; v5 already acknowledged with citations [161][162] | Resolved in v5 |

## 5. NeurIPS-shape gaps (from prior structural critique)

These were flagged earlier; restating for completeness:
- §1 Introduction lacks an **explicit bulleted contributions list** (NeurIPS convention)
- Figures/tables are **unnumbered and lack captions** ("Figure 1: ..." / "Table 1: ...")
- **§4 Limitations** should be its own top-level section (currently §3.1/3.2 subsections)
- **§5 Broader Impact** is absent (NeurIPS now requires)
- Document is **43 pages**, well over NeurIPS-D&B 9-page main + appendix budget

## 6. Recommended action

If you want to apply (1) + (4.3 reading-order fix) + NeurIPS-shape (§1 contributions list, §4 Limitations heading, table/figure numbering, missing-definition glosses), this is a clean **v7** in one pass:
- ~5-7 MUST-ADD insertions with verified citations
- ~6-10 missing-definition glosses
- Rename `reading_order_accuracy` "rank-correlation" → name the specific metric
- Add §1 contributions bullet list
- Promote §3.1+§3.2 to **§4 Limitations**
- Add §5 Broader Impact (1 paragraph)
- Add Figure/Table numbering and captions

Total addable references: ~10-15 new entries [188]-[202ish].

The 8 NICE-TO-ADD gaps are real but the doc is already at 43 pages and risks bloat. Recommend triaging them as a separate v7.1.

---

Sources cited above:
- [Extend Parse 2.0 launch](https://www.extend.ai/resources/parse-2-and-realdocbench-launch)
- [Extend RealDoc-Bench](https://www.extend.ai/resources/realdocbench)
- [xAI Grok models 2026](https://www.lorka.ai/ai-models/xai)
- [Grok 4 — Grokipedia](https://grokipedia.com/page/Grok_4)
- [Meta Llama 4 herd explainer](https://medium.com/@simranjeetsingh1497/llama-4-herd-behemoth-maverick-scout-explained-946c9f996349)
- [Llama 4 complete guide 2026](https://codersera.com/blog/llama-4-complete-guide-2026/)
- [Mindee best receipt parsers / leading OCR APIs](https://www.mindee.com/blog/leading-ocr-api-solutions)
- [Eden AI receipt parser comparison](https://www.edenai.co/post/best-receipt-parser-apis)
- [Veryfi 2025 invoice OCR benchmark](https://www.veryfi.com/ai-insights/invoice-ocr-competitors-veryfi/)
- [Modeling Layout Reading Order, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.540/)
- [FocalOrder reading order detection (2026)](https://arxiv.org/pdf/2601.07483)
