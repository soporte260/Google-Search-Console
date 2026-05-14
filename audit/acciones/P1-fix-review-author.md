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

## Causa raíz

Con Judge.me instalado, hay **dos fuentes posibles** del schema `Review` sin `author`:

### Fuente A — Judge.me usando Microdata en lugar de JSON-LD
Por defecto, Judge.me inyecta los reviews como **Microdata HTML** (no como JSON-LD). Google los lee, pero si el sitio también tiene un `Product` schema en JSON-LD del tema (Shopify Dawn y la mayoría de temas modernos lo hacen), **se produce un conflicto** y Google puede coger los Reviews "fantasma" sin `author` del Microdata.

### Fuente B — El tema Shopify genera Review schema sin author
Algunos temas (Dawn-based, Booster, Turbo, etc.) emiten un bloque `Product > Review` en JSON-LD pero **dejan `author` vacío** o le pasan `null` cuando hay reviews de Shopify nativas.

> En tu caso es **muy probable la Fuente A** (conflicto Judge.me Microdata ↔ Theme JSON-LD), porque los 7 productos coinciden con los que tienen mayor número de reviews en Judge.me.

---

## Solución paso a paso (15-30 minutos)

### Paso 1 · Activar JSON-LD en Judge.me (CRÍTICO)

1. Entrar en **Shopify Admin → Apps → Judge.me**.
2. Ir a **Settings → Google & SEO → SEO Rich Snippets**.
3. ✅ Marcar la casilla **"Add JSON-LD snippets (Default)"**.
4. En la sección **Advanced**, seleccionar:
   - ✅ **"Push average rating, number of reviews and reviews content of each product"**
5. Click en **Save**.

> Esto hace que Judge.me deje de inyectar el Microdata roto y use JSON-LD con `author` correctamente.

📚 Referencia oficial: [Displaying product ratings in Google Search Results — Judge.me Help Center](https://judge.me/help/en/articles/8409296-displaying-product-ratings-in-google-search-results)

---

### Paso 2 · Verificar si el tema genera Review schema duplicado

1. Abrir cualquiera de las 7 URLs afectadas, por ejemplo:
   `https://evacaravan.com/products/aire-acondicionado-telair-silent-3-8100h`
2. Ver código fuente (Ctrl+U).
3. Buscar `"@type":"Product"` y `"review"` o `"@type":"Review"` en el HTML.
4. **Contar cuántos JSON-LD diferentes hay con `Review`**:
   - Si hay **1 solo** (de Judge.me) → terminó, solo testear (Paso 3).
   - Si hay **2 o más** → ir al Paso 2b para eliminar el del tema.

#### Paso 2b · Eliminar Review schema del tema (si hay duplicado)

En Shopify Admin → **Sales channels → Online Store → Themes → Customize → Edit code**:

1. Buscar en `snippets/`:
   - `product-schema.liquid`
   - `product-json-ld.liquid`
   - `seo-schema-product.liquid`
   - `structured-data-product.liquid`
   - O similar (depende del tema)

2. Dentro del archivo, buscar el bloque que comienza con `"review":` o `"@type": "Review"` y comentarlo o eliminarlo. Ejemplo del bloque a eliminar:

   ```liquid
   {% if product.metafields.reviews.rating.value != blank %}
   ,"review": {
     "@type": "Review",
     "reviewRating": {
       "@type": "Rating",
       "ratingValue": "{{ product.metafields.reviews.rating.value }}"
     }
     {% comment %} ← falta "author" aquí, ese es el problema {% endcomment %}
   }
   {% endif %}
   ```

3. Eliminar este bloque para que **solo Judge.me genere el Review schema**.
4. **Guardar** los cambios.

> ⚠️ Antes de editar el tema, duplicarlo: **Online Store → Themes → … → Duplicate** (rollback fácil).

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

- [ ] Paso 1 — Activar JSON-LD en Judge.me
- [ ] Paso 2 — Verificar duplicación de schema (ver código fuente)
- [ ] Paso 2b — Eliminar Review del tema (solo si hay duplicado)
- [ ] Paso 3 — Validar con Rich Results Test
- [ ] Paso 4 — Solicitar reindexación de las 7 URLs
- [ ] Paso 5 — Marcar "Validar correcciones" en GSC

---

## Fuentes consultadas

- [Displaying product ratings in Google Search Results — Judge.me Help Center](https://judge.me/help/en/articles/8409296-displaying-product-ratings-in-google-search-results)
- [Troubleshooting for SEO rich snippets — Judge.me Support](https://support.judge.me/support/solutions/articles/44001260256-troubleshooting-for-seo-rich-snippets)
- [List of SEO Rich Snippets Integration — Judge.me Support](https://support.judge.me/support/solutions/articles/44001913541-list-of-seo-rich-snippets-integration)
- [Shopify Schema Markup: Fix Gaps, Add Rich Results & Validate (2026)](https://schemavalidator.org/guides/shopify-schema-markup)
