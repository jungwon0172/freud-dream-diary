# -*- coding: utf-8 -*-
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from data import SYMBOLS, CATEGORIES

ROOT = os.path.dirname(__file__)
from geo import DOMAIN, SITE, MODIFIED, ORG, ld, og, breadcrumb, article, faq, josa

from header_tpl import render_header as _rh, CAT_IDS

AD_SLOT = """<div class="wrap">
  <div class="ad-slot">
    <span class="ad-label">Advertisement</span>
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-2557338953436433"
         data-ad-slot="0000000000"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>
</div>
"""

FOOTER = """<footer class="site">
  <div class="wrap-wide">
    <span>© 2026 프로이트 꿈해몽. 이 사이트의 내용은 정신의학적 진단이 아닌 전통 해몽 및 교육 목적의 정보입니다.</span>
    <nav>
      <a href="{root}about.html">소개</a>
      <a href="{root}contact.html">문의</a>
      <a href="{root}privacy.html">개인정보처리방침</a>
      <a href="{root}terms.html">이용약관</a>
    </nav>
  </div>
</footer>

<script src="{root}assets/cookie-consent.js"></script>
"""

HEAD_COMMON = """<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="{root}assets/style.css">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2557338953436433" crossorigin="anonymous"></script>
"""


def render_header(root, current):
    return _rh(root, current)


def page_shell(root, current, title, description, canonical, body_html, extra_head=""):
    head = HEAD_COMMON.format(title=title, description=description, canonical=canonical, root=root) + og(title, description, canonical) + extra_head
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
{head}</head>
<body>

{render_header(root, current)}
{body_html}
{AD_SLOT}
{FOOTER.format(root=root)}
</body>
</html>
"""


def render_symbol_page(sym):
    root = "../"
    title = f"{sym['title']} 해몽 — 프로이트 꿈해몽"
    description = sym["summary"]
    canonical = f"{DOMAIN}/dream/{sym['slug']}.html"

    aliases_html = " · ".join(sym["aliases"])
    context_html = "".join(
        f"""    <div class="entry">
      <h3 class="qa-q">{situation}{josa(situation, '은', '는')} 어떤 의미인가요?</h3>
      <p class="entry-text">{meaning}</p>
    </div>
"""
        for situation, meaning in sym["context"].items()
    )
    situations = ", ".join(sym["context"].keys())
    t = sym["title"]
    faq_pairs = [(f"{t}{josa(t, '은', '는')} 무슨 뜻인가요?", sym["traditional"])]
    faq_pairs += [(f"{k}{josa(k, '은', '는')} 어떤 의미인가요?", v) for k, v in sym["context"].items()]
    faq_pairs.append((f"{t}{josa(t, '을', '를')} 심리학적으로 해석하면 어떤 의미인가요?", sym["psychological"]))
    jsonld = (ld(article(f"{t} 해몽", sym["summary"], canonical, sym["aliases"]))
              + ld(faq(faq_pairs))
              + ld(breadcrumb([("홈", DOMAIN + "/"), ("꿈해몽 전체 목록", DOMAIN + "/symbols.html"), (f"{t} 해몽", canonical)])))

    related = sym.get("related", [])
    related_map = {s["slug"]: s for s in SYMBOLS}
    related_html = "".join(
        f'<a class="chip" href="{r}.html">{related_map[r]["title"]}</a>\n' if r in related_map else ""
        for r in related
    )

    body = f"""<section class="hero wrap">
  <p class="eyebrow">DREAM DICTIONARY · {sym['category']}</p>
  <h1>{sym['title']} 해몽</h1>
  <p class="lede">{sym['summary']}</p>
  <p class="small mt-16">관련 검색어: {aliases_html}</p>
  <p class="small">최종 업데이트 {MODIFIED}</p>
</section>

