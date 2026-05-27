# CLAUDE.md — Google Search Console · evacaravan.com

## Contexto del proyecto

Repositorio de auditoría SEO basada en datos exportados de Google Search Console (GSC) para **evacaravan.com** (tienda Shopify de accesorios para caravanas y autocaravanas).

- **Fecha de los datos**: 14 mayo 2026
- **Período GSC analizado**: Últimos 3 meses (Feb–May 2026)
- **Issues GitHub**: 23 issues numerados [P1]–[P22] + [EXTRA]

## Estructura del repositorio

```
/                          ← Exportaciones GSC (.xlsx) + datos producto (.tsv)
audit/
  03-performance-search.md  ← Análisis de rendimiento en búsqueda
  05-tecnico.md             ← Auditoría técnica SEO
  data/
    404-urls-reales.csv              ← 1000 URLs en 404 (con y sin parámetros)
    404-urls-sin-parametros.csv      ← 530 URLs 404 reales (sin params)
    duplicadas-google-canonica.csv   ← 410 URLs con canónica ignorada por Google
    rastreadas-sin-indexar.csv       ← 1000 URLs rastreadas sin indexar
    descubiertas-sin-indexar.csv     ← 356 URLs descubiertas sin indexar
    paginas-top-rendimiento.csv      ← 1000 páginas con más tráfico
    paginas-oportunidad-ctr.csv      ← 133 páginas con CTR mejorable
    consultas-oportunidad-cero-clics.csv ← 77 consultas con impr y 0 clics
```

## Issues por prioridad

### 🟥 CRÍTICO (resolver primero)
- **[P1]** #1 — Fix `author` en Review snippets (7 productos) — 30 min
- **[P2]** #2 — Resolver duplicación HTTP/www vs HTTPS en home — 30 min ✅ *documentado en audit/05-tecnico.md §5.1*
- **[P3]** #3 — Limpiar 24 URLs en 404 del sitemap.xml — 1-2h
- **[P4]** #4 — Eliminar 7 combinaciones hreflang fantasma (178 URLs 404) — 2-4h

### 🟧 ALTA prioridad
- **[P5]** #5 — Añadir `hasMerchantReturnPolicy` + `shippingDetails` (110 productos) — 1-2h
- **[P6]** #6 — Crear landing "Cerraduras para furgonetas" (>11.500 impr sin capturar) — 4-8h
- **[P7]** #7 — Traducir 410 páginas DE/FR (canonical ignorada por Google) — semanas
- **[P8]** #8 — Instalar app reviews + emails post-venta (aggregateRating) — 2-3 días
- **[P9]** #9 — Asignar categoría Google product a 1.381 productos — 1-2 días

### 🟨 MEDIA prioridad
- **[P10]** #10 — Optimizar 5 colecciones con más impresiones y bajo CTR
- **[P11]** #11 — Redirigir 530 URLs 404 reales a páginas existentes
- **[P12]** #12 — Corregir 320 productos sin disponibilidad + 299 sin estado
- **[P13]** #13 — Auditar 2.468 URLs del sitemap rastreadas sin indexar
- **[P14]** #14 — Añadir `priceValidUntil` en schema (53 productos)
- **[P15]** #15 — Bloquear endpoints AJAX en robots.txt
- **[P16]** #16 — Noindex feeds .atom (26 URLs duplicadas)
- **[P17]** #17 — Auditar dominio localitybiz.es (200 backlinks)
- **[P18]** #18 — Solicitar backlinks a fabricantes del catálogo

### 🟩 BAJA prioridad (largo plazo)
- **[P19]** #19 — Estrategia blog: guías técnicas
- **[P20]** #20 — Schema `ItemList` en colecciones
- **[P21]** #21 — Migrar facetas a nofollow/JS (29.136 URLs bloqueadas)
- **[P22]** #22 — Construcción de backlinks editorial
- **[EXTRA]** #23 — 4 GTINs inválidos + 3 descripciones largas en Merchant listings

## Datos clave del diagnóstico

- **Páginas indexadas**: 4.059 (cayendo desde 6.740 en feb — alerta)
- **Sin indexar**: 74.320
- **404s totales**: 4.568 (incluye hreflang fantasma P4)
- **Canónica ignorada por Google**: 410 URLs (P7)
- **Crawl waste por facetas**: 29.136 URLs bloqueadas robots.txt (P21)
- **Clúster "cerradura furgoneta"**: ~11.500 impr/trim con 0 clics (P6)
- **CTR Fichas de Comerciante**: 6,10% — el tipo de resultado con mayor CTR

## Instrucciones de trabajo

Al arrancar una sesión:
1. Leer este CLAUDE.md para contexto
2. Ver el issue GitHub correspondiente a la prioridad a trabajar
3. Los datos de referencia están en `audit/data/*.csv`
4. Desarrollar en branch `claude/blissful-franklin-o3PkQ`
5. Los fixes de Shopify requieren acceso a Shopify Admin (no automatizable desde aquí)

## Fix de P2 — Estado

**Pendiente de ejecución manual en Shopify Admin.** Los pasos están documentados en `audit/05-tecnico.md §5.1`. No requiere código — solo configuración de dominio en Shopify Admin → Configuración → Dominios.
