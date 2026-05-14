# [P1] Fix Review snippets sin campo `author` — Judge.me + Shopify

> **Issue GitHub**: [#1](https://github.com/soporte260/Google-Search-Console/issues/1)
> **App de reviews instalada**: Judge.me
> **URLs afectadas**: 7 (todas productos top)
> **Severidad GSC**: 🟥 Crítica (único error crítico en schemas)

## URLs concretas con el problema

```
1. /products/aire-acondicionado-telair-silent-3-8100h
2. /en-eu/products/air-conditioner-telair-dual-clima-8400h
3. /products/escalon-electrico-thule-slide-out-400-mm
4. /es-eu/products/aire-acondicionado-telair-silent-3-8100h
5. /products/kit-estabilizador-alko-aks-3004-con-antirrobo
6. /products/aire-acondicionado-telair-clima-e-van-7400h
7. /products/aire-acondicionado-telair-dual-clima-8400h
```

---

## Causa raíz (CONFIRMADA tras inspección del HTML)

**El tema Shopify genera un bloque `Review` legacy sin `author`**, usando el metafield `product.metafields.reviews.rating.value` heredado de la antigua app deprecada "Shopify Product Reviews".

Bloque visible en el HTML de la página de producto actual:

```json
"review": {
  "@type": "Review",
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "5.0"
  }
}
```

**Lo que falta**: `author`, `reviewBody`, `datePublished`. Google marca este snippet como error crítico por la ausencia de `author`.

### Por qué Judge.me no es el culpable

Configuración Judge.me ya verificada y correcta:
- ✅ "Agregar fragmentos JSON-LD (predeterminado)" SELECCIONADO
- ❌ "Agregar fragmentos de microdatos" NO seleccionado
- ✅ "Enviar calificación promedio y número de reseñas de cada producto" (predeterminado)
- ⓘ La opción "Avanzado" (enviar contenido individual de reviews vía JSON-LD) requiere suscripción, pero **no es necesaria** para resolver este error.

### Por qué el tema sigue emitiendo el bloque legacy

Cuando se instaló Judge.me, el tema **no se actualizó** y sigue leyendo el rating de los metafields antiguos (`product.metafields.reviews.rating.value`), que es donde se guardaban las valoraciones de la app legacy de Shopify. El tema construye su propio bloque `review` sin enriquecerlo con `author` ni reviewBody, y Google lo lee como roto.

> **Estrategia**: eliminar el bloque `review` del tema y dejar que **solo Judge.me** gestione el schema (vía `aggregateRating` que ya emite por defecto).

---

## Solución paso a paso (15-30 minutos)

### Paso 1 · Judge.me JSON-LD ✅ YA ACTIVO

No hay nada que hacer en Judge.me. La configuración actual es la correcta:
- "Agregar fragmentos JSON-LD (predeterminado)" ya está seleccionado.
- La opción "Avanzado" (contenido individual de reviews) requiere suscripción pero **no es necesaria** para arreglar el error crítico — `aggregateRating` (estrellas + nº de reviews) es suficiente para el rich snippet de SERP.

📚 Referencia oficial: [Displaying product ratings in Google Search Results — Judge.me Help Center](https://judge.me/help/en/articles/8409296-displaying-product-ratings-in-google-search-results)

---

### Paso 2 · Eliminar el bloque `review` legacy del tema (FIX CLAVE)

**Antes de tocar nada: duplicar el tema** como rollback:

1. Shopify Admin → **Online Store → Themes**.
2. En el tema activo (el primero de la lista) → menú `…` → **Duplicate**. Esto crea una copia "Copy of [tu tema]" como backup.
3. Sobre el tema activo (el original) → menú `…` → **Edit code**.

#### 2.1 · Localizar el archivo con el JSON-LD legacy

En la barra de búsqueda izquierda del editor de código, buscar (una a una) en `snippets/`:

- `product-schema.liquid`
- `structured-data.liquid`
- `structured-data-product.liquid`
- `product-json-ld.liquid`
- `seo-product.liquid`
- `seo-schema-product.liquid`

Si no aparece ninguno, probar también en `sections/`:
- `main-product.liquid`
- `product-template.liquid`

**Atajo más rápido**: en cualquier archivo del editor, pulsar `Ctrl+Shift+F` (búsqueda global en todo el tema) y buscar el texto exacto:

```
product.metafields.reviews.rating
```

Eso te lleva directamente al archivo y la línea donde está el bloque.

#### 2.2 · Editar el bloque

Una vez localizado, el código se ve así (puede variar ligeramente):

```liquid
{% if product.metafields.reviews.rating.value != blank %}
  ,"aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{{ product.metafields.reviews.rating.value }}",
    "reviewCount": "{{ product.metafields.reviews.rating_count }}"
  }
  ,"review": {
    "@type": "Review",
    "reviewRating": {
      "@type": "Rating",
      "ratingValue": "{{ product.metafields.reviews.rating.value }}"
    }
  }
{% endif %}
```

**Eliminar SOLAMENTE el bloque `"review": { … }`** (junto con la coma que lo precede), dejando el `aggregateRating` si está presente. Quedaría así:

```liquid
{% if product.metafields.reviews.rating.value != blank %}
  ,"aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{{ product.metafields.reviews.rating.value }}",
    "reviewCount": "{{ product.metafields.reviews.rating_count }}"
  }
{% endif %}
```

> Si el archivo NO tiene `aggregateRating` (solo `review`), entonces elimina todo el `{% if %}…{% endif %}` completo. Judge.me ya emite su propio `aggregateRating` desde su JSON-LD.

#### 2.3 · Guardar

Pulsar **Save** arriba a la derecha. Shopify aplica el cambio inmediatamente.

#### 2.4 · Confirmar en producción

1. Abrir de nuevo `https://evacaravan.com/products/aire-acondicionado-telair-silent-3-8100h`.
2. `Ctrl+U` (ver código fuente) → buscar `"@type":"Review"`.
3. ✅ El bloque debe haber desaparecido por completo.
4. ✅ Si Judge.me funciona, verás un bloque `"aggregateRating":{…}` separado (en su propio `<script type="application/ld+json">`).

---

### Paso 3 · Validar con Rich Results Test

Para cada una de las 7 URLs (mínimo 2-3 muestreadas):

1. Abrir https://search.google.com/test/rich-results
2. Pegar la URL.
3. Verificar:
   - ✅ Aparece **"Fragmento de reseña"** o **"Fragmento de producto"** como detectado.
   - ✅ El bloque `Review` tiene el campo `author` con un valor (ej. nombre del cliente o "Verified Buyer").
   - ✅ **No hay advertencias críticas** sobre `author`.

Captura el screenshot del resultado para documentar.

---

### Paso 4 · Reindexar las 7 URLs en GSC

1. En Google Search Console → **Inspección de URLs**.
2. Para cada una de las 7 URLs:
   - Pegar la URL → "Solicitar indexación".
3. Esperar 1-3 días para que Google revalide.

---

### Paso 5 · Validar masivamente desde GSC

Tras 1-2 semanas:

1. GSC → **Mejoras → Fragmentos de reseña**.
2. Click en **"Validar correcciones"** sobre la incidencia "Falta el campo `author`".
3. Google revisará automáticamente las 7 URLs en ~7-14 días.

---

## KPIs a medir tras la corrección

| Métrica | Estado actual | Objetivo 30 días |
|---|---|---|
| Errores críticos en Review snippets | 1 (7 URLs) | 0 |
| Aparición en SERP de "Fragmento de reseña" | 324 impresiones / 90 días | 600+ impresiones / 30 días |
| CTR de productos con estrellas | n/a | +20% vs sin estrellas |

---

## Notas adicionales

- **Si Judge.me no muestra la opción JSON-LD**: estás en una versión muy antigua. Actualizar la app desde Shopify App Store.
- **Si tras la corrección Google sigue marcando error**: probablemente queda Microdata residual del tema. Buscar en el HTML `itemprop="review"` y `itemtype="https://schema.org/Review"` y eliminar.
- **Este fix también prepara P8** (ampliar reviews al 30%+ del catálogo): cuando Judge.me esté generando JSON-LD correcto, cada nueva review se mostrará en SERP automáticamente.

---

## Estado de ejecución

- [x] Paso 1 — Judge.me JSON-LD ya activo (verificado en panel)
- [x] Diagnóstico — confirmado bloque `review` legacy del tema sin `author` (2026-05-14)
- [x] Paso 2.1 — Localizado en `snippets/structured-data.liquid`
- [x] Paso 2.2 — Eliminado bloque `"review":{…}` del JSON-LD — solo queda `aggregateRating`
- [x] Paso 2.3 — Tema duplicado como backup antes de editar
- [x] Paso 2.4 — Verificado en HTML: `"@type":"Review"` ya no aparece
- [x] Paso 3 — Rich Results Test de `/products/aire-acondicionado-telair-silent-3-8100h`: ✅ 10 elementos válidos, 0 errores críticos
- [ ] Paso 3b — Repetir Rich Results Test en 2 URLs más para confirmar consistencia
- [ ] Paso 4 — Solicitar reindexación de las 7 URLs en GSC
- [ ] Paso 5 — Marcar "Validar correcciones" en GSC

---

## Resultado Rich Results Test (2026-05-14)

URL probada: `https://evacaravan.com/products/aire-acondicionado-telair-silent-3-8100h`

**✅ 10 elementos válidos detectados · 0 errores críticos**

Schemas detectados como válidos:
- Fragmentos de productos (×2)
- Fichas de comerciantes (×2)
- Rutas de exploración (×2)
- Organización (×1)
- Políticas de devoluciones (×1)
- Fragmentos de reseñas (×2)

**Problemas no críticos restantes** (ya cubiertos por otras tareas del plan):

| Campo faltante | Pertenece a |
|---|---|
| `priceValidUntil` (1) | P14 |
| `shippingDetails` (2) | P5 |
| `hasMerchantReturnPolicy` (2) | P5 |
| `description` en hasVariant (1) | P5 (subtarea) |

El error crítico original "Falta el campo `author`" en Review snippets **ha desaparecido**.

---

## Fuentes consultadas

- [Displaying product ratings in Google Search Results — Judge.me Help Center](https://judge.me/help/en/articles/8409296-displaying-product-ratings-in-google-search-results)
- [Troubleshooting for SEO rich snippets — Judge.me Support](https://support.judge.me/support/solutions/articles/44001260256-troubleshooting-for-seo-rich-snippets)
- [List of SEO Rich Snippets Integration — Judge.me Support](https://support.judge.me/support/solutions/articles/44001913541-list-of-seo-rich-snippets-integration)
- [Shopify Schema Markup: Fix Gaps, Add Rich Results & Validate (2026)](https://schemavalidator.org/guides/shopify-schema-markup)