<section class="section wrap article-body" style="padding-top:0;">
  <div class="answer-box">
    <span class="answer-label">핵심 답변</span>
    <p>{sym['summary']} 상황에 따라 해석이 달라지며, 대표적으로 {situations} 등으로 나뉩니다.</p>
  </div>

  <h2>전통 해몽 풀이</h2>
  <p>{sym['traditional']}</p>

  <h2 class="mt-40">상황별 의미</h2>
  <div class="mt-16">
{context_html}  </div>

  <h2 class="mt-40">심리학적으로 보면</h2>
  <p>{sym['psychological']}</p>

  <div class="disclaimer">이 풀이는 전통적으로 전해지는 꿈 해몽과 정신분석적 관점을 함께 소개하는 교육·오락 목적의 콘텐츠이며, 운세나 의학적 진단을 보장하지 않습니다.</div>

  <div class="mt-40">
    <p class="field-label">비슷한 꿈도 찾아보세요</p>
    <div class="chip-row">
{related_html}    </div>
  </div>

  <p class="mt-40"><a href="../symbols.html">← 전체 꿈해몽 목록으로</a></p>
</section>
"""
    return page_shell(root, "symbols", title, description, canonical, body, extra_head=jsonld)


def build_symbol_pages():
    outdir = os.path.join(ROOT, "dream")
    os.makedirs(outdir, exist_ok=True)
    for sym in SYMBOLS:
        html = render_symbol_page(sym)
        with open(os.path.join(outdir, f"{sym['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(html)


def build_search_data():
    data = [
        {
            "slug": s["slug"],
            "title": s["title"],
            "aliases": s["aliases"],
            "summary": s["summary"],
            "category": s["category"],
        }
        for s in SYMBOLS
    ]
    js = "window.DREAM_SYMBOLS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    with open(os.path.join(ROOT, "assets", "dream-data.js"), "w", encoding="utf-8") as f:
        f.write(js)


def build_index():
    root = ""
    title = "프로이트 꿈해몽 — 무료 꿈 해몽 검색 사전"
    description = "뱀꿈, 돈꿈, 이빨 빠지는 꿈 등 자주 검색되는 꿈해몽을 전통 해몽과 심리학적 관점으로 풀어드립니다. 궁금한 꿈을 검색해보세요."
    canonical = f"{DOMAIN}/"

    popular_slugs = ["snake", "money", "teeth", "pig", "falling", "chasing", "ex", "water"]
    popular_map = {s["slug"]: s for s in SYMBOLS}
    popular_cards = "".join(
        f"""      <a class="card" href="dream/{slug}.html" style="display:block;">
        <span class="concept-tag">{popular_map[slug]['category']}</span>
        <h3 style="font-family:var(--font-display); margin:6px 0 8px;">{popular_map[slug]['title']}</h3>
        <p style="margin:0; color:var(--ink-soft); font-size:14px;">{popular_map[slug]['summary']}</p>
      </a>
"""
        for slug in popular_slugs
    )

    body = f"""<section class="hero wrap">
  <p class="eyebrow">DREAM DICTIONARY — 꿈해몽 검색</p>
  <h1>어젯밤 꿈, 무슨 의미였을까요?</h1>
  <p class="lede">뱀꿈, 돈꿈, 이빨 빠지는 꿈처럼 자주 검색되는 꿈들을 전통 해몽과 정신분석 관점으로 함께 풀어드립니다. 아래에서 꿈에 나온 것을 검색해보세요.</p>
  <svg class="threshold" viewBox="0 0 700 64" preserveAspectRatio="none">
    <path d="M0,32 L18,18 L36,46 L54,14 L72,42 L90,20 Q130,8 170,32 T250,32 Q310,54 370,30 T460,32 Q540,8 600,32 T700,32" />
  </svg>
</section>

<section class="section wrap" style="border-top:none; padding-top:10px;">
  <div class="card" style="padding:18px 20px;">
    <label class="field-label" for="dream-search">꿈에 나온 것을 검색해보세요</label>
    <input type="text" id="dream-search" placeholder="예: 뱀, 돈, 이빨, 쫓기는 꿈...">
    <div id="search-results" class="mt-16"></div>
  </div>
