# Bitácora y auditoría de implementación — Argentina Oilfield Intelligence

**Corte de revisión:** 31 de octubre de 2026.  
**Repositorio:** [argentina-oilfield-intelligence](https://github.com/diegoalonsok-png/argentina-oilfield-intelligence)  
**Sitio:** [GitHub Pages](https://diegoalonsok-png.github.io/argentina-oilfield-intelligence/)  
**Criterio:** **Implementado** = código/archivo presente en el repositorio; **Parcial** = interfaz o código presente, pero falta datos, automatización o prueba funcional; **Pendiente** = no hay evidencia de implementación completa. Que un archivo exista **no acredita** que el botón o la integración funcione en el navegador.

## Resultado ejecutivo

- ✅ **846 registros reales** (planillas aportadas), enero–agosto de 2026: `datos.json` y `data/datos.json` existen, con la misma estructura y recuento. No prueban consumo final de la industria.
- ✅ **Separación de ejemplos:** `data/datos-ejemplo-consumo.json` contiene cuatro movimientos ilustrativos de 2024; no integrarlos al histórico real.
- ✅ **Catálogo y mapeo recibido:** `data/productos-quimicos-argentina.json` (30 entradas) y `data/empresas-mapeo.json` (15 grupos). Las cifras anuales indicadas como consumo no están verificadas de forma independiente.
- ⚠️ **Mapa nacional:** la página y el importador están escritos, **pero `data/pozos-oficiales.csv` y `data/pozos-origen.json` no existen al corte**. El mapa vacío del usuario es una falla real de entrega; no anunciar como poblado.
- ⚠️ **ARCA:** `estado_datos.json` indica expresamente `arca_integrado: false`. El módulo de consulta/carga manual no equivale a ingestión automática.
- ⚠️ **Pruebas integrales:** se ha comprobado sintaxis de scripts durante modificaciones, pero no existe acta de pruebas completa de navegador, enlaces, filtros, formatos, CORS, formularios y flujos PDF/correo.

## Registro de propuestas y estado verificable

| ID | Propuesta solicitada | Estado | Evidencia / limitación |
|---|---|---|---|
| AOI-01 | Portada académica e identidad visual institucional | ✅ Implementado en código | [index.html](index.html); falta prueba visual integral |
| AOI-02 | Carga de Excel reales y KPIs/tablas | ⚠️ Parcial | [datos.json](datos.json), [data/datos.json](data/datos.json), [index.html](index.html); datos presentes, visualización pública no certificada |
| AOI-03 | Solucionar `Cargando…` y rutas 404 | ⚠️ Parcial | Cargador con `./data/datos.json`, `./datos.json` y respaldo remoto; no hay prueba HTTP/JavaScript end-to-end que descarte errores |
| AOI-04 | Filtros producto, empresa, mes, año, origen y exportaciones | ⚠️ Parcial | Portada y [buscador-sectorial.html](buscador-sectorial.html); probar cada filtro y CSV |
| AOI-05 | Panel ejecutivo, KPIs, HHI y concentración | ⚠️ Parcial | [panel-ejecutivo.html](panel-ejecutivo.html); HHI solo de la muestra, no cuota nacional |
| AOI-06 | Tendencias, gráficos mensuales, evolución de FOB/t | ⚠️ Parcial | [buscador-sectorial.html](buscador-sectorial.html) incluye Chart.js; evolución del precio no está demostrada en todas las vistas |
| AOI-07 | Corregir gráfico que crece/desborda | ⚠️ Parcial | Hay CSS de contenedor y actualización Chart.js; prueba de casos de un mes/cambio de fuente todavía pendiente |
| AOI-08 | Ordenar todas las tablas al tocar encabezados | ⚠️ Parcial | Script de ordenamiento en portada, buscador y radar; inspeccionar compatibilidad con encabezados propios y modales |
| AOI-09 | Fichas de empresas con importaciones, vínculos y contactos | ⚠️ Parcial | [empresas_verificadas.json](empresas_verificadas.json) contiene 203 entradas; solo una minoría tiene identificación fiscal; LinkedIn y cambios societarios deben verificarse caso por caso |
| AOI-10 | Fichas de producto con meses, NCM/CAS, usos y participaciones | ⚠️ Parcial | Ficha emergente en [index.html](index.html), [catálogo](catalogo-quimico.html), [catálogo aportado](data/productos-quimicos-argentina.json); no tratar usos potenciales como prueba de destino |
| AOI-11 | Enviar por correo cuadros, fichas y tablas | ⚠️ Parcial | Botones `mailto:` en fichas de la portada; abren aplicación de correo, no remiten automáticamente ni adjuntan PDF |
| AOI-12 | Enlaces de filtros compartibles y modo oscuro | ⚠️ Parcial | Controles en [panel-ejecutivo.html](panel-ejecutivo.html), URL compartible en buscador; no aplicado uniformemente a todas las páginas |
| AOI-13 | Homologación empresas y aliases | ⚠️ Parcial | [data/empresas-mapeo.json](data/empresas-mapeo.json) recoge 15 grupos; coincidencia textual conservadora, no hay desambiguación validada de los 203 CUIT |
| AOI-14 | Radar comercial: nuevas firmas/productos y cambio mensual | ⚠️ Parcial | [radar-comercial.html](radar-comercial.html); alertas dentro del período de muestra, no inicio real de operaciones |
| AOI-15 | Glosario y metodología con fuentes/trazabilidad | ✅ Implementado en código | [metodologia.html](metodologia.html) y [panel-ejecutivo.html](panel-ejecutivo.html) |
| AOI-16 | ARCA separado; descarga y carga mensual automatizada | ❌ Pendiente | [arca.html](arca.html), [actualizaciones-mensuales.html](actualizaciones-mensuales.html), [estado_datos.json](estado_datos.json): todavía no ingesta oficial al histórico |
| AOI-17 | Seguimiento de versiones, archivos y cambios | ⚠️ Parcial | [CHANGELOG_DATOS.md](CHANGELOG_DATOS.md), [estado_datos.json](estado_datos.json); metadatos SHA-256 por paquete mensual no acreditados |
| AOI-18 | Mapa geográfico interactivo con filtro operadora/provincia/año | ⚠️ Parcial | [mapa-pozos.html](mapa-pozos.html) usa Leaflet; mapa sin pozos reales precargados |
| AOI-19 | Carga mensual de padrón de pozos oficial | ❌ No operativa al corte | Existen [script](scripts/actualizar_pozos.py) y [workflow](.github/workflows/actualizar-pozos.yml), pero **no** existe `data/pozos-oficiales.csv`: revisar ejecución, URL oficial y esquema; comprobar origen y geodesia antes de publicar |
| AOI-20 | Producción mensual/anual real por pozo y empresa | ⚠️ Parcial | Panel y sumas en mapa solo funcionan al cargar CSV compatible; no hay serie de producción poblada ni unión oficial con padrón |
| AOI-21 | Adjunto IV: etapas de fractura, arena y agua por pozo | ❌ Pendiente | Enlaces y documentación presentes, sin unificación estructurada pozo-mes ni capa cartográfica cargada |
| AOI-22 | Cruce importaciones ↔ pozos/fracturas | ❌ Pendiente | Únicamente comparación contextual nacional. No atribuir importaciones a un pozo u operadora por coincidencia |
| AOI-23 | Modelo de demanda de químicos por etapa | ❌ Pendiente | Requiere coeficientes técnicos documentados, incertidumbre y series compatibles |
| AOI-24 | Sankey/mapa de rutas país → empresa → producto | ❌ Pendiente | Existen barras de orígenes en buscador; Sankey y mapa de orígenes no implementados |
| AOI-25 | Informe ejecutivo PDF y exportación profesional | ⚠️ Parcial | Impresión del navegador y CSV; no generador PDF editorial con portada/fuente y gráficos certificado |
| AOI-26 | Tests automáticos de enlaces, botones y regresiones | ❌ Pendiente | No se identificó una suite integral verificada durante esta auditoría |
| AOI-27 | Actualización verificable y sello de fecha/fuente | ⚠️ Parcial | Documentación y estado de fuentes presentes; falta publicar controles de ingesta que garanticen vigencia |

## Fallas críticas y tareas en orden

1. **P0 — Mapa vacío:** conseguir y validar CSV oficial georreferenciado; resolver errores de descarga/esquema; publicar `data/pozos-oficiales.csv` y metadatos; luego comprobar puntos, filtros, unidades y rendimiento.
2. **P0 — Pruebas en navegador real:** abrir portada, buscador, radar, panel, fichas y mapa; confirmar que los datos cargan sin errores de consola, todos los botones funcionan y las URLs no dan 404.
3. **P1 — Corregir trazabilidad de producción:** separar padrón de coordenadas de series mensuales de producción; unir solo con identificador inequívoco y controlar registros duplicados.
4. **P1 — Homologación de los 203 importadores:** documentar CUIT, alias, fuente y fecha; no vincular razones sociales por parecido.
5. **P1 — Ingestión ARCA mensual:** validar un archivo oficial real antes de automatizar; mantener historia ARCA y Excel separada y calcular hashes.
6. **P2 — Reportes ejecutivos, mapas de origen, comparaciones con fracturas y modelos de demanda**, con fuentes y supuestos explícitos.

## Protocolo para nuevas tareas

Cada pedido debería registrarse con ID, fecha, requisito, prioridad, archivos modificados, commit, prueba estática, prueba visual, estado, fuente de datos, limitaciones y siguiente acción. Solo cambiar a **✅ Verificado** si existe evidencia de una prueba funcional; de lo contrario, dejar **⚠️ Parcial** aunque el código esté en GitHub.

**Regla editorial:** importaciones registradas ≠ consumo nacional ≠ consumo en pozo. Cuota observada en la muestra ≠ participación del mercado total. Cualquier afirmación de comprador final o proveedor requiere fuente comercial verificable.

## Actualización 31/10/2026 — Tema claro/oscuro unificado

- ✅ Añadido botón **Modo oscuro / Modo claro** a las 10 páginas HTML públicas confirmadas: `index.html`, `panel-ejecutivo.html`, `buscador-sectorial.html`, `radar-comercial.html`, `mapa-pozos.html`, `arca.html`, `metodologia.html`, `actualizaciones-mensuales.html`, `catalogo-quimico.html`, `productos.html`.
- ✅ La preferencia queda en `localStorage` mediante `aoi-theme` y se refleja en todas esas páginas; en el panel ejecutivo se conserva compatibilidad con `aoi-executive-dark`.
- ✅ Comprobación de sintaxis de los scripts tras cada cambio y confirmación de commits GitHub.
- ⚠️ Pendiente **certificación visual responsive** de contraste en tablas, modales, mapas y dispositivos móviles. No debe declararse completamente verificado antes de esa prueba.
- ⚠️ Sigue **sin existir** `data/pozos-oficiales.csv`; el workflow creado no equivale a datos poblados. El mapa geográfico nacional permanece en estado parcial hasta comprobar descarga y publicación.
- ⚠️ ARCA continúa `arca_integrado: false`: sin ingesta automática probada.
