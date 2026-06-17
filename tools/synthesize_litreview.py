#!/usr/bin/env python3
"""Synthesize 12-agent workflow output into NeurIPS-style HTML + PDF.

Inputs:  /private/tmp/.../wqiioklxi.output (workflow result JSON)
Outputs:
  /Users/niyati/Desktop/hyperapi-parse-x-research/command-center/LIT-REVIEW-2026-06-16.md
  /Users/niyati/Desktop/hyperapi-parse-x-research/command-center/LIT-REVIEW-2026-06-16.html
  /Users/niyati/Desktop/hyperapi-parse-x-research/command-center/LIT-REVIEW-2026-06-16.pdf
"""
from __future__ import annotations
import json, re, html, subprocess, sys
from pathlib import Path

WF_OUT = Path("/private/tmp/claude-501/-Users-niyati/73e72204-548e-414c-81b6-3c2150551344/tasks/wqiioklxi.output")
OUT_DIR = Path("/Users/niyati/Desktop/hyperapi-parse-x-research/command-center")
STEM = "LIT-REVIEW-2026-06-16"
MD_PATH   = OUT_DIR / f"{STEM}.md"
HTML_PATH = OUT_DIR / f"{STEM}.html"
PDF_PATH  = OUT_DIR / f"{STEM}.pdf"

DIM_ORDER = ["D-OCR","D-PARSE-INTENT","D-LAYOUT","D-BBOX","D-TABLE","D-DOC-QUALITY","D-LANG","D-DOWNSTREAM","D-COST-LATENCY"]
CROSS_ORDER = ["LINEAGE", "DATASETS", "VENDOR"]  # matches workflow CROSS order

# ---------- 1. Load + dedupe citations + renumber ----------
wf = json.load(WF_OUT.open())["result"]
sections = [s for s in wf["dimensions"] if s] + [s for s in wf["cross_cutting"] if s]

cite_text: dict[str, str] = {}
for s in sections:
    for c in s.get("citations", []):
        k = c["key"].strip()
        if k not in cite_text:
            cite_text[k] = c["text"].strip()

# Order keys by first-appearance in concatenated body.
order: list[str] = []
seen: set[str] = set()
CITE_RE = re.compile(r"\[([a-zA-Z0-9_\-]+)\]")
for s in sections:
    body = s.get("section_markdown", "")
    for m in CITE_RE.finditer(body):
        k = m.group(1)
        if k in cite_text and k not in seen:
            seen.add(k); order.append(k)
# Catch citations that exist in lists but never inline-referenced — append at end.
for k in cite_text:
    if k not in seen:
        seen.add(k); order.append(k)

key_to_num = {k: i+1 for i, k in enumerate(order)}

def renumber(md: str) -> str:
    def repl(m):
        k = m.group(1)
        if k in key_to_num: return f"[{key_to_num[k]}]"
        return m.group(0)
    return CITE_RE.sub(repl, md)

# ---------- 2. Assemble Markdown body ----------
def find(items, key):
    for it in items:
        if it and key.lower() in (it.get("section_markdown","").lower()[:200]):
            return it
    return None

# Map dim sections by D-key (first 200 chars of section_markdown contain the heading with the D-key)
dim_by_key: dict[str, dict] = {}
for s in [x for x in wf["dimensions"] if x]:
    head = s["section_markdown"].splitlines()[0]
    for k in DIM_ORDER:
        if k in head:
            dim_by_key[k] = s
            break
cross_by_key: dict[str, dict] = {}
for k, s in zip(CROSS_ORDER, [x for x in wf["cross_cutting"] if x]):
    cross_by_key[k] = s

TITLE = "Parse-x: A Literature Review for the Deep Benchmark Framework"
AUTHORS = "Hyperbots Research — hyperapi-parse-x-research team"
DATE = "2026-06-16"

