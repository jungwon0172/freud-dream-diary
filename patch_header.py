# -*- coding: utf-8 -*-
import re, glob, os
from header_tpl import render_header, CAT_IDS

header_re = re.compile(r'<header class="site">.*?</header>', re.DOTALL)
ACTIVE = {"index.html":"home","symbols.html":"symbols","diary.html":"diary","about.html":"about","contact.html":"contact"}

files = glob.glob("*.html") + glob.glob("theory/*.html") + glob.glob("dream/*.html")
for p in files:
    root = "../" if "/" in p else ""
    if p.startswith("dream/"): cur = "symbols"
    elif p.startswith("theory/"): cur = "theory"
    else: cur = ACTIVE.get(p)
    s = open(p, encoding="utf-8").read()
    s = header_re.sub(lambda m: render_header(root, cur), s, count=1)
    if p == "symbols.html":
        for name, cid in CAT_IDS:
            s = s.replace(f'<div class="section-head mt-40">\n    <span class="tag">{name}</span>',
                          f'<div class="section-head mt-40" id="cat-{cid}">\n    <span class="tag">{name}</span>', 1)
    open(p, "w", encoding="utf-8").write(s)
print("patched", len(files))

# generate.py도 동일 헤더/카테고리 id를 쓰도록 맞춤 (재생성 시 되돌아가지 않게)
g = open("generate.py", encoding="utf-8").read()
g = re.sub(r'HEADER = """.*?"""\n', 'from header_tpl import render_header as _rh, CAT_IDS\n', g, count=1, flags=re.DOTALL)
g = re.sub(r'def nav_active\(current\):.*?\n\n\ndef render_header\(root, current\):.*?\n    \)\n', 'def render_header(root, current):\n    return _rh(root, current)\n', g, count=1, flags=re.DOTALL)
g = g.replace('cat_html += f"""  <div class="section-head mt-40">', 'cat_html += f"""  <div class="section-head mt-40" id="cat-{dict(CAT_IDS)[cat]}">', 1)
open("generate.py", "w", encoding="utf-8").write(g)
