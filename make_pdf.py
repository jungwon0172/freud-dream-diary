# -*- coding: utf-8 -*-
"""꿈 해몽 기록지 (인쇄용) PDF 생성"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

# 나눔 폰트(순수 TrueType, glyf 외곽선)를 실제로 임베드
# 주의: Noto CJK .ttc는 CFF(PostScript) 외곽선이라 reportlab TTFont가 읽지 못함
pdfmetrics.registerFont(TTFont('NotoSerifKR', '/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf'))
pdfmetrics.registerFont(TTFont('NotoSansKR', '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'))

FONT_SERIF = 'NotoSerifKR'
FONT_SANS = 'NotoSansKR'
INK = (0.137, 0.129, 0.114)      # #23211d
WINE = (0.431, 0.165, 0.200)     # #6e2a33
LINE = (0.6, 0.58, 0.5)

W, H = A4
MARGIN = 20 * mm

c = canvas.Canvas("assets/dream-record-sheet.pdf", pagesize=A4)

def dotted_line(x1, x2, y):
    c.setDash(1, 2)
    c.setStrokeColorRGB(*LINE)
    c.setLineWidth(0.6)
    c.line(x1, y, x2, y)
    c.setDash()

def label(text, x, y, size=9, color=WINE, font=FONT_SANS):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    c.drawString(x, y, text)

# ---------- 헤더 ----------
c.setFillColorRGB(*INK)
c.setFont(FONT_SERIF, 20)
c.drawString(MARGIN, H - 26*mm, "꿈 해몽 기록지")

c.setFont(FONT_SANS, 9.5)
c.setFillColorRGB(*WINE)
c.drawString(MARGIN, H - 32*mm, "FREUD DREAM JOURNAL — 프로이트 꿈해몽")

c.setStrokeColorRGB(*WINE)
c.setLineWidth(1.1)
c.line(MARGIN, H - 35*mm, W - MARGIN, H - 35*mm)

y = H - 44*mm

# ---------- 날짜 / 감정 ----------
label("날짜", MARGIN, y)
dotted_line(MARGIN + 14*mm, MARGIN + 60*mm, y - 1*mm)
label("깨어났을 때 느낀 감정", MARGIN + 68*mm, y)
dotted_line(MARGIN + 68*mm + 40*mm, W - MARGIN, y - 1*mm)

y -= 12*mm

# ---------- 꿈의 내용 ----------
label("꿈의 내용 (기억나는 대로, 순서 상관없이)", MARGIN, y)
y -= 6*mm
for i in range(6):
    dotted_line(MARGIN, W - MARGIN, y)
    y -= 7*mm

y -= 3*mm

# ---------- 등장 요소 체크박스 ----------
label("등장 요소", MARGIN, y)
y -= 7*mm
tags = ["아는 사람", "낯선 사람", "가족", "어린 시절 장소", "추락 · 쫓김", "시험 · 과제", "반복되는 꿈", "죽음 · 이별"]
box = 4*mm
col_w = (W - 2*MARGIN) / 4
for i, tag in enumerate(tags):
    col = i % 4
    row = i // 4
    bx = MARGIN + col * col_w
    by = y - row * 9*mm
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(0.7)
    c.rect(bx, by - box + 1.5*mm, box, box, stroke=1, fill=0)
    c.setFont(FONT_SANS, 8.7)
    c.setFillColorRGB(*INK)
    c.drawString(bx + box + 2*mm, by - box + 2.4*mm, tag)

y -= 22*mm

# ---------- 프로이트식 질문 ----------
c.setFont(FONT_SERIF, 12.5)
c.setFillColorRGB(*INK)
c.drawString(MARGIN, y, "프로이트식 자기분석 질문")
y -= 9*mm

questions = [
    ("압축", "여러 사람, 장소, 기억이 하나로 뒤섞인 장면이 있었나요?"),
    ("전치", "사소해 보였지만 이상하게 강렬한 감정이 실렸던 대상이 있나요?"),
    ("낮의 잔재", "어제 실제로 겪은 일 중 이 꿈의 재료가 되었을 장면은?"),
]
for concept, q in questions:
    label(f"[{concept}]", MARGIN, y, size=9, color=WINE, font=FONT_SANS)
    c.setFont(FONT_SANS, 9.3)
    c.setFillColorRGB(*INK)
    c.drawString(MARGIN + 20*mm, y, q)
    y -= 6*mm
    dotted_line(MARGIN, W - MARGIN, y)
    y -= 6.5*mm
    dotted_line(MARGIN, W - MARGIN, y)
    y -= 10*mm

# ---------- 해석 메모 ----------
label("오늘의 해몽 메모 (전통 해몽 / 나의 생각)", MARGIN, y)
y -= 6*mm
for i in range(4):
    dotted_line(MARGIN, W - MARGIN, y)
    y -= 7*mm

# ---------- 푸터 ----------
c.setFont(FONT_SANS, 7.5)
c.setFillColorRGB(*LINE)
c.drawCentredString(W/2, 14*mm, "freud-dream-diary  ·  이 기록지는 개인 자기성찰 및 기록 목적의 서식입니다. 의학적 진단을 대체하지 않습니다.")

c.showPage()
c.save()
print("PDF 생성 완료: assets/dream-record-sheet.pdf")
