# Auditoría Técnica SEO — evacaravan.com

**Fecha de datos**: 14 de mayo de 2026  
**Período analizado**: Últimos 3 meses (Feb–May 2026)

---

## 5.1 Duplicación HTTP/www vs HTTPS (P2 — ✅ VERIFICADO RESUELTO — 27 mayo 2026)

### Diagnóstico

GSC registra **dos versiones de la home** con métricas completamente separadas (datos Feb–May 2026):

| URL | Clics | Impresiones | CTR | Posición |
|-----|-------|-------------|-----|----------|
| `https://evacaravan.com/` | 406 | 4.185 | 9,70% | 25,37 |
| `http://www.evacaravan.com/` | 156 | 4.273 | 3,65% | **6,48** |
| **TOTAL POTENCIAL** | **562** | **8.458** | — | — |

La versión HTTP/www tiene **mejor posición** (6,48 vs 25,37) por backlinks históricos acumulados. Al consolidar, la versión canónica heredará toda la autoridad.

**Impacto económico estimado**: +156 clics trimestrales + mejora de posición media hacia <15.

### Verificación realizada el 27/05/2026

**Redirección** (verificada con navegador incógnito y httpstatus.io):
```
http://www.evacaravan.com/  →  301  →  https://www.evacaravan.com/  →  301  →  https://evacaravan.com/
```
✅ Cadena completa de 301 funciona correctamente. El 403 que devuelven checkers externos es falso positivo (bloqueo bot por Shopify/Cloudflare); en navegador real la cadena es correcta.

**Canonical tag** (verificado en código fuente de `https://evacaravan.com/`):
```html
<link rel="canonical" href="https://evacaravan.com/" />
```
✅ Correcto. Controlado por **Yoast SEO for Shopify** (el tema nativo tiene el canonical desactivado con `disabled_by_yoast_seo`).

**Configuración Shopify Admin → Dominios** (verificada):
- Dominio principal: `evacaravan.com` ✅
- `www.evacaravan.com` → Tipo: "Redirige a evacaravan.com" ✅
- `eva-caravan.myshopify.com` → Tipo: "Redirige a evacaravan.com" ✅
- Certificado TLS provisionado en todos los dominios ✅

### Causa raíz real

La infraestructura técnica estaba correctamente configurada. El problema era únicamente que Google tenía **indexada y en caché la URL `http://www.evacaravan.com/`** con autoridad de backlinks históricos. No se requería ningún cambio técnico.

### Único paso pendiente

**Solicitar reindexación en GSC** (acción manual, ~2 minutos):

1. Ir a GSC → Herramienta de inspección de URLs
2. Introducir `https://evacaravan.com/`
3. Clic en **"Solicitar indexación"**
4. Opcionalmente, inspeccionar también `http://www.evacaravan.com/` para ver su estado actual

### Monitorización

- **Plazo esperado**: 4–8 semanas para que Google consolide ambas URLs
- **KPI**: `http://www.evacaravan.com/` desaparece del informe de páginas en GSC
- **KPI**: Clics consolidados en `https://evacaravan.com/` superan 500/trim
- **KPI**: Posición media home mejora hacia <15 al heredar autoridad de la versión www

---

## 5.2 Resumen de problemas técnicos detectados

| Problema | URLs afectadas | Prioridad |
|----------|---------------|-----------|
| Bloqueada por robots.txt | 29.136 | P21 |
| Página alternativa con canónica adecuada | 10.501 | — (correcto) |
| Página con redirección | 8.075 | — (correcto) |
| No se ha encontrado (404) | 4.568 | P3, P4, P11 |
| Rastreada, sin indexar | 19.715 | P13 |
| Excluida por noindex | 1.464 | — (revisar) |
| Error de redirección | 42 | P4 |
| Bloqueada por 4xx | 27 | P15 |
| Duplicada sin canónica | 26 | P16 |
| Duplicada (Google eligió otra canónica) | 410 | P7 |
| Descubierta, sin indexar | 356 | P13 |

---

## 5.3 Sitemap.xml — 24 URLs con 404 (P3 — CRÍTICO)

