# 04 · Datos estructurados / Rich snippets

Cada tipo de schema en GSC con su impacto en SERP.

## 4.1 Breadcrumbs ✅

| Métrica | Valor |
|---|---|
| Elementos válidos | 269 |
| Problemas críticos | 0 |
| Problemas no críticos | 0 |

**Estado**: OK. Sigue las recomendaciones Shopify por defecto y funciona.

Recomendación: mantener — no requiere acción.

---

## 4.2 Product snippets — 92 elementos válidos, 4 incidencias no críticas

### Incidencias

| Incidencia | URLs afectadas |
|---|---|
| Falta el campo `aggregateRating` | 92 |
| Falta el campo `review` | 92 |
| Falta el campo `priceValidUntil` (en `hasVariant.offers`) | 53 |
| Falta el campo `author` (en `review`) | 7 |

**Interpretación**:

- Los 92 productos NO tienen rating ni review estructurado. Cruzando con el TSV: **sólo 33 productos del feed tienen rating** (1,96 % del catálogo). El resto no muestra estrellas en SERP, lo que reduce CTR.
- 53 productos sin `priceValidUntil`. Tema relativamente menor pero Google lo pide para ofertas con caducidad. Genera "Failed to read offer" en el report.
- 7 productos con review pero sin `author` — los mismos 7 que dan error crítico en Review snippets (ver §4.4).

### Productos donde se ve el problema (muestra)

- `/products/sistema-maniobra-semiautomatico-em203`
- `/en-eu/products/pack-3-security-locks-fiamma-safe-door-frame`
- `/products/aire-acondicionado-telair-silent-3-8100h`
- `/products/escalon-electrico-thule-slide-out-400-mm`

**Acción recomendada**: implementar un sistema de reviews (Loox/Judge.me/Yotpo o similar) para alimentar `aggregateRating` y `review`. Beneficio: estrellas en SERP, +CTR esperado 20-30 % en consultas producto.

---

## 4.3 Merchant listings — 110 válidos, 6 incidencias

### Incidencias (todas no críticas, pero con impacto en visibilidad Merchant)

| Incidencia | URLs |
|---|---|
| Falta el campo `hasMerchantReturnPolicy` (en `offers`) | **110** |
| Falta el campo `shippingDetails` (en `offers`) | **110** |
| Falta el campo `description` | 57 |
| Falta el campo `author` (en `review`) | 7 |
| GTIN no válido | 4 |
| Longitud de `description` no válida | 3 |

### Por qué importa

`hasMerchantReturnPolicy` y `shippingDetails` son requisitos **endurecidos por Google a partir de 2024-2025**. Sin ellos, los listings pueden:
- Perder elegibilidad para Fichas de Comerciante en algunos países.
- No mostrar información de envíos/devoluciones en SERP, lo que **reduce el CTR significativamente** (recuerda: este search appearance ya es tu mejor CTR, 6,10 %).

Los **110 productos afectados** son los mismos en ambos casos (mismo template Shopify). Es una corrección **single-fix masiva**: implementar el schema una vez en el theme.

### GTIN no válido (4 productos)

Productos:
1. `/products/campana-extractora-baraldi-12v-especial-campers-negro`
2. `/products/campana-extractora-baraldi-12v-especial-campers-inox`
3. `/products/milenco-antirrobo-estabilizador-als-3004` (typo en nombre: probablemente `aks-3004`)
4. (uno más)

Acción: validar GTIN en el catálogo Shopify (campo `barcode`).

### Description length (3 productos)

Indica que la descripción excede el máximo (5.000 chars en Merchant) o no llega al mínimo. Productos afectados incluyen el Thule Slide Out 400mm.

---

## 4.4 Review snippets — 1 problema CRÍTICO

| Incidencia | URLs | Severidad |
|---|---|---|
| Falta el campo `author` | **7** | 🟥 Crítico |

**Estos son los productos con review pero sin autor**:
1. `/products/aire-acondicionado-telair-silent-3-8100h` (Aire Acondicionado Telair Silent 3 8100H)
2. `/en-eu/products/air-conditioner-telair-dual-clima-8400h`
3. `/products/escalon-electrico-thule-slide-out-400-mm`
4. `/es-eu/products/aire-acondicionado-telair-silent-3-8100h`
5. `/products/kit-estabilizador-alko-aks-3004-con-antirrobo`
6. `/products/aire-acondicionado-telair-clima-e-van-7400h`
7. `/products/aire-acondicionado-telair-dual-clima-8400h`

Son productos top-vendedores (varios aparecen en el top performance). El review está marcado en el schema pero sin `author.name` → Google lo descarta y NO muestra estrellas.

**Acción rápida (single-fix Shopify)**: localizar el bloque de schema `Review` en el theme, asegurar que para cada `Review` se incluye `author` con al menos `@type: Person` y `name`. Si las reviews vienen de una app (Loox/Judge.me), revisar la configuración del JSON-LD.

---

## 4.5 Resumen y orden de impacto schema

| Acción | Impacto SERP | Esfuerzo | Prioridad |
|---|---|---|---|
| Fix `author` en Review snippets (7 productos) | 🟥 ALTO — devuelve estrellas a top-products | 30 min | **#1** |
| Implementar `hasMerchantReturnPolicy` + `shippingDetails` (110 prod) | 🟧 ALTO — protege fichas comerciante, CTR | 1-2 h theme edit | **#2** |
| Implementar `aggregateRating`/`review` en 92 productos (app reviews) | 🟧 MEDIO-ALTO — estrellas en SERP | 1-2 días config app + invitar a reseñas | **#3** |
| Añadir `description` a los 57 productos sin ella | 🟨 MEDIO — necesario para Merchant | 2-4 h (revisar feed) | **#4** |
| Fix `priceValidUntil` (53 productos) | 🟨 BAJO-MEDIO | 1 h theme edit | **#5** |
| Fix 4 GTIN inválidos | 🟨 BAJO | 30 min | **#6** |
| Fix 3 descripciones con longitud inválida | 🟨 BAJO | 30 min | **#7** |

Continúa en [`05-tecnico.md`](./05-tecnico.md).
