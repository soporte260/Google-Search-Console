# Performance on Search — evacaravan.com

**Fecha de datos**: 14 de mayo de 2026  
**Período**: Últimos 3 meses (Feb–May 2026)  
**Tipo de búsqueda**: Web

---

## 3.1 Métricas globales

| Métrica | Valor |
|---------|-------|
| Clics totales | ~3.072 |
| Impresiones totales | ~151.983 |
| CTR medio | ~2,02% |
| Posición media | ~15,7 |

### Por país

| País | Clics | Impresiones | CTR | Posición |
|------|-------|-------------|-----|----------|
| España | 2.276 | 99.332 | 2,29% | 17,33 |
| Alemania | 235 | 19.886 | 1,18% | 11,49 |
| Francia | 113 | 5.047 | 2,24% | 14,09 |

### Por dispositivo

| Dispositivo | Clics | Impresiones | CTR | Posición |
|-------------|-------|-------------|-----|----------|
| Móvil | 1.973 | 79.639 | 2,48% | 12,82 |
| Ordenador | 1.024 | 69.897 | 1,47% | 18,01 |
| Tablet | 75 | 2.447 | 3,06% | 12,43 |

### Por tipo de aparición en búsqueda

| Tipo | Clics | Impresiones | CTR | Posición |
|------|-------|-------------|-----|----------|
| Fragmentos de productos | 1.752 | 115.596 | 1,52% | 17,83 |
| Fichas de comerciantes | 214 | 3.509 | **6,10%** | 3,58 |
| Fragmento de reseña | 3 | 324 | 0,93% | 7,36 |

> Las Fichas de Comerciante tienen el CTR más alto (6,10%) — priorizar P5 (shippingDetails) y P8 (reviews).

---

## 3.2 Páginas con mayor tráfico

| URL | Clics | Impresiones | CTR | Posición |
|-----|-------|-------------|-----|----------|
| `https://evacaravan.com/` | 406 | 4.185 | 9,70% | 25,37 |
| `http://www.evacaravan.com/` ⚠️ | 156 | 4.273 | 3,65% | 6,48 |
| `/collections/acampada-exteriores-alfombras` | 106 | 3.244 | 3,27% | 13,37 |
| `/products/aire-acondicionado-telair-clima-e-van-7400h` | 100 | 1.184 | 8,45% | 4,17 |
| `/products/mover-enduro-em313a-asistente-maniobras-caravana` | 50 | 1.104 | 4,53% | 5,09 |

> ⚠️ La URL HTTP/www de la home representa el 28% de los clics totales de la home y tiene mejor posición (6,48). Ver P2 para la corrección.

---

## 3.3 Home page — impacto de la duplicación (P2)

Situación actual:
- `https://evacaravan.com/`: posición 25,37 — pierde clics potenciales por ranking bajo
- `http://www.evacaravan.com/`: posición 6,48 — buena posición pero CTR bajo por HTTP

Tras corregir con 301 y consolidar autoridad:
- Posición esperada consolidada: cercana a 6–10
- CTR esperado con HTTPS + posición top: >8%
- **Clics potenciales**: 8.458 impr × 8% CTR = ~676 clics (vs 562 actuales) = +20% solo por esta corrección

---

## 3.4 Consultas con más impresiones y 0 clics (oportunidades P6)

El clúster de "cerradura furgoneta" es la mayor oportunidad no capturada:

| Consulta | Impresiones | Posición |
|----------|-------------|----------|
| cerraduras de seguridad para furgonetas | 1.097 | 44,56 |
| cerradura para furgonetas | 1.084 | 44,58 |
| cerraduras para furgonetas | 1.081 | 40,48 |
| cerradura furgoneta | 1.008 | 50,03 |
| cerradura seguridad furgoneta | 979 | 45,58 |
| cerraduras furgonetas | 948 | 43,18 |
| cerraduras seguridad furgonetas | 913 | 57,95 |
| cerraduras de seguridad para furgoneta | 815 | 35,44 |
| cerradura meroni | 631 | 10,76 |
| cerradura ufo | 544 | 11,49 |
| **TOTAL clúster estimado** | **~11.500** | >35 |

> Crear landing `/collections/cerraduras-para-furgonetas` (ver P6) podría capturar 300–500 clics/mes en 8–10 semanas.

---

## 3.5 La versión HTTP/www como síntoma de autoridad

La posición 6,48 de `http://www.evacaravan.com/` indica que esta URL acumula backlinks históricos relevantes. Los 214 enlaces registrados en GSC (200 de localitybiz.es) apuntan mayoritariamente a la versión www. Tras la consolidación con 301, toda esa autoridad pasará a la versión canónica HTTPS.

---

## 3.6 Páginas con alta oportunidad de CTR

Páginas con >200 impresiones y CTR <5% (muestra):

| URL | Impr | CTR | Posición |
|-----|------|-----|----------|
| `/collections/seguridad-antirrobo` | 5.348 | 0,17% | 40,03 |
| `/collections/seguridad-antirrobo-cerraduras` | 4.918 | 0,24% | 38,00 |
| `http://www.evacaravan.com/` | 4.273 | 3,65% | 6,48 |
| `/de-de/products/truma-therme-220v-warmwasserbereiter` | 3.355 | 0,72% | 8,29 |
| `/collections/acampada-exteriores-alfombras` | 3.244 | 3,27% | 13,37 |
| `/products/cerradura-meroni-ufo-plus` | 2.440 | 0,86% | 9,07 |

> `/collections/seguridad-antirrobo` con 5.348 impresiones y CTR 0,17% tiene posición media 40 — necesita contenido SEO y optimización de colección (ver P10).

---

## 3.7 Alemania: CTR bajo por contenido en español (P7)

Alemania genera 19.886 impresiones/trimestre (13% del total) con CTR 1,18% vs 2,29% en España.

Las páginas alemanas con más impresiones y bajo CTR:
- `/de-de/products/truma-therme-220v-warmwasserbereiter`: 3.355 impr, 0,72% CTR, pos 8,29
- Productos Thule con nombres en español pero locale DE

→ Traducción real al alemán puede doblar el CTR (de 1,18% a ~2,5%), añadiendo ~235 clics más/trimestre.

---

## 3.8 Colecciones con mayor potencial de optimización (P10)

| Colección | Clics | Impr | CTR | Posición | Acción |
|-----------|-------|------|-----|----------|--------|
| `alfombras` | 106 | 3.244 | 3,27% | 13,37 | Entrar top 10 |
| `seguridad-antirrobo` | 9 | 5.348 | 0,17% | 40,03 | Texto SEO + mejorar posición |
| `seguridad-antirrobo-cerraduras` | 12 | 4.918 | 0,24% | 38,00 | Texto SEO + mejorar posición |
| `remolque-chasis-nivelacion-movers-caravana` | 15 | 1.145 | 1,31% | 12,31 | Mejorar para top 10 |

---

## Referencias

- Issues: P2 (#2), P6 (#6), P7 (#7), P10 (#10)
- Datos fuente: `evacaravan.com-Performance-on-Search-2026-05-14.xlsx`
- CSVs: `audit/data/paginas-top-rendimiento.csv`, `audit/data/paginas-oportunidad-ctr.csv`, `audit/data/consultas-oportunidad-cero-clics.csv`
