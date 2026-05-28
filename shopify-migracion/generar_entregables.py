#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera los entregables de migracion Amazon -> Shopify a partir de
"EL SANTO GRIAL".xlsx.

ES/DE/FR/IT  -> se LEEN directamente de las hojas WEB (fuente de la verdad:
                incluyen el margen curado por producto en la columna F).
BX (Benelux) -> se CALCULA: mismo margen por producto que WEB FR, envio UPS
                Benelux incluido, IVA ref. 21% (Belgica).
EU (resto UE)-> se CALCULA: mismo margen por producto que WEB FR, SIN envio
                incluido (se cobra real en checkout), IVA ref. 21% (flota).

Modelo de envio (hibrido): ES/PT, DE, FR, IT, BX incluyen envio (zona estandar
gratis, diferencia para zonas caras). EU cobra el envio real en el checkout.
"""
import csv, os
import openpyxl

XLSX = "/root/.claude/uploads/259ae7d4-7adc-4988-b1e2-941e852f3926/6efcd1f0-__EL_SANTO_GRIAL.xlsx"
OUT  = "/home/user/Google-Search-Console/shopify-migracion"
os.makedirs(OUT, exist_ok=True)
wb = openpyxl.load_workbook(XLSX, data_only=True)

# --- constantes del modelo (identicas al Excel) ---
COSTE_FIJO     = 0.30
COSTE_VARIABLE = 0.021
IVA_CARRIER    = 1.21          # envio neto = envio_con_iva / 1.21
IVA = {"ES":1.21,"PT":1.23,"DE":1.19,"FR":1.20,"IT":1.22,"BX":1.21,"EU":1.21}

def fnum(v): return float(v) if isinstance(v,(int,float)) else None

# --- tablas de envio CON IVA ---
gls = wb["GLS"]; ups = wb["UPS"]
GLS_ROW = {"0-1":4,"1-2":5,"2-3":5,"3-4":6,"4-5":6,"5-6":7,"6-7":7,"7-8":7,
           "8-9":7,"9-10":7,"10-15":8,"15-20":10,"20-25":11,"25-30":12,
           "30-40":13,"MOVER":14,"PALE":15}
def gls_rate(b, col):
    r = GLS_ROW.get(b); return fnum(gls[f"{col}{r}"].value) if r else None
UPS_OFF = {"0-1":0,"1-2":1,"2-3":1,"3-4":2,"4-5":2,"5-6":3,"6-7":3,"7-8":4,
           "8-9":4,"9-10":4,"10-15":5,"15-20":6,"20-25":7,"25-30":8,"30-40":9,"MOVER":10}
UPS_ZONA = {"ES":("C",4),"PT":("F",4),"DE_FR_IT":("I",4),
            "BENELUX":("C",17),"POL_CZ":("F",17),"SE_AT_IE":("I",17)}
def ups_rate(b, zona):
    off = UPS_OFF.get(b);  c,base = UPS_ZONA[zona]
    return fnum(ups[f"{c}{base+off}"].value) if off is not None else None

# --- hojas WEB (row-aligned: WEB fila r  <->  STOCK fila r-1) ---
W = {m: wb[h] for m,h in [("ES","WEB ES"),("DE","WEB DE"),("FR","WEB FR"),("IT","WEB IT")]}
stock = wb["STOCK"]

def neto_con_envio(compra, margen, iva_ref, envio_con_iva):
    env_neto = (envio_con_iva/IVA_CARRIER) if envio_con_iva else 0.0
    denom = 1 - margen - COSTE_VARIABLE*iva_ref
    return (compra + env_neto + COSTE_FIJO)/denom

productos = []
wes = W["ES"]
for r in range(3, wes.max_row + 1):
    sku = wes[f"A{r}"].value
    if not sku: continue
    sku = str(sku).strip()
    sr = r - 1  # fila equivalente en STOCK
    compra = fnum(wes[f"E{r}"].value)
    if compra is None: continue
    br_gls = (str(stock[f"M{sr}"].value).strip() if stock[f"M{sr}"].value else "")
    br_ups = (str(stock[f"N{sr}"].value).strip() if stock[f"N{sr}"].value else "")
    margen_fr = fnum(W["FR"][f"F{r}"].value) or 0.0   # margen curado (mirror para BX/EU)

    p = dict(
        sku=sku,
        ean=("" if stock[f"F{sr}"].value is None else str(stock[f"F{sr}"].value).strip()),
        nombre=("" if wes[f"C{r}"].value is None else str(wes[f"C{r}"].value).strip()),
        estado=("" if wes[f"D{r}"].value is None else str(wes[f"D{r}"].value).strip()),
        compra=compra, br_gls=br_gls, br_ups=br_ups, margen_fr=margen_fr,
        kg=fnum(stock[f"J{sr}"].value), vol167=fnum(stock[f"K{sr}"].value),
        vol200=fnum(stock[f"L{sr}"].value),
    )
    # ES/DE/FR/IT leidos directamente de la hoja (fuente de la verdad)
    p["ES"] = dict(neto=fnum(wes[f"K{r}"].value), pvp=fnum(wes[f"J{r}"].value))
    for m in ("DE","FR","IT"):
        p[m] = dict(neto=fnum(W[m][f"K{r}"].value), pvp=fnum(W[m][f"J{r}"].value))
    # BX calculado: margen FR + envio UPS Benelux incluido
    env_bx = ups_rate(br_ups, "BENELUX")
    if env_bx is not None:
        nbx = neto_con_envio(compra, margen_fr, IVA["BX"], env_bx)
        p["BX"] = dict(neto=nbx, pvp=nbx*IVA["BX"], env=env_bx, margen=margen_fr)
    else:
        p["BX"] = None
    # EU calculado: margen FR, SIN envio incluido (se cobra real en checkout)
    neu = neto_con_envio(compra, margen_fr, IVA["EU"], None)
    p["EU"] = dict(neto=neu, pvp=neu*IVA["EU"], env=0.0, margen=margen_fr)
    productos.append(p)

print(f"Productos: {len(productos)}")

# --- validacion: ES/DE/FR/IT salen de la hoja, asi que la dif debe ser 0 ---
def f2(x): return round(x,2) if x is not None else ""

# ===== ENTREGABLE 1: precios =====
def w(path, header, rows):
    with open(os.path.join(OUT,path),"w",newline="",encoding="utf-8-sig") as f:
        cw=csv.writer(f); cw.writerow(header); cw.writerows(rows)
    print(f"  -> {path} ({len(rows)} filas)")

print("ENTREGABLE 1 - precios:")
hdr = ["SKU","EAN","NOMBRE","ESTADO","COMPRA","BR_GLS","BR_UPS","MARGEN_FR",
       "NETO_ES_PT","PVP_ES(21%)","PVP_PT(23%)",
       "PVP_DE(19%)","PVP_FR(20%)","PVP_IT(22%)",
       "PVP_BX(21%,env.incl)","PVP_EU(ref21%,SIN env.)"]
rows=[]
for p in productos:
    es=p["ES"]
    rows.append([p["sku"],p["ean"],p["nombre"],p["estado"],f2(p["compra"]),
        p["br_gls"],p["br_ups"], round(p["margen_fr"],4),
        f2(es["neto"]), f2(es["pvp"]),
        f2(es["neto"]*IVA["PT"] if es["neto"] else None),
        f2(p["DE"]["pvp"]), f2(p["FR"]["pvp"]), f2(p["IT"]["pvp"]),
        f2(p["BX"]["pvp"]) if p["BX"] else "", f2(p["EU"]["pvp"]) ])
w("precios_MAESTRO_comparativa.csv", hdr, rows)

MERC = {"ES":("ES_PT",True),"DE":("DE",True),"FR":("FR",True),
        "IT":("IT",True),"BX":("BX",True),"EU":("EU",False)}
for m,(nom,incl) in MERC.items():
    rr=[]
    for p in productos:
        d=p[m]
        if not d or d["pvp"] is None: continue
        rr.append([p["sku"],p["ean"],p["nombre"],f2(d["pvp"]),"EUR",
                   "SI" if incl else "NO (envio en checkout)"])
    w(f"precios_{nom}.csv",
      ["SKU","Barcode (EAN)","Title","Price (PVP con IVA)","Moneda","Envio incluido"], rr)

# ===== ENTREGABLE 2: envios =====
print("ENTREGABLE 2 - envios:")
zonas=[
 ["ES_PENINSULA","Principal (raiz)","Espana peninsular","GLS Economy RestoES","Incluido (gratis)"],
 ["ES_BALEARES","Principal","Baleares","GLS Economy Baleares","Diferencia vs peninsula"],
 ["PT","Principal","Portugal","GLS Economy Portugal","Diferencia vs peninsula"],
 ["DE","/de","Alemania (+Austria*)","UPS Std DE-FR-IT","Incluido; *AT diferencia"],
 ["FR","/fr","Francia, Monaco","UPS Std DE-FR-IT","Incluido (gratis)"],
 ["IT","/it","Italia","UPS Std DE-FR-IT","Incluido (gratis)"],
 ["BX","/bx","Belgica, Paises Bajos, Luxemburgo","UPS Std Benelux","Incluido (gratis)"],
 ["EU_POL_CZ","/eu","Polonia, Chequia, Eslovaquia, Eslovenia, Hungria, Croacia, Estonia, Letonia, Lituania, Bulgaria, Grecia, Rumania","UPS Std Polonia-Chequia","Real en checkout"],
 ["EU_SE_AT_IE","/eu","Suecia, Irlanda, Finlandia, Dinamarca, Austria","UPS Std Suecia-Austria-Irlanda","Real en checkout"],
 ["EU_BENELUX","/eu (si Benelux no es mercado propio)","Benelux","UPS Std Benelux","Real en checkout"],
]
w("envios_zonas_y_paises.csv",
  ["ZONA_SHOPIFY","MERCADO","PAISES","TARIFA","MODELO_HIBRIDO"], zonas)

BR=["0-1","1-2","2-3","3-4","4-5","5-6","6-7","7-8","8-9","9-10","10-15","15-20","20-25","25-30","30-40","MOVER"]
def rng(b): return ("40","+") if b=="MOVER" else tuple(b.split("-"))
tar=[]
for b in BR:
    kmin,kmax=rng(b)
    re_=gls_rate(b,"N"); pt=gls_rate(b,"Q")
    dfi=ups_rate(b,"DE_FR_IT"); bnl=ups_rate(b,"BENELUX")
    pol=ups_rate(b,"POL_CZ"); se=ups_rate(b,"SE_AT_IE")
    difpt = round(pt-re_,2) if (pt and re_ and pt>re_) else 0
    tar.append([b,kmin,kmax,f2(re_),f2(pt),difpt,f2(dfi),f2(bnl),f2(pol),f2(se)])
w("envios_tarifas_por_peso_CONIVA.csv",
  ["BRACKET","KG_MIN","KG_MAX","GLS_RestoES","GLS_Portugal","DIF_PT","UPS_DE_FR_IT",
   "UPS_Benelux","UPS_Pol_Chequia","UPS_Suecia_Austria_Irlanda"], tar)

# ===== ENTREGABLE 4: pesos facturables =====
print("ENTREGABLE 4 - pesos:")
pw=[]
for p in productos:
    cand=[x for x in (p["kg"],p["vol200"]) if x is not None]
    fact=max(cand) if cand else None
    def f3(x): return round(x,3) if x is not None else ""
    pw.append([p["sku"],p["nombre"],f3(p["kg"]),f3(p["vol167"]),f3(p["vol200"]),
               f3(fact),(int(round(fact*1000)) if fact is not None else ""),
               p["br_gls"],p["br_ups"]])
w("pesos_facturables.csv",
  ["SKU","NOMBRE","KG_REAL","VOL_GLS_167","VOL_UPS_200","PESO_FACTURABLE_KG",
   "PESO_FACTURABLE_GRAMOS","BRACKET_GLS","BRACKET_UPS"], pw)

# resumen rapido para inspeccion
print("\nMuestra (3 primeros productos):")
for p in productos[:3]:
    print(f"  {p['sku'][:22]:22} ES={f2(p['ES']['pvp'])} DE={f2(p['DE']['pvp'])} "
          f"FR={f2(p['FR']['pvp'])} IT={f2(p['IT']['pvp'])} "
          f"BX={f2(p['BX']['pvp']) if p['BX'] else '-'} EU={f2(p['EU']['pvp'])} (margen={p['margen_fr']})")
print("LISTO ->", OUT)
