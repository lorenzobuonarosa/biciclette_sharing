# Normalizza le tavole Istat "Mobilità urbana" (Ambiente urbano) in data/capoluoghi.csv.
# File attesi in <cartella>: tav/MOBILITA_URBANA_2024.xlsx, MOBILITA_URBANA_2023.xlsx, MOBILITA_2021.xlsx
import sys, re, csv, openpyxl, warnings
warnings.filterwarnings("ignore")
# uso: python3 scripts/capoluoghi.py <cartella tavole Istat> <centroidi.csv> data/capoluoghi.csv
I = sys.argv[1]; CENT = sys.argv[2]; OUT = sys.argv[3]
def rows(path, sheet):
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[sheet]
    out = {}
    started = False
    for r in ws.iter_rows(values_only=True):
        n = r[0]
        if isinstance(n, str) and n.strip() == "Torino" or (isinstance(n,str) and n.startswith("Torino")): started = True
        if not started: continue
        if n is None or not isinstance(n, str): 
            if started and out: break
            continue
        name = re.sub(r"\s*\([a-z]+(,\s*[a-z]+)*\)\s*$", "", n.strip()).strip()
        if name == "Bolzano - Bozen": name = "Bolzano/Bozen"
        out[name] = r
    return out
def pres(v):
    if v == "X": return 1
    if v in ("-", None, "..", "...."): return 0
    raise ValueError(v)
def val(v):
    if isinstance(v, (int, float)): return float(v)
    return 0.0 if v in ("-", None) else None
# (file, sheet, {anno: colonna})
f24 = I + "/tav/MOBILITA_URBANA_2024.xlsx"; f23 = I + "/MOBILITA_URBANA_2023.xlsx"; f21 = I + "/MOBILITA_2021.xlsx"
src = {
  "bici":   [(f24, "16.2", {2022: 9, 2023: 10, 2024: 11}), (f23, "16.2", {2021: 9}), (f21, "18.2", {2020: 18})],
  "bici_10k": [(f24, "17.1", {2022: 9, 2023: 10, 2024: 11}), (f23, "17.1", {2021: 9}), (f21, "19.1", {2020: 18})],
  "monopattini": [(f24, "18.2", {2022: 5, 2023: 6, 2024: 7}), (f23, "18.2", {2021: 5}), (f21, "18.2", {2020: 28})],
  "monopattini_10k": [(f24, "19.1", {2022: 5, 2023: 6, 2024: 7}), (f23, "19.1", {2021: 5}), (f21, "19.1", {2020: 28})],
}
data = {}
names = None
for var, specs in src.items():
    for path, sheet, cols in specs:
        rr = rows(path, sheet)
        nm = set(rr)
        if names is None: names = nm
        if nm != names: print("DIFF", var, path, sheet, nm ^ names, file=sys.stderr)
        for name, r in rr.items():
            for anno, c in cols.items():
                v = pres(r[c]) if var in ("bici", "monopattini") else val(r[c])
                data.setdefault((name, anno), {})[var] = v
cent = {r["COMUNE"]: r for r in csv.DictReader(open(CENT))}
missing = [n for n in names if n not in cent]
print("missing centroids:", missing, file=sys.stderr)
print("centroids not in table:", [n for n in cent if n not in names], file=sys.stderr)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("capoluogo;regione;lat;lon;anno;monopattini;bici;monopattini_10k;bici_10k\n")
    order = list(rows(f24, "18.2").keys())
    for name in order:
        if name == "Cesena": continue
        c = cent[name]
        for anno in range(2020, 2025):
            d = data[(name, anno)]
            for k in ("monopattini", "bici"):
                if d[k] == 0 and d[k + "_10k"] not in (0, None): print("WARN incoerente", name, anno, k, d, file=sys.stderr)
                if d[k] == 1 and not d[k + "_10k"]: print("WARN presente senza flotta", name, anno, k, d, file=sys.stderr)
            fm = lambda x: ("" if x is None else ("%.1f" % x).replace(".", ","))
            f.write(";".join([name, c["DEN_REG"], c["lat"].replace(".", ","), c["lon"].replace(".", ","), str(anno),
                              str(d["monopattini"]), str(d["bici"]), fm(d["monopattini_10k"]), fm(d["bici_10k"])]) + "\n")
