# 06 · Feed Shopping & catálogo

Datos del archivo `productos_2026-05-14_10-45-37.tsv` (export Shopify Sales Channel for Google).

## 6.1 Resumen del catálogo

| Indicador | Valor |
|---|---|
| Productos en el feed | **1.682** |
| Productos en stock | 1.097 (65 %) |
| Productos agotados | 265 (16 %) |
| Productos sin valor de `disponibilidad` | **320 (19 %)** 🟥 |
| Productos sin `estado` | **299 (18 %)** 🟥 |
| Productos con GTIN válido | 1.422 (84,5 %) |
| Productos con `existe identificador = sí` | 266 (16 %) |
| Productos con rating | 33 (1,96 %) 🟥 |
| Productos con categoría Google product | 301 (18 %) 🟥 |

### Idiomas del feed

| Idioma | Productos |
|---|---|
| es | 656 |
| de | 467 |
| fr | 334 |
| en | 225 |

### Países

| País | Productos |
|---|---|
| ES | 1.046 |
| DE | 205 |
| AT | 186 |
| FR | 123 |
| BE | 119 |
| PT, IT, NL | 1 cada uno |

🟥 **Anomalía**: PT/IT/NL tienen sólo 1 producto cada uno en el feed Merchant. Pero en GSC sí hay URLs en `pt-pt`, `it-it`, `nl-nl`. Esto significa que **las URLs existen pero NO están en el feed** — pierdes la posibilidad de Shopping Ads en esos países y la opción de aparecer en Fichas de Comerciante.

---

## 6.2 Top 20 marcas (a referenciar en landings de marca)

| Marca | Productos | Notas |
|---|---|---|
| Fiamma | 244 | Marca principal — colección dedicada? |
| Victron Energy | 184 | Energía solar/baterías |
| Thetford | 183 | Sanitario |
| AL-KO | 118 | Chasis/estabilizadores |
| Thule | 109 | Soportes/cerraduras |
| Truma | 63 | Calefacción/agua caliente |
| Dometic | 56 | Climatización |
| MERONI | 55 | Cerraduras 🎯 |
| Milenco | 52 | Estabilizadores |
| DCU Tecnologic | 33 | |
| Daken | 30 | Cerraduras 🎯 |
| HEOSolution | 21 | Cerraduras 🎯 |
| Mestic | 17 | |
| Reich | 16 | |
| Teleco | 16 | |
| Brunner | 15 | |
| EZA | 14 | |
| Pentair | 13 | |
| CBE | 13 | |
| Tonna | 11 | |

🎯 **MERONI (55) + Daken (30) + HEOSolution (21) = 106 productos** de cerraduras. Junto a Thule Van Lock y Fiamma Safe Door, base sólida para la landing de "cerraduras furgoneta" que ahora mismo no captura las >11.000 impresiones del clúster.

---

## 6.3 Productos sin `disponibilidad` ni `estado`

- **320 productos sin `disponibilidad`**: detalle en [`data/productos-sin-disponibilidad.csv`](./data/productos-sin-disponibilidad.csv).
- **299 productos sin `estado`** (debería ser "nuevo"): detalle en [`data/productos-sin-estado.csv`](./data/productos-sin-estado.csv).

Estos productos son rechazados por Google Merchant Center y NO aparecen en Shopping ni en Fichas. Probablemente cruzan con muchos de los 92 productos sin schema correcto.

**Acción**: ejecutar bulk update en Shopify para rellenar estos dos campos en los productos afectados. Si vienen de variants antiguas o duplicados, considerar archivar/borrar.

---

## 6.4 Productos sin GTIN (260)

84,5 % tienen GTIN, pero los **260 sin GTIN** suelen ser packs custom (sets, packs de 2/3 unidades, productos exclusivos sin código UPC/EAN). Estos requieren `identifier_exists: no` en lugar de un GTIN inválido.

→ Revisar [`data/productos-sin-gtin.csv`](./data/productos-sin-gtin.csv). 

Para los productos sin GTIN legítimos (packs), añadir:
- `identifier_exists: no` en Shopify (campo en Sales Channel for Google).
- O fijar un MPN único (Manufacturer Part Number).

Los **4 productos con GTIN inválido** (campanas Baraldi, milenco antirrobo) son distintos — esos sí tienen GTIN, pero el código falla checksum. Revisar manualmente.

---

## 6.5 Productos sin categoría Google product (1.381 = 82 %)

🟥 **Sólo 301 de 1.682 productos tienen `categoría en google product` asignada**. Esto:
- Reduce la capacidad de Google para clasificar correctamente el producto en Shopping
- Limita la elegibilidad para Fichas de Comerciante en ciertas verticales
- Empeora la calidad del feed según Google

Sample de categorías a usar (Google Product Taxonomy):
- Cerraduras → `Hardware > Hardware Accessories > Locks > Door Locks`
- Climatización caravana → `Vehicles & Parts > Vehicle Parts & Accessories > Motor Vehicle Parts > Motor Vehicle Climate Control Parts`
- Baterías → `Electronics > Electronics Accessories > Power > Batteries`
- Cocinas/neveras → `Vehicles & Parts > Vehicle Parts & Accessories > Motor Vehicle Camping Equipment`

→ Detalle: [`data/productos-sin-categoria-google.csv`](./data/productos-sin-categoria-google.csv).

**Acción**: asignar masivamente por `tipo producto` (Cocinas, Neveras, Cerraduras, Antenas, Aires acondicionados, etc.) — mucho menos esfuerzo que hacerlo producto a producto. Se puede hacer con bulk editor de Shopify o vía Sales Channel for Google config.

---

## 6.6 Productos agotados (265 = 16 %)

→ [`data/productos-agotados.csv`](./data/productos-agotados.csv).

Estos productos:
- Aparecen como rechazados en Merchant si no se actualiza `disponibilidad`.
- Si su URL recibe tráfico orgánico, **el usuario aterriza en producto que no puede comprar**.

**Acción**:
1. Si es agotado temporal: dejar la URL, añadir aviso "Disponible próximamente" con notificación de stock. Mantiene SEO ganado.
2. Si es descatalogado definitivo: 301 a producto sustituto o a la categoría padre. **NO dejar 404** (es una de las causas de los 530 404s reales).

---

## 6.7 Reviews — sólo 33 productos con rating

```
Productos con rating average: 33
Productos con rating count:   33
```

🟥 **1,96 % del catálogo tiene reviews**. Esto explica:
- Las 92 URLs con productSchema sin `aggregateRating` ni `review`.
- El bajísimo número de Fragmentos de reseña en SERP (sólo 3 clics, 324 impresiones en 90 días).

**Acción estratégica**: instalar/activar app de reviews (Loox, Judge.me, Yotpo, Stamped). Configurar emails automáticos post-venta. Objetivo: 30-50 % del catálogo con reviews en 12 meses → habilita estrellas SERP masivas.

Continúa en [`07-enlaces-externos.md`](./07-enlaces-externos.md).
