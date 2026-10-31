# Argentina Oilfield Intelligence (AOI)

**Observatorio documental de importaciones argentinas de insumos químicos vinculados a la cadena energética**  
**Autor:** Diego A. Kurilo · **Dataset:** v2026.08 · **Metodología:** v1.0 · **Fecha de documentación:** 31-10-2026.

## Alcance y archivos

- `datos.json`: 846 líneas de importación seleccionadas, enero–agosto de 2026, a partir de 11 planillas XLSX suministradas.
- `index.html`: buscador exclusivo de esas planillas; `productos.html`: análisis de productos.
- `arca.html`: módulo **independiente** para explorar fuentes públicas ARCA; no integra automáticamente las operaciones al índice original.
- `metodologia.html`: metodología, criterios de inclusión, indicadores de calidad, límites y cita.
- `empresas_verificadas.json`: directorio de 203 empresas con verificación externa parcial; los campos pendientes no equivalen a valores negativos ni a falta de inscripción.

Los datos representan **importaciones declaradas**, no compras finales de operadores ni consumos atribuibles a pozos. País de origen no equivale a nombre de proveedor extranjero. Participaciones y HHI se calculan sobre el universo observado, no sobre el mercado nacional.

## Calidad y reproducibilidad

En la consolidación se reportan 15 duplicados excluidos. Las 846 filas publicadas tienen cantidad, FOB y CIF numéricos no negativos, aunque 30 registran masa cero. Se conserva el identificador de operación y el ítem, cuando existen en la fuente consolidada. Los nombres de empresas no están homologados exhaustivamente por CUIT. Para reproducir desde origen se requieren los XLSX originales, su metadato de adquisición y el proceso de extracción; el `datos.json` solo permite reproducir agregaciones **a partir de las filas publicadas**.

**Fuente externa prioritaria:** [ARCA Información Agregada de Comercio Exterior](https://www.arca.gob.ar/operadoresComercioExterior/informacionAgregada/). Los archivos ZIP/LST mensuales deben analizarse y verificarse por esquema y licencia antes de publicar sus registros. INDEC, Secretaría de Energía y Comtrade son fuentes complementarias, no sustitutos transaccionales de ARCA.

## Cita

Kurilo, Diego A. (2026). *Argentina Oilfield Intelligence: Observatorio de importaciones de insumos químicos vinculados a la cadena energética* (dataset v2026.08). https://diegoalonsok-png.github.io/argentina-oilfield-intelligence/

No se ha asignado DOI. Las licencias y derechos de redistribución deben verificarse antes de depositar los datos en Zenodo o Figshare.

## Versiones

- **Dataset v2026.08:** enero–agosto de 2026, 846 registros conservados.
- **Metodología v1.0 (2026-10-31):** documentación bilingüe y auditoría cuantitativa.
- **Sitio:** evolución continua del código; la versión del dataset no cambia con cada ajuste visual.
