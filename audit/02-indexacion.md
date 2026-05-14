# 02 · Indexación y cobertura

## 2.1 Estado actual

Datos GSC al **2026-05-08** (último día consolidado):

| Origen | Indexadas | No indexadas | Ratio |
|---|---|---|---|
| Toda la propiedad | 4.059 | 74.320 | 5,2 % |
| sitemap.xml | 3.090 | 3.225 | 49 % |

**Interpretación**: el sitemap contiene unas **6.315 URLs** que Google conoce. Sólo ~3.090 se indexan (~49 %). Fuera del sitemap hay otras ~68.000 URLs descubiertas (filtros, parámetros, duplicados hreflang) que Google ha rechazado mayoritariamente.

> El ratio 49 % es **bajo** para un e-commerce. En tiendas Shopify saneadas se ve 70-90 %.

---

## 2.2 Análisis hreflang (raíz del problema)

Google ha rastreado URLs en **23 locales** distintos:

| Locale | URLs encontradas (en drilldowns problemáticos) | Estado |
|---|---|---|
| `es-default` (sin prefijo) | 787 | OK — versión canónica |
| `en-eu` | 521 | OK — inglés UE |
| `fr-fr`, `de-de`, `de-at`, `fr-be`, `nl-nl`, `pt-pt`, `it-it`, `es-eu` | 268-503 cada uno | Variantes país, MUCHOS duplicados |
| `it`, `en`, `fr`, `pt`, `nl`, `de` | 287-380 cada uno | Variantes idioma genérico (¿necesarias?) |
| `en-at`, `en-nl`, `en-it`, `en-pt`, `en-be`, `en-fr`, `en-de` | 7-45 cada uno | 🟥 **NO EXISTEN** (mayoritariamente 404) |

### Combinaciones que NO deberían existir (return mostly 404)

```
en-at  → 41 URLs en 404 reales
en-nl  → 33 URLs en 404 reales
en-it  → 31 URLs en 404 reales
en-pt  → 26 URLs en 404 reales
en-be  → 21 URLs en 404 reales
en-fr  → 21 URLs en 404 reales
en-de  →  5 URLs en 404 reales
─────────────────────────────────
TOTAL  → 178 URLs 404 sólo por estas combinaciones
```

**Acción recomendada**: Decidir si el inglés es global (`en-eu` o `en` suficientes) y eliminar/configurar correctamente los demás. Si no se ofrecen, no deben generarse links internos hacia ellos.

### Duplicadas con canónica diferente — la pista del contenido sin traducir

De los 410 productos donde Google ignoró la canónica:

| Locale | Casos |
|---|---|
| `fr-fr` | 134 |
| `de-de` | 129 |
| `fr-be` | 121 |
| `de-at` | 18 |
| `de`, `fr`, `it-it` | 8 totales |

Es decir, **el 100 % son páginas francesas o alemanas**. Esto suele significar que:
1. El contenido visible (título, descripción) se mantiene en español/inglés a pesar de la URL traducida, **o**
2. La traducción es muy mínima y Google considera la versión española como canónica real.

Resultado: tu inventario alemán/francés no aparece en Google.de/.fr.

### Páginas alternativas con canónica correcta

10.501 URLs caen aquí. Es **OK** — son las hreflang que sí funcionan. Pero el ratio "alternates correctas" : "duplicadas que fallan" debería ser mucho mayor.

---

## 2.3 Las 4.568 URLs en 404 — desglose

Sobre 1.000 URLs muestreadas:

| Patrón | Cantidad | Naturaleza |
|---|---|---|
| Sin parámetros (404 "reales") | 530 | Páginas que tu site enlaza/Google conoce pero no existen |
| Con `_pos`, `_fid`, `_ss` | 337 | URLs de filtros/paginación Shopify antiguos |
| Con `filter.*` | 17 | Filtros canónicos que ya no devuelven nada |
| Con `variant=` | 16 | Variantes producto eliminadas |
| Otros | 100 | — |

