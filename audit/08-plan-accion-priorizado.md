# 08 · Plan de acción priorizado

> Matriz **Urgencia × Impacto** con esfuerzo estimado. Los Px son la prioridad numerada para ejecutar de arriba abajo.

## Criterios

- 🟥 **Urgencia ALTA**: bloquea SEO actual / pierde tráfico hoy mismo.
- 🟧 **Urgencia MEDIA**: limita crecimiento, no hace daño activo.
- 🟨 **Urgencia BAJA**: mejora, no fix.
- **Impacto ALTO**: potencial de cambiar la curva de tráfico orgánico.
- **Impacto MEDIO**: mejora medible pero acotada.
- **Impacto BAJO**: limpieza, pero suma con el resto.

---

## ⚡ Fase 1 — Quick wins críticos (1-2 semanas)

> Esfuerzo bajo, impacto inmediato visible en 2-6 semanas en GSC.

### P1 · Fix Review snippets sin `author` (7 productos)
- **Urgencia**: 🟥 Crítica — único error crítico de GSC
- **Impacto**: Alto — devuelve estrellas en SERP a productos top
- **Esfuerzo**: 30 min de edición en theme/app de reviews
- **Archivos relevantes**: `data/duplicadas-google-canonica.csv` (cruzar URLs).
- **Cómo**:
  1. Abrir el JSON-LD `Review` en el theme Shopify (típicamente en `snippets/product-schema.liquid` o similar).
  2. Para cada `Review` asegurar campo `author` con `@type: Person, name: <reviewer name>` (si no hay nombre, usar `"Verified Buyer"` o nombre del producto).
  3. Si las reviews vienen de Loox/Judge.me/Yotpo: revisar configuración del JSON-LD output de la app.
  4. Validar con Rich Results Test de Google.
- **KPI a medir**: impresiones en "Fragmento de reseña" (hoy 324), apertura de estrellas en SERP en los 7 productos.

### P2 · Resolver duplicación HTTP/www de la home
- **Urgencia**: 🟥 Crítica
- **Impacto**: Alto — recupera autoridad/tráfico hacia HTTPS canónica
- **Esfuerzo**: 30 min en config DNS/Shopify
- **Cómo**:
  1. Verificar en Shopify Admin que el dominio principal está marcado como `evacaravan.com` (sin www) HTTPS.
  2. Forzar 301 de las 3 variantes (`http://evacaravan.com`, `http://www.evacaravan.com`, `https://www.evacaravan.com`) hacia `https://evacaravan.com`.
  3. Solicitar reindexación de la home en GSC.
- **KPI**: consolidación de impresiones/clics en la versión https.

### P3 · Limpiar sitemap.xml de URLs 404 (24 URLs)
- **Urgencia**: 🟥 Crítica
- **Impacto**: Medio — directo en cobertura del sitemap (49% → mejor)
- **Esfuerzo**: 1-2 h
- **Cómo**:
  1. Descargar el sitemap actual (acceder con navegador desde una IP no bloqueada).
  2. Cruzar con `data/404-urls-reales.csv` y `data/404-urls-parametros.csv` (las 24 URLs son subconjunto).
  3. Identificar si:
     - Son productos descatalogados → archivar/eliminar el producto en Shopify (Shopify regenera sitemap).
     - Son URLs huérfanas → forzar regeneración del sitemap.
  4. Resubmit sitemap en GSC.

### P4 · Eliminar combinaciones hreflang fantasma (`en-at`, `en-nl`, `en-pt`, `en-it`, `en-be`, `en-fr`, `en-de`)
- **Urgencia**: 🟥 Crítica
- **Impacto**: Alto — elimina ~178 URLs 404 reales y reduce crawl waste
- **Esfuerzo**: 2-4 h
- **Cómo**:
  1. Revisar la configuración multi-mercado en Shopify (Markets/Internacional).
  2. Decidir: o bien activar inglés correctamente para estos países (con contenido), o bien desactivar la opción y servir `es-es` o `en-eu`.
  3. Asegurar que el selector de país NO genera links a estas combinaciones.
  4. Servir 410 (Gone) o 301 desde estas URLs a la versión correcta (`en-eu` típicamente).
