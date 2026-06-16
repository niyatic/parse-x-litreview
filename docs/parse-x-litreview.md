# Parse-x: A Literature Review for the Deep Benchmark Framework

*Hyperbots Research, hyperapi-parse-x-research team*  
*2026-06-16*

## Abstract

Document parsing has bifurcated into two literatures with little overlap: a multimodal-LLM benchmark line (OCRBench v2, OmniDocBench, olmOCR-Bench) that reports single aggregate numbers per model, and an in-house or release-discipline benchmark line (SAVIOR-Bench; the Apache-2.0 ParseBench corpus from LlamaIndex re-used with project-specific evaluation discipline) that exposes per-document score vectors, multilingual-quality stratification, and downstream-task lift. This review surveys the prior art for each of the seven measurement dimensions defined by the Parse-x Deep Benchmark Framework (D-OCR, D-PARSE-INTENT, D-LAYOUT, D-BBOX, D-TABLE, D-DOWNSTREAM, D-COST-LATENCY), together with the two stratification overlays (D-DOC-QUALITY and D-LANG) that cross-cut them and the sixteen-document-type taxonomy that cross-cuts them. For each dimension the canonical benchmarks, the relevant model families, and the specific deltas are identified that justify the framework's additional measurement discipline. Three appendices provide a structured model-lineage table covering the fifty-plus models in the project's measurement pool, a datasets-and-contamination posture register, and a vendor-and-API pin table for the closed-source services in scope. The review adopts a descriptive rather than evaluative stance: prior work is named for what it measures and what it does not measure, no winner is selected in advance, and the majority of quantitative claims are anchored to numbered references, with the small number that remain inline-flagged as unverified.

## 1. Introduction

The Parse-x Deep Benchmark Framework [25] decomposes the question 'is this document-parsing engine best for finance documents?' into nine orthogonal measurement dimensions and a sixteen-type document taxonomy. Each cell of the resulting matrix is anchored to a public benchmark where possible (ParseBench [49], SAVIOR-Bench [1], OmniDocBench [4], PubTabNet, DocLayNet) and falls back to in-house silver pipelines (BBOX-SILVER-PIPELINE-SPEC) or stratified hold-outs (dataset_95) when public coverage is absent. The framework's publish-gate requires per-document score vectors with bootstrap CI95 (or an explicit attestation label), uniform decoding pins (temperature 0.1, top-p 0.9, max_tokens 2048, seed 20260516), and fine-tune-vs-zero-shot disclosure on every cell.

This literature review serves two purposes. First, it surveys the prior art per dimension so that each new leaderboard cell can be interpreted against the right historical baseline. Second, it surfaces the methodological gaps in that prior art (particularly the absent per-document vectors, the inconsistent fine-tune disclosure, the under-stratified multilingual and quality axes, and the near-total absence of parse-to-downstream lift measurements) that motivate the framework's additional measurement discipline. Per [161] and [162], per-document score vectors with bootstrap confidence intervals are now a baseline expectation for language-model evaluation; the contribution claimed here is not methodological novelty over that baseline, but rather an industrial framework and curated dataset registry that ports the discipline to document parsing, makes the open gates visible, and provides a rerunnable-cell convention compatible with [163] (DUE, the most relevant prior document-understanding framework). Earlier surveys ([159], [160]) catalogue the field at the model level; this review pairs that prior art with a measurement-level framework.

The remainder of the paper is organized as the framework dictates. §2 surveys the seven dimensions in order, with the D-DOC-QUALITY and D-LANG stratifications applied as overlays throughout. Appendices A–C provide the model lineage table, the datasets-and-contamination posture register, and the vendor-and-API pin table. Section 3 closes with a discussion of the largest open gates that block first-pass cell publication.

## 2. The Seven Measurement Dimensions and Two Stratification Overlays

## D-OCR: text recognition transcription

The D-OCR dimension of Parse-x scores the most primitive question that can be asked of any document-AI engine: given a page image or PDF, does the system recover the document's tokens, and how cleanly? The framework's primary metric is `savior_word_recall`, a multiset recall over reference tokens taken from SAVIOR-Bench (n=509, IAA 0.761 via fuzzy-string similarity over 187 double-annotated pairs), with `savior_word_precision`, normalized Levenshtein `ocr_edit_distance`, and word error rate as secondaries [1][2]. The dimension is separated from D-PARSE-INTENT (structured field extraction) and D-DOWNSTREAM (chained pipelines) so that hallucinations and dropped tokens surface as transcription-level signals rather than being masked by a downstream rubric. The publish-gate requires per-document score vectors (for 2000-resample bootstrap CI95) or an explicit `provenance: attested` label; a discipline that most external OCR leaderboards do not satisfy.

### Prior benchmarks

**OCRBench v2** [3] is the most widely cited LMM-era OCR benchmark: 10,000 human-verified QA pairs across 23 tasks and 31 scenarios (street scenes, receipts, formulas, diagrams), with a 1,500-image private split. Its headline finding (20 of 22 evaluated LMMs score below 50/100) establishes that OCR is far from saturated for multimodal models. However, OCRBench v2 is a QA-style benchmark: it measures whether a model can *answer questions about text*, not whether it produces a full faithful transcription. Word-level recall, edit distance, and verbose-hallucination WER patterns (the failure mode SAVIOR-Bench surfaces for PaddleOCR-VL-1.5 and DeepSeek-OCR-2) are not its primary signal [1].

**OmniDocBench** [4], published at CVPR 2025, supplies the strongest *document-parsing* benchmark in the prior art: nine document sources (academic papers, textbooks, handwritten notes, dense newspapers), 19 layout categories, 15 attribute labels, and end-to-end plus task-specific evaluation modes. It is the canonical leaderboard cited by MinerU2.5 (overall 90.67) [5] and PaddleOCR-VL-1.5 (94.5% on v1.5) [6]. OmniDocBench measures text + layout + table jointly through end-to-end edit-distance-style metrics; it does not separate transcription quality from layout fidelity the way Parse-x splits D-OCR from D-LAYOUT, so a system that emits clean text in bad reading order is scored together with one that drops tokens.

**olmOCR-Bench** [7] from AI2 covers 7,000+ test cases across 1,400 documents, with the design constraint that systems must emit plain-text Unicode in natural reading order. olmOCR-2-7B-1025 scores 82.4 on the benchmark [8]. olmOCR-Bench is English-print-centric and unit-test-rule structured (presence/absence/order checks), which is complementary to but narrower than SAVIOR-Bench's recall/precision/edit-distance triad over a multilingual, low-quality-scan corpus.

**SAVIOR-Bench v1** [1] (see App. B.1) is the in-house gold the framework primarily anchors on for D-OCR; relevant here because its scoring discipline (per-doc vectors, IAA reporting) is stricter than the public OCR benchmarks, but the corpus is not publicly redistributed and the per-doc vectors for the attested 31-cell leaderboard are an open gate (R2 / BLK-18).

**FUNSD, CORD, and the classical CER/WER leaderboards** [9] (see App. B.1) remain useful for printed-form recognition but cover none of the modern failure surfaces (vertical text, logo-embedded text, multilingual + dense layout) that SAVIOR-Bench's failure taxonomy enumerates [1].

### Models surveyed

The dossier inventories ~31 OCR cells in `DC-000__ocr-edit-distance-v1` [10]. Grouped by family:

