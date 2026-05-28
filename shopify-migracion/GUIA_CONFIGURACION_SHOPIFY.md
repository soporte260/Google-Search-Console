# Guía: replicar la lógica de precios y envíos de Amazon en Shopify

Objetivo: que tu web (evacaravan.com) calcule precio, IVA y envío igual que tu
Excel "EL SANTO GRIAL", con **6 mercados** y **un idioma por mercado**.

> **Idea clave**: el **precio NETO (sin IVA) es el ancla**. El IVA "flota" según
> el país al que se envía, y eso Shopify lo hace **de forma nativa** con un
> interruptor. El envío va por **peso × zona** (tablas GLS/UPS). Tú ya tienes
> los precios calculados; aquí solo los trasladamos a Shopify.

---

## Modelo de envío elegido: HÍBRIDO

| Mercado | URL | Envío |
|---|---|---|
| Principal (España + Portugal) | `evacaravan.com` | **Incluido** (gratis a península; diferencia a Baleares/Portugal) |
| Alemania | `/de` | **Incluido** (Austria: diferencia) |
| Francia | `/fr` | **Incluido** |
| Italia | `/it` | **Incluido** |
| Benelux | `/bx` | **Incluido** |
| Resto UE | `/eu` | **Real en el checkout** (zonas muy dispares) |

---

## Orden de trabajo (de mayor a menor impacto)

### PASO 1 — Impuestos (resuelve solo el 80% del problema)
`Configuración → Impuestos y aranceles`

1. **Date de alta en la Ventanilla Única (OSS)** de la UE (una sola alta cubre
   toda la UE) y mete el número en Shopify → sección *Unión Europea*. A partir
   de ahí Shopify cobra **el IVA del país de destino** automáticamente
   (Hungría 27 %, Italia 22 %, etc.).
2. Activa **"Mostrar todos los precios con impuestos incluidos"** (precios IVA
   incluido).
3. Activa **"Incluir o excluir impuestos según el país del cliente"**.
   - Esto hace *literalmente* tu fórmula: **mantiene el neto y cambia el IVA**.
   - Ejemplo Francia→Hungría: un producto a 100 € (IVA FR 20 %, neto 83,33 €)
     se le muestra al cliente húngaro a **83,33 × 1,27 = 105,83 €**. Exacto.

> Con esto, **dentro de cada mercado** el IVA ya se ajusta solo a cada país
> (España↔Portugal, Bélgica↔Países Bajos↔Luxemburgo, y todos los del `/eu`).

### PASO 2 — Mercados
`Configuración → Mercados`

1. Consolida los mercados actuales en estos **6** (mueve países a estos grupos):
   - **Principal**: España + Portugal (en el dominio raíz)
   - **/de**: Alemania (+ Austria)
   - **/fr**: Francia (+ Mónaco)
   - **/it**: Italia
   - **/bx**: Bélgica, Países Bajos, Luxemburgo
   - **/eu**: resto de países de la UE
2. En cada mercado → *Dominios e idiomas* → **Formato de URL = subcarpeta**
   para obtener `/de`, `/fr`, `/it`, `/bx`, `/eu`.
3. Ignora por ahora las sugerencias de crear EE. UU. y Reino Unido (fuera de la UE).

### PASO 3 — Idiomas (uno por mercado)
`Configuración → Idiomas` y dentro de cada mercado → *Idiomas*.

| Mercado | Idioma(s) publicado(s) |
|---|---|
| Principal | Español (predeterminado) + Portugués |
| /de | Alemán |
| /fr | Francés |
| /it | Italiano |
| /bx | Francés + Neerlandés |
| /eu | Inglés |

- Deja de publicar los idiomas que no correspondan a cada mercado (hoy tienes
  los 7 publicados en todos).
- Traduce con la app gratuita **Translate & Adapt** (o Weglot/Langify si quieres
  traducción automática asistida).

### PASO 4 — Precios por mercado
Cada mercado lleva su **lista de precios (catálogo)** porque tu margen y tu
envío cambian por mercado. **Ya los tienes calculados** en los CSV adjuntos.

- `precios_ES_PT.csv`, `precios_DE.csv`, `precios_FR.csv`, `precios_IT.csv`,
  `precios_BX.csv`, `precios_EU.csv` → columna **Price = PVP con IVA** del mercado.
- `precios_MAESTRO_comparativa.csv` → todos los mercados en una tabla para revisar.