Desde el filtro `sitemap.xml` en GSC:
- **24 URLs** del sitemap devuelven 404
- Ratio de indexación actual del sitemap: **49%** (3.090 indexadas / 6.315 enviadas)

**Acción**: cruzar con `audit/data/404-urls-sin-parametros.csv` filtrando las URLs que no tienen parámetros y están en el sitemap. Archivar productos descatalogados en Shopify (se eliminan automáticamente del sitemap) y crear 301 para los que queden.

---

## 5.4 Endpoints AJAX accesibles por Google (P15)

Google ha rastreado y reportado **27 URLs con error 4xx** que son endpoints internos de Shopify:

Muestra de URLs problemáticas:
- `https://evacaravan.com/en-eu/search/suggest`
- `https://evacaravan.com/fr-fr/search/suggest`
- `https://evacaravan.com/de-at/cart/add`

**Fix**: añadir en `config/robots.txt.liquid`:
```
Disallow: /*/search/suggest
Disallow: /*/cart/add
Disallow: /*/cart/change
Disallow: /*/cart/update
Disallow: /*/cart/clear
```

---

## 5.5 Feeds .atom indexables (P16)

**26 URLs `.atom`** sin canonical aparecen en "Duplicada: el usuario no ha indicado ninguna versión canónica":

Muestra:
- `https://evacaravan.com/collections/asa-seguridad.atom`
- `https://evacaravan.com/it-it/collections/climatizacion-frio-calefaccion-electrica.atom`
- `https://evacaravan.com/it-it/blogs/news.atom`

**Fix recomendado**: en `robots.txt.liquid`:
```
Disallow: /*.atom$
```

O añadir `X-Robots-Tag: noindex` para las respuestas `.atom`.

---

## 5.6 URLs noindex indexadas (1.464)

1.464 páginas tienen etiqueta `noindex` pero Google las ha rastreado. Muestra:
- `https://evacaravan.com/pt-pt/collections/vendors?page=1&q=Fiamma&grid_list`
- `https://evacaravan.com/de-de/collections/vendors?filter.v.availability=1&q=Milenco`
- Principalmente colecciones de vendors con filtros activos

Estas páginas tienen noindex correcto; el problema es que Google las descubre a través de enlaces HTML internos.

---

## 5.7 Tendencia de indexación (alerta)

La tendencia de páginas indexadas muestra **caída sostenida** en los últimos 3 meses:

| Fecha | Sin indexar | Indexadas |
|-------|-------------|-----------|
| 2026-02-14 | 53.433 | 6.740 |
| 2026-03-25 | 58.921 | 4.356 |
| 2026-04-28 | 73.255 | 4.165 |
| 2026-05-08 | 74.320 | 4.059 |

**Pérdida**: de 6.740 → 4.059 páginas indexadas en 3 meses (-40%). Esto es crítico y debe investigarse. Principales causas probables:
1. Migración de mercados/locales que generó canónicas rotas
2. Cambios en el theme que modificaron tags noindex
3. Proliferación de URLs de filtros/facetas descubiertos por Google

---

## 5.8 Crawl waste por facetas de navegación (P21)

**29.136 URLs bloqueadas por robots.txt** — todas son combinaciones de filtros:
- `/collections/all?filter.p.vendor=Fiamma&filter.v.availability=1`
- `/pt-pt/collections/vendors?page=1&q=Fiamma&grid_list`
- Variantes de `grid_list`, `view`, `page`, etc.

Google las **descubre** a través del HTML antes de leer robots.txt → waste de crawl budget masivo.

**Ver P21** para opciones de solución (nofollow en enlaces de filtro o renderizado JS).

---

## Referencias

- Issues: P2 (#2), P3 (#3), P4 (#4), P15 (#15), P16 (#16), P21 (#21)
- Datos fuente: `evacaravan.com-Coverage-2026-05-14.xlsx`, `Coverage-Drilldown-*.xlsx`
- CSVs: `audit/data/404-urls-reales.csv`, `audit/data/404-urls-sin-parametros.csv`