- **KPI**: bajada en GSC del número de 404 reportados; mejora en "rastreadas no indexadas".

### P5 · Fix `hasMerchantReturnPolicy` + `shippingDetails` en schema producto (110 productos)
- **Urgencia**: 🟧 Alta (Google endurece requisitos)
- **Impacto**: Alto — protege/mejora Fichas de Comerciante (mejor CTR del site)
- **Esfuerzo**: 1-2 h (single fix en theme)
- **Cómo**:
  1. Editar `snippets/product-schema.liquid` (o equivalente) y añadir dentro de `offers`:
     ```json
     "shippingDetails": {
       "@type": "OfferShippingDetails",
       "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "EUR"},
       "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "ES"},
       "deliveryTime": {"@type": "ShippingDeliveryTime", "handlingTime": {...}, "transitTime": {...}}
     },
     "hasMerchantReturnPolicy": {
       "@type": "MerchantReturnPolicy",
       "applicableCountry": "ES",
       "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
       "merchantReturnDays": 14,
       "returnMethod": "https://schema.org/ReturnByMail",
       "returnFees": "https://schema.org/FreeReturn"
     }
     ```
  2. Adaptar los valores reales a tu política.
  3. Validar con Rich Results Test.
- **KPI**: validación masiva en Search Console > Merchant listings.

---

## 🚀 Fase 2 — Recuperación de tráfico (2-6 semanas)

### P6 · Crear landing/colección "Cerraduras para furgonetas" optimizada
- **Urgencia**: 🟧 Alta
- **Impacto**: 🟥 **MUY ALTO** — clúster con >11.500 impresiones/trimestre a 0 clics
- **Esfuerzo**: 4-8 h (contenido + organización)
- **Cómo**:
  1. Crear colección `/collections/cerraduras-furgonetas` (slug exacto importa).
  2. Incluir: Meroni UFO, Thule Van Lock, Daken Saturn Go, Heosafe, Fiamma Safe Door, Milenco Floor Lock — todos los 100+ productos del catálogo.
  3. H1: "Cerraduras de seguridad para furgonetas camperizadas".
  4. Texto SEO: 400-600 palabras explicando tipos (interna, externa, suplementaria), normativa (EN 1303), instalación, modelos populares.
  5. Filtros: por marca, por tipo (UFO, mortise, slider), por compatibilidad (Fiat Ducato, Mercedes Sprinter, Renault Trafic…).
  6. Internal linking desde home, blog y productos relacionados.
- **KPI**: clics en cluster "cerradura furgoneta*" (objetivo: pasar de 1 a >50 clics/mes en 8 semanas).

### P7 · Traducir realmente las 50 páginas alemanas/francesas con más impresiones
- **Urgencia**: 🟧 Alta
- **Impacto**: 🟥 Alto — resuelve los 410 productos "canónica ignorada"
- **Esfuerzo**: 2-4 semanas con traductor humano o sistema (Weglot/Langify)
- **Cómo**:
  1. Cruzar `data/duplicadas-google-canonica.csv` con `data/paginas-top-rendimiento.csv` para priorizar las 50 con más impresiones.
  2. Asegurar título, meta description, H1, descripción del producto y FAQ traducidos *de verdad* (no contenido en español con URL alemana).
  3. Especial atención a:
     - `/de-de/products/truma-therme-220v-warmwasserbereiter` (3.355 impresiones)
     - `/de-de/products/thule-transporter-schloss-sicherheitsschloss` (608 impresiones)
     - `/de/products/thule-transporter-schloss-sicherheitsschloss` (527 impresiones)