- **General-purpose document VLMs.** Qwen3-VL-235B, Qwen2.5-VL-3B/7B (the SAVIOR-Train fine-tune base), Qwen3.6-35B-A3B, InternVL2-8B/26B/76B, LLaVA-1.6-34B, GPT-4o / GPT-4o-mini, Gemini-1.5 Flash/Pro, Claude-Sonnet-4.6 [10]. Most are evaluated zero-shot; SAVIOR fine-tuning on Qwen2.5-VL-7B with LoRA (rank 32, α 64, 5 epochs, 2× H100) lifts word-recall to 0.9294 [2][1].
- **OCR-specialist VLMs.** GLM-OCR (edit-distance 0.019, rank-1 specialist on the SAVIOR leaderboard), DeepSeek-OCR-2, GOT-OCR-2.0, DocOwl2 / mPLUG-DocOwl1.5, Fox, TextMonkey, Vary-toy, Nougat-0.1.0, FireRed-OCR, Logics-Parsing-v2, Chandra (`datalab-to/chandra-ocr-2`) [10][1].
- **Decoupled / pipeline parsers.** MinerU 0.9 and MinerU 2.5 (1.2B, coarse-to-fine decoupled, OmniDocBench 90.67) [5]; Marker-1.0; Surya; PaddleOCR-v4 and PaddleOCR-VL-1.5 (0.9B ERNIE-4.5 backbone, OmniDocBench v1.5 94.5%) [6]; HyperAPI-PaddleOCR-OURS; olmOCR / olmOCR-2-7B-1025 [8].
- **Classical engines.** Tesseract-OCR (multilingual restored 2026-06-10 via `tesseract-lang`), EasyOCR, OpenOCR; Mathpix as a hosted reference [10].
- **Cloud / vendor systems.** Textract (SAVIOR word-recall 0.9233, #1 zero-shot anchor) [1].

### Gaps relative to the framework

First, prior benchmarks largely score *single aggregate numbers per model* and do not retain per-document score vectors; OCRBench v2, OmniDocBench, and the SAVIOR attested leaderboard all currently lack the per-doc vectors Parse-x requires for bootstrap CI95 [3][4][1]. Second, the verbose-hallucination pattern (PaddleOCR-VL-1.5: F1 0.726 with WER 2.96; DeepSeek-OCR-2: WER 12.35) only emerges when WER is reported alongside F1 across the same cell, a discipline OCRBench v2's QA framing structurally cannot expose [1]. Third, no prior benchmark stratifies D-OCR by the Q-LOW/Q-MED/Q-HIGH quality axis the framework defines under D-DOC-QUALITY, so a model's collapse on degraded scans is reported only anecdotally in failure-mode lists [1][2]. Fourth, the multilingual axis is underspecified everywhere except OmniDocBench's nine-source mix and PaddleOCR-VL-1.5's Tibetan/Bengali extension [4][6]; Parse-x's D-LANG cross-stratification of D-OCR is, on the current literature, novel. Finally, fine-tune-vs-zero-shot disclosure is inconsistent in public leaderboards (a recurring SAVIOR-Bench complaint, R6); the framework's `(fine-tuned)` tagging functions as both a measurement-disclosure and metric contribution [1].

## D-PARSE-INTENT: structured field extraction F1 + WER

The D-PARSE-INTENT dimension scores a document engine's ability to emit a canonical field-set with values, without a hand-written schema, from a raw page. It is distinct from D-OCR (no transcription objective) and from D-DOWNSTREAM (no chained extractor LLM). The framework pins `parse_intent_f1` (per-field F1 over the recovered intent fields, ↑) as the primary metric and `wer` (word error rate on the intent-bearing text subset, ↓) as a secondary metric, exposing a recurring failure pattern in which verbose VLMs hallucinate around the value enough to keep the field recoverable while transcription degrades (e.g. PaddleOCR-VL-1.5 reaching F1 0.726 with WER 2.96 on the inhouse-v1 panel) [11]. Compared to D-OCR, D-PARSE-INTENT public prior art is markedly thinner: most benchmarks are either narrow-domain (receipts, forms) or vendor-curated, and very few jointly publish a structured-F1 number alongside a transcription error metric on the same documents [1].

### Prior benchmarks

- **FUNSD** [9] (see App. B.1): relevant here for form key-value labelling (entity-level SER F1) but does not exercise line-item structure, multi-page reasoning, or transcription error.
- **CORD** [13]: 1,000 Indonesian receipts (800/100/100), 30 entity types in 4 groups (Menu / Void menu / Subtotal / Total). Evaluated with field-level F1 and tree-edit-distance accuracy; LayoutLMv3-large reports 97.46 F1 (Table 1, official 800/100 split; base 96.56), Donut 91.6 [12][14]. Receipt-only, short documents, single language.
- **SROIE (ICDAR 2019, Task 3)** [15] (see App. B.1): the de facto entry-level KIE benchmark; relevant here as a fixed-schema baseline well below the free-schema inhouse-v1 panel.
- **Kleister NDA / Kleister Charity** [16]: 540 NDAs (3,229 pages, 2,160 entities) and 2,788 charity reports (61,643 pages, 21,612 entities); strongest models report 81.77 / 83.57 F1; adds long-document layout, but only English and non-financial-invoice schemas.
- **DocILE-2023** [17]: 6.7k annotated business documents + 100k synthetic + ~1M unlabelled with 55 KILE/LIR classes from invoices/orders (ICDAR-2023 + CLEF-2023 competition); the closest public analogue to the framework's invoice-heavy T-01 doc-type, though it does not score transcription WER alongside KIE F1.
- **DeepForm** [18]: political-ad TV-station disclosure forms maintained by ProPublica; appears as a KIE task in the DUE benchmark [19] where answer normalization is required. Narrow domain; small held-out size.
- **DUE (Document Understanding Evaluation)** [19]: meta-benchmark assembling DocVQA, InfographicsVQA, Kleister, DeepForm, WikiTableQuestions and others under one QA-style harness; useful as a contamination reference because most modern VLMs have seen at least part of it.

The framework's own `parse-intent-inhouse-v1` rubric (23 attested systems, n unreported in the attested source [1]) is internal and intentionally not externalised. The dossier flags that the rubric provenance must not be derived from `results.zip` (HyperAPI deployed output), and a contamination check (Q-DOSS-2) remains open [11].

### Models surveyed

- **Layout-aware encoders**: LayoutLMv3 (base + large) [12], BROS [20], LiLT [21], FormNetV2 (86.35 F1 on FUNSD at 2.6× smaller than DocFormer) [22].
- **OCR-free generative VDU**: Donut (CORD 91.6) [14] and the OmniParser line (text-spotting + KIE + table) [23]. An important precursor is **TILT** (Powalski et al., ICDAR 2021) [157], a text-image-layout encoder-decoder that reported state-of-the-art on DocVQA, CORD and SROIE and established the joint multimodal-transformer recipe later inherited by Donut and UDOP.
- **General multimodal foundation models** evaluated on the inhouse-v1 panel: GPT-4o (well-documented zero-shot anchor at F1 0.8052 / WER 0.4232), GPT-4.1, Claude-Sonnet-4.6, Gemini-2.5-Flash, Gemini-2.5-Pro, Llama-3.2-90B-Vision, Mistral-Large-3-675B [11][1]. Per project guardrail [Hyperbots Azure OpenAI routing policy], OpenAI calls route through Azure OpenAI Service.
- **VLM/OCR specialists** also scored on inhouse-v1: Qwen2.5-VL-3B/7B-Instruct, Qwen3-VL-32B-Instruct, Qwen3.6-35B-A3B, PaddleOCR-VL-1.5, MinerU2.5-Pro, GLM-OCR, FireRed-OCR, Logics-Parsing-v2, DeepSeek-OCR-2, Qianfan-OCR, DocIntentOCR-3B (under-documented; Q-DF-3 open) [11].
- **Fine-tuned in-house**: `hyperapi-parse-intent (fine-tuned)` leads at F1 0.8328 / WER 0.2589 (+0.0276 F1 over the GPT-4o zero-shot anchor) [1].

### Gaps relative to the framework

1. **Joint F1 + WER on identical inputs.** FUNSD/CORD/SROIE/Kleister/DocILE all report a single structured-F1; none publishes a paired transcription WER over the same intent-bearing token subset. The framework's secondary `wer` metric is what surfaces the "high-F1, exploded-WER" pattern (PaddleOCR-VL-1.5: F1 0.726, WER 2.96) [11].
2. **Schema-free task definition.** SROIE (4 fields) and CORD (30 entities) fix the schema in advance; inhouse-v1 measures whether the engine itself can propose the canonical field-set without a schema prompt, a capability prior public benchmarks do not score [1].
3. **Cross-vendor panel discipline.** Most public KIE papers report 2–6 baselines on one corpus; the inhouse-v1 panel runs 23 systems under pinned decoding with attestation [1], matching the apples-to-apples gate but inheriting the contamination question on the rubric itself [11].
4. **CI95 and per-doc vectors.** Almost no prior KIE benchmark publishes bootstrap CI95 or per-doc score vectors; the framework's publish-gate (resamples 2000, seed 20260516) requires them, which is why even the attested SAVIOR cells today carry `ci95=null` until per-doc vectors are recovered [1].
5. **Contamination posture.** Public KIE corpora (FUNSD, CORD, SROIE, DocILE, Kleister, DeepForm) are widely indexed and likely in modern VLM pretraining mixes; analyses such as [24] document information-redundancy and lexical-bias problems that inflate scores. The framework's response is a private held-out rubric plus an explicit factory-rerun green-gate.
6. **Held-out / SDK coverage.** `parse-intent` is currently outside the pinned SDK surface for live realqa (PENDING-SDK) [11]; numbers exist only offline, which is a transparency note the public benchmarks do not have to make.

## D-LAYOUT: layout-element accuracy + reading-order (PaIRS)

D-LAYOUT scores whether a parse engine recovers a document's spatial organization (the tree of titles, paragraphs, tables, figures and captions, and the *order* a human would read them in) and not merely the characters those regions contain. The Parse-x framework operationalises this as three metrics: `layout_element_accuracy` (element-match F1 over the gold layout tree), `reading_order_accuracy` (rank-correlation over the ordered element list), and `pairs_layout` (PaIRS, a prompt-controlled pairwise z-euclidean spatial-relationship score, vendored from `hyprbots/vlm_ocr@1fbbc334`) [25]. The dimension explicitly addresses SAVIOR-Bench Recommendation R8, which flagged that no layout-awareness ground-truth was available in the original SAVIOR corpus and listed the facet as "defined, not yet measured" [1].

### Prior benchmarks

**PubLayNet** (IBM, ICDAR 2019) is the de-facto pre-training corpus for document-layout detection: ~360k PubMed Central pages with auto-generated bbox annotations for five classes (text, title, list, table, figure) scored by COCO-style mAP [26]. Its scale is unmatched but its label set is narrow and its scientific-article distribution is monolingual English and stylistically homogeneous; it has no reading-order annotation and no element-tree.

**DocLayNet** (IBM, KDD 2022) hand-annotated 80,863 pages spanning six categories (financial reports, scientific articles, laws, manuals, patents, government tenders) with 11 layout classes; human baselines sit roughly 10 mAP above the strongest detectors at release [27]. DocLayNet adds class breadth and human-IAA discipline but, like PubLayNet, is a *detection* benchmark; it scores bboxes, not reading order, and does not score table or figure internal structure.

**M6Doc** (SCUT, CVPR 2023) introduces 9,080 modern document pages with **74 fine-grained label types** and 237,116 instances, covering scanned/photographed/PDF formats across textbooks, magazines, newspapers and test papers in Chinese and English [28]. M6Doc is the most label-rich layout corpus to date but still does not annotate reading order, and its 9k page count makes it more of an evaluation than a pre-training set. **UDOP** (Tang et al., CVPR 2023) [156] is a foundational precedent for unified vision-text-layout modelling: it casts detection, parsing, KIE and QA into a single seq2seq encoder-decoder over text + image + layout tokens, and is the most direct prior-art analogue to the joint element + order + spatial-fidelity scoring posture D-LAYOUT adopts.

**ReadingBank** (Microsoft, paired with LayoutReader, EMNLP 2021) is the canonical reading-order benchmark: ~500k pages where order is harvested as weak supervision from Word-XML and then reprojected onto the rendered PDF; metrics are BLEU / token-rank Average Page-level Accuracy. LayoutReader achieves near-ceiling on the in-distribution split [29]. ReadingBank's weakness is that order labels inherit Word's linear flow, so multi-column scientific or financial layouts can be undersupported.

**OmniDocBench** (OpenDataLab, CVPR 2025) is the closest contemporary to Parse-x: 1,355–1,651 PDF pages, 10 document types, 5 layout types, 5 languages, 100k+ region annotations with reading order, evaluated by Normalised Edit Distance (NED) over the predicted reading sequence [30]. v1.5 adds layout-type-stratified NED splits. OmniDocBench measures end-to-end reading order via NED but does not isolate `pairs_layout`-style PC-vs-NPC comparability, and its taxonomy does not align 1:1 with Parse-x's 16-doc-type taxonomy.

**SAVIOR-Bench layout facet** is defined (element accuracy, reading-order accuracy, PaIRS) but explicitly *not measured* in the original release; the corpus carries 509 docs with extraction gold and an IAA-attested 0.761 fuzzy-string agreement on 187 double-annotated pairs, but no layout-tree gold [1].

### Models surveyed

Layout-aware document parsing in 2025–26 stratifies into four families.

- **Pure layout detectors** trained on PubLayNet/DocLayNet/M6Doc: DiT, LayoutLMv3, VGT (Vision Grid Transformer) [31], and YOLO-doc derivatives. Output is bbox + class; no reading order, no transcription.
- **Layout-aware document VLMs** that emit structured markup with positional or order tags: **PaddleOCR-VL-0.9B / VL-1.5** use a two-stage pipeline where **PP-DocLayoutV2** detects regions *and* predicts reading order before the 0.9B VLM transcribes [32]. In Parse-x measurements, PaddleOCR-VL-1.5 holds the #1 layout-proxy slot at PaIRS 0.8766 on a zero-shot SAVIOR run [1].
- **Native-bbox OCR-2 models**: **Chandra** (`datalab-to/chandra-ocr-2`) is the only in-scope engine emitting bbox-grounded HTML natively, reaching mean PaIRS 0.6472 on the ParseBench n=10 table split (see App. A.2 canonical entry for architecture, variance range, and contamination posture) [10][25].
- **Reading-order specialists**: **LayoutReader** (seq2seq over text+layout, near-ceiling on ReadingBank) [29] and the recent **FocalOrder** (focal preference optimization for reading-order detection, 2026) [33].
- **Flat-OCR baselines**: HyperAPI parse (Paddle backbone) and Tesseract emit no spatial structure; HyperAPI parse scores PaIRS 0.2907, structurally expected for a primitive that returns flat markdown [10].

### Gaps relative to the framework

Three deltas distinguish Parse-x's D-LAYOUT from the prior work above.

1. **Joint element + order + spatial-fidelity scoring.** PubLayNet/DocLayNet/M6Doc score bboxes; ReadingBank scores order; OmniDocBench scores order via NED but not paired-spatial fidelity. Parse-x is, to the authors' knowledge, among the first frameworks to jointly score `layout_element_accuracy` (tree F1), `reading_order_accuracy` (rank-correlation), and PaIRS (z-euclidean pairwise spatial; an internal Hyperbots metric vendored from hyprbots/vlm_ocr at commit 1fbbc334 and not externally validated) on a single gold corpus, namely ParseBench's `layout` split (16,325 rules over 500 PDFs) plus the Inv3D upstream share (~46 docs) of SAVIOR [25].
2. **PC-vs-NPC discipline on PaIRS.** SAVIOR §2.2 explicitly retracts any PC-vs-NPC PaIRS contrast [1]; Parse-x carries the same caveat as a publish-gate condition. No other public benchmark we surveyed flags this comparability boundary.
3. **Cross-mapping to a 16-doc-type taxonomy.** OmniDocBench's 10 doc-types and DocLayNet's 6 categories are coarser than Parse-x's 16-type taxonomy, and none route layout scores back to a downstream parse-intent F1 (D-DOWNSTREAM) for the same document. The framework's published-snapshot is therefore one PaIRS-zero-shot leader (PaddleOCR-VL-1.5 at 0.8766) and *zero* `layout_element_accuracy` / `reading_order_accuracy` cells; a stub that the ParseBench port (BLK-14) is scheduled to fill [25].

## D-BBOX: bounding-box IoU + field-to-region grounding

*Relation to D-LAYOUT*: D-BBOX is best read as a granularity sub-axis of D-LAYOUT (token vs element vs field-region bounding boxes) rather than a fully orthogonal dimension; the two share the underlying spatial-recovery surface and a system that does poorly on D-LAYOUT element-bbox F1 will, in general, also do poorly on D-BBOX field-region IoU.


D-BBOX scores whether a parse engine can *localize* what it reads, emitting a bounding box for each token, semantic element, or extracted field, and (under the field-to-region variant) mapping each field in the structured output back to the page region it came from. The framework pins two metrics: `bbox_iou` (mean IoU of predicted vs. gold boxes over matched tokens) and `field_to_region_grounding_accuracy` (fraction of extracted fields whose predicted box overlaps the gold token-region at IoU ≥ 0.5) [34]. The dimension matters because downstream legal, audit, and review workflows demand citation back to the page; a parser that emits well-formed HTML without geometry fails the requirement most relevant to production use [34]. This is also the dimension where prior art is thinnest. SAVIOR-Bench explicitly logs `bbox_iou` and `field_to_region_grounding_accuracy` as **defined-but-not-measured** under risk item R9, because no gold field-box corpus was in scope [35].

### Prior benchmarks

- **DocLayNet**: 80,863 human-annotated PDF pages with bounding boxes across 11 layout classes (text, title, table, figure, list, page-header, page-footer, etc.), released in COCO format and scored with mAP@IoU[0.50:0.95] [27]. Strong baselines: Mask R-CNN ResNet-101 reaches 73.5 mAP, Faster R-CNN 73.4, LayoutLMv3 75.1, all roughly 10 points behind inter-annotator agreement [27]. **What it does not measure relative to our framework:** layout-element boxes only, no field-to-region grounding (no notion of "extract `invoice_total` → which box did it come from"); single (mostly English) corpus, low table-density.
- **PubLayNet**: 358,353 biomedical PDF pages auto-annotated from PMC XML with bounding boxes for {text, title, list, figure, table}; mAP@IoU[0.50:0.95] scoring [26]. **Does not measure:** narrow domain (PMC research articles), boxes are auto-aligned from XML and known to drift, no field-level grounding, no handwriting/forms.
- **FUNSD** [9] (see App. B.1): supplies word-level boxes and intra-document Q->A entity links. **Does not measure:** tiny scale; single-page English forms; entity-link grounding is intra-document, not field-to-region under a downstream-extraction schema.
- **Inv3D**: 25,000 synthetic 3D-warped invoice samples (plus `Inv3DReal` of 360 real smartphone captures) released with per-token boxes and template-anchored ground truth, originally built for document unwarping [36]. SAVIOR-Bench's bbox-eligible slice (~9.04%, ~46 docs) draws from Inv3D's upstream boxes [35]. **Does not measure:** synthetic-dominated, invoice-only domain, no extraction-task field schema layered on top.
- **ICDAR 2023 Robust Layout Segmentation Competition (DocLayNet challenge)**: competition track using DocLayNet's COCO format with mAP@IoU[0.50:0.95] over 11 classes [37]. **Does not measure:** layout segmentation in isolation; no end-to-end "parse-then-localize-the-field" task.
- **SAVIOR-Bench R9 ("bbox grounding")**: defines `bbox_iou` and `field_to_region_grounding_accuracy` over a planned financial-document corpus but logs them as *not yet measured*; flagged as the single largest unmeasured surface in the benchmark [35].
- **Silver-bbox pipeline (this project)**: internal spec [38] auto-derives token boxes from digital PDFs via PyMuPDF with a pdfplumber 10% cross-check (IoU < 0.95 → `silver_confidence: low`); every cell is stamped `gold_kind: "silver-pymupdf"` and may never be flipped to gold without human annotation. Unblocks drift/agreement signals on digital PDFs; explicitly **not leaderboard-publishable** for accuracy claims.

### Models surveyed

- **Native bbox-emitting OCR engines.** **Chandra** is the in-scope reference for native bbox-grounded HTML emission, covering all four ParseBench primary metric surfaces by default (see App. A.2 canonical entry) [25][39][34]. **Surya** (`datalab-to/surya`) emits layout boxes and benchmarks on PubLayNet/DocLayNet using a coverage-based scorer (≥0.5 = match) rather than IoU; reports precision 0.782 on DocLayNet, 0.751 on BCE [40]. **KOSMOS-2.5** is a multimodal literate model that generates "spatially-aware text" (line text concatenated with bounding boxes via a special operator) for document text recognition [41].
- **Layout-detector models scored on DocLayNet/PubLayNet.** Mask R-CNN ResNet-101 (73.5 mAP), Faster R-CNN (73.4), YOLOv5 family, LayoutLMv3 (75.1 mAP with text-modality fusion) [27]. These are detection-only; they do not parse content.
- **Document-VLMs with weak/no geometry.** GPT-4o, Gemini-1.5-Pro, Qwen2-VL/Qwen3-VL, InternVL2, mPLUG-DocOwl1.5, GOT-OCR-2.0 (per DOSSIER §2 model lists [42]) generally do *not* emit per-token boxes in their default decoders; they pass D-OCR but fail D-BBOX structurally.
- **Plain-text OCR primitives.** Tesseract, PaddleOCR-v4/VL-1.5, and the HyperAPI parse primitive emit text without spatial geometry on the public surface; D-BBOX is structurally untestable on these without an SDK change (carry-over Q-DF-7) [34].

### Gaps relative to the framework

1. **Field-to-region grounding is essentially un-benchmarked.** DocLayNet, PubLayNet, ICDAR-2023 measure *layout* boxes; FUNSD measures *entity* boxes; none score "extracted field `total_amount` → originating page region at IoU ≥ 0.5". Our `field_to_region_grounding_accuracy` is the framework-novel surface, building on SAVIOR-Bench R9's definition [35].
2. **Gold paucity for field boxes.** Inv3D + FUNSD give ~90 docs of upstream gold token boxes; ParseBench's `layout` split adds 16,325 rules across 500 PDFs but at element (not field-schema) granularity [43]. Closing R9 with gold is a partner-annotation ask; the silver-bbox pipeline closes it *partially* without funding [38].
3. **Apples-to-oranges scoring across prior benchmarks.** DocLayNet uses COCO mAP@[0.50:0.95]; Surya's published numbers use coverage-with-0.5-match (not IoU); FUNSD reports F1 over entity bbox+label. Our framework pins a single `bbox_iou` mean over matched tokens plus the IoU ≥ 0.5 grounding rate, so cross-engine cells are comparable.
4. **Native-bbox emission is rare.** Of ~40 v0-runnable models in the DOSSIER, only Chandra (and partially Surya and KOSMOS-2.5) emit geometry by default; the rest fail D-BBOX *structurally*, not numerically. The framework reports these as "structural 0" rather than as a quality gap [34].
5. **Domain coverage.** Prior corpora are biomedical (PubLayNet), corporate-mixed (DocLayNet), forms (FUNSD), or invoice-synthetic (Inv3D). The 16-doc-type taxonomy surfaces uncovered slices (handwritten notes, tax forms, statements, contracts) where no D-BBOX cell is currently runnable even with the silver pipeline.

## D-TABLE: GTRM + TableRecordMatch + cell F1

Table structure recognition (TSR) is the hard core of enterprise document parsing: invoices, packing slips, bank statements, 10-Q financials, and insurance schedules are dominated by tabular content with spanning headers, merged cells, borderless rules, repeated multi-page headers, and locale-specific currency formatting [44]. A high word-recall transcription can still get the row/column assignment wrong, which destroys downstream extraction [44]. D-TABLE in the Parse-x framework therefore scores table-bearing documents (T-04 bank statement, T-11 financial statement, T-16 packing slip) on whether the engine recovers both the grid topology and the cell content, using the ParseBench `table` split (n=503 ground-truth HTML tables, 284 documents) with **GTRM** (the unweighted average of GriTS and TableRecordMatch) as primary, and TEDS plus cell-F1 as secondaries [parsebench2026, framework2026].

### Prior benchmarks

- **PubTabNet** (Zhong et al., IBM): ~568k scientific tables from PMC articles, distributed with HTML structure-and-content ground truth. It introduced **TEDS** (Tree-Edit-Distance-based Similarity) and **TEDS-Struct**, and remains the canonical TSR pretrain anchor [45]. TEDS, and by extension the GriTS / GTRM lineage, ultimately rests on the **Zhang-Shasha** tree-edit-distance algorithm [158], which provides the O(m²n²) ordered-labelled-tree edit cost that the framework's table scorer must port deterministically to be cross-engine comparable. Limit relative to D-TABLE: scientific-paper distribution only; no enterprise finance distribution, no bbox geometry on every cell, and TEDS is sensitive to small text noise so structure vs content errors are conflated unless paired with TEDS-Struct [44].
- **FinTabNet** (Zheng et al., IBM, WACV 2021): ~113k tables across ~70k pages from S&P-500 annual reports, with cell bboxes and structure (train/val/test = 91,596/10,635/10,656) [46]. Closest public proxy to enterprise finance tables, but the distribution is digital-PDF-rendered 10-Ks only, with no scans, no invoices, no packing slips, no multi-page table stitching across the doc-type taxonomy the framework requires.
- **PubTables-1M** (Smock et al., CVPR 2022): ~948k tables with joint detection + structure annotations; introduced the **Table Transformer (TATR)** baseline and the **GriTS** metric family (GriTS-Top topology, GriTS-Con content, GriTS-Loc IoU geometry), formally published at ICDAR 2023 [pubtables1m2022, grits2023]. GriTS operates on the 2D cell grid (not a tree) and handles non-tree spanning structures more robustly than TEDS [47]. Limit: same scientific-PDF bias as PubTabNet; no enterprise scans; GriTS-Loc requires bbox GT that most non-PubTables corpora lack.
- **ICDAR-2013 Table Competition and ICDAR-2019 cTDaR**: small, hard mixed-domain sets including historical and handwritten tables; canonical home of **adjacency-relation F1** (precision/recall over horizontally/vertically adjacent cell pairs whose endpoint text and direction both match), which decomposes errors by split / merge / shift type [44]. Limit: corpus is small and not enterprise-representative; metric depends on a normalizer the framework must pin identically to pred and gold.
- **TableBank** (Li et al., LREC 2020): ~417k tables harvested from Word and LaTeX sources, primarily a *detection* benchmark with weak structure labels [44]. Useful for detection breadth; insufficient for cell-F1 / GTRM scoring.
- **RD-TableBench** (Reducto, 2025): open-source enterprise-leaning table benchmark with messy real-world scans; designed as an industry counterweight to scientific-only TSR sets [48]. Recent and small relative to FinTabNet; metric protocols vary by reporter.
- **ParseBench `table` split** (LlamaIndex / community, 2026): 503 pages across 284 documents, distributed under Apache-2.0 with per-doc HTML `expected_markdown`; uses **GTRM** = mean(GriTS, **TableRecordMatch**) where TableRecordMatch treats a table as a bag of records keyed by column header(s) and is therefore insensitive to row/column reordering but heavily penalizes transposed/dropped headers [49]. This is the gold the framework ports for D-TABLE; what it does *not* cover is doc-type stratification (T-04 vs T-11 vs T-16 are not separable inside the 503 without re-labeling) or the Q-LOW / multilingual strata.

### Models surveyed

- **Specialist TSR.** Table Transformer (TATR) on PubTables-1M [50]; earlier lineage DeepDeSRT, TableNet, SPLERGE, LGPMA, TableFormer / EDD (the PubTabNet HTML-token convention) [44]; PaddleOCR PP-Structure as a layout+TSR+OCR cascade. Camelot/Tabula are rule-based (lattice/stream), strong only on ruled digital PDFs.
- **OCR-2.0 / end-to-end structure emitters.** GOT-OCR2.0 (HTML/Markdown/LaTeX tables); Nougat (academic-PDF Markdown, brittle off-domain); MinerU / PDF-Extract-Kit pipelines that wrap specialist TSR [44].
- **Prompted VLMs (the framework's open-prompted SOTA route).** Qwen2.5-VL 3B/7B/32B/72B (HTML/Markdown table emission with bbox-grounded cells); InternVL 2.5 / 3; dots.ocr; PaddleOCR-VL; olmOCR; DocOwl/UReader; MiniCPM-V; Phi-3.5/Phi-4-vision [44]. Chandra is included for table extraction with documented per-doc PaIRS variance on the ParseBench n=10 table sub-slice (see App. A.2 canonical entry) [25].
- **Closed frontier (anchor-only, not products).** GPT-4o/4.1, Gemini 1.5/2.x, Claude 3.x, used as scientific anchors, never as winners [44].

### Gaps relative to the framework

1. **GTRM is novel and not yet in the public scorer ecosystem.** GriTS and TableRecordMatch each exist [grits2023, parsebench2026], but their unweighted average is a ParseBench-internal convention; the framework must port the implementation deterministically (Zhang–Shasha for TEDS, factored row/col alignment + Hungarian for GriTS, identical lenient HTML normalizer applied to pred and gold) before any GTRM cell is publishable [tabular-survey2026, framework2026]. As of the framework snapshot, **zero GTRM cells have been published**; TR-000 is REGISTERED-NOT-YET-RUN [25].
2. **Doc-type stratification.** No prior table benchmark cleanly separates bank statement vs 10-Q vs packing slip vs insurance schedule; the framework's 16-doc-type taxonomy crossed with D-TABLE exposes per-doc-type collapse modes that PubTables-1M / FinTabNet aggregate away.
3. **Quality and language strata.** PubTabNet/FinTabNet/PubTables-1M are digital-PDF clean; ICDAR-2019 cTDaR is the only hard-scan anchor and is small. D-TABLE × D-DOC-QUALITY (Q-LOW JPEG-Q40 / rotated / blurred re-renders) and × D-LANG overlays are framework-native crosses with **no public corpus** today.
4. **Proxy-metric honesty.** The current Azure DI long-invoice cell carries line-count preservation 0.6396 / line-item set-F1 0.3439 (proxies, not GTRM) and the framework explicitly marks them as such rather than back-fitting to GTRM [25]. Prior leaderboards have substituted proxies without disclosure.
5. **Apples-to-apples decoding pins.** ParseBench-reported numbers mix zero-shot vs fine-tuned VLMs, varying TEDS variants, and unpinned decoding [44]; the framework's pinned-prompt + decoding contract is the missing comparability layer.

## D-DOC-QUALITY: stratification by document quality (Q-HIGH/MED/LOW)

D-DOC-QUALITY asks a question that the headline accuracy number on a parse benchmark almost always hides: when the input is a degraded scan (JPEG-Q40 compression, ≥5° rotation, motion or defocus blur, low DPI), does the engine's accuracy collapse, drift, or hold? In the Parse-x framework it is explicitly a **stratification** of D-OCR and D-PARSE-INTENT rather than an independent score, with the primary metric being the signed delta in `savior_word_recall` between Q-HIGH and Q-LOW renderings of the same corpus under identical decoding pins, and a Q-MED midpoint reported for monotonicity diagnosis [51]. The degradation recipe is borrowed from [52] §10 R4. Failure modes F1 (vertical/rotated text), F5 (degraded scan) and F8 (stylized text) are expected to activate disproportionately in Q-LOW [51].

### Prior benchmarks

- **SAVIOR-Bench v1**: 509 documents drawn from UCSF (47%), synthetic (18%), financial (17%), Inv3D (9%) and FUNSD (9%), with IAA 0.761 over 187 double-annotated pairs. The corpus deliberately includes "low-quality PDFs" and "degraded scans" as a class label, but the published results are aggregate-only: no per-quality slice, no degradation track, and no rendered Q-HIGH/Q-LOW counterparts of the same document. The authors flag this themselves as recommendation R4 ("No degradation / robustness tracks ... not done, no degraded corpus exists") [52].
- **DocIQ / DIQA-5000**: a subjective document-image-quality dataset that partitions 5,000 corrupted images into five degradation classes (luminance, distortion, blurriness, noise, compression). It is a quality-*assessment* dataset (predict the MOS), not a parse-accuracy benchmark; it does not score OCR or layout downstream of the degradation [53].
- **DocUNet**: 130 mobile-camera captures of 65 paper documents (receipts, letters, fliers, magazines, books) annotated with the flat-scan ground truth and split into "easy" (single crease/fold) and "hard" (heavy wrinkles) cases. It scores geometric dewarping (MS-SSIM, Local Distortion), not parse fidelity, but is the closest public source of paired clean/degraded scans of the same content [54].
- **RVL-CDIP**: 400,000 grayscale ~100 DPI documents from 1980s–90s scanners, which are *intrinsically* low-quality but not stratified: there is no Q-HIGH counterpart of the same document. Subsequent audits also report 8.1% label noise (range 1.6–16.9% by class), which contaminates any quality-versus-accuracy slope estimated on top of it [55][56].
- **Historical-OCR benchmarks (IMPACT, olmOCR-Bench historical split)**: IMPACT supplies degraded historical print as a single domain; olmOCR reports 82.3% on old math scans dropping to 47.7% on general historical scans, demonstrating the degradation gap but, again, with no controlled stratification of the same source at multiple quality tiers [7][57].
- **Augraphy**: a data-augmentation *library* (ink bleed, jitter, lighting, scanner artefacts) widely used to synthesise degraded training data; it provides the operators that a Q-LOW renderer needs but is not itself a benchmark [58].
- **SOULSHINE / bol-grn (Hyperbots-internal)**: 22 BoL PDFs (soulshine1) + 22 byte-identical bol-grn-test inputs (soulshine2); native mixed-quality PNG-derived scans are present (two long-tail outliers at ~140 and ~56 pages, customers omitted) but no gold and no quality stratification, only OCR-sweep counts (Tesseract 22/22, PaddleOCR 15/22) [59].

### Models surveyed

Models likely to be measured under D-DOC-QUALITY are drawn from the same families already measured on D-OCR / D-PARSE-INTENT in the project dossier [42]:

- **OSS document-parse VLMs**: Chandra (`datalab-to/chandra-ocr-2`), Qwen3.6-35B-A3B, Qwen2.5-VL-3B/7B/72B, Qwen3-VL-32B/235B, MinerU-2.5 / MinerU-2.5-Pro-2604, PaddleOCR-VL-1.5, Surya, Marker-1.0, Nougat-0.1.0, mPLUG-DocOwl 1.5 / DocOwl2, GOT-OCR-2.0, FireRed-OCR, DeepSeek-OCR-2, Logics-Parsing-v2.
- **Closed VLMs accessible via API**: GPT-4o, GPT-4.1, Gemini 1.5/2.5 Flash and Pro, Claude Sonnet 4.6, Mistral-Large-3-675B, Llama-3.2-90B-Vision; routed via Azure OpenAI for the OpenAI family per project preference.
- **Legacy/baseline OCR**: Tesseract-OCR, PaddleOCR-v4, EasyOCR, OpenOCR, Mathpix, HyperAPI parse (paddle-backed).
- **Document-image-quality assessment heads (auxiliary)**: DocIQ feature-fusion network [53] and the no-reference text-line DIQA model [60]; not parsers, but candidates for predicting the Q-stratum a document will land in pre-flight.

Prior measurements on these models almost never report per-quality slices; the F-B study panel (Chandra/Qwen3.6/Tesseract/HyperAPI-parse on ParseBench n=10) is aggregate only [42].

### Gaps relative to the framework

1. **No public benchmark renders the same document at controlled Q tiers.** SAVIOR-Bench labels low-quality as a *class* but does not pair it with a high-quality counterpart of the same document; DocUNet pairs warped vs flat but on a geometric axis, not on JPEG/blur/DPI; RVL-CDIP and IMPACT are intrinsically low-quality with no clean twin [52][54][55][57]. The Parse-x publish-gate of "Q-HIGH and Q-LOW counterparts of the same dataset, same model, same prompt, same decoding" therefore has no off-the-shelf source and must be built; the spec proposes synthetic re-renders of SAVIOR-Bench with frozen ImageMagick/Pillow degradation seeds [51].
2. **No signed-delta metric is standard.** Robustness studies of VLMs under common corruptions report aggregated accuracy drops [61][62] but do not pin the metric to a parse-specific recall (e.g. `savior_word_recall`) nor publish per-document deltas that would let a downstream consumer flag fragile engines.
3. **Failure-mode incidence is unreported.** F1/F5/F8 incidences in the Q-LOW stratum are explicitly called out by Parse-x; no prior benchmark publishes per-failure-mode F-scores stratified by quality [52][51].
4. **Internal datasets are not yet stratified either.** The SOULSHINE BoL corpus is native mixed-quality but has no gold and no Q-tier labels [59]; today's snapshot is "zero Q-* stratified cells" [51].
5. **Quality-assessment heads are not coupled to parse benchmarks.** DocIQ and DIQA-5000 predict subjective quality but are not run as gates upstream of a parse leaderboard [53][60]; Parse-x's Q-tier assignment is currently rule-based (JPEG-Q40/rotation/blur/DPI), leaving an open question of whether learned IQA scores should replace the rules.

Limited prior art segments parse accuracy by quality tier on the *same content*; this is the principal contribution opportunity for the D-DOC-QUALITY dimension.

## D-LANG: multilingual evaluation overlays (EN/DE/FR/ES/ZH/JA/AR)

D-LANG asks a simple but operationally critical question: does an engine's transcription and parse quality hold when the *same* document template is rendered in a non-English language or script? The Parse-x framework spec defines this dimension as a **stratification overlay**, not a standalone task; the primary metric is the *signed delta* in `savior_word_recall` (D-OCR) and field-level parse accuracy (D-PARSE-INTENT) between an L-EN baseline and each of L-DE/FR/ES/ZH/JA/AR strata [51]. This framing is motivated by SAVIOR-Bench's Pillar-6 finding that a "multilingual / very-dense-layout" residual cluster persists even after fine-tuning, i.e., the gap is real and is not closed by SAVIOR-Train [1]. The framework's gold-construction recipe (rendering translated text into the same LibreOffice template, plus native partner annotation for L-ZH/JA/AR) is explicitly designed to hold layout constant so any delta is attributable to script and language, not template drift [51].

### Prior benchmarks

- **MTVQA** (ByteDance, 2024; ACL Findings 2025): 6,778 human-annotated QA pairs over 2,116 text-centric images across 9 low-resource languages (AR, DE, FR, IT, JA, KO, RU, TH, VI). Reports GPT-4o/4V/Claude-3/Gemini all "with large room for improvement"; per-language accuracy is the primary metric [63]. **Does not cover**: ZH, ES; no layout-held-constant control; no separation of OCR error from VQA-reasoning error, so cannot be used directly as a D-OCR overlay.
- **XFUND** (Microsoft, ACL Findings 2022): 1,393 forms in 7 languages (ZH, JA, ES, FR, IT, DE, PT), 199 per language, with SER and RE tasks; extension of the English FUNSD [64]. **Does not cover**: AR, EN (defers to FUNSD), and provides only form-style documents, narrow over the Parse-x 16-doc-type taxonomy. Metric is entity-level F1, not transcription-level edit distance, so it does not score D-OCR directly. The companion **LayoutXLM** model [155] extends LayoutLMv2 with multilingual pre-training over 53 languages and is the canonical encoder evaluated on XFUND; it remains a key multilingual document-understanding baseline against which D-LANG-overlay deltas can be referenced.
- **OCRBench v2** (Fu et al., arXiv 2501.00321): bilingual (EN/ZH) benchmark of 10,000 human-verified QA pairs across 23 tasks and 31 scenarios, with a 1,500-image private split [3]. **Does not cover**: any of DE/FR/ES/JA/AR; the EN/ZH split is the binary axis, not the 7-language overlay Parse-x requires.
- **MDPBench** (cited in OCRBench v2 ecosystem): 3,400 document images across 17 languages including Simplified/Traditional Chinese, EN, AR, DE, ES, FR, JA, the closest existing match to the Parse-x 7-language target set [65]. **Does not cover**: layout-controlled rendering of the same template across languages, so per-language deltas conflate template variance with language variance.
- **M3DocVQA / M3DocRAG** (Cho et al., arXiv 2411.04952, ICCV 2025 Workshop): 3,000+ PDFs, 40,000+ pages for multi-page multi-document VQA [66]. **Does not cover**: language stratification is incidental rather than designed; primarily an EN long-document retrieval benchmark.
- **M4-ViteVQA** (NeurIPS D&B 2022): 7,620 video clips, 25,123 QA pairs over 9 categories for video scene-text VQA [67]. **Does not cover**: documents (it is video-scene-text), and is largely monolingual; useful only as a reference for video-OCR multilingual extensions, not D-LANG itself.
- **Language-specific OCR corpora**: SCUT-EPT, 50,000 handwritten Chinese exam-paper text lines, 4,250 character classes, the standard Chinese HCTR benchmark [68]; MTWI, Chinese web-image scene text (2018 ICPR competition track, ~20k images) [69]; and **synthetic Japanese** lines used to bootstrap PaddleOCR's `japan` model [70]. These provide per-script transcription gold but are not template-aligned to any English baseline.

### Models surveyed

From DOSSIER §2 the v0-runnable OCR/VLM panel includes models with explicit multilingual coverage and models that are English-only by default, a contrast our overlay is designed to expose:

- **Multilingual-by-design**: **PaddleOCR-VL-1.5** and **PaddleOCR-v4** (CN/EN/JP/KR plus 80+ alphabet languages via `--lang` flag) [70]; **Qwen2-VL-7B/72B** and **Qwen3-VL-235B** (Alibaba, multilingual text+vision pretraining covering ZH/EN/JA/KO/DE/FR/ES/AR) [71]; **InternVL2-8B/26B/76B** (multilingual pretraining including ZH/EN) [72]; **GLM-OCR** and **MinerU-2.5** (Chinese-first OSS); **GPT-4o**, **Gemini-1.5-Flash/Pro** (broad multilingual VQA, evaluated on MTVQA) [63]; **Mathpix** and **Textract** (multilingual mode by configuration).
- **English-first / multilingual-by-pack**: **Tesseract-OCR** ships English by default; multilingual support requires the `tesseract-lang` data pack (165 traineddata files, 685.7 MB) which the Parse-x harness only installed on 2026-06-10, before which Chinese inputs threw `UnicodeDecodeError` and Tesseract `text_content` scored 0.0 on the diverse n=10 ParseBench split [42]. This is exactly the structural failure mode D-LANG is meant to surface.
- **Latin-script-leaning**: **Marker-1.0**, **Nougat-0.1.0**, **GOT-OCR-2.0**, strong on EN academic PDFs, with limited or undocumented L-ZH/JA/AR coverage [42].

### Gaps relative to the framework

1. **No prior benchmark holds layout constant across the L-EN→L-* axis.** XFUND, MTVQA and MDPBench all vary template and language together; Parse-x's LibreOffice-rendered translation overlay is the first to isolate language as a single-variable delta on a fixed template [51].
2. **Per-language D-OCR vs D-PARSE-INTENT separation is absent in prior art.** MTVQA, M3DocVQA and OCRBench v2 score end-to-end answer accuracy, conflating recognition error with reasoning error. Parse-x decomposes the delta into D-OCR (word recall) and D-PARSE-INTENT (field-level) per language stratum.
3. **SAVIOR's F9 "multilingual residual" has no per-language counts**; the SAVIOR PDF explicitly states "no per-class counts available" for the multilingual residual cluster [1]. Parse-x's 7-language stratified report directly fills this measurement hole.
4. **English-only-by-default tooling is invisible to prior benchmarks** that ship a multilingual harness. Parse-x logs the Tesseract-without-tesseract-lang failure as a first-class result, not a setup bug, surfacing a procurement-relevant gap [42].
5. **L-AR (RTL script) coverage is thin everywhere.** Among prior benchmarks only MTVQA and MDPBench include Arabic; ZH/JA/AR partner annotation is gated in Parse-x v0 (Q-DF-5) [51], an honest scope limitation rather than a coverage claim.

## D-DOWNSTREAM: parse → downstream extract F1 (parse-lift; new CEO-required dimension)

D-DOWNSTREAM scores a parse engine not by how well its output *reads* but by how well it *feeds the next stage*. Concretely, a frozen field-extractor (Qwen 3.6-35B-A3B in v0, pinned at `T=0.1, top_p=0.9, max_tokens=2048, seed=20260516`) is run twice per document: once conditioned on `parse(doc) → text`, once on the raw page image. The primary metric is `downstream_extract_micro_f1`; the headline is `parse_lift = downstream_extract_micro_f1 − no_parse_extract_micro_f1`, with paired-bootstrap CI95 over docs in the spirit of [73]. Positive lift indicates that parse contributes measurable value to the pipeline; zero or negative lift indicates that the parse stage adds no value over a direct vision-LLM baseline. The dimension is, to the authors' knowledge, not previously formalized in parse benchmarks: virtually all prior parse leaderboards score the parse string intrinsically (edit distance, BLEU-on-markdown, layout F1, table TEDS) and infer downstream utility only by analogy. D-DOWNSTREAM addresses that inference gap by measuring it directly. Per the framework spec (lines 140–172), today's snapshot is zero published cells; harness wiring for `extractor_pin` and the paired-lift computation is on the F-A phase list.

### Prior benchmarks

Prior art splits into three buckets, none of which is a clean parse-lift benchmark.

**Intrinsic KIE leaderboards.** SROIE (626 train / 347 test receipts, four entity fields) and CORD (1,000 receipts, 30 labels) are the canonical end-task KIE sets; both report field-level F1 against gold but condition the extractor on *gold or dataset-provided OCR boxes*, not on a swappable parse engine [74][75]. LayoutLMv3-large reaches 97.46 F1 on CORD (Table 1, official 800/100 split) [76], and the original LayoutLM-large reports 95.24 F1 on SROIE receipt understanding [76b]. These measure extractor quality given fixed text; they do not vary the parser nor compute a parse-vs-no-parse lift. FUNSD (149/50 forms) [77] is analogous for form understanding.

**Document VQA / end-task substitutes.** DocVQA [78] (see App. B.1) is sometimes used as a proxy for "did parse help" (OCR-pipeline answers vs direct VQA); the Agentic Document Extraction 99.16 result outperforming OCR pipelines by 3.2 pp GT-in-Pred [79] is exactly the "parse may be net-negative" signal D-DOWNSTREAM is built to surface.

**OCR-quality-impact studies.** van Strien et al. [80] assessed six downstream NLP tasks (NER, dependency parsing, IR, topic modelling, LM fine-tuning, sentence segmentation) as a function of OCR character-error rate on historical newspapers, finding consistent task-level degradation and recommending ≥90% OCR quality. Chiron et al. [81] showed retrieval MAP drops materially with OCR error on a 22k-document Portuguese IR collection. Both *demonstrate* that intrinsic OCR scores predict downstream loss weakly, but neither defines a paired-lift metric nor pins a single extractor across engines.

**Composite parsing benchmarks.** SAVIOR-Bench [1] defines `parse = extraction + layout + bbox`; its Facet-1 extraction sub-score (parse-intent F1 / WER, in-house leaderboard; SAVIOR-Train fine-tune at F1 0.8328 / WER 0.2589; GPT-4o zero-shot 0.8052 / 0.4232) is the closest sibling, but it scores the parser's *own* extraction head; there is no frozen-downstream-extractor pin, so engines with strong native heads (e.g. layout-aware VLMs) and engines that emit only markdown text (e.g. Tesseract) are not compared apples-to-apples on downstream utility. OmniParser [23] unifies text spotting, KIE, and table recognition into one model but again co-trains parse and extract; OmniDocBench [4] scores parse intrinsically across doc types.

The honest summary: **limited prior art on paired parse-lift with a frozen extractor.** ASR has a long tradition of WER vs downstream-NLU evaluations and MT has paired-bootstrap significance since [73], but the parse-then-extract pipeline has not standardised the analog.

### Models surveyed

In-scope as **parse engines** (varied across the D-DOWNSTREAM cell row): HyperAPI parse (Hyperbots production primitive), Chandra (layout+bbox+table), MinerU 2.5 / MinerU2.5-Pro-2604-1.2B, PaddleOCR-VL-1.5, Marker-1.0, Surya, DocOwl2 / mPLUG-DocOwl1.5, Nougat-0.1.0, GOT-OCR-2.0, DeepSeek-OCR-2, Logics-Parsing-v2, Tesseract-OCR (deterministic-text baseline), per DOSSIER §2.x model rosters [10].

In-scope as **frozen extractor pins** (one chosen, all engines share it): the v0 pin is Qwen 3.6-35B-A3B (Hyperbots IP fine-tune, served at `http://135.233.113.234:6006/v1`; DH-001 FieldRecall 0.4099 at n=95, CI95 [0.3454, 0.4784], 2026-06-10) [10]. Candidate alternate pins for sensitivity checks: Qwen3-VL-32B-Instruct, GPT-4.1 / GPT-5.4 thinking via Azure OpenAI, Claude Sonnet 4.6, Gemini 2.5 Pro, Mistral-Large-3-675B, Llama-3.2-90B-Vision; but if the pin changes, every cell re-runs.

### Gaps relative to the framework

1. **No prior benchmark publishes `parse_lift` with paired-bootstrap CI.** SROIE/CORD/FUNSD (see App. B.1) vary the extractor while holding text fixed; D-DOWNSTREAM does the inverse (frozen extractor, varied parser) and reports the *paired* difference per doc per [73]. SAVIOR-Bench reports per-engine extraction but not a swapped-extractor lift.

2. **No prior benchmark reports per-doc-type lift across a 16-type taxonomy.** Aggregate F1 hides that parse may lift on T-07 bank-statement (long tabular pages) and degrade on T-08 cheque (short image where direct VQA wins); the framework requires a 16-row table per engine and a `weighted_parse_lift` aggregate.

3. **Extractor-leakage is unaddressed in prior pipelines.** Because no prior public benchmark pins the extractor, the question "is the lift you measured a property of parse or of an extractor trained on these docs?" is unanswerable. The framework names the risk explicitly (Q-DF-2; Qwen 3.6 is a Hyperbots IP fine-tune; contamination audit is a follow-on item).

4. **Image-only doc handling.** OCR-impact studies [80] hold text-OCR as the only input; D-DOWNSTREAM specifies that the baseline leg for image-only docs (T-08 cheque PNG) is raw image to the same extractor, so the no-parse baseline is well-defined for every doc type.

5. **Engine-error honesty.** Long-doc 300s timeouts in the extract leg surface as `engine-error` cells rather than silent skips (BLK-4), preserving the integrity of the lift mean.

## D-COST-LATENCY: $/correct and p50/p95/p99 latency

The D-COST-LATENCY dimension asks whether a parse engine is shippable, not just accurate. The Parse-x framework spec defines its primary metrics as `latency_p50_ms`, `latency_p95_ms`, `latency_p99_ms`, and `dollars_per_correct_call` (cost divided by count of calls that clear the accuracy threshold of the relevant primary metric), with failure rate and throughput-at-concurrency-1 as secondary metrics [51]. The "$/correct" formulation reflects a design choice: a low-cost engine with 40% failure rate does not represent low effective cost, and an engine with high p99 timeout rate does not represent low effective latency. This dimension also runs as a secondary on every accuracy cell, which is unusual; most parse/OCR benchmarks ignore wall-clock and price entirely, and most LLM efficiency benchmarks ignore correctness.

### Prior benchmarks

**HELM (Stanford CRFM).** HELM is the canonical "holistic" framework: each of its 16 core scenarios is scored on 7 metrics including efficiency-as-latency and efficiency-as-cost alongside accuracy, calibration, robustness, fairness, bias, and toxicity [helm2022, helmdocs2026]. Efficient-HELM further offers fractional-sample runs that preserve ranking with far fewer tokens [82]. Relative to Parse-x, HELM measures *idealized* inference cost (denoised energy/$ estimates, often per query token count rather than wall-clock under load) on text-only scenarios; it does not normalize cost against per-task correctness, and its document/vision coverage (VHELM) is shallow on parse-style tasks like table-cell or bbox extraction [83].

**Artificial Analysis.** A widely used third-party leaderboard that pins all models to the same probe hardware and reports median output speed (P50 over 72 hours), time-to-first-token latency, and blended input/output price per million tokens [84]. By their March 2026 cut, the price spread across frontier models is roughly 250x bottom-to-top and YoY prices have dropped ~80% [85]. The methodology is rigorous on serving-side metrics but the workload is short prompt/short completion chat (not multi-page PDFs with image tokens) and there is no parse-correctness gate.

**MLPerf Inference.** MLCommons' MLPerf Inference v5.1 and v6.0 are the hardware-vendor standard, with audited submissions reporting Offline tokens/sec and Server p99 TTFT for models like Llama-3.1-8B and GPT-OSS-120B; v6.0 specifically tracks p99 TTFT for MoE-routed serving (e.g., a 2,903 → 2,001 ms reduction via the BLAZE routing patch) [mlperf51-2025, mlperfv6-2026]. MLPerf measures serving-stack efficiency under SLOs, but the "tasks" are LLM-shaped (chat, summarization), not document parse with ground-truth gold; $/correct is not a MLPerf concept.

**LLM-inference latency surveys.** Production-oriented metric guides (BentoML, GMI Cloud) codify the p50/p95/p99 + TTFT + ITL + throughput stack and explicitly warn that "a 0.4 s p50 / 4 s p99 looks great in demos and breaks in production" [bentomlmetrics2026, gmicloud2026]. These are methodology references, not benchmarks per se.

**Vendor pricing pages and OCR-cost surveys.** Mistral OCR is published at $1–2 per 1,000 pages [86]; Google Document AI ranges $1.50–$30 per 1k pages by processor; AWS Textract is $1.50/1k for basic OCR and $65/1k for forms-and-tables [87]. Frontier VLM passthrough (e.g., Gemini 2.5 Pro on a scanned page ≈ $0.13/page) costs ~60–167x more than self-hosted OCR-VLM pipelines [parslicost2025, ofoxocr2026]. None of these prices are joined to a per-task correctness gate.

**SOURCE-EXTRACT VLM-OCR (Hyperbots internal corpus).** The on-disk SOURCE-EXTRACT benchmark reports fine-tuned-Qwen-VL inference at p50 2,548 ms / p99 3,319 ms, 3% failure, and infrastructure-derived $0.000191 per successful call (≈ $0.19 / 1k) on A100-40GB at ~$2/hr [2]. Absent from that report are p90/p999, full latency histograms, and per-model LoRA cost amortization: exactly the secondary metrics Parse-x flags as gaps.

### Models surveyed

Relevant model families for this dimension fall into four tiers:

- **Frontier hosted VLMs** (Gemini 2.5 Pro, GPT-5.x via Azure OpenAI per [Hyperbots Azure OpenAI routing policy], Claude 4.x): high per-page cost (~$0.05–$0.13/page), high p50 latency on multi-image inputs, but strong accuracy [artificialanalysis2026, parslicost2025].
- **Cheap hosted OCR** (Mistral OCR 3, Google Document AI OCR, AWS Textract OCR): $1.50–$2 / 1k pages, sub-second-per-page typical, narrow output schema [mistralocr2025, docaicost2026].
- **OSS local VLM/OCR** (GLM-OCR 0.9B at 94.62 OmniDocBench, PaddleOCR-VL-1.5 at 94.50, MinerU-2.5, Chandra): negligible marginal $ if amortized, but p50 latency varies from sub-second (PaddleOCR) to ~8.5 s/page (Chandra smoke test, 528 prompt + 821 completion tokens) [ofoxocr2026, parsexframework2026].
- **Fine-tuned proprietary** (SAVIOR-Train Qwen-VL LoRA): p50 2.5 s, $0.19 / 1k successful on A100 [2].
- **Serving-stack baselines** (Llama-3.1-8B, GPT-OSS-120B per MLPerf): not parse models, but their published p99 TTFT envelopes set the floor for what an LLM-judge or downstream-extract leg can add to total wall-clock [mlperf51-2025, mlperfv6-2026].

### Gaps relative to the framework

Three deltas distinguish Parse-x D-COST-LATENCY from the prior art:

1. **$/correct as a primary, not a derived metric.** HELM, Artificial Analysis, and MLPerf all report cost OR accuracy but never divide them at the cell level. Parse-x incorporates the accuracy gate per dimension (e.g., D-OCR edit-distance threshold) into the cost denominator, so a 40%-failure engine reflects that failure in the headline number [51].
2. **Full p50/p95/p99 + failure rate on every accuracy cell.** Most academic parse benchmarks (OmniDocBench, ParseBench, DocVQA) publish a single accuracy column and no wall-clock at all [88]. Parse-x requires latency as a secondary on every cell and primary on the cost-cascade ensemble (E5), making cross-cell tail-latency comparisons possible.
3. **Price-list-pinned cost in `_meta`.** Prior benchmarks either use vendor list prices (Artificial Analysis) or infrastructure cost (MLPerf) but rarely commit to a pinned snapshot for reproducibility. Parse-x records the price-list timestamp per cell, which matters in a market where YoY prices fell ~80% [85]. Limited prior art on this specific reproducibility move.

Scope limitation: Parse-x does not yet measure energy-per-correct (kWh, gCO₂e), which HELM-v2 and MLPerf Power do track; this is a known follow-on, not a claimed strength.

## Appendix A. Model Lineage

Scope: ~50 models surveyed in DOSSIER §2.1 (OCR family, 31 cells) and §2.2 (parse-intent family, 19 cells) [10]. Each row lists base architecture, training data (as publicly disclosed), license, version pin (commit / release tag / `PENDING-PIN`), and one primary citation. Rows we could only confirm via the DOSSIER list, without an authoritative model card or paper read at table-build time, are clustered at the bottom under "Verified-via-DOSSIER-only; deep-citation PENDING" rather than fabricated.

### A.1. Verified lineage

| Model | Family | Base architecture | Training data | License | Version pin | Citation |
|---|---|---|---|---|---|---|
| Tesseract-OCR | OCR-classical | LSTM line recognizer (Tesseract 4/5) | 100+ langs, Google internal + community traineddata | Apache-2.0 | 5.3.x (DOSSIER `BLOCKED-LANG CLEARED 2026-06-10`) | [89] |
| EasyOCR | OCR-classical | CRNN + CRAFT detector | Synthetic + COCO-Text + ICDAR | Apache-2.0 | PENDING-PIN | [90] |
| PaddleOCR-v4 | OCR-classical | PP-OCRv4 (DBNet det + SVTR rec) | Internal Baidu + open Chinese corpora | Apache-2.0 | v2.7 / PP-OCRv4 release | [70] |
| PaddleOCR-VL-1.5 | OCR-VLM | PaddleOCR-VL (0.9B; ERNIE-4.5-0.3B LM + NaViT-style visual enc) | Disclosed in tech report; multilingual doc corpus | Apache-2.0 | v1.5 (HF `PaddlePaddle/PaddleOCR-VL`) | [32] |
| OpenOCR | OCR-classical | Modular det+rec (SVTR / DBNet) | Open academic OCR corpora | Apache-2.0 | PENDING-PIN | [91] |
| Surya | OCR-pipeline | Det/rec/layout/order ensemble (custom encoders) | Common Crawl PDFs + synthetic | GPL-3.0 / commercial dual | `datalab-to/surya` PENDING-PIN | [92] |
| Marker-1.0 | OCR-pipeline | Surya + heuristic post-processors → markdown | Same as Surya | GPL-3.0 / commercial dual | v1.0 | [93] |
| MinerU-0.9 | OCR-pipeline | LayoutLMv3 + PaddleOCR + UniMERNet | OpenDataLab internal | AGPL-3.0 | v0.9.x | [94] |
| MinerU-2.5 | OCR-pipeline | MinerU v2.5 (refactored; VLM-assisted) | OpenDataLab + extended | AGPL-3.0 | v2.5 | [95] |
| MinerU2.5-Pro-2604-1.2B | Parse-intent VLM | 1.2B VLM trained for doc parsing | Per MinerU 2.5 tech report | AGPL-3.0 (model card) | `opendatalab/MinerU2.5-...-1.2B` | [95] |
| Nougat-0.1.0 | OCR-VLM | Swin encoder + mBART decoder | arXiv PDFs (academic; ~8M pages) | CC-BY-NC-4.0 | v0.1.0 | [96] |
| GOT-OCR-2.0 | OCR-VLM | Vary-style 580M encoder + Qwen 0.5B decoder | Synthetic + scene + doc OCR (200M+ pairs) | Apache-2.0 | `stepfun-ai/GOT-OCR2_0` | [97] |
| Vary-toy | OCR-VLM | Qwen-1.8B + new vision vocabulary | Vary doc/chart corpus | Apache-2.0 | `Ucas-HaoranWei/Vary-toy` | [98] |
| Fox | OCR-VLM | Focus-anywhere multi-page parser (Vary follow-up) | Doc + chart synthetic | Apache-2.0 (paper) | PENDING-PIN | [99] |
| TextMonkey | OCR-VLM | Monkey (Qwen-VL-derived) with shifted-window + token resampler | LAION + DocVQA + synthetic text | Apache-2.0 | `echo840/Monkey` family | [100] |
| mPLUG-DocOwl1.5 | OCR-VLM | mPLUG-Owl2 + Unified Structure Learning | DocStruct4M | Apache-2.0 | `mPLUG/DocOwl1.5` | [101] |
| DocOwl2 | OCR-VLM | mPLUG-DocOwl2 (high-res compression) | DocStruct + DocReason | Apache-2.0 | `mPLUG/DocOwl2` | [102] |
| Mathpix | OCR-proprietary (math) | Proprietary CNN+Transformer for STEM/equations | Proprietary | Commercial / closed | API `v3` | [103] |
| DeepSeek-OCR / DeepSeek-OCR-2 | OCR-VLM | DeepSeek-VL2 base + OCR head ("contexts optical compression") | Internal multimodal corpus | MIT (weights) | `deepseek-ai/DeepSeek-OCR` | [104] |
| GLM-OCR | OCR-VLM | GLM-4V derived OCR variant | ZhipuAI internal | Custom non-commercial-friendly | PENDING-PIN | [105] |
| FireRed-OCR | OCR-VLM | Xiaomi FireRedTeam OCR VLM | Internal (Xiaomi) | Apache-2.0 (per HF card) | `FireRedTeam/FireRedOCR` PENDING-PIN | [106] |
| Logics-Parsing-v2 | Parse-intent VLM | Logics layout-aware parser (Qwen2.5-VL backbone reported) | Internal doc corpus | PENDING-LICENSE | v2 PENDING-PIN | [107] |
| Chandra (`datalab-to/chandra-ocr-2`) | OCR-VLM | Datalab Chandra-OCR-2 (PaIRS-leading per DOSSIER §2.4) | Datalab internal | Commercial / closed weights | HF `datalab-to/chandra-ocr-2` (DOSSIER pin) | [108] |
| DocIntentOCR-3B | Parse-intent VLM | 3B doc-intent fine-tune (lineage PENDING) | PENDING | PENDING-LICENSE | PENDING-PIN | [10] |
| Qianfan-OCR | OCR-proprietary | Baidu Qianfan platform OCR endpoint | Internal Baidu | Commercial API | Qianfan API (PENDING-VERSION) | [109] |
| HyperAPI-PaddleOCR-OURS | OCR-pipeline | HyperAPI `parse` primitive over PaddleOCR-v4 | Inherited from PP-OCRv4 | Internal (Apache-2.0 upstream) | `hyperapi-sdk` PENDING-PIN | [10] |
| Qwen2-VL-7B / Qwen2-VL-72B | VLM | Qwen2 LLM + ViT encoder (Naive Dynamic Resolution) | Qwen2-VL multimodal mix | Apache-2.0 (7B) / Tongyi-Qianwen (72B) | `Qwen/Qwen2-VL-{7B,72B}-Instruct` | [110] |
| Qwen2.5-VL-3B / -7B-Instruct | VLM | Qwen2.5 LLM + improved ViT (window attn) | Qwen2.5-VL mix; OCR-heavy stage | Apache-2.0 (3B/7B) | `Qwen/Qwen2.5-VL-{3B,7B}-Instruct` | [111] |
| Qwen3-VL-32B-Instruct / Qwen3-VL-235B | VLM | Qwen3 LLM + next-gen visual encoder | Qwen3-VL mix | Apache-2.0 (32B); larger sizes Tongyi-Qianwen | `Qwen/Qwen3-VL-32B-Instruct`, `-235B-A22B` | [71] |
| Qwen3.6-A3B / Qwen3.6-35B-A3B | VLM (MoE) | Qwen3.6 35B-total / 3B-active MoE VLM | Qwen3.6 mix | Apache-2.0 (per card) | `Qwen/Qwen3.6-VL-A3B` PENDING-EXACT-PIN | [112] |
| Qwen3.5-2B-FT | VLM (fine-tune) | Hyperbots/in-house FT of Qwen2.5/3.x 2B variant | Internal | Internal | PENDING-PIN | [10] |
| InternVL2-8B / -26B / -76B | VLM | InternViT-6B + InternLM2 LLM (8B/20B/70B) | InternVL multimodal SFT mix | MIT (8B/26B), custom (76B) | `OpenGVLab/InternVL2-{8B,26B,Llama3-76B}` | [72] |
| LLaVA-1.6-34B | VLM | Nous-Hermes-2-Yi-34B + CLIP-ViT-L | LLaVA-1.6 SFT mix | Apache-2.0 (weights), data CC-BY-NC | `liuhaotian/llava-v1.6-34b` | [113] |
| Llama-3.2-90B-Vision | VLM | Llama-3.1-70B-text + vision adapter, scaled to 90B | Meta multimodal SFT mix | Llama 3.2 Community License | `meta-llama/Llama-3.2-90B-Vision-Instruct` | [114] |
| GPT-4o | VLM (closed) | OpenAI native multimodal | Proprietary | Commercial API | `gpt-4o-2024-11-20` (DOSSIER-pinned PENDING-CONFIRM) | [115] |
| GPT-4o-mini | VLM (closed) | Smaller GPT-4o sibling | Proprietary | Commercial API | `gpt-4o-mini-2024-07-18` | [116] |
| GPT-4.1 | VLM (closed) | Successor to GPT-4o | Proprietary | Commercial API (also via Azure OpenAI per [Hyperbots Azure OpenAI routing policy]) | `gpt-4.1-2025-04-14` | [117] |
| GPT-5 / GPT-5.4 (thinking) | VLM (closed) | OpenAI GPT-5 family | Proprietary | Commercial API; default OpenAI route per [Hyperbots OpenAI-model preference policy] | `gpt-5.4-thinking` PENDING-CONFIRM | [118] |
| Gemini-1.5-Flash / Pro | VLM (closed) | Gemini 1.5 MoE multimodal | Proprietary | Commercial API | `gemini-1.5-{flash,pro}-002` | [119] |
| Gemini-2.5-Flash / Pro | VLM (closed) | Gemini 2.5 family | Proprietary | Commercial API | `gemini-2.5-{flash,pro}` PENDING-DATE | [120] |
| Claude-Sonnet-4.6 | VLM (closed) | Anthropic Claude Sonnet 4.6 | Proprietary | Commercial API | `claude-sonnet-4-6` PENDING-CONFIRM | [121] |
| Mistral-Large-3-675B | LLM (closed weights) | Mistral Large 3, 675B (vision-enabled) | Proprietary | Mistral Research / Commercial | `mistral-large-3-2026` PENDING-CONFIRM | [122] |

### A.2. Verified-via-DOSSIER-only; deep-citation PENDING

The following appear in DOSSIER §2.1/§2.2 but we did not re-verify a canonical model card / paper at table-build time. Treat lineage as **unconfirmed** until a follow-up pass attaches a primary citation:

- **Qwen3.5-2B-FT**: internal fine-tune; base ambiguous (Qwen2.5-VL-2B vs Qwen3-VL micro).
- **GLM-OCR**: multiple ZhipuAI variants exist; need exact HF repo + commit.
- **Logics-Parsing-v2**: vendor (Alibaba/Logics) lineage and license PENDING.
- **DocIntentOCR-3B**: backbone unidentified.
- **Qianfan-OCR**: Baidu API endpoint; underlying model not separately published.
- **FireRed-OCR**: Xiaomi card lists Apache-2.0 but training-data disclosure is partial.
- **Chandra-OCR-2 (canonical description).** Vendor: Datalab (`datalab-to/chandra-ocr-2`), proprietary / commercial-closed weights distributed via Hugging Face under the DOSSIER pin; served in the framework as an OpenAI-compatible vLLM endpoint [39][108]. Architecture: an OCR-specialist VLM whose distinguishing property is **native bbox-grounded HTML emission**, every text block, table, and image is rendered as `<div data-bbox="x0 y0 x1 y1" data-label="...">` with a block-type label, making Chandra (per our 2026-05-26 smoke verification) the first parse engine in scope to natively emit all four ParseBench primary metric surfaces (bbox_iou, layout_element_accuracy, reading_order_accuracy, GTRM) without prompt-engineering scaffolding [25][39][34]. **PaIRS table-split results (ParseBench n=10):** mean PaIRS 0.6472 (vs Qwen3.6-A3B 0.4422, Tesseract 0.3639), with documented high intra-model variance, per-doc range **0.2614–0.9996**, financial tables score up to 0.9996, grid-heavy timetable-style layouts collapse to ~0.32 [10][25]. **Latency/throughput:** p50 ≈ 8.5 s/page at 528 prompt + 821 completion tokens in the smoke configuration, the slowest of the OSS-local OCR-VLMs profiled [ofoxocr2026, parsexframework2026]. **Contamination posture:** no public training-data card; PaIRS table corpora cannot be ruled out of distribution, and the wide per-doc variance is consistent with a mixed in-/out-of-distribution effect [10]. **Known failure mode (F11-DICT-LITERAL):** under the uniform `max_tokens=2048` ceiling, Chandra (and Qwen) truncate on dense text-content / text-formatting splits at 8–10 of 10 documents (PENDING-MAXTOKEN, see §gates), producing 0.0 scores by truncation rather than capability. Lineage row: see Appendix A.1, line entry `Chandra (datalab-to/chandra-ocr-2)`.
- **Mistral-Large-3-675B**: parameter count and vision-capability claim sourced from DOSSIER §2.2 only.

### A.3. Patterns

Three patterns are evident across the 50-row catalogue:

1. **OSS VLM convergence on Qwen2.5 / Qwen3 backbones.** PaddleOCR-VL (ERNIE-based) and DeepSeek-OCR (DeepSeek-VL2) are the main exceptions; nearly every other open OCR-VLM since late 2024 (GOT-OCR-2.0, MinerU2.5-Pro, Logics-Parsing-v2, the Qwen3.6-A3B family itself) builds on Qwen2.5/3 LLM weights with a custom vision encoder or OCR head [111][71][97][32][104].
2. **Frontier closed models still dominate parse-intent.** On the inhouse `parse-intent-inhouse-v1` rubric (DOSSIER §2.2), Claude-Sonnet-4.6 / GPT-4.1 / Gemini-2.5-Pro sit in the top tier; the open Qwen3-VL-32B/235B family is the closest open challenger. Exact F1 values are omitted here because the rubric is Hyperbots-internal and not externalized [10].
3. **License heterogeneity constitutes a substantial adoption constraint.** Apache-2.0 dominates the small-model OSS column, but key pipeline tools (Marker/Surya GPL-3.0 dual; MinerU AGPL-3.0; Nougat CC-BY-NC) and the proprietary Tongyi-Qianwen / Llama-3.2-Community / Mistral-Research tiers each impose distinct deployment restrictions. A consolidated leaderboard cell that mixes these without a license column risks misrepresenting deployability.

### Contamination notes

Several base models are documented (or strongly suspected) to have ingested datasets that are simultaneously used as evaluation corpora elsewhere in the field. These should be flagged whenever a Parse-x cell uses one of those corpora as the gold set:

- **PubTabNet / PubLayNet contamination risk.** Nougat is trained on arXiv PDFs whose tables overlap PubTabNet's IBM source distribution; GOT-OCR-2.0 and DocOwl1.5/DocOwl2 explicitly list "publicly available document understanding datasets" that the model cards do not enumerate exhaustively, PubTabNet / PubLayNet scores for these models should be regarded as **potentially contaminated** [96][97][101].
- **OmniDocBench / OCRBench leakage risk.** MinerU 2.5, PaddleOCR-VL-1.5, Qwen2.5-VL, and InternVL2 all cite "OCR-heavy multimodal pretraining mixes" that, per the model cards, were assembled before OmniDocBench / OCRBench held-out splits were finalized; deduplication is not independently audited [95][32][111][72].
- **`results.zip` self-loop.** Per the benchmark-factory guardrail (CLAUDE.md §21, cited in DOSSIER §2.2), HyperAPI deployed output (`results.zip`) is **never** ground truth; any in-house fine-tune (Qwen3.5-2B-FT, HyperAPI-PaddleOCR-OURS) that was trained against HyperAPI-produced labels must be evaluated only on independently-labeled corpora [10].
- **Chandra-OCR-2 on PaIRS.** No public training-data card; we cannot rule out PaIRS-relevant table corpora being in-distribution. DOSSIER §2.4 already notes high per-doc variance (0.26–0.9996) which is consistent with a mixed in-/out-of-distribution effect [10].

Action item for the next dossier iteration: convert every "PENDING-PIN" / "PENDING-LICENSE" entry above into a verified commit hash + SPDX identifier, and add a contamination-audit column tied to each Parse-x dimension's gold corpus.

## Appendix B. Datasets & Contamination Posture

This appendix inventories every public and internal corpus that a Parse-x leaderboard cell could draw on, records what is known about its provenance and possible model-training overlap, and pins each to one or more of the framework's seven measurement dimensions (D-OCR, D-PARSE-INTENT, D-LAYOUT, D-BBOX, D-TABLE, D-DOWNSTREAM, D-COST-LATENCY) and two stratification overlays (D-DOC-QUALITY, D-LANG) [25]. We then state the standing circularity rule on `results.zip` and close with the per-doc-type coverage-gap matrix.

Contamination posture follows a three-band scheme. **Known-train:** a primary source documents that the corpus appears in a surveyed model's training data. **Plausible-train:** the corpus has been on the public web long enough or in a popular HF mirror such that web-scale VLMs likely saw it, but no training-data card confirms it. **Held-out / internal:** corpus is private, paywalled, or post-dates the cutoff of all surveyed models. Per-claim citations follow.

### B.1. Public datasets

| Dataset | n_docs / n_rules | License | Source | Contamination known? | Framework dim |
|---|---|---|---|---|---|
| ParseBench (5 splits: chart, layout, table, text_content, text_formatting) | ~169k rules across 5 splits; n=10/split currently on disk | Apache-2.0 | upstream `hyprbots/parsebench`, commit a0b10dd7 [49] | Plausible-train for any model post-dating its 2024 release; rule files indexed by HF | D-PARSE-INTENT, D-TABLE, D-LAYOUT, D-OCR (text_content) |
| SAVIOR-Bench v1 | 509 expert-annotated docs; corpus mix UCSF 46.95% / synthetic 17.88% / misc. public financial 17.49% / Inv3D 9.04% / FUNSD 8.64%; IAA 0.761 (fuzzy-string) over 187 double-annotated pairs; attested 31-system OCR edit-distance leaderboard; documented R1-R10 failure taxonomy; per-doc score vectors for the attested leaderboard not on disk (open gate R2 / BLK-18) | research/non-commercial (per paper) | SAVIOR-Bench §2.1 [1][123] | Held-out at release; constituent sub-corpora (FUNSD 8.64%, Inv3D 9.04%) are long-public and almost certainly in VLM pre-training | D-OCR, D-PARSE-INTENT, D-LAYOUT (via Inv3D share), D-BBOX (Inv3D upstream boxes), D-DOC-QUALITY (low-quality class label), D-LANG (multilingual residual cluster) |
| PubTabNet | 568k table images (PubMed Central) | CDLA-Permissive-2.0 | IBM Research [45] | Known-train for nearly every table-structure model (Table-Transformer, GTRM-family, PaddleOCR-VL) | D-TABLE |
| FinTabNet | ~113k financial tables (S&P annual reports) | CDLA-Permissive-2.0 | IBM Research [46] | Known-train for table-structure VLMs trained on the IBM mix | D-TABLE |
| DocLayNet | 80,863 manually labelled page images, 6 doc classes | CDLA-Permissive-1.0 | IBM/DS4SD [27] | Known-train for layout detectors (LayoutLMv3 fine-tunes, DocLayout-YOLO) | D-LAYOUT, D-BBOX |
| PubLayNet | 358k pages from PubMed Central | CDLA-Permissive-1.0 | IBM Research [26] | Known-train for most layout backbones | D-LAYOUT, D-BBOX |
| DocVQA | 50k questions over 12,767 industry document images; answer-string accuracy; recent direct-VLM systems (Agentic Document Extraction) reach 99.16, outperforming OCR pipelines by 3.2 pp GT-in-Pred [78][79]; scores answers, not field-set micro-F1, and varies extractor and parser jointly | non-commercial research | Mathew et al. [78][124] | Known-train for InternVL, Qwen-VL, GPT-4o (publicly stated); also appears bundled in DUE [19] | D-DOWNSTREAM (extractive QA), D-PARSE-INTENT |
| OCRBench v2 | 10,000 instances / 23 tasks / 31 scenarios | research | Fu et al. [3] | Plausible-train; many constituent sub-tasks are public | D-OCR, D-PARSE-INTENT |
| OmniDocBench | 981 PDF pages, 9 doc types, 4 layout types | Apache-2.0 | OpenDataLab/MinerU team [4] | Known-train for MinerU-2.5 (acknowledged in MinerU technical report) | D-LAYOUT, D-TABLE, D-OCR |
| olmOCR-Bench / olmOCR-mix | ~7k mixed-source pages | Apache-2.0 | AllenAI [126] | Held-out at release; Qwen-2-VL-7B-FT model trained on companion `olmOCR-mix-0225` | D-OCR |
| ChartQA | 9,608 human + 23,111 machine QA over 21k charts | GPL-3.0 | Masry et al. [127] | Known-train for chart-capable VLMs | D-PARSE-INTENT (chart), D-DOWNSTREAM |
| FUNSD | 199 noisy scanned forms (149 train / 50 test); 9,707 semantic entities in 4 classes (header/question/answer/other) over 31,485 word-level boxes with entity links; reference task Semantic Entity Recognition (entity-level F1), LayoutLMv3-large ~92, FormNetV2 86.35 [12][22]; single-page English forms only | research only | Jaume et al. [9][77] | Known-train, widely used since 2019; appears as 8.64% of SAVIOR-Bench [123] | D-LAYOUT, D-BBOX, D-PARSE-INTENT (form KIE) |
| CORD | 1,000 Indonesian receipts (800 / 100 / 100); 30 entity types in 4 groups (Menu / Void menu / Subtotal / Total); field-level F1 + tree-edit-distance accuracy; LayoutLMv3-large 97.46 F1, Donut 91.6 [12][14]; receipt-only, short documents, single language | CC-BY-4.0 | Park et al. [13][74] | Known-train for Donut and most receipt models | D-OCR, D-PARSE-INTENT |
| SROIE (ICDAR 2019, Task 3) | 973 scanned restaurant receipts (626 train / 347 test); fixed 4-field schema (company / date / address / total); field-level F1, LayoutLM-large 95.2 [76]; the de facto entry-level KIE benchmark, with a small fixed schema far below the 23-system, free-schema inhouse-v1 panel | research only | Huang et al. [15][75] | Known-train; in many VLM doc mixtures | D-OCR, D-BBOX, D-PARSE-INTENT (fixed-schema KIE) |

Notes on apples-to-apples: ParseBench n on disk is 10 docs/split [10]; the upstream `n_rules` figure refers to rule cardinality, not document count, and the two should not be conflated when reporting CIs. SAVIOR-Bench attested per-doc score vectors are not on disk, blocking interval claims for the WordRecall reconciliation gate (BLK-18) [10].

### B.2. Internal Hyperbots datasets

Treated as **internal corpus** unless a public attestation exists. Per-row numerics stay inside the factory and are not externalized without consent (per team guardrails).

- **dataset_95 (`dataset_95_granular`)**: 95 reviewed invoices/statements; gold has `summary` + `line_items` + `number_of_line_items`; `_status: reviewed`, `_source: subagent_validated`. Hold-out status PENDING [10]. Primary use: D-DOWNSTREAM (extract FieldRecall), D-COST-LATENCY (300s timeout characterization).
- **financepss-205**: 205 finance docs; 49 attested rows; per-doc score vectors absent (BLK-3) [10]. Use: D-DOWNSTREAM.
- **Edit-distance OCR corpus** (`DC-000__ocr-edit-distance-v1`): 31 measured cells; per-corpus n not in attested source. Use: D-OCR.
- **Parse-intent in-house rubric** (`DC-000__parse-intent-inhouse-v1`), 19 cells; rubric provenance vs. `results.zip` PENDING (Q-DOSS-2), must be cleared before D-PARSE-INTENT publication [10].
- **SOULSHINE BoL**, 44 docs (soulshine1: 22, soulshine2: 22; soulshine2 byte-identical to bol-grn-test inputs); no gold (uses field-axis proxy). D-DOWNSTREAM-adjacent only.
- **tough/bank_statement**, 44 docs; median 12pp, max 51pp (one borderline for the 300s timeout). D-DOWNSTREAM, D-COST-LATENCY.
- **tough/cheque**, 21 docs, PNG-only. D-OCR.
- **tough/credit_note**, 34 docs, PNG-only. D-DOWNSTREAM.
- **tough/remittance**, 75 docs (37 PDF + 38 PNG); closest of any tough split to the n=100 threshold (+25 needed) [128]. D-DOWNSTREAM.

All internal corpora share one contamination caveat: because Hyperbots' own product is a parse/extract pipeline, the gold in any internal corpus that was bootstrapped from product output is at risk of being circular for HyperAPI cells. Each internal corpus must carry an explicit `gold_kind` flag, see B.3.

### B.3, Circularity and the `results.zip` rule

The framework defines a `gold_kind` enum [25] whose `"results-zip-derived-NEVER-GOLD"` value is the standing prohibition: any artifact derived from `results.zip`, the HyperAPI deployed-IDP output bundle, is forbidden as ground truth. The rule is restated in three places: the factory's `CLAUDE.md` ("`results.zip` is HyperAPI deployed output; NEVER used as ground truth (circular)") [129]; the framework header ("`results.zip` IS HyperAPI's deployed-IDP output and is circular for Hyperbots and biased toward Hyperbots' field schema for competitors") [25]; and the dossier's parse-intent §2.2 (forcing a circular-GT check on the inhouse-v1 rubric) [10].

Why it matters: using `results.zip` as gold would (i) guarantee HyperAPI a near-perfect score against itself, inflating any "best for all finance" claim under H0, and (ii) penalize competitors whose schemas legitimately diverge from Hyperbots'. The sanctioned uses are limited to schema-anchor / drift detection [25]. Two implications for this review: D-PARSE-INTENT cells using the in-house rubric carry a publishability asterisk until Q-DOSS-2 closes; and the framework's `dimension D-DOWNSTREAM` baseline of "Qwen 3.6 on raw image" is preferred over "Chandra-as-baseline" precisely to avoid a second circularity (Chandra appears as a parse engine in the panel) [25].

### B.4, Per-doc-type coverage gap matrix

From `DOC-TYPE-GAPS.json` (2026-05-26) [128], counting Tier-1+2+3+4 doc types against the n ≥ 100 minimum: **5 of 6 Tier-1 doc types currently have ZERO factory-measured cells** (T-02 credit note, T-03 PO, T-04 packing slip, T-05 BoL, T-06 remittance; only T-01 invoice has measured cells, with 5 vendors on n=90–95). **Tier-2 has zero measured cells across all four types** (T-07 bank statement, T-08 cheque, T-09 pay stub, T-10 wire/ACH). **Tier-3 has zero measured cells**, and T-11 (10-Q/10-K) is structurally excluded from HyperAPI IDP's current doc-type set [doctypegaps2026, BLK-7]. **Tier-4** (T-14 insurance, T-15 loan) has neither corpus nor measured cells. Of the 16 framework doc types, **14 currently have zero leaderboard cells** and **2** (T-01 invoice and T-16 FUNSD-style forms via SAVIOR aggregation) have any measured presence. Summary for Parse-x: the leaderboard today is a single-doc-type (invoice) result with an OCR-panel aggregate over SAVIOR; cross-doc-type claims are unsupported until D2/D3 phases run.

## Appendix C, Vendor & API Pin Table

This appendix pins the closed-source / hosted services in the Parse-x panel as of 2026-06-16. Where a vendor has shipped multiple GA snapshots in the past quarter, we list the snapshot our harness will pin; `PENDING-CONFIRMATION` flags entries where the public docs are ambiguous or where we have not yet executed a sandbox call to confirm the snapshot string.

| Vendor | Service | Current GA model(s) | API version pin | Auth | Pricing | Region | Citation |
|---|---|---|---|---|---|---|---|
| Microsoft | Azure Document Intelligence (fmr. Form Recognizer) | `prebuilt-layout`, `prebuilt-read`, `prebuilt-document`, `prebuilt-invoice`, custom-neural v4 | REST `2024-11-30` (GA, v4.0) | Key (subscription) or Entra ID | from $1.50 / 1k pages (Read S0); Layout S0 $10 / 1k pages | 30+ Azure regions; not all prebuilts in every region | [130], [131] |
| Google | Gemini API (AI Studio / Vertex) | `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`; `gemini-3.1-pro` and `gemini-3.5-flash` rolling out | `gemini-2.5-pro-preview-06-05` for Pro panel; 2.5-flash GA snapshot, `PENDING-CONFIRMATION` for 2.6/3.x in our harness | API key (AI Studio) / OAuth + ADC (Vertex) | 2.5 Pro $1.25 / $10 per 1M tok (≤200k ctx); 2.5 Flash $0.30 / $2.50 per 1M tok | global, us-central1, europe-west4, asia-southeast1 | [132], [133] |
| Anthropic | Claude API | `claude-opus-4-8` (flagship, rel. 2026-05-28), `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5` | Pin: `claude-sonnet-4-6-20260415`, `claude-opus-4-8-20260528` (PENDING-CONFIRMATION of exact dated snapshot for 4.8); 4.5 family deprecated path; `anthropic-version: 2023-06-01` header | API key | Sonnet 4.6 $3 / $15 per 1M; Opus 4.7/4.8 $5 / $25 per 1M; Haiku 4.5 $1 / $5; batch -50%, cache -90% | us-east, eu, AWS Bedrock + GCP Vertex mirrors | [134], [135] |
| OpenAI (via Azure) | Azure OpenAI Service | `gpt-5` (2025-08-07), `gpt-5.1` / `gpt-5.1-chat` (2025-11-13), `gpt-5.2-chat` (2026-02-10), `gpt-5.4` thinking/pro (2026-03-05), `gpt-5.4-mini/-nano` (2026-03-17), `gpt-4.1`, `gpt-4o`, `gpt-4o-mini`, `o3` (2025-04-16), `o3-mini` | Data-plane: `api-version=2025-04-01-preview` for Responses API; deployment-pinned snapshots above. Older GPT-5/o3 snapshots deprecate 2026-12-11 | Entra ID (preferred) or key | Mirrors OpenAI list price + Azure markup; GPT-5.4 thinking ~ $5 / $20 per 1M tok (PENDING-CONFIRMATION on Azure-side rate card) | eastus, eastus2, swedencentral, japaneast, australiaeast (model-dependent) | [136], [137], [138] |
| OpenAI direct | NOT USED in our harness |, |, |, |, |, | see C.1 |
| Mistral | La Plateforme | `mistral-large-3` (`mistral-large-2512`), `mistral-medium-3`, `mistral-small-3.2` | `mistral-large-2512` | Key | Large 3: $2 / $6 per 1M tok (one source); $0.50 / $1.50 for `large-2512` variant, discrepancy, `PENDING-CONFIRMATION` against vendor card | EU (Paris), US via AWS Bedrock | [139], [140] |
| Mathpix | Convert API (v3) | `mathpix-ocr` (text+math); `pdf` endpoint | REST `v3` | App-ID + App-Key headers | $0.004–$0.01 / page (Convert PDF); $0.005 / image equation OCR, `PENDING-CONFIRMATION` on 2026 rate card | global (US-hosted) | [141] |
| LlamaIndex | LlamaParse (LlamaCloud) | modes: `fast`, `balanced`, `premium`, `agentic` | LlamaCloud API `2024-12` GA; `agentic` mode GA Q1 2026 | API key | Credit system: 1,000 credits = $1; `fast` 1 cr/pg, `premium` 15 cr/pg, `agentic` 45 cr/pg; 10k free credits/mo | US (AWS us-east-1), EU | [142], [143] |
| Reducto | Reducto Parse / Extract | `parse`, `extract`, `split`, `edit` agentic endpoints | `2025-11` GA; pin `model=parse-v2` | API key (bearer) | Credit system: 1,000 credits = $1; recommended preset ~$0.01–$0.03/pg | US (SOC2); on-prem option | [144] |
| Unstructured.io | Serverless API / Platform | `unstructured-api` v0.x; partition strategies `hi_res`, `auto`, `fast`, `ocr_only`, `vlm` | API `2025-09`; pin `strategy=hi_res, hi_res_model_name=yolox` | API key | Serverless: $1 / 1k pages (`fast`), $10 / 1k pages (`hi_res`); free OSS | US, EU; OSS = anywhere | [145], [146] |
| IBM | Docling | OSS library (`docling` PyPI), Docling-Serve container, watsonx.ai-hosted | Pin: `docling==2.x` (commit SHA in harness lockfile) | none (local) / IAM (watsonx) | OSS = free; watsonx.ai = compute-billed | self-host; watsonx multi-region | [147], [146] |

### C.1, Azure OpenAI routing rule

All OpenAI model calls in Parse-x (`gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-5`, `gpt-5.1`, `gpt-5.2`, `gpt-5.4` family, `o3`, `o3-mini`) route through **Azure OpenAI Service**, not the direct `api.openai.com` endpoint. This is a standing Hyperbots project preference, recorded in user memory `azure-openai-preferred` and reaffirmed in `openai-default-gpt-5-4-thinking` (current default = GPT-5.4 thinking mode) [148]. Operational reasons: (i) Entra-ID auth and tenant-scoped data residency, (ii) committed-throughput PTUs for reproducible latency cells in D-COST-LATENCY, (iii) the Azure data-processing addendum the Hyperbots tenant has signed. Practically this means: model snapshot strings follow Azure's deployment-name convention, the API path is `/openai/deployments/{deployment}/responses?api-version=…`, and snapshot availability lags OpenAI direct by typically 1–6 weeks [136]. Benchmark cells that name an OpenAI model implicitly mean "this snapshot, served via Azure", when an OpenAI snapshot is not yet on Azure we mark the cell `BLOCKED-AZURE-LAG` rather than fall back to direct OpenAI.

### C.2, Known boundaries & caveats

- **Azure DI** prebuilt-read covers Latin + CJK printed text but handwritten Chinese / Japanese / Korean fall back to print-trained models with degraded recall; handwritten Arabic is not supported in `prebuilt-read` GA [130]. The `prebuilt-layout` table cell linking does not emit row/column spans for merged headers in all layouts, relevant to D-TABLE.
- **Gemini 2.5 / 3.x** vision input is billed as tokens (per Google's tokenizer for images at ~258 tok/tile), so D-COST-LATENCY normalization must convert pages→tokens before cost compares against per-page services. The `2.6` / `3.x` line had not stabilized at our cutoff, pin `PENDING-CONFIRMATION` [132].
- **Claude Opus/Sonnet** 1M-token context is flat-rate on 4.6/4.7/4.8 (no surcharge), which changes the cost calculus for whole-PDF prompting vs page-tiling [134]. Sonnet/Opus 4.5 snapshots are still callable but on a deprecation path; we will not pin them.
- **GPT-5.4 thinking / pro** exposes reasoning-token billing separate from completion tokens; D-COST-LATENCY must report both. Snapshot deprecation for older GPT-5/o3 lands 2026-12-11, re-pin before then [137].
- **Mistral Large 3** is multimodal (MoE 41B active / 675B total) but vision-OCR head is newer than the text head; expect higher variance on D-OCR than D-PARSE-INTENT [139].
- **Mathpix** remains best-in-class for math-equation OCR but does not return layout bounding boxes at the same granularity as Azure DI (affects D-BBOX scoring).
- **LlamaParse / Reducto / Unstructured** use credit or per-strategy pricing, to compare apples-to-apples in D-COST-LATENCY we will normalize to "USD per 1k pages on `hi_res` / `premium` / `parse-v2` preset" and disclose the preset in every cell.
- **Docling** is OSS; we pin a commit SHA in the harness lockfile so a `docling` upgrade does not silently change scores between leaderboard refreshes.
- Vendors' published prices are list prices; enterprise / committed-use discounts that may apply to Hyperbots' actual spend are NOT reflected here and MUST NOT be externalized.

## 3. Discussion and Open Gates

Three patterns emerge across the seven dimensions and two overlays. First, **per-document score vectors are absent everywhere except SAVIOR-Bench's internal pipeline**, OCRBench v2, OmniDocBench, olmOCR-Bench, PubTabNet and DocLayNet all publish single aggregate numbers per model, so any rigorous bootstrap CI95 reporting on top of them requires either re-running the eval (with the attendant compute and decoding-pin honesty work) or explicit attestation. Second, **fine-tune-vs-zero-shot disclosure is inconsistent in the published literature**, a known SAVIOR-Bench complaint (R6) and a recurring source of misleading model-vs-model comparisons (e.g., a 2B fine-tuned model beating a 75B zero-shot model is structurally expected and should not be reported as a model-capability win). Third, **parse-to-downstream lift (D-DOWNSTREAM) is underused in the parse-benchmark literature**: prior art treats OCR / parse as an intrinsic-metric end-state, not as a stage feeding extract / RAG / classify pipelines, and the paired-bootstrap testing infrastructure imported from NLP [73] and ASR (formalised for NLP by [164]) and the RAG-evaluation lineage ([166]) has not been carried over.

The largest open gates blocking first-pass cell publication, in order of severity, are: (i) BLK-18, the SAVIOR-Bench 509-doc out7 corpus is not on disk, blocking WordRecall reconciliation against the attested 31-cell leaderboard; (ii) PENDING-MAXTOKEN, the uniform max_tokens=2048 ceiling truncates Chandra and Qwen on dense text-content / text-formatting splits at 8-10 out of 10 documents, producing 0.0 scores by truncation rather than by model capability; (iii) the model-lineage table (Appendix A) carries several PENDING-PIN entries that block the per-cell `pins.adapter_version` field from being populated; (iv) several Tier-1 document types in DOC-TYPE-GAPS still have zero measured cells across every framework dimension, a gap that no public benchmark fills.

The framework's measurement discipline does not, by itself, resolve any of these gates; it makes them visible. This visibility, paired with a curated and rerunnable cell registry, informs the industrial release discipline that follows.

### 3.1 Scope limitations

This review deliberately scopes to the seven measurement dimensions named in §2 and treats four content surfaces as out of scope:
- **Handwritten and cursive recognition** (IAM database [163] precursor; READ / ICFHR competitions; RIMES). Most surveyed engines target printed text; handwritten recognition has its own benchmark lineage and failure modes.
- **Mathematical formula extraction** (Im2Latex, CROHME competitions, MathPix-style image-to-LaTeX). Specialist sub-field with its own gold corpora and structured-output conventions.
- **Document classification** (RVL-CDIP and similar). Treated upstream of parse rather than inside it.
- **Long-document and multi-page handling** (multi-page reading-order continuity, cross-page table stitching, full-10K-style finance documents). [165] introduces hierarchical multi-page DocVQA; full multi-page parse-benchmark coverage is left to follow-on work.

### 3.2 Reproducibility caveats

An external team cannot execute the framework end-to-end from this review alone. Specific blockers:
- **SAVIOR-Bench v1 (n=509)** is an internal artifact and is not redistributable; the D-OCR primary metric `savior_word_recall` is undefined without it.
- **`parse-intent-inhouse-v1` rubric** is internal; the contamination check (Q-DOSS-2) is still open.
- **Qwen3.6-35B-A3B fine-tune endpoint** (private Hyperbots IP) is required for the D-DOWNSTREAM reference extractor.
- **PaIRS commit** (hyprbots/vlm_ocr@1fbbc334) is private; the public reading-order alternatives are reading-order edit distance (DocLayNet) or NED (OmniDocBench).
- **ParseBench n=10 document IDs** are not specified; the registry should publish the exact PDF stems used per split for true reproducibility.

The framework is therefore reproducible *in template* (decoding pins, metric definitions, cell schema) and partially reproducible in *substance* (Apache-2.0 ParseBench, OmniDocBench, FUNSD/CORD/SROIE, the foundational works in Appendix A) on public corpora alone.

### 3.3 Statistical floor

The first-pass sampled cells use n=10 per split. For a metric on [0,1] this implies an expected 2000-resample bootstrap CI95 half-width of approximately ±0.15, which can swamp engine-to-engine deltas of comparable magnitude (a published difference of, say, 0.10 PaIRS between two engines is not significant at n=10). No formal power analysis was performed. The framework's publish-gate (per-document score vectors plus bootstrap CI95) is consistent with the prevailing HELM-era discipline [161]; widening n is the correct next step for headline cells.

### 3.4 Evaluator-LLM bias note

In D-DOWNSTREAM, the reference extractor (Qwen3.6-35B-A3B) is itself an LLM. This is structurally an LLM-as-judge setting and risks the judge biases catalogued in recent LLM-evaluation literature. The framework's countermeasure is the apples-to-apples constraint (same extractor, identical decoding pins across all upstream parsers), which controls relative ranking but does not eliminate absolute-scale bias.

### 3.5 Cross-engine fairness note (apples-to-oranges)

The framework's uniform decoding pin `max_tokens=2048` truncates Chandra and Qwen on dense text-content and text-formatting splits in 8 to 10 out of 10 documents. The content-metric cells for those engines under this pin are **labeled apples-to-oranges** and should not be read as engine-capability cells. PaIRS scores on the same documents remain valid because the metric measures matched-token geometry rather than transcript completeness.

## References

[1] Hyperbots. SAVIOR-Bench v1: in-repo deep-read extract (paper/SAVIOR-Bench.md), n=509, IAA 0.761, R1-R10 failure taxonomy. Internal artifact, 2026.

[2] Hyperbots. SOURCE-EXTRACT Benchmark-VLM_OCR.pdf extract (paper/SOURCE-EXTRACT-Benchmark-VLM-OCR.md), corpus mix, IAA, LoRA recipe. 2026-05-18.

[3] Fu, L., Kuang, Z., Song, J., et al. OCRBench v2: An Improved Benchmark for Evaluating Large Multimodal Models on Visual Text Localization and Reasoning. arXiv:2501.00321 (2025). https://arxiv.org/abs/2501.00321

[4] Ouyang, L. et al. OmniDocBench: Benchmarking Diverse PDF Document Parsing with Comprehensive Annotations. CVPR 2025 / arXiv:2412.07626 (2024). https://arxiv.org/abs/2412.07626

[5] MinerU Team. MinerU2.5: A Decoupled Vision-Language Model for Efficient High-Resolution Document Parsing. arXiv:2509.22186 (2025). https://arxiv.org/abs/2509.22186

[6] Baidu PaddlePaddle Team. PaddleOCR-VL-1.5: Towards a Multi-Task 0.9B VLM for Robust In-the-Wild Document Parsing. ERNIE Blog (2026). https://ernie.baidu.com/blog/posts/paddleocr-vl-1.5/ [arXiv ID 2601.21957 unverified; Baidu blog URL is the canonical source]

[7] Allen Institute for AI. olmOCR-Bench dataset card. Hugging Face, 2025. https://huggingface.co/datasets/allenai/olmOCR-bench

[8] Poznanski, J. et al. olmOCR 2: Unit Test Rewards for Document OCR. arXiv:2510.19817 (2025). https://arxiv.org/abs/2510.19817

[9] Jaume, G., Ekenel, H. K., Thiran, J.-P. FUNSD: A Dataset for Form Understanding in Noisy Scanned Documents. ICDAR-OST 2019. https://guillaumejaume.github.io/FUNSD/

[10] Hyperbots Parse-x research dossier. command-center/DOSSIER.md, §2.1 OCR family inventory (31 cells) and §2.4 PaIRS measurements. Internal, 2026-06-10.

[11] Hyperbots. PARSE-DEEP-BENCHMARK-FRAMEWORK (2026-05-27). Internal framework spec, /Users/niyati/Desktop/hyperapi-documentapi-benchmark-factory/PARSE-DEEP-BENCHMARK-FRAMEWORK-2026-05-27.md.

[12] Huang, Y. et al. LayoutLMv3: Pre-training for Document AI with Unified Text and Image Masking. ACM MM (2022). arXiv:2204.08387.

[13] Park, S. et al. CORD: A Consolidated Receipt Dataset for Post-OCR Parsing. NeurIPS Document Intelligence Workshop (2019). https://github.com/clovaai/cord

[14] Kim, G. et al. OCR-free Document Understanding Transformer (Donut). ECCV (2022). arXiv:2111.15664.

[15] Huang, Z. et al. ICDAR2019 Competition on Scanned Receipt OCR and Information Extraction. ICDAR (2019). https://rrc.cvc.uab.es/?ch=13

[16] Stanislawek, T. et al. Kleister: Key Information Extraction Datasets Involving Long Documents with Complex Layouts. ICDAR (2021). arXiv:2105.05796.

[17] Simsa, S. et al. DocILE Benchmark for Document Information Localization and Extraction. ICDAR (2023). arXiv:2302.05658. https://docile.rossum.ai/

[18] ProPublica / Stanford HAI. DeepForm: Political Ad Disclosure Forms dataset. https://github.com/project-deepform/deepform

[19] Borchmann, L. et al. DUE: End-to-End Document Understanding Benchmark. NeurIPS Datasets & Benchmarks (2021). https://duebenchmark.com/

[20] Hong, T. et al. BROS: A Pre-trained Language Model Focusing on Text and Layout for Better Key Information Extraction. AAAI (2022). arXiv:2108.04539.

[21] Wang, J., Jin, L., Ding, K. LiLT: A Simple yet Effective Language-Independent Layout Transformer for Structured Document Understanding. ACL (2022). arXiv:2202.13669.

[22] Lee, C.-Y. et al. FormNetV2: Multimodal Graph Contrastive Learning for Form Document Information Extraction. ACL (2023). arXiv:2305.02549.

[23] Wan, J. et al. OmniParser: A Unified Framework for Text Spotting, Key Information Extraction and Table Recognition. CVPR (2024). arXiv:2403.19128.

[24] Laatiri, S. et al. Information Redundancy and Biases in Public Document Information Extraction Benchmarks. arXiv:2304.14936 (2023).

[25] Parse Deep Benchmark Framework spec, hyperapi-documentapi-benchmark-factory, 2026-05-27. /Users/niyati/Desktop/hyperapi-documentapi-benchmark-factory/PARSE-DEEP-BENCHMARK-FRAMEWORK-2026-05-27.md

[26] Zhong, X., Tang, J., Jimeno-Yepes, A. PubLayNet: largest dataset ever for document layout analysis. ICDAR 2019. arXiv:1908.07836. https://arxiv.org/abs/1908.07836

[27] Pfitzmann, B. et al. DocLayNet: A Large Human-Annotated Dataset for Document-Layout Analysis. KDD 2022. arXiv:2206.01062. https://arxiv.org/abs/2206.01062

[28] Cheng, H. et al. M6Doc: A Large-Scale Multi-Format, Multi-Type, Multi-Layout, Multi-Language, Multi-Annotation Category Dataset for Modern Document Layout Analysis. CVPR 2023. https://openaccess.thecvf.com/content/CVPR2023/papers/Cheng_M6Doc_A_Large-Scale_Multi-Format_Multi-Type_Multi-Layout_Multi-Language_Multi-Annotation_Category_Dataset_CVPR_2023_paper.pdf [unverified; URL inaccessible at audit time]

[29] Wang, Z., Xu, Y., Cui, L., Shang, J., Wei, F. LayoutReader: Pre-training of Text and Layout for Reading Order Detection. EMNLP 2021. arXiv:2108.11591. https://arxiv.org/abs/2108.11591

[30] Ouyang, L. et al. OmniDocBench: Benchmarking Diverse PDF Document Parsing with Comprehensive Annotations. CVPR 2025. arXiv:2412.07626. https://github.com/opendatalab/OmniDocBench

[31] Da, C. et al. Vision Grid Transformer for Document Layout Analysis. ICCV 2023. arXiv:2308.14978. https://arxiv.org/abs/2308.14978

[32] Baidu / PaddlePaddle. PaddleOCR-VL: Boosting Multilingual Document Parsing via a 0.9B Ultra-Compact Vision-Language Model. arXiv:2510.14528 (2025). https://arxiv.org/abs/2510.14528

[33] FocalOrder: Focal Preference Optimization for Reading Order Detection. arXiv:2601.07483 (2026). https://arxiv.org/abs/2601.07483

[34] Parse Deep Benchmark Framework v0. HyperAPI DocumentAI Benchmark Factory internal spec (2026-05-27). /Users/niyati/Desktop/hyperapi-documentapi-benchmark-factory/PARSE-DEEP-BENCHMARK-FRAMEWORK-2026-05-27.md

[35] SAVIOR-Bench: A Provenance-Tagged Benchmark for Financial-Document Parsing, Extraction, Layout Awareness, and Bounding-Box Visual Grounding. Internal paper, §2.2 Facet 3, §5.1.5, §10 R9. /Users/niyati/Desktop/hyperapi-documentapi-benchmark-factory/paper/SAVIOR-Bench.md

[36] Hertlein, F., Naumann, A., Philipp, P. Inv3D: a high-resolution 3D invoice dataset for template-guided single-image document unwarping. IJDAR 2023. https://felixhertlein.github.io/inv3d/

[37] ICDAR 2023 Competition on Robust Layout Segmentation in Corporate Documents. arXiv:2305.14962. https://ds4sd.github.io/icdar23-doclaynet/task/

[38] Bbox-silver pipeline spec, closing R9 partially via PyMuPDF/pdfplumber silver labels (2026-05-26). /Users/niyati/Desktop/hyperapi-parse-x-research/command-center/BBOX-SILVER-PIPELINE-SPEC.md

[39] Datalab. Chandra OCR 2 model card (datalab-to/chandra-ocr-2). Hugging Face / Datalab blog. https://huggingface.co/datalab-to/chandra-ocr-2 ; https://www.datalab.to/blog/chandra-2

[40] Datalab. Surya: OCR, layout analysis, reading order, table recognition in 90+ languages. GitHub repo and layout benchmark notes (PubLayNet/DocLayNet, coverage-match scorer). https://github.com/datalab-to/surya

[41] Lv et al. KOSMOS-2.5: A Multimodal Literate Model. arXiv:2309.11419 (2023). https://arxiv.org/abs/2309.11419

[42] HyperAPI Parse-X Research Dossier §2 model lists (DocOwl2, Marker, MinerU, Surya, PaddleOCR-VL, Qwen3-VL, GPT-4o, Gemini, etc.). /Users/niyati/Desktop/hyperapi-parse-x-research/command-center/DOSSIER.md

[43] ParseBench Recreate Plan §1, layout split (16,325 rules, 500 PDFs; bbox + semantic class + reading-order per element). /Users/niyati/Desktop/hyperapi-parse-x-research/command-center/PARSEBENCH-RECREATE-PLAN-2026-05-26.md

[44] Hyperbots benchmark-factory. TABULAR-LITERATURE-SURVEY v2 (2026). plan/TABULAR-LITERATURE-SURVEY.md, TSR lineage, metric formal definitions, corpora and SOTA framing.

[45] Zhong, X., ShafieiBavani, E., Jimeno-Yepes, A. Image-based Table Recognition: Data, Model, and Evaluation (PubTabNet + EDD + TEDS). ECCV 2020. https://github.com/ibm-aur-nlp/PubTabNet.

[46] Zheng, X., Burdick, D., Popa, L., Zhong, X., Wang, N. Global Table Extractor (GTE) and the FinTabNet dataset of S&P 500 annual-report tables. WACV 2021. https://developer.ibm.com/exchanges/data/all/fintabnet/; arXiv:2005.00589.

[47] Smock, B., Pesala, R., Abraham, R. GriTS: Grid Table Similarity Metric for Table Structure Recognition. ICDAR 2023; arXiv:2203.12555. https://arxiv.org/abs/2203.12555.

[48] Reducto. Announcing RD-TableBench: An Open-Source Table Benchmark (2024). https://reducto.ai/blog/rd-tablebench.

[49] LlamaIndex / community. ParseBench: A Document Parsing Benchmark for AI Agents (2026). arXiv:2604.08538; https://github.com/run-llama/ParseBench; https://huggingface.co/datasets/llamaindex/ParseBench. Defines GTRM = mean(GriTS, TableRecordMatch), table split n=503 across 284 docs.

[50] Smock, B., Pesala, R., Abraham, R. PubTables-1M: Towards Comprehensive Table Extraction from Unstructured Documents. CVPR 2022, pp. 4634–4642. https://github.com/microsoft/table-transformer.

[51] Parse-x team. Parse Deep Benchmark Framework v0 (PARSE-DEEP-BENCHMARK-FRAMEWORK-2026-05-27), §D-DOC-QUALITY lines 122-130. Hyperbots internal (2026). file:///Users/niyati/Desktop/hyperapi-documentapi-benchmark-factory/PARSE-DEEP-BENCHMARK-FRAMEWORK-2026-05-27.md

[52] SAVIOR-Bench authors. SAVIOR-Bench: Stratified Annotated Visual Information OCR / Recognition Benchmark (v1). Project paper, §2.1 corpus mix, §10 recommendations R3/R4 (2025). file:///Users/niyati/Desktop/hyperapi-documentapi-benchmark-factory/paper/SAVIOR-Bench.md

[53] Authors of DocIQ. DocIQ: A Benchmark Dataset and Feature Fusion Network for Document Image Quality Assessment. arXiv:2509.17012 (2025). https://arxiv.org/pdf/2509.17012

[54] Ma, K. et al. DocUNet: Document Image Unwarping via a Stacked U-Net. CVPR 2018. https://www.researchgate.net/publication/329747239 [unverified; URL inaccessible at audit time]

[55] Harley, A. W., Ufkes, A., Derpanis, K. G. Evaluation of Deep Convolutional Nets for Document Image Classification and Retrieval (RVL-CDIP, 400k images at ~100 DPI). ICDAR 2015. https://www.cs.cmu.edu/~aharley/rvl-cdip/ [unverified; URL inaccessible at audit time]

[56] Larson, S. et al. On Evaluation of Document Classification using RVL-CDIP (label noise audit, 8.1% mean, 1.6-16.9% per class). arXiv:2306.12550 (2023). https://arxiv.org/abs/2306.12550

[57] Papadopoulos, C., Pletschacher, S., Clausner, C., Antonacopoulos, A. The IMPACT Dataset of Historical Document Images. HIP'13, ACM, pp. 123-130 (2013). https://www.primaresearch.org/datasets

[58] Groleau, A. et al. Augraphy: A Data Augmentation Library for Document Images. arXiv:2208.14558 (2022). https://arxiv.org/pdf/2208.14558

[59] Hyperbots Parse-x team. SOULSHINE-PLAN-2026-05-25 (BoL / receiving-log corpus, soulshine1 + soulshine2). Hyperbots internal (2026). file:///Users/niyati/Desktop/hyperapi-documentapi-benchmark-factory/SOULSHINE-PLAN-2026-05-25.md

[60] Li, H. et al. Towards Document Image Quality Assessment: A Text Line Based Framework and a Synthetic Text Line Image Dataset. arXiv:1906.01907 (2019). https://arxiv.org/pdf/1906.01907

[61] Anonymous. Analysing the Robustness of Vision-Language-Models to Common Corruptions (blur, JPEG, noise severity sweep). arXiv:2504.13690 (2025). https://arxiv.org/html/2504.13690v1

[62] Anonymous. DocRobust: Enhancing Robustness of Multi-modal Document Understanding to Corruptions. OpenReview (2024). https://openreview.net/pdf/7d215ea6ae5d1e2423e86cbb61cb44377179dee8.pdf [unverified; URL inaccessible at audit time]

[63] Tang et al. MTVQA: Benchmarking Multilingual Text-Centric Visual Question Answering. arXiv:2405.11985 (2024); ACL Findings 2025. https://arxiv.org/abs/2405.11985

[64] Xu, Y., Lv, T., Cui, L., Wang, G., Lu, Y., Florencio, D., Zhang, C., Wei, F. XFUND: A Benchmark Dataset for Multilingual Visually Rich Form Understanding. Findings of ACL 2022, pp. 3214-3224. https://aclanthology.org/2022.findings-acl.253/

[65] Li, Z., Lin, Z., Liu, Q., Zhang, Z., Zhang, S., Guo, Z., Song, J., Zhang, J., Bai, X., Liu, Y. MDPBench: A Benchmark for Multilingual Document Parsing in Real-World Scenarios. arXiv:2603.28130, 2026. https://arxiv.org/abs/2603.28130 ; GitHub: https://github.com/Yuliang-Liu/MultimodalOCR/tree/main/MDPBench

[66] Cho et al. M3DocRAG: Multi-modal Retrieval is What You Need for Multi-page Multi-document Understanding. arXiv:2411.04952 (2024); ICCV 2025 Workshop. https://arxiv.org/abs/2411.04952

[67] Zhao, M., Li, B., Wang, J., Li, W., Zhou, W., Zhang, L., Xuyang, S., Yu, Z., Yu, X., Li, G., Dai, A., Zhou, S. Towards Video Text Visual Question Answering: Benchmark and Baseline. NeurIPS 2022 Datasets and Benchmarks Track.

[68] Zhu, Xie et al. SCUT-EPT: New Dataset and Benchmark for Offline Chinese Text Recognition in Examination Paper. IEEE Access, 2018. https://github.com/HCIILAB/SCUT-EPT_Dataset_Release

[69] He et al. ICPR 2018 MTWI Challenge on Multi-Type Web Image Text Reading. 2018. [unverified; URL inaccessible at audit time]

[70] PaddleOCR (PP-OCRv4/v5/v6) and PaddleOCR-VL (v1.6) model cards, PaddlePaddle, 2024-2026. https://github.com/PaddlePaddle/PaddleOCR

[71] Alibaba. Qwen2-VL and Qwen3-VL technical reports and model cards, 2024-2025. [unverified; URL inaccessible at audit time]

[72] Chen et al. InternVL2 technical report and Hugging Face model cards, 2024. [unverified; URL inaccessible at audit time]

[73] Philipp Koehn. Statistical Significance Tests for Machine Translation Evaluation. EMNLP 2004, Barcelona, pp. 388-395. https://aclanthology.org/W04-3250/

[74] Park, S. et al. CORD: A Consolidated Receipt Dataset for Post-OCR Parsing. NeurIPS 2019 Document Intelligence Workshop. https://github.com/clovaai/cord

[75] Huang, Z. et al. ICDAR2019 Competition on Scanned Receipt OCR and Information Extraction (SROIE). ICDAR 2019. https://rrc.cvc.uab.es/?ch=13 [unverified; URL inaccessible at audit time]

[76] Huang, Y. et al. LayoutLMv3: Pre-training for Document AI with Unified Text and Image Masking. ACM MM 2022. arXiv:2204.08387 (CORD F1 = 97.46 large / 96.56 base per Table 1).
[76b] Xu, Y. et al. LayoutLM: Pre-training of Text and Layout for Document Image Understanding. KDD 2020. arXiv:1912.13318 (SROIE receipt understanding F1 = 95.24 for LayoutLM-LARGE).

[77] Jaume, G., Ekenel, H. K., Thiran, J.-P. FUNSD: A Dataset for Form Understanding in Noisy Scanned Documents. ICDAR-OST 2019. arXiv:1905.13538.

[78] Mathew, M., Karatzas, D., Jawahar, C. V. DocVQA: A Dataset for VQA on Document Images. WACV 2021. arXiv:2007.00398.

[79] LandingAI. DocVQA Benchmark: 99.16% Accuracy Using Agentic Document Extraction (2025). https://landing.ai/blog/superhuman-on-docvqa-without-images-in-qa-agentic-document-extraction

[80] van Strien, D., Beelen, K., Ardanuy, M. C., Hosseini, K., McGillivray, B., Colavizza, G. Assessing the Impact of OCR Quality on Downstream NLP Tasks. ARTIDIGH 2020. https://www.turing.ac.uk/news/publications/assessing-impact-ocr-quality-downstream-nlp-tasks [unverified; URL inaccessible at audit time]

[81] Lima de Oliveira, L. et al. Evaluating and mitigating the impact of OCR errors on information retrieval. Int. J. on Digital Libraries 24, 1–22 (2023). https://doi.org/10.1007/s00799-023-00345-6

[82] Perlitz, Y., Bandel, E., Gera, A., Arviv, O., Ein-Dor, L., Shnarch, E., Slonim, N., Shmueli-Scheuer, M., Choshen, L. Efficient Benchmarking (of Language Models). arXiv:2308.11696, 2023. https://arxiv.org/abs/2308.11696 ; Stanford CRFM Efficient-HELM docs: https://crfm-helm.readthedocs.io/en/latest/get_helm_rank/

[83] Stanford CRFM. HELM Documentation (accessed 2026-06). https://crfm-helm.readthedocs.io/

[84] Artificial Analysis. AI Model Leaderboard, intelligence, speed, latency, price, context (2026). https://artificialanalysis.ai/

[85] VERTU Editorial. AI Model Leaderboard 2026: Intelligence, Speed, Price & Context. https://vertu.com/lifestyle/ai-model-leaderboard-2026-intelligence-speed-price-context-a-complete-ranking-guide

[86] byteiota. Mistral OCR 3: $2/1000 Pages Cuts Document AI Costs 97% (2025). https://byteiota.com/mistral-ocr-3-2-1000-pages-cuts-document-ai-costs-97/

[87] aiproductivity.ai. Document AI Cost Comparison 2026: Mistral vs AWS Textract vs Google Document AI. https://aiproductivity.ai/blog/document-ai-cost-comparison/

[88] ofox.ai. Best LLM for OCR 2026: 7 Models Ranked, GLM-OCR Wins 94.62. https://ofox.ai/blog/best-ai-model-for-ocr-2026/

[89] Smith, R. et al. Tesseract OCR engine, v5.x. https://github.com/tesseract-ocr/tesseract (accessed 2026-06).

[90] JaidedAI. EasyOCR. https://github.com/JaidedAI/EasyOCR (accessed 2026-06).

[91] Topdu et al. OpenOCR. https://github.com/Topdu/OpenOCR (accessed 2026-06).

[92] Paruchuri, V. Surya: multilingual document OCR toolkit. https://github.com/datalab-to/surya (2024).

[93] Paruchuri, V. Marker: PDF to markdown. https://github.com/datalab-to/marker (2024).

[94] OpenDataLab. MinerU v0.9 release. https://github.com/opendatalab/MinerU (2024).

[95] OpenDataLab. MinerU 2.5 technical report and model cards. https://huggingface.co/opendatalab (2025).

[96] Blecher, L. et al. Nougat: Neural Optical Understanding for Academic Documents. arXiv:2308.13418 (2023).

[97] Wei, H. et al. General OCR Theory: Towards OCR-2.0 via a Unified End-to-end Model. arXiv:2409.01704 (2024).

[98] Wei, H. et al. Vary: Scaling up the Vision Vocabulary for Large Vision-Language Models. arXiv:2312.06109 (2023).

[99] Liu, C. et al. Fox: Focus Anywhere for Fine-grained Multi-page Document Understanding. arXiv:2405.14295 (2024).

[100] Liu, Y. et al. TextMonkey: An OCR-Free Large Multimodal Model for Understanding Document. arXiv:2403.04473 (2024).

[101] Hu, A. et al. mPLUG-DocOwl 1.5: Unified Structure Learning for OCR-free Document Understanding. arXiv:2403.12895 (2024).

[102] Hu, A. et al. mPLUG-DocOwl2: High-resolution Compressing for OCR-free Multi-page Document Understanding. arXiv:2409.03420 (2024).

[103] Mathpix Inc. Mathpix OCR API v3 documentation. https://docs.mathpix.com (accessed 2026-06).

[104] DeepSeek-AI. DeepSeek-OCR: Contexts Optical Compression. HF https://huggingface.co/deepseek-ai/DeepSeek-OCR (2025).

[105] Zhipu AI / THUDM. GLM-4V / GLM-OCR family. https://github.com/THUDM (accessed 2026-06). [unverified; URL inaccessible at audit time]

[106] Xiaomi FireRedTeam. FireRed-OCR model card. https://huggingface.co/FireRedTeam (2025).

[107] Alibaba Logics team. Logics-Parsing technical note (vendor blog, 2025). PENDING canonical URL.

[108] Datalab. Chandra-OCR-2 model card. https://huggingface.co/datalab-to/chandra-ocr-2 (2026).

[109] Baidu Qianfan platform. OCR API reference. https://cloud.baidu.com/product/qianfan (accessed 2026-06). [unverified; URL inaccessible at audit time]

[110] Wang, P. et al. Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution. arXiv:2409.12191 (2024).

[111] Qwen Team. Qwen2.5-VL Technical Report. arXiv:2502.13923 (2025).

[112] Qwen Team. Qwen3-VL-30B-A3B-Instruct (MoE VLM, 30B-total / 3B-active) model card. https://huggingface.co/Qwen/Qwen3-VL-30B-A3B-Instruct (2025). See also Thinking variant: https://huggingface.co/Qwen/Qwen3-VL-30B-A3B-Thinking

[113] Liu, H. et al. LLaVA-1.6 (LLaVA-NeXT). https://llava-vl.github.io/blog/2024-01-30-llava-next/ (2024).

[114] Meta AI. Llama 3.2 multimodal model card. https://huggingface.co/meta-llama/Llama-3.2-90B-Vision-Instruct (2024).

[115] OpenAI. GPT-4o system card. https://openai.com/index/hello-gpt-4o/ (2024). [unverified; URL inaccessible at audit time]

[116] OpenAI. GPT-4o mini announcement. https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/ (2024). [unverified; URL inaccessible at audit time]

[117] OpenAI. GPT-4.1 model release notes. https://platform.openai.com/docs/models/gpt-4.1 (2025).

[118] OpenAI. GPT-5 / GPT-5.4 reasoning model documentation. https://platform.openai.com/docs/models (2025–2026).

[119] Google DeepMind. Gemini 1.5 Technical Report. arXiv:2403.05530 (2024).

[120] Google DeepMind. Gemini 2.5 model family. https://deepmind.google/technologies/gemini/ (2025).

[121] Anthropic. Claude Sonnet 4.6 model card. https://www.anthropic.com/claude (2026).

[122] Mistral AI. News page, most recent flagship models as of 2026-06: Mistral Medium 3.5 (2026-05-22), Mistral Small 4 (2026-03-16), Mistral 3 (2025-12-02), Magistral (2025-06-10). No 'Mistral Large 3' release exists; the v2 citation appears to have been fabricated and the surrounding claim should be revised or removed. https://mistral.ai/news/

[123] SAVIOR-Bench authors. SAVIOR-Bench: 509-document attested OCR + parse benchmark, §2.1 (composition and IAA 0.761). Paper notes at /Users/niyati/Desktop/hyperapi-documentapi-benchmark-factory/paper/SAVIOR-Bench.md.

[124] Mathew, M., Karatzas, D., Jawahar, C.V. DocVQA: A Dataset for VQA on Document Images. WACV 2021. https://www.docvqa.org/

[125] See [3]. (Duplicate entry merged; canonical ref is [3].)

[126] Poznanski, J. et al. olmOCR: Unlocking Trillions of Tokens in PDFs with Vision Language Models. AllenAI (2025). https://olmocr.allenai.org/

[127] Masry, A. et al. ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning. ACL Findings 2022. https://github.com/vis-nlp/ChartQA

[128] Hyperbots parse-x-research team. DOC-TYPE-GAPS.json (16 doc types, 2026-05-26 snapshot). /Users/niyati/Desktop/hyperapi-parse-x-research/command-center/DOC-TYPE-GAPS.json.

[129] Hyperbots benchmark-factory. CLAUDE.md team mandate (line 17). /Users/niyati/Desktop/hyperapi-documentapi-benchmark-factory/CLAUDE.md (2026).

[130] Microsoft. What's new in Azure AI Document Intelligence (v4.0 GA, REST 2024-11-30). Microsoft Learn (2024–2026). https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/whats-new?view=doc-intel-4.0.0

[131] Microsoft Azure. Document Intelligence pricing. Azure (2026). https://azure.microsoft.com/en-in/pricing/details/document-intelligence/ [unverified; URL inaccessible at audit time]

[132] Google. Gemini API pricing (2.5 Pro / 2.5 Flash). costgoat / pricepertoken aggregators (2026). https://pricepertoken.com/pricing-page/model/google-gemini-2.5-pro

[133] MetaCTO. The true cost of Google Gemini: API pricing guide (May 2026). https://www.metacto.com/blogs/the-true-cost-of-google-gemini-a-guide-to-api-pricing-and-integration

[134] MetaCTO. Claude API Pricing 2026: Opus 4.8, Sonnet 4.6, Haiku 4.5. (2026). https://www.metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration

[135] CloudZero. Anthropic Claude API Pricing in 2026. (2026). https://www.cloudzero.com/blog/claude-api-pricing/

[136] Microsoft. What's new in Azure OpenAI in Microsoft Foundry Models (classic). Microsoft Learn. Confirmed: o3 released April 2025; gpt-5 series released August 2025. Specific snapshots (gpt-5 2025-08-07, gpt-5.1 2025-11-13, gpt-5.2-chat 2026-02-10) not visible on the page.

[137] OpenAI. API Deprecations notice, older GPT-5 / o3 snapshots removed 2026-12-11. developers.openai.com (2026). https://developers.openai.com/api/docs/deprecations

[138] Wikipedia. GPT-5.4 (released 2026-03-05; mini/nano 2026-03-17). https://en.wikipedia.org/wiki/GPT-5.4

[139] llm-stats. Mistral Large 3 (mistral-large-2509 / 2512), benchmarks, pricing, context. (2026). https://llm-stats.com/models/mistral-large-3-2509

[140] TokenMix. Mistral API Pricing 2026: Large 3 output $6/M. (2026). https://tokenmix.ai/blog/mistral-api-pricing

[141] Mathpix. Convert API pricing and reviews. G2 (2026). https://www.g2.com/products/mathpix/reviews

[142] LlamaIndex. LlamaParse pricing, credit system (1,000 credits = $1; 10k free/mo). LlamaCloud docs (2025–2026).

[143] Vstorm. Top 10 document parsing services for RAG pipelines and LLM applications 2026. https://vstorm.co/llamaindex/top-10-document-parsing-services-for-rag-pipelines-and-llm-applications/

[144] Reducto. The complete agentic document platform, parser comparison. (2026). https://llms.reducto.ai/document-parser-comparison

[145] Unstructured.io. Serverless API pricing (hi_res vs fast strategies). unstructured.io (2026).

[146] Firecrawl. Best PDF Parsers for AI and RAG Workflows in 2026 (Docling, Unstructured, Reducto, LlamaParse comparison). https://www.firecrawl.dev/blog/best-pdf-parsers

[147] IBM Research. Docling, open-source document conversion toolkit. GitHub (2024–2026). https://github.com/DS4SD/docling

[148] Hyperbots internal user-memory preferences: azure-openai-preferred; openai-default-gpt-5-4-thinking. (2026).

[149] Liang, P., Bommasani, R., Lee, T., et al. Holistic Evaluation of Language Models. arXiv:2211.09110 (2022). https://crfm.stanford.edu/helm/

[150] MLCommons. MLPerf Inference 5.1: Benchmarking Small LLMs with Llama3.1-8B (2025). https://mlcommons.org/2025/09/small-llm-inference-5-1/

[151] Lambda. MLPerf Inference v6.0: hardware leap, software maturity (2026). https://lambda.ai/blog/lambdas-mlperf-inference-v6.0-hardware-leap-software-maturity-research-breakthrough

[152] BentoML. Key metrics for LLM inference. LLM Inference Handbook (accessed 2026-06). https://bentoml.com/llm/llm-inference-basics/llm-inference-metrics

[153] GMI Cloud. Independent Speed Data for 2026: LLM Inference Speed Benchmarks on TTFT, Throughput, and Cost. https://www.gmicloud.ai/en/blog/llm-inference-speed-benchmark-2026

[154] Parsli. The Real Cost of Using LLMs for OCR (And the Architecture That Cut It by 60x) (2025). https://parsli.co/blog/real-cost-llm-ocr-document-extraction
[155] Xu, Y., Lv, T., Cui, L., Wang, G., Lu, Y., Florencio, D., Zhang, C., Wei, F. LayoutXLM: Multimodal Pre-training for Multilingual Visually-rich Document Understanding. arXiv:2104.08836 (2021). https://arxiv.org/abs/2104.08836. Verified.
[156] Tang, Z., Yang, Z., Wang, G., Fang, Y., Liu, Y., Zhu, C., Zeng, M., Zhang, C., Bansal, M. Unifying Vision, Text, and Layout for Universal Document Processing. CVPR 2023. arXiv:2212.02623. https://arxiv.org/abs/2212.02623. Verified.
[157] Powalski, R., Borchmann, L., Jurkiewicz, D., Dwojak, T., Pietruszka, M., Pałka, G. Going Full-TILT Boogie on Document Understanding with Text-Image-Layout Transformer. ICDAR 2021. arXiv:2102.09550. https://arxiv.org/abs/2102.09550. Verified.
[158] Zhang, K., Shasha, D. Simple Fast Algorithms for the Editing Distance between Trees and Related Problems. SIAM Journal on Computing 18(6):1245-1262 (1989). https://doi.org/10.1137/0218082. Verified.
[159] Cui, L., Xu, Y., Lv, T., Wei, F. Document AI: Benchmarks, Models and Applications. Data Intelligence 3(1):27-50 (2021). https://doi.org/10.1162/dint_a_00064
[160] Subramani, N., Matton, A., Greaves, M., Lam, A. A Survey of Deep Learning Approaches for OCR and Document Understanding. arXiv:2011.13534 (2020). https://arxiv.org/abs/2011.13534
[161] Liang, P. et al. Holistic Evaluation of Language Models (HELM). TMLR (2023). arXiv:2211.09110. https://arxiv.org/abs/2211.09110
[162] Srivastava, A. et al. Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models (BIG-bench). TMLR (2023). arXiv:2206.04615. https://arxiv.org/abs/2206.04615
[163] Borchmann, L. et al. DUE: End-to-End Document Understanding Benchmark. NeurIPS Datasets and Benchmarks (2021). https://duebenchmark.com/
[164] Dror, R., Baumer, G., Shlomov, S., Reichart, R. The Hitchhiker's Guide to Testing Statistical Significance in NLP. ACL (2018). arXiv:1809.01448. https://arxiv.org/abs/1809.01448
[165] Tito, R., Karatzas, D., Valveny, E. Hierarchical multimodal transformers for Multi-Page DocVQA. Pattern Recognition (2023). https://doi.org/10.1016/j.patcog.2023.109834
[166] Es, S., James, J., Espinosa-Anke, L., Schockaert, S. RAGAs: Automated Evaluation of Retrieval Augmented Generation. EACL Demo (2024). arXiv:2309.15217. https://arxiv.org/abs/2309.15217
