#!/usr/bin/env python3
"""Render a markdown literature-review file to NeurIPS-styled HTML.
Usage: render_md_to_html.py INPUT.md OUTPUT.html [TITLE]"""
import sys, re, html
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from synthesize_litreview import md_to_html, NEURIPS_CSS

src = Path(sys.argv[1]); dst = Path(sys.argv[2])
title = sys.argv[3] if len(sys.argv) > 3 else "Parse-x: A Literature Review for the Deep Benchmark Framework"

md = src.read_text()
body = md_to_html(md)
body = re.sub(r"<h2>Abstract</h2>\s*<p>(.*?)</p>",
              r'<div class="abstract"><h2>Abstract</h2><p>\1</p></div>',
              body, count=1, flags=re.S)

doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{html.escape(title)}</title>
<style>{NEURIPS_CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""
dst.write_text(doc)
print(f"rendered: {src} -> {dst} ({len(doc)} chars)")
