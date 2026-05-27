# Progreso auditoría SEO — evacaravan.com
Datos base: GSC export 14-05-2026 | Ratio indexación actual: **49%**

---

## ✅ [P3] — 24 URLs en 404 en sitemap.xml — RESUELTO

**Causa:** 3 colecciones renombradas/eliminadas sin redirect previo, multiplicadas por los 9 mercados de Shopify (Alemania, Austria, Bélgica, Francia, Italia, Países Bajos, Portugal, Resto Europa, Spain) × 7 idiomas publicados.

**Colecciones eliminadas:**
- `climatizacion-camper` → `/collections/climatizacion-frio-claraboyas-caravana`
- `cocina-gas-neveras` → `/collections/cocina-gas`
- `protector-para-cabina` → `/collections/seguridad-antirrobo`

**Producto eliminado:**
- `nevera-compresor-thetford-t1090-de-90-l` → `/collections/climatizacion-frio-aires-acondicionados`
- `ce-con-el-remolque-acoplado-y-en-la-otra-las-medidas` → `/` (URL basura)

**Acciones completadas:**
- [x] 31 redirects importados en Shopify Admin → Navegación → Redirecciones URL (30 nuevos + 1 actualizado)
- [x] Verificación manual de redirects: OK
- [x] Validación iniciada en GSC
- [x] Mercados y Translate & Adapt revisados — configuración correcta, no requiere cambios

**Archivos generados:**
- `P3_sitemap_404_redirects_shopify.csv` — CSV importado en Shopify
- `P3_clean_404_redirects_full.csv` — análisis completo de 110 URLs limpias en 404

**Regla para el futuro:** Añadir redirect ANTES de eliminar cualquier colección o producto.

---

## 🔜 Pendientes (por prioridad)

Los problemas identificados en GSC a 14-05-2026 (Sitemap: Todas las páginas conocidas):

| # | Incidencia | URLs afectadas | Impacto |
|---|---|---|---|
| P1 | Bloqueada por robots.txt | 29.136 | Crítico |
| P2 | Página alternativa con etiqueta canónica adecuada | 10.501 | Crítico |
| — | ~~404 en sitemap.xml~~ | ~~24~~ | ✅ Resuelto |
| P4 | Página con redirección (en sitemap) | 8.075 | Alto |
| P5 | No se ha encontrado (404) — total rastreo | 4.568 | Alto |
| P6 | Excluida por noindex | 1.464 | Medio |
| P7 | Rastreada: sin indexar | 19.715 | Crítico |
| P8 | Error de redirección | 42 | Medio |
| P9 | Bloqueada por otro 4xx | 27 | Medio |
| P10 | Duplicada sin canónica | 26 | Bajo |

**Próximo a trabajar:** El que el usuario indique al inicio de la nueva sesión.

---

## Contexto técnico del sitio

- **Plataforma:** Shopify
- **Dominio:** evacaravan.com
- **Mercados activos:** Alemania, Austria, Bélgica, Francia, Italia, Países Bajos, Portugal, Resto Europa (16 regiones), Spain, Suecia
- **Idiomas publicados:** Español (predeterminado), Alemán, Francés, Holandés, Inglés, Italiano, Portugués
- **App traducción:** Translate & Adapt (nativa Shopify)
- **Productos en catálogo:** ~739 slugs únicos / 3.158 variantes en TSV
- **Colecciones activas:** 34 (ver `P3_clean_404_redirects_full.csv` para listado completo)
