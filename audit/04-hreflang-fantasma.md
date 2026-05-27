# P4 — Eliminar combinaciones hreflang fantasma
> Urgencia: CRÍTICA | Impacto: ALTO | Esfuerzo: 2-4 h en Shopify Admin

## Diagnóstico

Shopify Markets generó URLs para **7 combinaciones idioma-país que no existen** en la
tienda. Google las descubre por los tags `hreflang` del HTML, las intenta rastrear y
recibe 404. Resultado: **178 URLs en 404** + crawl budget desperdiciado.

| Locale fantasma | País | URLs en 404 | Locale correcto |
|---|---|---|---|
| `en-at` | Austria | **41** | `de-at` |
| `en-nl` | Países Bajos | **33** | `nl-nl` |
| `en-it` | Italia | **31** | `it-it` |
| `en-pt` | Portugal | **26** | `pt-pt` |
| `en-be` | Bélgica | **21** | `fr-be` |
| `en-fr` | Francia | **21** | `fr-fr` |
| `en-de` | Alemania | **5** | `de-de` |
| **TOTAL** | | **178** | |

**Datos completos:** `audit/data/404-hreflang-fantasma-con-redirects.csv`
(175 redirecciones 301 + 3 endpoints AJAX para robots.txt)

---

## Solución en 3 pasos

### Paso 1 — Desactivar combinaciones en Shopify Markets

1. Shopify Admin → **Configuración → Mercados**
2. Para cada mercado afectado, eliminar el idioma inglés:

| Mercado | Acción |
|---|---|
| **Austria** | Eliminar idioma "Inglés" del mercado Austria → dejar solo "Alemán" (`de-at`) |
| **Países Bajos** | Eliminar "Inglés" → dejar "Neerlandés" (`nl-nl`) |
| **Italia** | Eliminar "Inglés" → dejar "Italiano" (`it-it`) |
| **Portugal** | Eliminar "Inglés" → dejar "Portugués" (`pt-pt`) |
| **Bélgica** | Eliminar "Inglés" → dejar "Francés" (`fr-be`) y/o "Neerlandés" |
| **Francia** | Eliminar "Inglés" → dejar "Francés" (`fr-fr`) |
| **Alemania** | Eliminar "Inglés" → dejar "Alemán" (`de-de`) |

> Esto hace que Shopify deje de generar URLs `en-XX/*` y las elimine del sitemap y
> de los tags `hreflang` del HTML automáticamente.

---

### Paso 2 — Crear redirecciones 301 (para las URLs ya rastreadas por Google)

Las 175 URLs de productos y colecciones necesitan 301 hacia el locale correcto.
El CSV `audit/data/404-hreflang-fantasma-con-redirects.csv` tiene la columna
`url_destino` con el destino exacto para cada una.

**Método rápido — Shopify Admin:**
1. Shopify Admin → Online Store → **Navigation → URL Redirects**
2. Opción A (manual): "Add URL redirect" para las más importantes
3. Opción B (masiva): usar la **importación CSV** de redirecciones de Shopify:
   - Formato: columnas `Redirect from` y `Redirect to`
   - Preparar el CSV desde `404-hreflang-fantasma-con-redirects.csv`
     filtrando `accion = 301` y usando `path` → `url_destino`

**Ejemplo de las primeras redirecciones por locale:**

```
/en-at/collections/accesorios-gas    →  /de-at/collections/accesorios-gas
/en-at/collections/alarma            →  /de-at/collections/alarma
/en-nl/collections/accesorios-gas    →  /nl-nl/collections/accesorios-gas
/en-nl/collections/alarma            →  /nl-nl/collections/alarma
/en-it/collections/alarma            →  /it-it/collections/alarma
/en-pt/collections/accesorios-gas    →  /pt-pt/collections/accesorios-gas
/en-be/collections/cocina            →  /fr-be/collections/cocina
/en-fr/collections/antenas-tv        →  /fr-fr/collections/antenas-tv
/en-de/collections/claraboyas        →  /de-de/collections/claraboyas
```

> Nota: En Shopify, los redirects se definen sin dominio (solo el path `/en-at/...`).

---

### Paso 3 — Bloquear endpoints AJAX en robots.txt

3 URLs de carrito fueron rastreadas en locales fantasma:

```
/en-at/cart/change
/en-be/cart
/en-nl/cart/add
```

Añadir en `config/robots.txt.liquid` (además de los del issue P15):

```
Disallow: /*/cart
Disallow: /*/cart/add
Disallow: /*/cart/change
Disallow: /*/cart/update
```

---

## Verificación posterior

1. **24-48h después de los cambios**: comprobar en GSC que los locales fantasma
   dejan de aparecer en los tags `hreflang` del HTML.
   - Herramienta: inspeccionar cualquier producto en GSC → ver hreflang declarados
2. **1-2 semanas**: GSC → Indexación → Páginas → filtrar 404:
   - Total 404 debe bajar ~178 URLs (de 4.568 hacia ~4.390)
3. **Sitemap**: verificar que el sitemap ya no incluye URLs `en-at/*`, `en-nl/*`, etc.

## KPI objetivo

| Métrica | Antes | Objetivo |
|---|---|---|
| URLs en 404 totales | 4.568 | < 4.390 (−178) |
| Locales `en-XX` en hreflang | 7 | 0 |
| URLs `en-XX` en sitemap | ~40+ | 0 |

## Referencia cruzada

- Este fix también beneficia **P11** (530 URLs en 404 reales): al resolver
  los 178 hreflang fantasma, el total baja automáticamente.
- Los endpoints AJAX coordinan con **P15** (bloquear `/*/search/suggest`, `/*/cart/add`).