Cómo importarlos:
- **Recomendado**: app **Matrixify** (importa catálogos/listas por mercado desde CSV).
- **Nativo**: en *Mercados → [mercado] → Productos y precios* puedes fijar precios
  por catálogo (manual o exportando/importando el CSV de catálogo de Shopify).

> El precio se introduce **IVA incluido** al tipo de referencia del mercado
> (ES 21 %, DE 19 %, FR 20 %, IT 22 %, BX 21 %, EU ref. 21 %). Shopify recalcula
> el IVA para los demás países del mercado (gracias al Paso 1).

Notas de los mercados nuevos:
- **BX**: calculado con el **mismo margen por producto que Francia**, envío UPS
  Benelux incluido. Para Luxemburgo (IVA 17 %) Shopify mostrará algo más barato.
- **EU**: calculado con el **mismo margen por producto que Francia** pero **SIN
  envío incluido** (por eso el PVP parece bajo: el cliente paga el envío en el
  checkout). Revisa la columna `MARGEN_FR` por si quieres subir margen en `/eu`.

### PASO 5 — Pesos de producto
`productos` → peso de cada variante. Usa `pesos_facturables.csv`:

- Carga **PESO_FACTURABLE_GRAMOS** como peso de la variante en Shopify.
- Es el mayor entre el peso real y el **volumétrico de UPS (÷5000)**, que es el
  que determina lo que te cobra el transportista en los envíos que SÍ cobras.
- Shopify no calcula peso volumétrico solo; por eso lo precargamos aquí.

### PASO 6 — Envíos (zonas + tarifas)
`Configuración → Envíos y entrega → perfiles → zonas y tarifas`.

1. Crea las **zonas** agrupando países según `envios_zonas_y_paises.csv`.
2. Mete las **tarifas por tramo de peso** de `envios_tarifas_por_peso_CONIVA.csv`
   (columnas según zona). Aplica el modelo híbrido:
   - Mercados con envío **incluido** (ES/PT, DE, FR, IT, BX): la **zona estándar
     = Gratis** (ya va en el precio). Para destinos más caros del mismo mercado
     (Baleares, Portugal, Austria) crea una tarifa = **DIF** (la diferencia).
     - Ej.: Portugal tramo 0-1 kg → cobra **1,95 €** (col `DIF_PT`).
   - Mercado **/eu** (envío real): mete la tarifa **completa** por peso de la
     zona correspondiente (Pol-Chequia / Suecia-Austria-Irlanda / Benelux).

---

## Cómo se valida tu ejemplo (Francia → Hungría)

1. El producto en `/fr` está a, p. ej., **100 €** (IVA FR 20 % incluido → neto 83,33 €).
2. Cliente francés que envía a **Hungría**: Shopify (Paso 1) recalcula el IVA →
   **83,33 × 1,27 = 105,83 €**. ✅ Igual que tu Excel.
3. Envío: si Francia iba incluido (gratis) y Hungría cuesta más, en `/eu` se
   cobra la tarifa real de la zona Pol-Chequia por peso. ✅

---

## Avisos importantes

- **El ÷1,21 del envío es tu COSTE, no lo que cobras.** El transportista te
  factura IVA español (recuperable). Lo que cobras al cliente lleva el IVA del
  país de destino (lo gestiona Shopify con OSS). No lo cuentes dos veces.
- **Mismo SKU/EAN en todos los mercados**: el catálogo solo cambia el precio,
  no duplica productos.
- **Margen por producto**: tus hojas tienen márgenes curados por producto
  (0,125–0,43, algunos en blanco). Se han respetado tal cual; para BX/EU se ha
  reutilizado el de Francia (revisable en `precios_MAESTRO_comparativa.csv`).
- **Divisa**: todo en EUR. Si quieres SEK/PLN en `/eu`, actívalos en el mercado
  (Shopify convierte y redondea solo; sustituye tu celda D1).
- **9 productos** sin tarifa Benelux (paléts/“PALE”): se gestionan aparte.

---

## Archivos entregados (carpeta `shopify-migracion/`)

| Archivo | Para qué |
|---|---|
| `precios_MAESTRO_comparativa.csv` | Revisar todos los mercados de un vistazo |
| `precios_ES_PT/DE/FR/IT/BX/EU.csv` | Importar precios por mercado |
| `envios_zonas_y_paises.csv` | Crear las zonas de envío |
| `envios_tarifas_por_peso_CONIVA.csv` | Tarifas por peso (y diferencias) |
| `pesos_facturables.csv` | Cargar el peso de cada producto |
| `generar_entregables.py` | Script que regenera todo desde el Excel |
