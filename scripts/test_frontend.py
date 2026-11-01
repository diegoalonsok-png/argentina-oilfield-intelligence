#!/usr/bin/env python3
"""Validación estática sin dependencias: scripts JS incrustados y rutas locales HTML."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent
class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.scripts=[];self.links=[];self.capture=False;self.parts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="script" and not a.get("src") and (not a.get("type") or a.get("type") in ("text/javascript","module")):
            self.capture=True;self.parts=[]
        if tag in ("a","link","script","img"):
            attr={"a":"href","link":"href","script":"src","img":"src"}[tag]
            if a.get(attr):self.links.append((tag,a[attr]))
    def handle_data(self,data):
        if self.capture:self.parts.append(data)
    def handle_endtag(self,tag):
        if tag=="script" and self.capture:
            self.scripts.append("".join(self.parts));self.capture=False
def main():
    problems=[];checked=0
    for page in sorted(ROOT.glob("*.html")):
        doc=Document();doc.feed(page.read_text(encoding="utf-8"))
        for n,js in enumerate(doc.scripts,1):
            if not js.strip():continue
            p=subprocess.run(["node","--check","-"],input=js,text=True,capture_output=True)
            checked+=1
            if p.returncode:problems.append(f"{page.name}: script {n}: {p.stderr.strip()[:500]}")
        for tag,raw in doc.links:
            if raw.startswith(("https:","http:","mailto:","tel:","javascript:","data:","#","//")):continue
            url=urlsplit(raw).path
            if not url or "{" in url or "<" in url:continue
            target=(ROOT / unquote(url.lstrip("/"))).resolve()
            if not target.is_relative_to(ROOT):continue
            if not target.exists():problems.append(f"{page.name}: {tag} apunta a archivo ausente: {raw}")
    print(f"HTML: {len(list(ROOT.glob('*.html')))} páginas; JavaScript: {checked} bloques comprobados")
    if problems:
        print("\n".join(problems[:60]));sys.exit(1)
    print("PASS: sin errores sintácticos JS ni archivos locales faltantes")
if __name__=="__main__": main()
