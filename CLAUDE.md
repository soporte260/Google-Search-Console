# Proyecto: Auditoría SEO evacaravan.com

## Contexto esencial
- **Sitio**: Tienda Shopify multi-idioma/multi-país (caravanas/camper)
- **Rama de trabajo**: `claude/audit-evacaravan-seo-Dwvc0`
- **Datos GSC**: `/home/user/Google-Search-Console/audit/` (no releer los .xlsx salvo que sea estrictamente necesario)
- **Estado de tareas**: `audit/acciones/README.md`

## Cómo arrancar una sesión nueva

1. Leer `audit/acciones/README.md` para ver qué tarea sigue.
2. Si la tarea tiene doc en `audit/acciones/P*.md`, leerlo.
3. Ejecutar. Hacer commit al terminar cada paso significativo.
4. Actualizar estado en `audit/acciones/README.md` y en el doc de la tarea.

**Comando rápido**: `/next-task` — localiza la próxima tarea pendiente y arranca.

## Estado del proyecto (actualizar aquí al cerrar cada tarea)

| # | Tarea | Estado |
|---|---|---|
| P1 | Fix Review snippets sin `author` | ✅ Fix aplicado — GSC validación pendiente 2026-05-29 |
| P2 | Resolver duplicación HTTP/www vs HTTPS | ⏸ Pendiente |
| P3 | Limpiar sitemap.xml (24 URLs 404) | ⏸ Pendiente |
| P4 | Eliminar hreflang fantasma | ⏸ Pendiente |
| P5 | hasMerchantReturnPolicy + shippingDetails | ⏸ Pendiente |
| P6 | Landing "Cerraduras para furgonetas" | ⏸ Pendiente |
| P7 | Traducir páginas DE/FR top | ⏸ Pendiente |
| P8 | Configurar Judge.me + campaign reviews | ⏸ Pendiente |
| P9 | Categoría Google product (1.381 productos) | ⏸ Pendiente |
| P10 | Optimizar 5 colecciones débiles | ⏸ Pendiente |
| P11 | Redirigir 530 URLs 404 reales | ⏸ Pendiente |
| P12 | 320 disponibilidad + 299 estado | ⏸ Pendiente |
| P13 | Auditar 2.468 rastreadas no indexadas | ⏸ Pendiente |
| P14 | priceValidUntil (53 productos) | ⏸ Pendiente |
| P15 | Bloquear AJAX en robots.txt locales | ⏸ Pendiente |
| P16 | Eliminar/noindex feeds .atom | ⏸ Pendiente |
| P17 | Auditar localitybiz.es (disavow?) | ⏸ Pendiente |
| P18 | Backlinks a fabricantes | ⏸ Pendiente |
| P19 | Estrategia de contenido blog | ⏸ Pendiente |
| P20 | Schema ItemList en colecciones | ⏸ Pendiente |
| P21 | Facetas con nofollow/JS | ⏸ Pendiente |
| P22 | Backlinks editoriales | ⏸ Pendiente |
| EXTRA | Fix 4 GTINs + 3 descripciones largas | ⏸ Pendiente |

## Convenciones

- **Commits**: prefijo `[Pn]` — ej. `[P2] Fix HTTP→HTTPS redirección home`
- **Rama**: siempre `claude/audit-evacaravan-seo-Dwvc0`, nunca main
- **Shopify tema**: archivo clave es `snippets/structured-data.liquid`
- **Datos**: los CSV en `audit/data/` son la fuente de verdad para cada tarea

## Lo que NO hacer (ahorra tokens)

- No releer los `.xlsx` — ya están procesados en los CSV de `audit/data/`
- No releer `audit/01-*.md` a `audit/08-*.md` salvo necesidad específica
- No explorar el repo completo — ir directo al doc de la tarea

## Herramientas disponibles

- **MCP Shopify** (`mcp__be728d7a-...`): productos, colecciones, GraphQL — requiere reautorización cada sesión
- **Shopify CLI**: para editar archivos de tema (instalar si no está: `npm install -g @shopify/cli @shopify/theme`)
- **GitHub MCP**: repo `soporte260/Google-Search-Console`
