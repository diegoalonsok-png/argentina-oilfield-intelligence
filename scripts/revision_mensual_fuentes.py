#!/usr/bin/env python3
"""Monthly official source catalogue. Does not claim unverified data ingestion."""
import datetime as dt, hashlib, json, os, re, urllib.request
from html.parser import HTMLParser
from pathlib import Path

URL="https://www.arca.gob.ar/operadoresComercioExterior/informacionAgregada/"
ENERGIA="https://datos.gob.ar/ar/dataset/energia-produccion-petroleo-gas-por-pozo-capitulo-iv"
OUT=Path("data/estado-actualizacion-mensual.json")
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            d=dict(attrs); href=d.get("href","")
            if href:self.links.append(href)
def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"AOI-public-data-monitor/1.0","Accept":"text/html"})
    with urllib.request.urlopen(req,timeout=30) as r:
        data=r.read(4_000_000)
        return r.geturl(),data,r.status
def main():
    now=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    out={"verificado_utc":now,"estado":"sin_verificar","arca":{"url":URL,"datos_integrados":False},"energia":{"url":ENERGIA,"datos_integrados":False},
      "nota":"Control mensual de fuentes; no implica que el dataset curado se haya actualizado."}
    try:
        final,data,status=get(URL); p=Links();p.feed(data.decode("utf-8","replace"))
        from urllib.parse import urljoin
        links=sorted(set(urljoin(final,x) for x in p.links if re.search(r"\.(zip|csv|xlsx|xls)(\?|$)",x,re.I)))
        out["arca"].update({"http":status,"pagina_sha256":hashlib.sha256(data).hexdigest(),"archivos_detectados":links[:300],"cantidad_enlaces":len(links)})
        out["estado"]="fuente_consultada"
    except Exception as e:
        out["arca"]["error"]=str(e)[:240];out["estado"]="fuente_no_disponible"
    try:
        final,data,status=get(ENERGIA)
        out["energia"].update({"http":status,"pagina_sha256":hashlib.sha256(data).hexdigest(),"url_final":final})
    except Exception as e:out["energia"]["error"]=str(e)[:240]
    OUT.parent.mkdir(exist_ok=True)
    old=json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}
    # Persist status per execution, not unverifiable monthly import entries.
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"ARCA: {out['estado']}; discovered {out['arca'].get('cantidad_enlaces',0)} links")
    if out["estado"]=="fuente_no_disponible":
        raise SystemExit("Official download page unavailable; status recorded, no data modified.")
if __name__=="__main__":main()