→ Detalle completo en [`data/404-urls-reales.csv`](./data/404-urls-reales.csv) (530 filas) y [`data/404-urls-parametros.csv`](./data/404-urls-parametros.csv) (470 filas).

### 404 por locale (críticos = sin parámetros)

```
es-default    78   ← productos descatalogados sin redirección
en-at         41   ← combinación hreflang fantasma
de-at         41
en-nl         33   ← fantasma
fr-be         32
en-it         31   ← fantasma
de-de         30
en-eu         29
nl-nl         27
en-pt         26   ← fantasma
en-fr         21   ← fantasma
en-be         21   ← fantasma
…
```

**Patrón claro**: 178 de los 530 (~34 %) son combinaciones idioma-país inexistentes. Otro 35 % son productos descatalogados sin 301 a producto sustituto/categoría.

---

## 2.4 Las 19.715 URLs "rastreadas, sin indexar"

Es la **mayor fuga de crawl budget**. Google las visita pero decide no indexar. Causas habituales:

- **Thin content**: páginas producto con descripción mínima (typical Shopify default desc)
- **Duplicación cross-locale**: misma descripción en `es`, `en`, `fr` cuando idioma del visitante coincide
- **Bajo valor**: páginas colección con 1-2 productos, o sólo agotados
- **Páginas hreflang sin traducir**: contenido idéntico al canónico
- **Páginas `.atom`** (feeds RSS): se han detectado en el drilldown (`*.atom` URLs)

Sobre las 1.000 muestreadas:
- 632 son **producto** (60 %)
- 332 son **colección** (33 %)
- 75 son **page** (políticas, contacto…)
- 30 son **blog**

→ Detalle: [`data/rastreadas-sin-indexar.csv`](./data/rastreadas-sin-indexar.csv) (muestra de 1.000 de las 19.715 reales).

---

## 2.5 Las 356 "descubiertas, no rastreadas"

Estas son páginas que Google **encontró en links pero todavía no ha rastreado**. Causa típica: crawl budget agotado por las 29.136 bloqueadas-por-robots y 8.075 redirecciones.

Análisis de las 356:
- 181 colecciones (la mayoría en `de-at`, `de-de` — colecciones recién creadas o sin enlaces internos)
- 98 productos
- 75 pages (políticas duplicadas por locale)
- 2 blog

URLs notables:
- `https://evacaravan.com/blogs/news` — la página de blog principal **no se rastrea**
- `https://evacaravan.com/collections/novedades-climatizador-htw` — colección sin enlaces internos visibles
- 16 colecciones `de-at` y 12 colecciones `de-de` — el árbol alemán está aislado del español

→ Detalle: [`data/descubiertas-sin-indexar.csv`](./data/descubiertas-sin-indexar.csv) (356 filas, todas).

---

## 2.6 Bloqueadas por robots.txt — 29.136

Mayoritariamente combinaciones de filtros con doble parámetro (`filter.v.availability` + `filter.p.vendor`, etc.). El bloqueo es **correcto** (evita facetas infinitas), pero la magnitud sugiere que la navegación facetada genera demasiados links internos hacia estas URLs antes de ser bloqueadas — sigue gastando crawl budget en descubrimiento.

**Acción**: Añadir `rel="nofollow"` o pasar a JS-loaded filters para evitar enlaces crawleables.

---

## 2.7 Conclusión técnica indexación

1. **El núcleo del problema es la internacionalización mal montada**. Genera dos efectos: 530 páginas 404, 410 canónicas ignoradas, miles de URLs duplicadas no indexadas.
2. **El sitemap está sucio**: 24 URLs en 404 deben quitarse.
3. **La arquitectura de enlazado interno** sangra crawl budget hacia filtros/parámetros bloqueados por robots.

Próximo: [`03-performance-search.md`](./03-performance-search.md).
