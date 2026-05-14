# 01 · Resumen ejecutivo

## KPIs del último trimestre (90 días, 13 feb → 12 may 2026)

| Métrica | Valor |
|---|---|
| Clics totales | **3.072** |
| Impresiones totales | **151.983** |
| CTR medio | **2,00 %** |
| Posición media | **15,46** (página 2) |
| Tendencia | **Negativa**. El último mes ronda 30-44 clics/día; al inicio del periodo 12-34 clics/día (subida temprana, estabilización media). La posición media ha mejorado de ~20 a ~15. |

### Distribución del tráfico

- **Por dispositivo**: Móvil 64 %, Ordenador 33 %, Tablet 2 %.
- **Por país**: España **74 %** (2.276 clics), Alemania 7,6 % (235), Francia 3,7 % (113). El resto de mercados aportan menos del 2 %.
- **Por search appearance**: Fragmentos de producto generan 76 % del tráfico y el 76 % de las impresiones; Fichas de comerciantes el 7 % de clics pero con CTR 6,10 % (la mejor SERP); Fragmento de reseña casi nulo.

---

## Indexación: el problema #1

| Indicador | Total propiedad | Sólo sitemap.xml |
|---|---|---|
| Páginas indexadas | **4.059** | 3.090 |
| Páginas NO indexadas | **74.320** | 3.225 |
| Ratio de indexación | **5,2 %** | **49 %** |

### Top motivos de NO indexación (toda la propiedad)

| Motivo | URLs | Severidad |
|---|---|---|
| Bloqueada por robots.txt | 29.136 | 🟢 OK (filtros de catálogo, intencional) |
| Rastreada, actualmente sin indexar | **19.715** | 🟥 ALTO — Google decidió no indexar (thin/duplicate) |
| Página alternativa con canónica adecuada | 10.501 | 🟢 OK (variantes hreflang correctas) |
| Página con redirección | 8.075 | 🟨 Revisar (saneamiento) |
| **No se ha encontrado (404)** | **4.568** | 🟥 ALTO — Limpieza obligatoria |
| Excluida por noindex | 1.464 | 🟢 OK (cart, account, vendors) |
| Duplicada (Google canónica distinta) | 410 | 🟥 Hreflang roto |
| Descubierta, sin indexar | 356 | 🟨 No rastreadas aún |

### Sólo desde el sitemap.xml

| Motivo | URLs |
|---|---|
| Rastreada, actualmente sin indexar | **2.468** |
| Duplicada (Google canónica distinta) | 360 |
| Descubierta, sin indexar | 356 |
| **No se ha encontrado (404)** | **24** ← deberían eliminarse del sitemap |
| Página alternativa con canónica adecuada | 17 |

---

## Rich snippets / Schema (último estado)

| Tipo | Válidos | Problemas críticos | Problemas no críticos |
|---|---|---|---|
| Breadcrumbs | 269 | 0 | 0 |
| Merchant listings | 110 | 0 | 6 incidencias (110 + 110 + 57 + 7 + 4 + 3) |
| Product snippets | 92 | 0 | 4 incidencias (92 + 92 + 53 + 7) |
| Review snippets | — | **1 crítico** (7 URLs sin `author`) | 0 |

**Problema crítico**: Review snippets sin campo `author` en 7 URLs producto top.

---

## Conclusiones

1. **El sitio tiene un problema masivo de indexación** que actúa como techo de crecimiento orgánico. La mitad del catálogo del sitemap no aparece en Google.
2. **La internacionalización está mal montada**: 23 locales detectados, varios sin contenido real, generando 530 páginas 404 reales y 410 duplicadas.
3. **El catálogo de producto es bueno** (1.682 productos, 84,5 % con GTIN) pero el feed Merchant tiene huecos de datos (`hasMerchantReturnPolicy`, `shippingDetails`, `description`).
4. **Hay un nicho de alta intención sin explotar**: cerraduras para furgonetas (>7.000 impresiones/mes a 0 clics).
5. **La marca funciona** pero el tráfico no-marca depende mucho de un puñado de páginas (top 30 acumula >80 % de clics).

→ Continuar en [`02-indexacion.md`](./02-indexacion.md) para el análisis técnico, o saltar directamente al [`08-plan-accion-priorizado.md`](./08-plan-accion-priorizado.md) para la hoja de ruta.