- **KPI**: ratio "Duplicada Google canónica distinta" en GSC; CTR Alemania (hoy 1,18 %, objetivo 2,5 %).

### P8 · Implementar app de reviews + invitar a primeros 100 clientes
- **Urgencia**: 🟧 Alta
- **Impacto**: 🟥 Alto — habilita estrellas SERP en todo el catálogo
- **Esfuerzo**: 2-3 días setup + onboarding
- **Cómo**:
  1. Instalar Loox o Judge.me (recomendado por integración Shopify y JSON-LD nativo).
  2. Configurar emails automáticos post-compra (a 14 días).
  3. Importar/migrar reviews existentes (los 33 productos con rating actuales).
  4. Configurar el snippet del JSON-LD para que incluya `author` (cierra también P1 a futuro).
- **KPI**: % productos con reviews (hoy 1,96 %, objetivo 30 % en 6 meses).

### P9 · Asignar categoría Google product a los 1.381 productos sin ella
- **Urgencia**: 🟧 Media-alta
- **Impacto**: Medio-alto — habilita Shopping/Merchant en muchos productos
- **Esfuerzo**: 1-2 días con bulk editor
- **Cómo**: usar `data/productos-sin-categoria-google.csv`. Agrupar por `tipo producto` y asignar masivamente:
  - Aire acondicionado → `Vehicles & Parts > ... > Motor Vehicle Climate Control Parts`
  - Cocinas → `Vehicles & Parts > ... > Motor Vehicle Camping Equipment`
  - etc.

### P10 · Mejorar contenido de las 5 colecciones débiles top-impresión
- **Urgencia**: 🟧 Media
- **Impacto**: Medio-alto
- **Esfuerzo**: 1-2 días
- **Páginas**: 
  - `/collections/acampada-exteriores-alfombras` (106 clics, 3.244 impr, pos 13 → optimizar a top 10)
  - `/collections/remolque-chasis-nivelacion-movers-caravana` (15 clics, 1.145 impr, pos 12)
  - `/collections/acampada-exteriores-parasoles-aislantes-termicos-caravanas` (13 clics, 1.338 impr, pos 22)
  - Crear/optimizar "antenas para caravanas" (432 impr, pos 20)
  - Crear/optimizar "claraboya autocaravana" (404 impr, pos 42)

---

## 🛠️ Fase 3 — Limpieza estructural (1-3 meses)

### P11 · Fix 530 URLs 404 reales (sin parámetros)
- **Urgencia**: 🟨 Media
- **Impacto**: Medio
- **Esfuerzo**: 1-2 días
- **Cómo**:
  1. Para los productos descatalogados con tráfico: **301 a producto sustituto** o colección padre.
  2. Para los productos sin tráfico ni sustituto: dejar 404 (correcto) pero quitar enlaces internos hacia ellos.
  3. Usar `data/404-urls-reales.csv`.
- **KPI**: bajada de 4.568 → <500 en GSC.

### P12 · Productos sin `disponibilidad` / `estado` (320 + 299 productos)
- **Urgencia**: 🟨 Media
- **Impacto**: Medio (Shopping)
- **Esfuerzo**: 4-8 h con bulk editor
- **Cómo**: revisar `data/productos-sin-disponibilidad.csv` y `data/productos-sin-estado.csv`, decidir si archivar o completar metadatos.

### P13 · Auditar las 19.715 "Rastreadas, no indexadas"
- **Urgencia**: 🟨 Media
- **Impacto**: Alto a medio plazo
- **Esfuerzo**: 3-5 días (análisis), semanas (ejecución)
- **Cómo**:
  1. Empezar por las que están en el sitemap (2.468 → muestra en `data/rastreadas-sin-indexar.csv`).
  2. Identificar páginas con descripción <50 palabras → reescribir.
  3. Identificar páginas con contenido idéntico a otra (cross-locale sin traducción) → traducir o canonicalizar.
  4. Identificar colecciones con ≤2 productos → consolidar/eliminar.

