# 05 · Auditoría técnica

## 5.1 Resolución de host: HTTP vs HTTPS, www vs apex

GSC reporta dos páginas de inicio separadas:

| URL | Clics | Impresiones | CTR | Posición |
|---|---|---|---|---|
| `https://evacaravan.com/` | 406 | 4.185 | 9,70 % | 25,37 |
| `http://www.evacaravan.com/` | 156 | 4.273 | 3,65 % | 6,48 |

Esto sugiere que **la versión HTTP/www no redirige correctamente a la versión HTTPS canónica** (apex), o que Google sigue indexando ambas porque algún backlink antiguo apunta a HTTP.

**Acción**: comprobar y forzar 301 desde:
- `http://evacaravan.com/*` → `https://evacaravan.com/*`
- `http://www.evacaravan.com/*` → `https://evacaravan.com/*`
- `https://www.evacaravan.com/*` → `https://evacaravan.com/*`

Sin esta consolidación se pierden ~156 clics/trimestre de autoridad que deberían sumar al dominio principal.

> Curiosamente, la versión `http://www.evacaravan.com/` tiene **mejor posición media** (6,48 vs 25,37). Eso es probablemente porque retiene backlinks históricos de antes de la migración a HTTPS.

---

## 5.2 Parámetros y URLs sucias

### URLs con parámetros indexadas o rastreadas

Detectado en 6.861 URLs muestreadas:

| Patrón parámetro | Frecuencia | Acción |
|---|---|---|
| `?_pos=`, `?_fid=`, `?_ss=` | Mayoritarios en filtros bloqueados | Bloquear en robots.txt (ya lo está) |
| `?variant=` | 16 en 404 | Productos con variantes eliminadas |
| `?utm_source=`, `?utm_medium=` | Aparece en 1 página top performance (campana extractora) | 🟥 Añadir UTM a parámetros canonicalizados |
| `?country=`, `?currency=` | Indica selector geo | Verificar que canonical evita estas |
| `?filter.p.product_type=`, `?filter.p.vendor=`, `?filter.v.availability=` | 29.136 URLs bloqueadas | Resolver bloqueando antes (nofollow) |

### URLs `.atom`

Detectadas en "Duplicada: el usuario no ha indicado canónica":
- `/collections/asa-seguridad.atom`
- `/it-it/collections/climatizacion-frio-calefaccion-electrica.atom`
- `/it-it/blogs/news.atom`

Son RSS feeds. Aparecen en sitemap o están enlazados. Deberían tener `noindex` o canonical a la página HTML correspondiente.

---

## 5.3 Redirecciones

8.075 URLs reportadas como "Página con redirección" (toda la propiedad). Análisis sobre las 1.000 muestreadas:

- 838 son **colecciones**
- 159 son **productos**
- 580 (58 %) tienen query params

Muestra:
- `/de-at/collections/all/products/milenco-precision-calibre`
- `/fr-fr/products/cerradura-para-furgoneta-meroni-ufo2`
- `/products/remis-remitop-vario-ii-con-manivela-claraboya-para-caravana-40x40-cm?_fid=ca26727c3&_pos=1&_ss=c`

Muchas son **legítimas** (productos renombrados, slugs cambiados). Sin embargo, 42 dan **Error de redirección** (loops, cadenas demasiado largas):

```
/en-at/collections/estabilizadores?filter.v.availability=0&view=view-36&grid_list=grid-view
/en-de/collections/estabilizadores
/en-pt/collections/estabilizadores
```

→ Estas combinaciones `en-de`, `en-pt`, `en-at` repiten el patrón hreflang fantasma.

**Acción**: 
1. Auditar los 42 errores de redirección con `screaming-frog` o `httpstat` para ver dónde fallan.
2. Acortar cadenas si hay >2 saltos.

---

## 5.4 Bloqueos 4xx no-404

27 URLs reportadas como "Se ha bloqueado debido a otro problema de tipo 4xx" (probablemente 403/429). Muestra:

- `/en-eu/search/suggest`
- `/fr-fr/search/suggest`
- `/de-at/cart/add`
- otros endpoints internos Shopify

Son endpoints AJAX/internos que **no deberían ser crawleados**. Aparecen porque tu HTML los referencia o porque algo los enlaza.

**Acción**: añadir a robots.txt:
```
Disallow: /*/search/suggest
Disallow: /*/cart/add
Disallow: /*/cart/change
```

(Verificar que Shopify por defecto ya bloquea pero las versiones locale-prefijadas suelen escaparse).

---

## 5.5 Duplicada: el usuario no ha indicado ninguna canónica (26 URLs)

Estas son las `.atom` y similares. Muestra:
- `/collections/asa-seguridad.atom`
- 25 más, mayoritariamente `.atom` feeds y un par de blogs

**Acción**: Excluir feeds Atom del sitemap si están dentro, y servir `<link rel="canonical">` apuntando a la versión HTML, **o** servir el feed con cabecera `X-Robots-Tag: noindex`.

---

## 5.6 robots.txt — recomendaciones

No he podido descargar el robots.txt (bot blocking), pero por los patrones detectados, las reglas habituales de Shopify están funcionando:

✅ Bloquea: filtros (`?filter.*`), variants pagination con todos los params combinados.

⚠️ Recomendaciones de mejora a verificar:
- ¿Bloquea `?_pos=` y `?_fid=` y `?_ss=`? Estos generan miles de duplicados/404.
- ¿Bloquea endpoints AJAX `*/search/suggest` y `*/cart/add` en versiones locale?
- ¿Bloquea `*.atom` o están canonicalizados?

---

## 5.7 Sitemap.xml — observaciones

Aunque no he podido descargarlo directamente, los datos de GSC permiten deducir:

- Contiene ~6.315 URLs (3.090 indexadas + 3.225 no indexadas).
- **Incluye 24 URLs en 404** — saneamiento obligatorio.
- Probablemente lista versiones hreflang `de-de`, `fr-fr`, `de-at`, `fr-be`, `nl-nl`, `pt-pt`, etc. cuando no todas tienen contenido traducido.

**Acción**: 
1. Descargar el sitemap (acceder con navegador, browser extension, o desde otra máquina).
2. Quitar las URLs 404 (cruzar con `data/404-urls-reales.csv`).
3. Considerar dividir en sitemaps por idioma para diagnóstico más fácil en GSC.

---

## 5.8 Crawl budget

Indicadores que sugieren que Google **gasta el crawl budget en URLs sin valor**:

- 29.136 bloqueadas por robots.txt → Google las descubre antes de bloquearlas (links internos las pasan).
- 4.568 404s → Google sigue intentando.
- 8.075 redirecciones → cada visita consume budget.
- 410 duplicadas con canónica ignorada → reintentos.
- 19.715 rastreadas sin indexar → visitadas pero no aprovechadas.

**Total páginas que Google rastrea y descarta**: ~62.000 contra 4.059 indexadas. **Ratio de "desperdicio"** ≈ 15:1.

**Acciones que reducen drásticamente este número**:
1. Eliminar combinaciones hreflang fantasma (`en-at`, `en-nl`, etc.) → corta cientos de 404 y reduce links a generar.
2. Limpiar `.atom` y endpoints internos.
3. Implementar `nofollow` o JS-loaded filters en facetas para evitar el descubrimiento masivo.
4. Quitar 24 URLs 404 del sitemap.

Continúa en [`06-feed-shopping.md`](./06-feed-shopping.md).
