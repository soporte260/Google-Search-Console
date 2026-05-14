# `audit/data/` — Datos extraídos para ejecución

CSVs derivados de los Excel de Google Search Console y del feed TSV, con la información necesaria para ejecutar las acciones del plan.

## Inventario

### Indexación / cobertura

| Archivo | Filas | Origen | Uso (acción del plan) |
|---|---|---|---|
| `404-urls-reales.csv` | 530 | GSC drilldown "No se ha encontrado (404)" filtrado a URLs sin parámetros | P11 — redirigir o asumir 404 |
| `404-urls-parametros.csv` | 470 | Mismo drilldown, URLs con params (`_pos`, `_fid`, `_ss`, etc.) | P15 / análisis filtros |
| `duplicadas-google-canonica.csv` | 410 | GSC "Duplicada: Google ha elegido una versión canónica diferente a la del usuario" | P7 — traducir contenido DE/FR |
| `descubiertas-sin-indexar.csv` | 356 | GSC "Descubierta, actualmente sin indexar" — TODAS | P13 — analizar |
| `rastreadas-sin-indexar.csv` | 1.000 | GSC "Rastreada, actualmente sin indexar" — muestra de 19.715 reales | P13 — analizar |

### Performance / oportunidades

| Archivo | Filas | Origen | Uso (acción del plan) |
|---|---|---|---|
| `consultas-oportunidad-cero-clics.csv` | 94 | GSC Consultas ≥100 impresiones y ≤1 clic | P6 + P10 — landings nuevas/optimización |
| `consultas-buena-posicion-bajo-ctr.csv` | 45 | GSC Consultas en top10 con CTR <3 % | Optimización de título/meta |
| `paginas-top-rendimiento.csv` | 120 | GSC Páginas con ≥5 clics | Priorización |
| `paginas-oportunidad-ctr.csv` | 103 | GSC Páginas con ≥200 impresiones y CTR <2 % | P7 + Optimización |

### Catálogo / feed Merchant

| Archivo | Filas | Origen | Uso (acción del plan) |
|---|---|---|---|
| `productos-sin-gtin.csv` | 260 | TSV productos | Revisar packs / añadir `identifier_exists: no` |
| `productos-sin-estado.csv` | 299 | TSV productos | P12 — bulk update |
| `productos-sin-disponibilidad.csv` | 320 | TSV productos | P12 — bulk update |
| `productos-agotados.csv` | 265 | TSV productos | Decisión: aviso / 301 / mantener |
| `productos-sin-categoria-google.csv` | 1.381 | TSV productos | P9 — asignación masiva |

## Re-generar los CSV

Los scripts Python originales viven en `/tmp/` durante una sesión de Claude Code. Si necesitas re-generar con un nuevo export de GSC, los pasos son:

1. Sustituir los `.xlsx` en la raíz del repo con los nuevos.
2. Re-ejecutar:
   ```bash
   python3 /tmp/export_data.py
   ```
   (script versionable en un commit futuro si se quiere automatizar).

## Notas sobre límites de GSC

- GSC exporta máximo **1.000 URLs por drilldown**. Cuando un motivo tiene >1.000 URLs (Rastreada sin indexar 19.715, Bloqueada robots.txt 29.136, etc.), sólo tenemos muestra.
- Para análisis completo recomendado: usar la API de GSC o herramientas tipo Screaming Frog para crawl completo.