ABSTRACT = (
"Document parsing has bifurcated into two literatures with little overlap: a multimodal-LLM benchmark line "
"(OCRBench v2, OmniDocBench, olmOCR-Bench) that reports single aggregate numbers per model, and an internal "
"benchmark line (SAVIOR-Bench, ParseBench) that exposes per-document score vectors, multilingual-quality "
"stratification, and downstream-task lift. We survey the prior art for each of the nine measurement dimensions "
"defined by the Parse-x Deep Benchmark Framework (D-OCR, D-PARSE-INTENT, D-LAYOUT, D-BBOX, D-TABLE, "
"D-DOC-QUALITY, D-LANG, D-DOWNSTREAM, D-COST-LATENCY) and the sixteen-document-type taxonomy that cross-cuts them. "
"For each dimension we name the canonical benchmarks, the relevant model families, and the specific deltas that "
"justify the framework's additional measurement discipline. Three appendices provide a structured model-lineage "
"table covering the fifty-plus models in the project's measurement pool, a datasets-and-contamination posture "
"register, and a vendor-and-API pin table for the closed-source services in scope. The review is researcher-not-"
"advocate: prior work is named for what it measures and what it does not measure, no winner is pre-picked, and "
"every quantitative claim carries a citation."
)

INTRO = (
"## 1. Introduction\n\n"
"The Parse-x Deep Benchmark Framework [framework2026] decomposes the question 'is this document-parsing engine "
"best for finance documents?' into nine orthogonal measurement dimensions and a sixteen-type document taxonomy. "
"Each cell of the resulting matrix is anchored to a public benchmark where possible (ParseBench [parsebench2024], "
"SAVIOR-Bench [savior2026], OmniDocBench [omnidocbench2024], PubTabNet, DocLayNet) and falls back to in-house "
"silver pipelines (BBOX-SILVER-PIPELINE-SPEC) or stratified hold-outs (dataset_95) when public coverage is absent. "
"The framework's publish-gate requires per-document score vectors with bootstrap CI95 (or an explicit attestation "
"label), uniform decoding pins (temperature 0.1, top-p 0.9, max_tokens 2048, seed 20260516), and fine-tune-vs-"
"zero-shot disclosure on every cell.\n\n"
"This literature review serves two purposes. First, it surveys the prior art per dimension so that each new "
"leaderboard cell can be interpreted against the right historical baseline. Second, it surfaces the methodological "
"gaps in that prior art — particularly the absent per-document vectors, the inconsistent fine-tune disclosure, "
"the under-stratified multilingual and quality axes, and the near-total absence of parse-to-downstream lift "
"measurements — that motivate the framework's additional measurement discipline. We are deliberate that the "
"contribution being claimed is *measurement discipline*, not new models or new datasets.\n\n"
"The remainder of the paper is organized as the framework dictates. §2 surveys the nine dimensions in order. "
"Appendices A–C provide the model lineage table, the datasets-and-contamination posture register, and the "
"vendor-and-API pin table. We close (§3) with a discussion of the largest open gates that block first-pass "
"cell publication.\n"
)

CONCLUSION = (
"## 3. Discussion and Open Gates\n\n"
"Three patterns surface across the nine dimensions. First, **per-document score vectors are absent everywhere "
"except SAVIOR-Bench's internal pipeline** — OCRBench v2, OmniDocBench, olmOCR-Bench, PubTabNet and DocLayNet all "
"publish single aggregate numbers per model, so any rigorous bootstrap CI95 reporting on top of them requires "
"either re-running the eval (with the attendant compute and decoding-pin honesty work) or explicit attestation. "
"Second, **fine-tune-vs-zero-shot disclosure is inconsistent in the published literature**, a known SAVIOR-Bench "
"complaint (R6) and a recurring source of misleading model-vs-model comparisons (e.g., a 2B fine-tuned model "
"beating a 75B zero-shot model is structurally expected and should not be reported as a model-capability win). "
"Third, **parse-to-downstream lift (D-DOWNSTREAM) is methodologically new for parse benchmarks**: prior art treats "
"OCR / parse as an intrinsic-metric end-state, not as a stage feeding extract / RAG / classify pipelines, and the "
"paired-bootstrap testing infrastructure imported from NLP / ASR [koehn2004] has not been carried over.\n\n"
"The largest open gates blocking first-pass cell publication, in order of severity, are: (i) BLK-18 — the SAVIOR-"
"Bench 509-doc out7 corpus is not on disk, blocking WordRecall reconciliation against the attested 31-cell "
"leaderboard; (ii) PENDING-MAXTOKEN — the uniform max_tokens=2048 ceiling truncates Chandra and Qwen on dense "
"text-content / text-formatting splits at 8-10 out of 10 documents, producing 0.0 scores by truncation rather than "
"by model capability; (iii) the model-lineage table (Appendix A) carries several PENDING-PIN entries that block "
"the per-cell `pins.adapter_version` field from being populated; (iv) several Tier-1 document types in DOC-TYPE-"
"GAPS still have zero measured cells across every framework dimension, a gap that no public benchmark fills.\n\n"
"The framework's measurement discipline does not, by itself, resolve any of these gates — but it makes them "
"visible. We treat that as the contribution.\n"
)

