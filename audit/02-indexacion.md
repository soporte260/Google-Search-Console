# Auditoría de Indexación — evacaravan.com
> Datos: Google Search Console exportado 2026-05-14

## 2.1 Estado global de indexación

| Métrica | Valor |
|---|---|
| URLs indexadas | ~3.090 (sitemap) |
| URLs en sitemap | 6.315 |
| Ratio de indexación | **49%** |
| Total URLs descubiertas (GSC) | ~38.000+ |

---

## 2.2 Duplicados: Google elige canónica diferente al usuario (410 URLs)

**Archivo:** `audit/data/duplicadas-google-canonica.csv` (410 URLs)

Google ignora la canonical declarada en 410 URLs. Distribución por locale:

| Locale | URLs afectadas |
|---|---|
| fr-fr | ~134 |
| de-de | ~129 |
| fr-be | ~121 |
| de-at | ~18 |
| otros | ~8 |

**Causa:** El contenido en DE/FR está en español o es una traducción automática pobre.
Google unifica estas variantes con la versión `es-default`.

**Acción:** Ver issue [P7] — traducir las 50 páginas DE/FR con más impresiones.

---

## 2.3 Sitemap.xml con URLs en 404 (24 URLs) {#2.3}

**Archivo:** `audit/data/404-sitemap-urls.csv`

Google reporta 24 URLs del `sitemap.xml` que devuelven 404. Esto reduce la
fiabilidad del sitemap y baja el ratio de indexación.

### URLs confirmadas en sitemap con 404 (muestra del export GSC)

| URL | Tipo | Último rastreo |
|---|---|---|
| `https://evacaravan.com/collections/climatizacion-camper` | colección | 2026-05-09 |
| `https://evacaravan.com/collections/cocina-gas-neveras` | colección | 2026-05-09 |
| `https://evacaravan.com/collections/protector-para-cabina` | colección | 2026-05-09 |
| + ~21 más (obtener filtro sitemap en GSC) | — | — |

> **Nota:** El export GSC (máx. 1.000 URLs de 5.177 totales) muestra sólo 3 URLs canónicas
> de sitemap con 404. Para obtener las 24 completas, filtrar en GSC:
> Cobertura → filtrar por sitemap → estado "No se ha encontrado (404)".

### Cómo corregir

**Paso 1 — Obtener la lista completa en GSC**
1. Ir a GSC → Indexación → Páginas
2. Filtrar: Motivo = "No se ha encontrado (404)"
3. En el panel lateral, activar filtro "Sitemap: sitemap.xml"
4. Exportar → descargar URLs

**Paso 2 — Para cada URL 404 del sitemap**

| Si la URL es… | Acción |
|---|---|
| Colección eliminada | → Shopify Admin: crear redirección 301 a colección padre |
| Producto descatalogado | → Archivarlo en Shopify (se elimina del sitemap) + 301 a producto sustituto |
| Producto renombrado | → Añadir redirección 301 desde URL antigua a nueva URL |
| Página eliminada | → 301 a página equivalente existente |

**Ejemplo para colecciones 404 confirmadas:**

```
/collections/climatizacion-camper  →  /collections/climatizacion-frio-calefaccion-electrica
/collections/cocina-gas-neveras    →  /collections/cocina-gas
/collections/protector-para-cabina →  /collections/cerraduras  (o la más apropiada)
```

**Paso 3 — Crear redirecciones en Shopify**
1. Shopify Admin → Online Store → Navigation → URL Redirects
2. "Add URL redirect" para cada URL del sitemap en 404

**Paso 4 — Forzar regeneración y reenvío del sitemap**
1. En Shopify: una vez archivados los productos, el sitemap se regenera automáticamente
2. GSC → Sitemaps → Volver a enviar `sitemap.xml`
3. Esperar 24-48 h y verificar que las 404 han desaparecido del informe

### KPI
- GSC "No se ha encontrado (404)" filtrado por sitemap: bajar de 24 a 0
- Ratio de indexación del sitemap: subir de 49% a >55%

---

## 2.4 URLs rastreadas pero no indexadas (2.468 en sitemap)

**Archivo:** `audit/data/rastreadas-sin-indexar.csv` (muestra de 1.000)

Google rastreó estas páginas y decidió no indexarlas. Causas identificadas:

| Causa | % estimado |
|---|---|
| Contenido thin (<50 palabras) | ~40% |
| Duplicado cross-locale (sin traducción real) | ~35% |
| Colecciones vacías o con pocos productos | ~15% |
| Otras | ~10% |

**Acción:** Ver issue [P13] — auditar y mejorar estas URLs.

---

## 2.5 URLs descubiertas sin indexar (356 URLs)

**Archivo:** `audit/data/descubiertas-sin-indexar.csv` (356 URLs)

Google las conoce por enlaces pero no las ha rastreado aún o ha decidido no indexarlas.
Mejorará automáticamente al resolver P3 (crawl budget mejorado) y P7 (traducciones).

---

## 2.6 Total URLs en 404 (5.177 URLs)

**Archivo:** `audit/data/404-urls-reales.csv` (530 sin parámetros de la muestra de 1.000)

| Tipo | Cantidad (en muestra) |
|---|---|
| Con parámetros `?` (no accionables desde SEO) | 470 |
| Locales fantasma `en-at`, `en-nl`, etc. | 179 |
| Locale real (de-at, fr-be, nl-nl…) | ~103 |
| **Canónicas sin locale (es-default)** | **77** |

Las 77 canónicas son las más críticas (ver `audit/data/404-urls-reales.csv`, filtrar `clase=canonical`).
Las 179 hreflang fantasma se resuelven en [P4].

### Referencia cruzada con issues
- **P3** (este doc §2.3): 24 URLs del sitemap en 404
- **P4**: 178 URLs con locale fantasma en 404
- **P11**: 530 URLs en 404 sin parámetros — crear redirecciones 301