</section>

<section class="section wrap">
  <div class="section-head">
    <span class="tag">자주 찾는 꿈</span>
    <h2>가장 많이 검색되는 꿈해몽</h2>
  </div>
  <div class="grid-2">
{popular_cards}  </div>
  <p class="mt-24"><a href="symbols.html">전체 꿈해몽 목록 보기 →</a></p>
</section>

<section class="section wrap">
  <div class="section-head">
    <span class="tag">꿈 기록</span>
    <h2>꿈을 기록하고 스스로 해석해보기</h2>
  </div>
  <p>해몽과 함께, 나만의 꿈을 기록하고 패턴을 확인하고 싶다면 꿈 일기 도구를 이용해보세요. 달력으로 지난 기록을 한눈에 보고, 기록지를 PDF로 인쇄할 수도 있습니다.</p>
  <a class="btn mt-8" href="diary.html">꿈 일기 쓰러 가기</a>
</section>
"""
    extra_head = f'<meta name="naver-site-verification" content="d3627b8ed52b0d92def5e199084707c7e6b07005">\n<script defer src="{root}assets/dream-data.js"></script>\n<script defer src="{root}assets/dream-search.js"></script>\n'
    extra_head += ld({"@type": "WebSite", "@id": DOMAIN + "/#website", "name": SITE, "url": DOMAIN + "/",
                      "inLanguage": "ko-KR", "description": description, "publisher": ORG})
    extra_head += ld({"@context": "https://schema.org", **ORG})
    html = page_shell(root, "home", title, description, canonical, body, extra_head=extra_head)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_symbols_listing():
    root = ""
    title = "꿈해몽 전체 목록 — 프로이트 꿈해몽"
    description = "자주 검색되는 꿈해몽을 카테고리별로 모두 모았습니다. 뱀꿈부터 돈꿈, 이빨 빠지는 꿈까지 검색해서 찾아보세요."
    canonical = f"{DOMAIN}/symbols.html"

    by_cat = {c: [] for c in CATEGORIES}
    for s in SYMBOLS:
        by_cat.setdefault(s["category"], []).append(s)

    cat_html = ""
    for cat in CATEGORIES:
        items = by_cat.get(cat, [])
        if not items:
            continue
        cards = "".join(
            f"""      <a class="card" href="dream/{s['slug']}.html" style="display:block;">
        <h3 style="font-family:var(--font-display); margin:0 0 6px; font-size:17px;">{s['title']}</h3>
        <p style="margin:0; color:var(--ink-soft); font-size:13.5px;">{s['summary']}</p>
      </a>
"""
            for s in items
        )
        cat_html += f"""  <div class="section-head mt-40" id="cat-{dict(CAT_IDS)[cat]}">
    <span class="tag">{cat}</span>
  </div>
  <div class="grid-2">
{cards}  </div>
"""

    body = f"""<section class="hero wrap">
  <p class="eyebrow">DREAM DICTIONARY — 전체 목록</p>
  <h1>꿈해몽 전체 목록</h1>
  <p class="lede">카테고리별로 정리된 꿈해몽 목록입니다. 원하는 항목을 검색하거나 눌러서 자세한 풀이를 확인하세요.</p>
</section>

<section class="section wrap" style="border-top:none; padding-top:10px;">
  <div class="card" style="padding:18px 20px;">
    <label class="field-label" for="dream-search">검색</label>
    <input type="text" id="dream-search" placeholder="예: 뱀, 돈, 이빨, 쫓기는 꿈...">
    <div id="search-results" class="mt-16"></div>
  </div>
</section>

