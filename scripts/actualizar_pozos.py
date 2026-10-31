#!/usr/bin/env python3
"""Descarga padrón geográfico oficial Capítulo IV, sin inventar geolocalizaciones."""
import csv, io, json, os, sys, urllib.request, datetime
from pathlib import Path

URL = "https://datos.energia.gob.ar/dataset/c846e79c-026c-4040-897f-1ad3543b407c/resource/cb5c0f04-7835-45cd-b982-3e25ca7d7751/download/capitulo-iv-pozos.csv"
root = Path(__file__).resolve().parents[1]
req = urllib.request.Request(URL,headers={"User-Agent":"ArgentinaOilfieldIntelligence/1.0 academic data importer"})
with urllib.request.urlopen(req,timeout=100) as res:
    raw=res.read()
if len(raw)<200: raise RuntimeError("Archivo oficial vacío")
txt=raw.decode("utf-8-sig",errors="replace")
dialect=csv.Sniffer().sniff(txt[:10000],delimiters=",;\t")
reader=csv.DictReader(io.StringIO(txt),dialect=dialect)
header={h.lower().strip():h for h in (reader.fieldnames or [])}
def field(row,*names):
    for name in names:
        if name in header: return row.get(header[name],"")
    return ""
if "coordenadax" not in header or "coordenaday" not in header:
    raise RuntimeError("Esquema del archivo cambió: faltan coordenadax y coordenaday")
dst=root/"data"/"pozos-oficiales.csv"
dst.parent.mkdir(parents=True,exist_ok=True)
n=0
with dst.open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["idpozo","sigla","empresa","provincia","tipo_recurso","coordenadax","coordenaday"])
    for row in reader:
        try:
            x=float(field(row,"coordenadax").replace(",","."))
            y=float(field(row,"coordenaday").replace(",","."))
            # En cartografía X suele ser longitud e Y latitud; validar rangos
            # en lugar de asumir el orden del origen.
            if -74 <= x <= -53 and -57 <= y <= -21:
                lon,lat=x,y
            elif -74 <= y <= -53 and -57 <= x <= -21:
                lon,lat=y,x
            else:
                continue
        except ValueError: continue
        if not (-57<=lat<=-21 and -74<=lon<=-53):continue
        w.writerow([field(row,"idpozo"),field(row,"sigla"),field(row,"empresa","empresa_informante"),field(row,"provincia"),field(row,"tipo_recurso"),lat,lon])
        n+=1
if n<100: raise RuntimeError(f"Solo {n} pozos válidos: revisar esquema antes de publicar")
(root/"data"/"pozos-origen.json").write_text(json.dumps({"fuente":URL,"fecha_descarga_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"filas_geolocalizadas":n,"advertencia":"Padrón geográfico: no contiene necesariamente producción por mes ni consumo de químicos."},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"{n} pozos geolocalizados publicados")
