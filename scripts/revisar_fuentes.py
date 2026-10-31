import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCES = {
    "ARCA - Información agregada de comercio exterior":
        "https://www.arca.gob.ar/operadoresComercioExterior/informacionAgregada/",
    "Datos abiertos - Ministerio de Economía":
        "https://datos.gob.ar/"
}
results = {}
for name, url in SOURCES.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AOI-monitor/1.0 (GitHub Pages research portal)"})
        with urllib.request.urlopen(req, timeout=20) as response:
            results[name] = {"url": url, "http_status": response.status, "accesible": 200 <= response.status < 400}
    except Exception as exc:
        results[name] = {"url": url, "accesible": False, "error": type(exc).__name__}
today = datetime.now(timezone.utc).isoformat(timespec="seconds")
payload = {
    "ultima_comprobacion_utc": today,
    "tipo": "Monitoreo de accesibilidad de fuentes; no descarga ni integra nuevas operaciones",
    "fuentes": results,
    "nota": "Los 846 registros de los Excel y sus fechas no se modifican. Una respuesta HTTP correcta no significa que ARCA haya publicado datos nuevos."
}
Path("estado_fuentes.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False))
