# -*- coding: utf-8 -*-
"""공통 헤더: 1행(브랜드 + 우측 소개/문의), 2행(꿈 메뉴칸)"""
CAT_IDS = [("동물","animal"),("자연/재난","nature"),("신체","body"),("관계/사람","people"),
           ("재물/행운","fortune"),("학업/일상","daily"),("초자연","supernatural"),("감정/상황","emotion")]

def render_header(root, current):
    def a(key): return ' class="active"' if key == current else ''
    cats = "\n".join(f'        <a href="{root}symbols.html#cat-{cid}">{name}</a>' for name, cid in CAT_IDS)
    return f'''<header class="site">
  <div class="wrap-wide top-row">
    <a class="brand" href="{root}index.html">
      <svg class="mark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 15 Q7 6 12 15 T21 12" stroke="#6e2a33" stroke-width="1.8" stroke-linecap="round"/>
      </svg>
      프로이트 꿈해몽
    </a>
    <nav class="util-nav" aria-label="사이트 정보">
      <a href="{root}about.html"{a('about')}>소개</a>
      <a href="{root}contact.html"{a('contact')}>문의</a>
    </nav>
  </div>
  <nav class="dream-menu" aria-label="꿈 메뉴">
    <div class="wrap-wide">
      <div class="dream-menu-scroll">
        <a href="{root}index.html"{a('home')}>해몽 검색</a>
        <a href="{root}symbols.html"{a('symbols')}>전체 목록</a>
{cats}
        <a href="{root}diary.html"{a('diary')}>꿈 일기</a>
        <a href="{root}theory/index.html"{a('theory')}>이론 노트</a>
      </div>
    </div>
  </nav>
</header>'''
