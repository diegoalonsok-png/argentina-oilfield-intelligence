#!/usr/bin/env python3
"""Descarga padrón geográfico oficial Capítulo IV, sin inventar geolocalizaciones."""
import csv, io, json, os, sys, urllib.request, datetime, tempfile, hashlib
from pathlib import Path

URL = "https://datos.energia.gob.ar/dataset/c846e79c-026c-4040-897f-1ad3543b407c/resource/cb5c0f04-7835-45cd-b982-3e25ca7d7751/download/capitulo-iv-pozos.csv"
root = Path(__file__).resolve().parents[1]
# Resolver URL por el catálogo oficial antes de usar la copia histórica.
# El sitio puede cambiar las rutas directas manteniendo el identificador de recurso.
CATALOG = "https://datos.gob.ar/api/3/action/package_show?id=energia-produccion-petroleo-gas-por-pozo-capitulo-iv"
urls = []
try:
    req = urllib.request.Request(CATALOG, headers={"User-Agent": "ArgentinaOilfieldIntelligence/1.0"})
    with urllib.request.urlopen(req, timeout=40) as response:
        package = json.load(response)["result"]
    for resource in package.get("resources", []):
        title = str(resource.get("name", "")).lower().strip()
        fmt = str(resource.get("format", "")).lower().strip()
        target = resource.get("url", "")
        if "capítulo iv - pozos" in title or "capitulo iv - pozos" in title:
            if fmt == "csv" and target.startswith("https://"):
                urls.append(target)
except Exception as exc:
    print("Aviso: catálogo oficial no disponible:", exc, file=sys.stderr)
urls.append(URL)
raw = None
resolved_url = None
errors = []
for candidate in dict.fromkeys(urls):
    try:
        req = urllib.request.Request(candidate, headers={"User-Agent": "ArgentinaOilfieldIntelligence/1.0 academic data importer"})
        with urllib.request.urlopen(req, timeout=100) as res:
            data = res.read()
        if len(data) < 200:
            raise ValueError("Archivo demasiado pequeño")
        raw = data
        resolved_url = candidate
        break
    except Exception as exc:
        errors.append(str(exc))
if raw is None:
    raise RuntimeError("No fue posible descargar el padrón: " + " | ".join(errors))
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
        w.writerow([field(row,"idpozo"),field(row,"sigla"),field(row,"empresa","empresa_informante"),field(row,"provincia"),field(row,"tipo_recurso"),lon,lat])
        n+=1
if n<100:
    dst.unlink(missing_ok=True)
    raise RuntimeError(f"Solo {n} pozos válidos: revisar esquema antes de publicar")
(root/"data"/"pozos-origen.json").write_text(json.dumps({"fuente":resolved_url,"fecha_descarga_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"filas_geolocalizadas":n,"sha256_archivo_original":hashlib.sha256(raw).hexdigest(),"orden_coordenadas_publicado":"coordenadax=longitud, coordenaday=latitud","advertencia":"Padrón geográfico: no contiene necesariamente producción por mes ni consumo de químicos."},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"{n} pozos geolocalizados publicados")
