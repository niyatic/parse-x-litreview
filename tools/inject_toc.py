#!/usr/bin/env python3
"""Inject a Table of Contents into an HTML file. Usage: inject_toc.py INPUT.html [OUTPUT.html]"""
from __future__ import annotations
import re, html as html_mod, unicodedata, sys
from pathlib import Path

src = Path(sys.argv[1]); dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src
text = src.read_text()

def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode()
    s = re.sub(r"<[^>]+>", "", s); s = re.sub(r"[^a-zA-Z0-9\s\-]", "", s).lower().strip()
    return re.sub(r"\s+", "-", s)[:80]

HEADING_RE = re.compile(r"<(h[23])(\s[^>]*)?>(.*?)</\1>", re.S)
seen=set(); toc_items=[]
def repl(m):
    tag, attrs, inner = m.group(1), (m.group(2) or ""), m.group(3)
    txt = re.sub(r"<[^>]+>", "", inner).strip()
    if not txt or txt.lower()=="abstract": return m.group(0)
    if 'id="' in attrs:
        sid = re.search(r'id="([^"]+)"', attrs).group(1)
    else:
        base = slugify(txt) or "sec"; sid = base; i = 2
        while sid in seen: sid = f"{base}-{i}"; i += 1
        attrs = (attrs or "") + f' id="{sid}"'
    seen.add(sid); toc_items.append((tag, sid, txt))
    return f"<{tag}{attrs}>{inner}</{tag}>"
text = HEADING_RE.sub(repl, text)

toc = ['<nav class="toc"><details open><summary><strong>Contents</strong></summary>', '<ol class="toc-list">']
in3 = False
for tag, sid, txt in toc_items:
    safe = html_mod.escape(txt)
    if tag == "h2":
        if in3: toc.append("</ol></li>"); in3 = False
        toc.append(f'<li><a href="#{sid}">{safe}</a>')
    else:
        if not in3: toc.append("<ol>"); in3 = True
        toc.append(f'<li><a href="#{sid}">{safe}</a></li>')
if in3: toc.append("</ol></li>")
toc.append("</ol></details></nav>")

toc_css = """
nav.toc{font-size:.92em;background:#fbfbf6;border:1px solid #d9d9c8;border-radius:4px;padding:.8em 1.2em;margin:1.2em 0 2em 0;}
nav.toc summary{cursor:pointer}nav.toc ol{padding-left:1.6em;margin:.4em 0}
nav.toc ol ol{list-style:lower-alpha}nav.toc a{color:#1a4f8f;text-decoration:none}
nav.toc a:hover{text-decoration:underline}h2,h3{scroll-margin-top:1em}
"""
text = text.replace("</style>", toc_css + "</style>", 1)
m = re.search(r'(<div class="abstract">.*?</div>)', text, re.S)
if m:
    text = text[:m.end()] + "\n" + "\n".join(toc) + "\n" + text[m.end():]
else:
    text = text.replace("</h1>", "</h1>\n" + "\n".join(toc) + "\n", 1)
dst.write_text(text)
print(f"TOC injected: {len(toc_items)} entries -> {dst}")