<section class="section wrap">
{cat_html}</section>
"""
    extra_head = f'<script defer src="{root}assets/dream-data.js"></script>\n<script defer src="{root}assets/dream-search.js"></script>\n'
    extra_head += ld({"@type": "CollectionPage", "name": title, "url": canonical, "inLanguage": "ko-KR",
                      "mainEntity": {"@type": "ItemList", "itemListElement": [
                          {"@type": "ListItem", "position": i + 1, "name": f"{s['title']} 해몽",
                           "url": f"{DOMAIN}/dream/{s['slug']}.html"} for i, s in enumerate(SYMBOLS)]}})
    extra_head += ld(breadcrumb([("홈", DOMAIN + "/"), ("꿈해몽 전체 목록", canonical)]))
    html = page_shell(root, "symbols", title, description, canonical, body, extra_head=extra_head)
    with open(os.path.join(ROOT, "symbols.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_sitemap():
    urls = ["/", "/symbols.html", "/diary.html", "/theory/index.html",
            "/theory/condensation.html", "/theory/displacement.html",
            "/theory/wish-fulfillment.html", "/theory/day-residue.html",
            "/about.html", "/contact.html", "/privacy.html", "/terms.html"]
    urls += [f"/dream/{s['slug']}.html" for s in SYMBOLS]
    items = "\n".join(
        f'  <url><loc>{DOMAIN}{u}</loc><lastmod>{MODIFIED}</lastmod><changefreq>{"weekly" if u == "/" else "monthly"}</changefreq><priority>{"1.0" if u=="/" else "0.7"}</priority></url>'
        for u in urls
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def build_llms():
    lines = [f"# {SITE}", "",
             "> 뱀꿈·돈꿈·이빨 빠지는 꿈 등 자주 검색되는 꿈을 전통 해몽과 정신분석(프로이트) 관점으로 함께 풀이하는 한국어 꿈해몽 사전. 꿈 일기·달력·기록지 PDF 도구와 프로이트 꿈 이론 노트를 제공한다. 풀이는 교육·오락 목적이며 운세나 의학적 진단이 아니다.", "",
             "## 꿈해몽 풀이"]
    for s in SYMBOLS:
        lines.append(f"- [{s['title']} 해몽]({DOMAIN}/dream/{s['slug']}.html): {s['summary']}")
    lines += ["", "## 도구와 이론",
              f"- [꿈 일기]({DOMAIN}/diary.html): 꿈 기록, 달력, 패턴 통계, 꿈 해몽 기록지 PDF",
              f"- [이론 노트]({DOMAIN}/theory/index.html): 압축·전치·소원성취·낮의 잔재 등 프로이트 꿈 이론 정리",
              f"- [전체 목록]({DOMAIN}/symbols.html): 카테고리별 꿈해몽 목록", "",
              "## 사이트 정보",
              f"- [소개]({DOMAIN}/about.html)", f"- [문의]({DOMAIN}/contact.html)", ""]
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    full = [f"# {SITE} — 전체 해몽 콘텐츠", "", f"출처: {DOMAIN}/ (최종 업데이트 {MODIFIED})", ""]
    for s in SYMBOLS:
        full += [f"## {s['title']} 해몽", f"URL: {DOMAIN}/dream/{s['slug']}.html",
                 f"분류: {s['category']} / 관련 검색어: {', '.join(s['aliases'])}", "",
                 f"요약: {s['summary']}", "", "### 전통 해몽 풀이", s["traditional"], "", "### 상황별 의미"]
        full += [f"- {k}: {v}" for k, v in s["context"].items()]
        full += ["", "### 심리학적으로 보면", s["psychological"], ""]
    with open(os.path.join(ROOT, "llms-full.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(full))


def build_robots():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended"]
    txt = "User-agent: *\nAllow: /\n\n"
    txt += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    txt += f"Sitemap: {DOMAIN}/sitemap.xml\n"
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)


if __name__ == "__main__":
    build_llms()
    build_robots()
    build_search_data()
    build_symbol_pages()
    build_index()
    build_symbols_listing()
    build_sitemap()
    print(f"Generated {len(SYMBOLS)} symbol pages + index + symbols listing + sitemap.")
