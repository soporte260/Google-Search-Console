# Auditoría SEO — evacaravan.com
> Fecha de datos: 2026-05-14 | Fuente: Google Search Console

## Documentos de auditoría

| Archivo | Tema | Issues relacionados |
|---|---|---|
| `01-resumen-ejecutivo.md` | Resumen y prioridades | Todos |
| `02-indexacion.md` | Indexación, sitemaps, 404s | P3, P4, P11, P13 |
| `04-schemas.md` | Rich Results, JSON-LD | P1, P5, P14, Extra |
| `05-tecnico.md` | Técnico: robots, redirects | P3, P15, P16 |
| `06-feed-shopping.md` | Merchant Center, feed | P5, P9, P12 |
| `07-enlaces-externos.md` | Backlinks, perfil de enlaces | P17, P18 |
| `08-plan-accion-priorizado.md` | Plan con fases y prioridades | Todos |

## Archivos de datos (`audit/data/`)

### Indexación y cobertura
| Archivo | Descripción | Filas |
|---|---|---|
| `404-urls-reales.csv` | 404 sin parámetros (muestra 1.000/5.177) | 530 |
| `404-sitemap-urls.csv` | 404 directamente en sitemap.xml | 3+ (ver §2.3) |
| `404-hreflang-fantasma.csv` | 404 de locales en-XX no existentes (P4) | 179 |
| `rastreadas-sin-indexar.csv` | Rastreadas pero no indexadas por Google | 1.000 |
| `descubiertas-sin-indexar.csv` | Descubiertas pero no rastreadas | 356 |
| `duplicadas-google-canonica.csv` | Google eligió canónica distinta a la declarada | 410 |
| `duplicadas-sin-canonica.csv` | Sin canonical → feeds .atom y duplicados | 26 |
| `errores-redireccion.csv` | Error en cadena de redirección | 42 |
| `bloqueadas-4xx.csv` | Bloqueadas por error 4xx (AJAX endpoints) | 27 |

### Rendimiento en búsqueda
| Archivo | Descripción | Filas |
|---|---|---|
| `paginas-top-rendimiento.csv` | Top 1.000 páginas por clics/impresiones | 1.000 |
| `paginas-oportunidad-ctr.csv` | Páginas con >100 impr y CTR <5% | 232 |
| `consultas-oportunidad-cero-clics.csv` | Consultas con >50 impr y 0 clics | 186 |

### Schemas y Rich Results
| Archivo | Descripción | Filas |
|---|---|---|
| `merchant-sin-shippingdetails.csv` | Sin shippingDetails (P5) | 53 |
| `merchant-sin-returnpolicy.csv` | Sin hasMerchantReturnPolicy (P5) | 53 |
| `merchant-sin-author.csv` | Sin author en review (P1) | 7 |
| `merchant-sin-description.csv` | Sin description en Merchant | 53 |
| `merchant-gtin-invalido.csv` | GTIN inválido (Extra) | 4 |
| `merchant-description-larga.csv` | Descripción >5.000 chars (Extra) | 3 |
| `productos-sin-review.csv` | Sin campo review en schema (P8) | 46 |
| `productos-sin-pricevaliduntil.csv` | Sin priceValidUntil (P14) | 53 |

### Catálogo de productos (feed Merchant Center)
| Archivo | Descripción | Filas |
|---|---|---|
| `productos-sin-disponibilidad.csv` | Campo disponibilidad vacío (P12) | 320 |
| `productos-sin-estado.csv` | Campo estado vacío (P12) | 299 |
| `productos-agotados.csv` | Marcados como agotados (P12) | 265 |
| `productos-sin-categoria-google.csv` | Sin categoría Google Product (P9) | 1.381 |

## Estado de los issues

| Issue | Título | Estado |
|---|---|---|
| P1 | Fix Review snippets sin `author` | ✅ Cerrado |
| P2 | Resolver duplicación HTTP/www vs HTTPS | ✅ Cerrado |
| P3 | Limpiar sitemap de 24 URLs en 404 | ✅ Validado por Google (2026-06-01) |
| P4 | Eliminar hreflang fantasma en-XX | 🔄 Análisis completado — pendiente ejecución en Shopify |
| P5 | shippingDetails + hasMerchantReturnPolicy | ⏳ Pendiente |
| P6 | Landing cerraduras para furgonetas | ⏳ Pendiente |
| P7 | Traducir páginas DE/FR con más impresiones | ⏳ Pendiente |
| P8 | App de reviews + emails post-venta | ⏳ Pendiente |
| P9 | Categoría Google Product a 1.381 productos | ⏳ Pendiente |
| P10 | Optimizar colecciones con más impresiones | ⏳ Pendiente |
| P11 | Redirigir 530 URLs con 404 real | ⏳ Pendiente |
| P12 | Corregir productos sin disponibilidad/estado | ⏳ Pendiente |
| P13 | Auditar URLs rastreadas sin indexar | ⏳ Pendiente |
| P14 | priceValidUntil en schema offers | ⏳ Pendiente |
| P15 | Bloquear endpoints AJAX en robots.txt | ⏳ Pendiente |
| P16 | Noindex feeds .atom | ⏳ Pendiente |
| P17 | Auditar localitybiz.es (backlinks) | ⏳ Pendiente |
| P18 | Backlinks a fabricantes | ⏳ Pendiente |
| P19 | Guías técnicas en blog | ⏳ Pendiente |
| P20 | Schema ItemList en colecciones | ⏳ Pendiente |
| P21 | Nofollow en facetas de navegación | ⏳ Pendiente |
| P22 | Backlinks editoriales | ⏳ Pendiente |
