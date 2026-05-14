# Auditoría SEO — evacaravan.com

> **Fecha de extracción de datos**: 2026-05-14
> **Periodo analizado en GSC**: 2026-02-13 → 2026-05-12 (90 días)
> **Tipo de sitio**: Tienda Shopify multi-idioma/multi-país (caravanas/camper)
> **Catálogo**: 1.682 productos en feed; ~6.315 URLs en sitemap conocidas por Google

---

## Índice de la auditoría

| Documento | Contenido |
|---|---|
| [`01-resumen-ejecutivo.md`](./01-resumen-ejecutivo.md) | KPIs principales y diagnóstico de una página |
| [`02-indexacion.md`](./02-indexacion.md) | Análisis profundo de cobertura, hreflang y canónicas |
| [`03-performance-search.md`](./03-performance-search.md) | Tráfico orgánico, consultas y oportunidades |
| [`04-schemas.md`](./04-schemas.md) | Rich snippets: Merchant, Product, Review, Breadcrumb |
| [`05-tecnico.md`](./05-tecnico.md) | Problemas técnicos: 404, redirecciones, parámetros |
| [`06-feed-shopping.md`](./06-feed-shopping.md) | Análisis del feed de productos (TSV de Merchant) |
| [`07-enlaces-externos.md`](./07-enlaces-externos.md) | Perfil de backlinks |
| [`08-plan-accion-priorizado.md`](./08-plan-accion-priorizado.md) | **Roadmap priorizado (urgencia × impacto)** |
| [`data/`](./data/) | CSV de URLs/consultas problemáticas para ejecución |

---

## Diagnóstico en 30 segundos

🟥 **CRÍTICO**: Sólo **3.090 de 6.315 URLs del sitemap están indexadas (49%)**. Sobre toda la propiedad, **74.320 páginas no indexadas vs 4.059 indexadas (5,2%)**.

🟧 **URGENTE**: **530 URLs reales devuelven 404** (sin contar las que tienen parámetros), 24 de ellas están en el sitemap. La mayoría son combinaciones hreflang inexistentes (`/en-at/`, `/en-nl/`, `/en-pt/`, etc.).

🟧 **URGENTE**: **410 productos** tienen "canónica distinta a la del usuario" en versiones francesas (`fr-fr`, `fr-be`) y alemanas (`de-de`, `de-at`) — el contenido no está realmente traducido y Google los une con la versión española.

🟨 **ALTO IMPACTO**: 8 consultas de **"cerraduras para furgonetas"** generan **>7.000 impresiones mensuales con 0 clics** (posición media 40-50). Producto con potencial enorme sin landing optimizada.

🟨 **MEDIO**: 7 URLs producto sin `author` en review schema (problema crítico en Review snippets). Faltan campos `hasMerchantReturnPolicy` y `shippingDetails` en 110 productos del feed Merchant.

🟩 **OPORTUNIDAD**: La marca "eva caravan" tiene un CTR del **53,8%** y posición media 2 — el branding funciona. El problema es que se traduce en poco tráfico genérico no marca.

---

## Workflow de este proyecto

Este repo guarda el progreso de la auditoría y de las acciones implementadas. Cada cambio relevante se commitea en la rama `claude/audit-evacaravan-seo-Dwvc0`.

**Próximos pasos sugeridos** (priorizados en [`08-plan-accion-priorizado.md`](./08-plan-accion-priorizado.md)):

1. Eliminar combinaciones hreflang inexistentes (`en-at`, `en-nl`, `en-pt`, `en-it`, `en-be`, `en-fr`, `en-de`) o configurarlas correctamente.
2. Añadir `author` y `hasMerchantReturnPolicy`/`shippingDetails` al schema de productos.
3. Crear/optimizar landing para clúster "cerradura/cerraduras furgoneta(s)".
4. Limpieza del sitemap: quitar 24 URLs 404 que están en él.
5. Mejorar contenido o consolidar las 2.468 URLs "rastreadas, no indexadas" del sitemap.
