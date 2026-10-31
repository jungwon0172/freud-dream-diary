# -*- coding: utf-8 -*-
"""generate.py가 만들지 않는 정적 페이지(소개/문의/약관/일기/이론)에 도메인 치환 + OG + JSON-LD 적용"""
import re, glob
from geo import *

OLD = "https://PLACEHOLDER-DOMAIN.vercel.app"
block_re = re.compile(r"<!--geo-->.*?<!--/geo-->\n", re.S)
STATIC = ["about.html", "contact.html", "privacy.html", "terms.html", "diary.html"] + sorted(glob.glob("theory/*.html"))

for p in STATIC:
    s = open(p, encoding="utf-8").read().replace(OLD, DOMAIN)
    s = block_re.sub("", s)
    title = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)"', s).group(1)
    url = DOMAIN + "/" + p
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, count=1)
    crumbs = [("홈", DOMAIN + "/")]
    if p == "about.html":      node, t = {"@type": "AboutPage", "name": title, "url": url, "inLanguage": "ko-KR", "description": desc, "publisher": ORG}, "website"
    elif p == "contact.html":  node, t = {"@type": "ContactPage", "name": title, "url": url, "inLanguage": "ko-KR", "description": desc}, "website"
    elif p in ("privacy.html", "terms.html"): node, t = {"@type": "WebPage", "name": title, "url": url, "inLanguage": "ko-KR", "description": desc}, "website"
    elif p == "diary.html":
        node, t = {"@type": "WebApplication", "name": "꿈 일기", "url": url, "inLanguage": "ko-KR", "description": desc,
                   "applicationCategory": "LifestyleApplication", "operatingSystem": "Web",
                   "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}, "publisher": ORG}, "website"
        crumbs.append(("꿈 일기", url))
    elif p == "theory/index.html":
        node, t = {"@type": "CollectionPage", "name": title, "url": url, "inLanguage": "ko-KR", "description": desc}, "website"
        crumbs.append(("이론 노트", url))
    else:
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S).group(1).strip()
        node, t = article(h1, desc, url), "article"
        crumbs += [("이론 노트", DOMAIN + "/theory/index.html"), (h1, url)]
    blk = "<!--geo-->\n" + og(title, desc, url, t) + ld(node) + (ld(breadcrumb(crumbs)) if len(crumbs) > 1 else "") + "<!--/geo-->\n"
    s = s.replace("</head>", blk + "</head>", 1)
    open(p, "w", encoding="utf-8").write(s)
print("geo patched", len(STATIC))
