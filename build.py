# -*- coding: utf-8 -*-
"""전체 빌드: 페이지 생성 -> GEO/SEO 패치 -> 배포용 dist/ 폴더 생성 (스크립트 제외)"""
import subprocess, sys, shutil, os, glob

for step in ("generate.py", "geo_patch.py", "seo_patch.py"):
    subprocess.run([sys.executable, step], check=True)

if os.path.isdir("dist"):
    shutil.rmtree("dist")
os.makedirs("dist")
for pat in ("*.html", "ads.txt", "robots.txt", "sitemap.xml", "llms.txt", "llms-full.txt",
            "favicon.ico", "favicon.svg", "apple-touch-icon.png"):
    for f in glob.glob(pat):
        shutil.copy(f, "dist/")
for d in ("dream", "theory", "assets", "og"):
    shutil.copytree(d, f"dist/{d}")
print("dist ready:", sum(len(fs) for _, _, fs in os.walk("dist")), "files")
