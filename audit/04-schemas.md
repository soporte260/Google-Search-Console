# Auditoría de Schema Markup — evacaravan.com

**Fecha de datos**: 14 de mayo de 2026
**Período analizado**: Últimos 3 meses (Feb–May 2026)

---

## 4.1 Inventario de schemas activos

La página de producto emite **4 bloques JSON-LD** distintos:

| Fuente | Schema types | Estado |
|--------|-------------|--------|
| Yoast SEO for Shopify | Organization, ImageObject, WebSite, ItemPage, ProductGroup, BreadcrumbList | ✅ Correcto |
| Tema Empire (theme.liquid) | Product (con aggregateRating), BreadcrumbList, WebSite | ⚠️ Duplicado parcial con Yoast |
| Judge.me (JavaScript async) | Review (individual, con reviewRating) | ❌ Falta `author` en 7 productos |
| Tema Empire | BreadcrumbList | ⚠️ Duplicado con Yoast |

### Configuración Judge.me detectada (product page source)

```json
"disable_json_ld": false,
"enable_json_ld_products": false
```

- `disable_json_ld: false` → JSON-LD habilitado globalmente
- `enable_json_ld_products: false` → Judge.me NO genera el bloque `Product` completo (correcto: evita duplicar el del tema), pero SÍ inyecta objetos `Review` individuales vía JavaScript

---

## 4.2 ProductGroup schema (Yoast) — estructura actual

```json
{
  "@type": "ProductGroup",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": 5.0,
    "reviewCount": 1
  },
  "hasVariant": [{
    "@type": "Product",
    "sku": "07430",
    "gtin": "8054633002544",
    "offers": {
      "@type": "Offer",
      "availability": "https://schema.org/InStock",
      "category": "Vehículos y recambios > ...",
      "priceSpecification": [...]
    }
  }]
}
```

**Puntos positivos**: usa `ProductGroup` + `hasVariant`, incluye `gtin`, `category`, `priceSpecification` con precio tachado.
**Punto pendiente**: no incluye `hasMerchantReturnPolicy` ni `shippingDetails` (ver P5).

---

## 4.3 Product schema (tema Empire) — estructura actual

```json
{
  "@context": "http://schema.org/",
  "@type": "Product",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "5.0",
    "reviewCount": "1"
  },
  "offers": {
    "@type": "Offer",
    "priceValidUntil": "2027-05-27"
  }
}
```

Este bloque es redundante con el de Yoast. No causa errores pero duplica información.

---

## 4.4 Error crítico: Review snippets sin `author` — P1 ✅ EN PROCESO

### Diagnóstico (27 mayo 2026)

GSC reporta error crítico en Review snippets para **7 productos**:

1. `/products/aire-acondicionado-telair-silent-3-8100h`
2. `/en-eu/products/air-conditioner-telair-dual-clima-8400h`
3. `/products/escalon-electrico-thule-slide-out-400-mm`
4. `/es-eu/products/aire-acondicionado-telair-silent-3-8100h`
5. `/products/kit-estabilizador-alko-aks-3004-con-antirrobo`
6. `/products/aire-acondicionado-telair-clima-e-van-7400h`
7. `/products/aire-acondicionado-telair-dual-clima-8400h`

**Causa raíz**: Judge.me inyecta objetos `Review` individuales via JavaScript para productos con reseñas. En estos 7 productos, las reseñas tienen el campo `name` del revisor vacío (enviadas como anónimas), lo que genera JSON-LD inválido:

```json
// ❌ Lo que genera Judge.me (inválido):
{
  "@type": "Review",
  "reviewRating": { "@type": "Rating", "ratingValue": "5" },
  "author": { "@type": "Person", "name": "" }  ← nombre vacío = error
}

// ✅ Lo que debería generar:
{
  "@type": "Review",
  "reviewRating": { "@type": "Rating", "ratingValue": "5" },
  "author": { "@type": "Person", "name": "Comprador Verificado" }
}
```

### Fix — Pasos en Judge.me Admin

**Paso 1**: Shopify Admin → Apps → Judge.me → **Manage Reviews**
- Filtrar por cada uno de los 7 handles de producto afectados
- Editar cada reseña → rellenar campo "Name" con el nombre del revisor o `Comprador Verificado`
- Guardar

**Paso 2**: Shopify Admin → Apps → Judge.me → **Settings** → sección "Rich Snippets" / "SEO"
- Verificar que "Enable rich snippets" está activado
- Buscar opción de nombre por defecto para reseñas anónimas y configurarla

**Paso 3**: Validar con Google Rich Results Test:
- URL de prueba: `https://search.google.com/test/rich-results`
- Introducir una de las 7 URLs afectadas
- Verificar que el error de `author` ha desaparecido

### KPI a medir

- GSC → Mejoras → Fragmentos de reseña: error "author faltante" baja a 0 URLs
- Impresiones en "Fragmento de reseña": >324 (valor actual del trim)
- Aparición de estrellas en SERP para los 7 productos en 2–4 semanas

---

## 4.5 AggregateRating — estado

`aggregateRating` presente y válido en todos los productos con reseñas. Fuentes:
- Tema Empire: `"ratingValue": "5.0", "reviewCount": "1"` (string format)
- Yoast: `"ratingValue": 5.0, "reviewCount": 1` (number format — más correcto)

Ambos son aceptados por Google. El formato numérico de Yoast es preferible.

---

## 4.6 Schemas pendientes de implementar

| Schema | Issue | Productos afectados | Prioridad |
|--------|-------|---------------------|-----------|
| `hasMerchantReturnPolicy` | P5 | 110 productos | Alta |
| `shippingDetails` | P5 | 110 productos | Alta |
| `priceValidUntil` | P14 | 53 productos | Media |
| `ItemList` en colecciones | P20 | Todas las colecciones | Baja |

---

## Referencias

- Issues: P1 (#1), P5 (#5), P14 (#14), P20 (#20)
- App de reviews: Judge.me (instalada desde bloque `shopify://apps/judge-me-reviews`)
- Tema: Empire v11.0.0 (FUTURA WEB, ID 160841826646)
- Yoast SEO for Shopify: activo, controla canonical y meta tags