body_parts = [
    f"# {TITLE}\n\n*{AUTHORS}*  \n*{DATE}*\n",
    f"## Abstract\n\n{ABSTRACT}\n",
    renumber(INTRO),
    "## 2. The Nine Measurement Dimensions\n",
]
for k in DIM_ORDER:
    s = dim_by_key.get(k)
    if not s:
        body_parts.append(f"### {k}\n\n*[Section unavailable — agent returned null.]*\n")
        continue
    body_parts.append(renumber(s["section_markdown"]).rstrip() + "\n")

for k in CROSS_ORDER:
    s = cross_by_key.get(k)
    if not s: continue
    body_parts.append(renumber(s["section_markdown"]).rstrip() + "\n")

body_parts.append(renumber(CONCLUSION))

# Bibliography
bib_lines = ["## References\n"]
for k in order:
    n = key_to_num[k]
    bib_lines.append(f"[{n}] {cite_text[k]}\n")
body_parts.append("\n".join(bib_lines))

md_full = "\n".join(body_parts)
MD_PATH.write_text(md_full)
print(f"wrote {MD_PATH} ({len(md_full)} chars, {len(order)} unique citations)")

# ---------- 3. Markdown -> HTML (custom minimal MD parser sufficient here) ----------
def md_to_html(md: str) -> str:
    # Convert markdown tables before line-by-line treatment
    lines = md.split("\n")
    out: list[str] = []
    in_list = False
    i = 0
    def close_list():
        nonlocal in_list
        if in_list: out.append("</ul>"); in_list = False
    def inline(s: str) -> str:
        s = html.escape(s, quote=False)
        # bold/italic/code
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*([^*\n]+)\*", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        # links [text](url)
        s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
        # citation [N]  -> superscript link
        s = re.sub(r"\[(\d+)\]", r'<sup class="cite">[<a href="#ref-\1">\1</a>]</sup>', s)
        return s
    while i < len(lines):
        ln = lines[i]
        # Tables: a line containing | followed by a divider row of |---|
        if "|" in ln and i+1 < len(lines) and re.match(r"^\s*\|[\s\-|:]+\|\s*$", lines[i+1]):
            close_list()
            header = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append('<table>')
            out.append("<thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in header) + "</tr></thead>")
            out.append("<tbody>")
            for r in rows:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</tbody></table>")
            continue
        if ln.startswith("# "):
            close_list(); out.append(f"<h1>{inline(ln[2:])}</h1>"); i+=1; continue
        if ln.startswith("## "):
            close_list(); out.append(f"<h2>{inline(ln[3:])}</h2>"); i+=1; continue
        if ln.startswith("### "):
            close_list(); out.append(f"<h3>{inline(ln[4:])}</h3>"); i+=1; continue
        if ln.startswith("#### "):
            close_list(); out.append(f"<h4>{inline(ln[5:])}</h4>"); i+=1; continue
        if re.match(r"^\s*[-*]\s+", ln):
            if not in_list: out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(re.sub(r'^\s*[-*]\s+', '', ln))}</li>")
            i+=1; continue
        # Reference list lines like "[1] Author. Title..."
        m = re.match(r"^\[(\d+)\]\s+(.*)$", ln)
        if m:
            close_list()
            n, rest = m.group(1), m.group(2)
            out.append(f'<p class="ref" id="ref-{n}"><span class="refnum">[{n}]</span> {inline(rest)}</p>')
            i+=1; continue
        if ln.strip() == "":
            close_list(); out.append(""); i+=1; continue
        close_list(); out.append(f"<p>{inline(ln)}</p>"); i+=1
    close_list()
    return "\n".join(out)

