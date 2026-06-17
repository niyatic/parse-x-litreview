"""Reusable Markdown -> HTML converter + NeurIPS-style CSS.

Pure module: NO side effects on import. Exports:
  - md_to_html(md: str) -> str
  - NEURIPS_CSS: str

Used by tools/render_md_to_html.py (CLI wrapper) and the GitHub Action.
The original imperative v1-synthesis script is preserved as a separate
script outside the tools/ directory in the original repo.
"""
from __future__ import annotations
import re
import html as html_mod

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
}
.refnum { display: inline-block; min-width: 2em; font-weight: bold; }
.abstract { font-size: 10pt; margin: 0.6em 1em; }
.abstract h2 { font-size: 11pt; border: none; text-align: center; margin-top: 0; }
"""


def md_to_html(md: str) -> str:
    """Minimal Markdown -> HTML for the literature review (tables, refs, links, formatting)."""
    lines = md.split("\n")
    out: list[str] = []
    in_list = False
    i = 0

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def inline(s: str) -> str:
        s = html_mod.escape(s, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*([^*\n]+)\*", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
        s = re.sub(r"\[(\d+)\]", r'<sup class="cite">[<a href="#ref-\1">\1</a>]</sup>', s)
        return s

    while i < len(lines):
        ln = lines[i]
        if "|" in ln and i + 1 < len(lines) and re.match(r"^\s*\|[\s\-|:]+\|\s*$", lines[i + 1]):
            close_list()
            header = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append("<table>")
            out.append("<thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in header) + "</tr></thead>")
            out.append("<tbody>")
            for r in rows:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</tbody></table>")
            continue
        if ln.startswith("# "):
            close_list(); out.append(f"<h1>{inline(ln[2:])}</h1>"); i += 1; continue
        if ln.startswith("## "):
            close_list(); out.append(f"<h2>{inline(ln[3:])}</h2>"); i += 1; continue
        if ln.startswith("### "):
            close_list(); out.append(f"<h3>{inline(ln[4:])}</h3>"); i += 1; continue
        if ln.startswith("#### "):
            close_list(); out.append(f"<h4>{inline(ln[5:])}</h4>"); i += 1; continue
        if re.match(r"^\s*[-*]\s+", ln):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(re.sub(r'^\s*[-*]\s+', '', ln))}</li>")
            i += 1; continue
        m = re.match(r"^\[(\d+)\]\s+(.*)$", ln)
        if m:
            close_list()
            n, rest = m.group(1), m.group(2)
            out.append(f'<p class="ref" id="ref-{n}"><span class="refnum">[{n}]</span> {inline(rest)}</p>')
            i += 1; continue
        if ln.strip() == "":
            close_list(); out.append(""); i += 1; continue
        close_list(); out.append(f"<p>{inline(ln)}</p>"); i += 1

    close_list()
    return "\n".join(out)
