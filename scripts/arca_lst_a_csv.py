#!/usr/bin/env python3
"""AOI: conversión prudente LST delimitado a CSV; nunca modifica datos.json.
Uso: python scripts/arca_lst_a_csv.py entrada.LST salida.csv --encoding cp1252
Si el archivo tiene ancho fijo o carece de encabezados, detenerse y usar su diseño oficial.
"""
import argparse, csv, pathlib, collections, json
def main():
    p=argparse.ArgumentParser()
    p.add_argument("origen",type=pathlib.Path)
    p.add_argument("destino",type=pathlib.Path)
    p.add_argument("--encoding",default="cp1252")
    p.add_argument("--delimiter",choices=["tab","semicolon","comma","pipe"],default=None)
    args=p.parse_args()
    if args.origen.resolve()==args.destino.resolve():p.error("No sobrescribir el original")
    raw=args.origen.read_bytes()
    try: content=raw.decode(args.encoding)
    except UnicodeError as e:p.error(f"Codificación incorrecta: {e}")
    sample=content[:65536]
    table={"tab":"\t","semicolon":";","comma":",","pipe":"|"}
    if args.delimiter: sep=table[args.delimiter]
    else:
        try: sep=csv.Sniffer().sniff(sample,delimiters="\t;,|").delimiter
        except csv.Error:p.error("No se detectó delimitador: posible ancho fijo. Revisar diseño LST oficial.")
    rows=list(csv.reader(content.splitlines(),delimiter=sep))
    if len(rows)<2:p.error("No hay encabezados y registros suficientes.")
    headers=[x.strip().lstrip("\ufeff") for x in rows[0]]
    if len(headers)<3 or any(not h for h in headers):p.error("Encabezado inválido; verificar diseño del archivo.")
    sizes=collections.Counter(len(r) for r in rows[1:] if any(c.strip() for c in r))
    if set(sizes)!={len(headers)}:p.error(f"Filas inconsistentes: cabecera {len(headers)} campos; filas {dict(sizes)}.")
    if len(set(h.casefold() for h in headers))!=len(headers):p.error("Encabezados duplicados; revisar diseño.")
    args.destino.parent.mkdir(parents=True,exist_ok=True)
    with args.destino.open("w",encoding="utf-8-sig",newline="") as out:
        w=csv.writer(out,delimiter=";")
        w.writerow(headers)
        w.writerows(rows[1:])
    print(json.dumps({"archivo":args.origen.name,"registros":len(rows)-1,"campos":headers,"salida":str(args.destino),"advertencia":"Conversión estructural solamente; no valida pesos, unidades, importadores, NCM ni duplicados."},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
