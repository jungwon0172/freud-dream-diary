# -*- coding: utf-8 -*-
import re, os

FILES = {
    "diary.html": {"root": "", "active": "diary"},
    "about.html": {"root": "", "active": None},
    "contact.html": {"root": "", "active": None},
    "privacy.html": {"root": "", "active": None},
    "terms.html": {"root": "", "active": None},
    "theory/index.html": {"root": "../", "active": "theory"},
    "theory/condensation.html": {"root": "../", "active": "theory"},
    "theory/displacement.html": {"root": "../", "active": "theory"},
    "theory/wish-fulfillment.html": {"root": "../", "active": "theory"},
    "theory/day-residue.html": {"root": "../", "active": "theory"},
}

def nav_html(root, active):
    def cls(key):
        return ' class="active"' if key == active else ''
    return f'''<header class="site">
  <div class="wrap-wide">
    <a class="brand" href="{root}index.html">
      <svg class="mark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 15 Q7 6 12 15 T21 12" stroke="#6e2a33" stroke-width="1.8" stroke-linecap="round"/>
      </svg>
      프로이트 꿈해몽
    </a>
    <nav class="site-nav">
      <a href="{root}index.html"{cls('home')}>해몽 검색</a>
      <a href="{root}symbols.html"{cls('symbols')}>전체 목록</a>
      <a href="{root}diary.html"{cls('diary')}>꿈 일기</a>
      <a href="{root}theory/index.html"{cls('theory')}>이론 노트</a>
    </nav>
  </div>
</header>'''

AD_SLOT_TMPL = '''<div class="wrap">
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
</div>'''

header_re = re.compile(r'<header class="site">.*?</header>', re.DOTALL)
adslot_re = re.compile(r'<div class="wrap">\s*<div class="ad-slot".*?</div>\s*</div>', re.DOTALL)
footer_open_re = re.compile(r'<footer class="site">')
brand_copy_re = re.compile(r'프로이트 꿈 일기')
cookie_script_re = re.compile(r'<script src="[./a-z]*assets/cookie-consent\.js"></script>\s*')

for path, cfg in FILES.items():
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # 1) header/nav 교체
    content = header_re.sub(nav_html(cfg["root"], cfg["active"]), content, count=1)

    # 2) 브랜드/카피라이트 텍스트 통일
    content = brand_copy_re.sub("프로이트 꿈해몽", content)

    # 3) 기존 위치의 광고 슬롯 제거 (중복 스크립트 방지 위해 먼저 전부 제거)
    content = adslot_re.sub("", content)

    # 4) 기존 쿠키 배너 스크립트 태그 제거 (중복 방지, 아래서 footer 앞에 새로 삽입)
    content = cookie_script_re.sub("", content)

    # 5) footer 바로 앞에 광고 슬롯 1개 + footer 뒤에 쿠키 스크립트 삽입
    content = footer_open_re.sub(AD_SLOT_TMPL + "\n\n" + '<footer class="site">', content, count=1)
    content = content.replace(
        "</footer>",
        f'</footer>\n\n<script src="{cfg["root"]}assets/cookie-consent.js"></script>',
        1
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("patched", len(FILES), "files")
