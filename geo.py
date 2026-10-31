# -*- coding: utf-8 -*-
"""GEO/SEO 공통: JSON-LD, Open Graph, 조사 처리"""
import json, html

DOMAIN = "https://freud-dream-diary.vercel.app"
SITE = "프로이트 꿈해몽"
MODIFIED = "2026-10-31"
EMAIL = "yjw2172@naver.com"

ORG = {"@type": "Organization", "@id": DOMAIN + "/#org", "name": SITE, "url": DOMAIN + "/",
       "email": EMAIL}


def josa(word, with_final, without_final):
    """받침 유무에 따라 조사 선택 (은/는, 을/를, 이/가)"""
    ch = word.strip()[-1]
    if "가" <= ch <= "힣":
        return with_final if (ord(ch) - 0xAC00) % 28 else without_final
    return with_final


def ld(obj):
    if isinstance(obj, dict) and "@context" not in obj:
        obj = {"@context": "https://schema.org", **obj}
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>\n"


def og(title, description, url, og_type="website"):
    e = lambda s: html.escape(s, quote=True)
    return (f'<meta property="og:type" content="{og_type}">\n'
            f'<meta property="og:site_name" content="{SITE}">\n'
            f'<meta property="og:locale" content="ko_KR">\n'
            f'<meta property="og:title" content="{e(title)}">\n'
            f'<meta property="og:description" content="{e(description)}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta name="twitter:card" content="summary">\n'
            f'<meta name="twitter:title" content="{e(title)}">\n'
            f'<meta name="twitter:description" content="{e(description)}">\n')


def breadcrumb(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def article(headline, description, url, keywords=None):
    a = {"@type": "Article", "headline": headline, "description": description, "inLanguage": "ko-KR",
         "datePublished": MODIFIED, "dateModified": MODIFIED,
         "author": {"@type": "Organization", "name": SITE, "url": DOMAIN + "/"},
         "publisher": ORG, "mainEntityOfPage": {"@type": "WebPage", "@id": url}}
    if keywords:
        a["keywords"] = ", ".join(keywords)
    return a


def faq(pairs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}
