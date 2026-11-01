#!/usr/bin/env python3
"""AOI regression suite: stdlib-only, read-only, offline. No invented well data."""
import csv, json, re, sys
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
errors=[]; warnings=[]; checks=0
def test(ok,label,warning=False):
    global checks
    checks+=1
    if not ok: (warnings if warning else errors).append(label)
    print(("PASS" if ok else "WARN" if warning else "FAIL")+" "+label)
class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=set();self.duplicate_ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:self.duplicate_ids.add(a["id"])
            self.ids.add(a["id"])
        if tag in ("a","script","link") and (a.get("href") or a.get("src")):
            self.links.append(a.get("href") or a.get("src"))
files=sorted(ROOT.glob("*.html"))
test(len(files)>=12,"Módulos HTML presentes (mínimo 12)")
for name in ["index.html","mapa-pozos.html","pozo-promedio-vaca-muerta.html","tortas-importacion-productos.html","panel-ejecutivo.html","buscador-quimico.html","metodologia.html"]:
    test((ROOT/name).is_file(),f"Página obligatoria: {name}")
for f in files:
    parser=Links()
    try: parser.feed(f.read_text(encoding="utf-8"))
    except Exception as exc: test(False,f"HTML legible: {f.name}: {exc}");continue
    for target in parser.links:
        if target.startswith(("https:","http:","mailto:","tel:","javascript:","data:","//")): continue
        short=target.split("?")[0].split("#")[0]
        if not short: continue
        p=(f.parent/short.lstrip("/")) if not short.startswith("/") else ROOT/short.lstrip("/")
        test(p.is_file(),f"Enlace local: {f.name} -> {short}")
    test(not parser.duplicate_ids,f"IDs únicos: {f.name}"+(f" ({sorted(parser.duplicate_ids)})" if parser.duplicate_ids else ""),warning=True)
for path in ["data/datos.json","data/productos-quimicos.json","data/diccionario.json"]:
    test((ROOT/path).exists(),f"Archivo de referencia: {path}")
data=json.loads((ROOT/"data/datos.json").read_text(encoding="utf-8"))
rows=data["registros"]
test(len(rows)>0,"Hay movimientos aduaneros")
required=["producto","mes","empresa","ncm","pais","toneladas","fob","cif","identificador"]
for k in required:test(all(k in x for x in rows),f"Campo documentado: {k}")
test(all(re.fullmatch(r"20\d{2}-\d{2}",r["mes"] or "") for r in rows),"Formato de período AAAA-MM")
test(all(isinstance(r["toneladas"],(float,int)) and r["toneladas"]>=0 for r in rows),"Toneladas válidas y no negativas")
test(all(isinstance(r["fob"],(float,int)) and r["fob"]>=0 for r in rows),"FOB válido y no negativo")
test(all(len(re.sub(r"\D","",r["ncm"]))>=6 for r in rows),"NCM compatible con HS6")
test(all(not any(k in r for k in ["exportador","vendedor_extranjero","proveedor_extranjero"]) for r in rows),"No atribución falsa de exportadores")
byprod=defaultdict(float);bymonth=defaultdict(float)
for r in rows:
    byprod[r["producto"]]+=r["toneladas"];bymonth[r["mes"]]+=r["toneladas"]
total=sum(r["toneladas"] for r in rows)
test(abs(sum(byprod.values())-total)<1e-6,"Reconciliación toneladas por producto")
test(abs(sum(bymonth.values())-total)<1e-6,"Reconciliación toneladas por mes")
test(abs(sum(v/total*100 for v in byprod.values())-100)<1e-8,"La torta de productos suma 100%")
catalog=json.loads((ROOT/"data/productos-quimicos.json").read_text(encoding="utf-8"))
catalog_names={x["producto"] for x in catalog}
test({r["producto"] for r in rows}.issubset(catalog_names),"Todos los productos importados están en el catálogo")
test("tortas-importacion-productos.html" in (ROOT/"index.html").read_text(),"Torta enlazada desde portada")
test('aoi-pie-nav-button' in (ROOT/"index.html").read_text(),"Botón de tortas en navegación visible")
test("pozo-promedio-vaca-muerta.html" in (ROOT/"index.html").read_text(),"Pozo interactivo enlazado desde portada")
test("data/pozos-oficiales.csv" in (ROOT/"mapa-pozos.html").read_text(),"Mapa intenta cargar padrón geográfico")
test((ROOT/"data/pozos-oficiales.csv").exists(),"Padrón oficial de pozos publicado",warning=True)
print(f"\nRESULTADO: {checks} controles; {len(errors)} fallos; {len(warnings)} advertencias")
for x in errors:print("ERROR:",x)
for x in warnings:print("PENDIENTE:",x)
sys.exit(1 if errors else 0)