### P14 · Fix priceValidUntil (53 productos)
- **Urgencia**: 🟨 Baja
- **Impacto**: Bajo-medio
- **Esfuerzo**: 1 h theme edit (añadir fecha de fin de oferta o fecha lejana).

### P15 · Bloquear endpoints AJAX en versiones locale
- **Urgencia**: 🟨 Baja
- **Impacto**: Bajo
- **Esfuerzo**: 30 min
- **Cómo**: añadir a robots.txt (o config Shopify si lo permite):
  ```
  Disallow: /*/search/suggest
  Disallow: /*/cart/add
  Disallow: /*/cart/change
  ```

### P16 · Limpiar feeds `.atom` indexables
- **Urgencia**: 🟨 Baja
- **Impacto**: Bajo
- **Esfuerzo**: 1 h
- **Cómo**: servir `X-Robots-Tag: noindex` desde `*.atom` o canonicalizar.

### P17 · Auditar `localitybiz.es` y considerar disavow
- **Urgencia**: 🟨 Baja
- **Impacto**: Variable (de preventivo a corrector)
- **Esfuerzo**: 1-2 h investigación + setup disavow
- **Cómo**: 
  1. Visitar muestra de páginas en `localitybiz.es` que enlazan.
  2. Si son páginas de baja calidad (texto auto-generado, contenido pobre), considerar disavow.
  3. Si son legítimas, dejar.

### P18 · Solicitar enlaces a fabricantes oficiales (Fiamma, Thule, Truma, Dometic, Meroni, AL-KO)
- **Urgencia**: 🟨 Baja-media
- **Impacto**: Medio (en 3-6 meses)
- **Esfuerzo**: outreach por email
- **Cómo**: contactar departamento comercial de cada fabricante solicitando inclusión como distribuidor oficial en sus webs.

---

## 📊 Fase 4 — Crecimiento estratégico (3-12 meses)

### P19 · Estrategia de contenido (blog)
- Crear guías técnicas indexables:
  - Cómo elegir cerradura furgoneta (ataca clúster identificado)
  - Comparativa aires acondicionados Telair vs Truma vs Dometic
  - Antenas para caravana: terrestre vs satélite vs omnidireccional
  - Mantenimiento de calefacción Truma
  - Instalación de movers Enduro EM313A paso a paso
- Cada artículo debe enlazar internamente a 5-10 productos/colecciones.

### P20 · Schema mejorado en colecciones
- Implementar `ItemList` + `Product` parcial en páginas de colección.
- Aumenta probabilidad de aparecer como "lista" en SERP.

### P21 · Migrar facetas a sistema con `nofollow` o JS
- Reduce drásticamente las 29.136 URLs bloqueadas por robots.txt y elimina el waste de crawl en filtros combinados.

### P22 · Construcción de backlinks editorial
- 5-10 backlinks de medios especializados/blogs camper en 6 meses.

---

## Mapa visual de prioridades

```
URGENCIA ↑
🟥 P1  P2  P3  P4  P5
       │   │       │
       │   │   ┌───┘
🟧 P6  P7  P8  P9  P10
       │
🟨 P11 P12 P13 P14 P15 P16 P17 P18
🟩 P19 P20 P21 P22
   ────────────────────→ IMPACTO
```

---

## Tracking del progreso

Cada acción ejecutada se documenta como un commit en este repo con prefijo `[Pn]`:
```
[P1] Fix Review snippets author en 7 productos
[P3] Sitemap saneado: quitadas 24 URLs en 404
[P4] Eliminadas combinaciones hreflang en-at/en-nl/en-pt/en-it/en-be/en-fr/en-de
…
```

Los archivos CSV en [`data/`](./data/) son la fuente de verdad para verificar progreso (recrear con el script de extracción cuando llegue un nuevo export GSC).