body_html = md_to_html(md_full)

NEURIPS_CSS = r"""
@page {
  size: A4;
  margin: 1.0in 1.0in 1.0in 1.0in;
  @bottom-center { content: counter(page); font-family: 'Latin Modern Roman', 'Computer Modern', Georgia, serif; font-size: 9pt; color: #444; }
}
html { font-size: 10.5pt; }
body {
  font-family: 'Latin Modern Roman', 'Computer Modern', 'CMU Serif', 'STIX Two Text', Georgia, 'Times New Roman', serif;
  color: #111;
  line-height: 1.42;
  text-align: justify;
  hyphens: auto;
  max-width: 6.5in;
  margin: 0 auto;
}
h1 {
  font-size: 17pt;
  font-weight: bold;
  text-align: center;
  margin: 0.4em 0 0.2em 0;
  line-height: 1.2;
}
h1 + p { text-align: center; font-style: italic; color: #444; margin: 0.1em 0; }
h2 {
  font-size: 13pt;
  font-weight: bold;
  margin: 1.3em 0 0.4em 0;
  border-bottom: 1px solid #bbb;
  padding-bottom: 2px;
}
h3 {
  font-size: 11.5pt;
  font-weight: bold;
  margin: 0.9em 0 0.3em 0;
  font-style: italic;
}
h4 {
  font-size: 10.5pt;
  font-weight: bold;
  margin: 0.7em 0 0.2em 0;
}
p { margin: 0.4em 0; }
sup.cite { font-size: 0.78em; }
sup.cite a { color: #1a4f8f; text-decoration: none; }
ul { margin: 0.3em 0 0.4em 1.3em; padding: 0; }
li { margin: 0.15em 0; }
code {
  font-family: 'Latin Modern Mono', 'CMU Typewriter', 'Courier New', monospace;
  font-size: 0.92em;
  background: #f3f3f3;
  padding: 1px 3px;
  border-radius: 2px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.6em 0 0.8em 0;
  font-size: 9.5pt;
}
thead { border-top: 1.2px solid #222; border-bottom: 0.8px solid #444; }
tbody { border-bottom: 1.2px solid #222; }
th { text-align: left; padding: 4px 6px; font-weight: bold; }
td { padding: 3px 6px; vertical-align: top; }
tr + tr td { border-top: 0.4px solid #ddd; }
a { color: #1a4f8f; text-decoration: none; }
.ref {
  font-size: 9pt;
  margin: 0.15em 0;
  padding-left: 2.4em;
  text-indent: -2.4em;
  text-align: left;
  hyphens: none;
  word-break: break-word;
}
.refnum { display: inline-block; min-width: 2em; font-weight: bold; }
.abstract { font-size: 10pt; margin: 0.6em 1em; }
.abstract h2 { font-size: 11pt; border: none; text-align: center; margin-top: 0; }
"""

# Post-process: wrap abstract in styled box (h2 'Abstract' + next p)
body_html_styled = re.sub(
    r"<h2>Abstract</h2>\s*<p>(.*?)</p>",
    r'<div class="abstract"><h2>Abstract</h2><p>\1</p></div>',
    body_html, count=1, flags=re.S,
)

html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{html.escape(TITLE)}</title>
<style>{NEURIPS_CSS}</style>
</head>
<body>
{body_html_styled}
</body>
</html>
"""
HTML_PATH.write_text(html_doc)
print(f"wrote {HTML_PATH} ({len(html_doc)} chars)")

# ---------- 4. PDF via weasyprint ----------
rc = subprocess.call(["/opt/homebrew/bin/weasyprint", str(HTML_PATH), str(PDF_PATH)],
                     stdout=sys.stderr, stderr=sys.stderr)
print(f"weasyprint rc={rc}; pdf={'OK' if PDF_PATH.exists() else 'MISSING'} "
      f"size={PDF_PATH.stat().st_size if PDF_PATH.exists() else 0}")
