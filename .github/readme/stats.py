#!/usr/bin/env python3
"""Panel de estadísticas del README (assets/stats-light.svg y stats-dark.svg).

Lo ejecuta cada día la GitHub Action `.github/workflows/stats.yml`.
En local:  GITHUB_TOKEN=xxx python .github/readme/stats.py
           python .github/readme/stats.py --data datos.json     (sin red)
"""
import argparse, datetime as dt, json, os, urllib.request

from design import THEMES, T, begin, eyebrow, measure, svg_doc, write

LOGIN = "Mauro-vs"

# Solo lenguajes de programación; el marcado y la configuración no cuentan.
IGNORED = {"HTML", "CSS", "SCSS", "Less", "Dockerfile", "Shell", "Batchfile", "PowerShell",
           "Makefile", "Procfile", "Jupyter Notebook", "Mustache", "Handlebars"}
# Orden y color fijos. Los cuatro tonos se distinguen por luminancia, no solo por
# matiz, y la leyenda repite nombre y porcentaje (el color nunca va solo).
LANGS = [("C#", "accent"), ("TypeScript", "signal"), ("Python", "lang3"), ("JavaScript", "lang4")]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
MESES_LARGO = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
               "septiembre", "octubre", "noviembre", "diciembre"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
    publicRepos: repositories(privacy: PUBLIC) { totalCount }
    owned: repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      nodes { languages(first: 20, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
}"""


def fetch(token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": f"{LOGIN}-readme-stats"})
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)
    if res.get("errors"):
        raise SystemExit(f"GraphQL: {res['errors']}")
    u = res["data"]["user"]
    cal = u["contributionsCollection"]["contributionCalendar"]
    langs = {}
    for repo in u["owned"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    return {
        "total": cal["totalContributions"],
        "days": [[d["date"], d["contributionCount"]] for w in cal["weeks"] for d in w["contributionDays"]],
        "public_repos": u["publicRepos"]["totalCount"],
        "languages": langs,
        "updated": dt.date.today().isoformat(),
    }


def es_num(n):
    return f"{n:,}".replace(",", ".")


def es_pct(p):
    return f"{p:.1f}".replace(".", ",") + " %"


def summarize(data):
    days = sorted((dt.date.fromisoformat(d), n) for d, n in data["days"])
    best = cur = 0
    for _, n in days:
        cur = cur + 1 if n > 0 else 0
        best = max(best, cur)
    active = sum(1 for _, n in days if n > 0)
    prog = {k: v for k, v in data["languages"].items() if k not in IGNORED}
    total = sum(prog.values()) or 1
    segs, other = [], 0.0
    for name, key in LANGS:
        p = prog.pop(name, 0) / total * 100
        if p >= 0.5:
            segs.append((name, key, p))
        else:
            other += p
    other += sum(prog.values()) / total * 100
    if other >= 0.5:
        segs.append(("Otros", None, other))
    return days, best, active, segs


def level(n, cuts):
    if n == 0:
        return 0
    return 1 + sum(n > c for c in cuts)


def render(th, data):
    c = THEMES[th]
    begin()
    W = 1200
    days, best, active, segs = summarize(data)
    b = []

    # --- cifras
    tiles = [(es_num(data["total"]), "contribuciones", "en el último año"),
             (es_num(active), "días con actividad", "en los últimos 12 meses"),
             (es_num(best), "días seguidos", "mi racha más larga"),
             (es_num(data["public_repos"]), "repositorios", "públicos")]
    tw = (W - 128) / len(tiles)
    for i, (num, l1, l2) in enumerate(tiles):
        x = 64 + i * tw
        if i:
            b.append(f'<line x1="{x-24}" x2="{x-24}" y1="64" y2="176" stroke="{c["line"]}" stroke-width="1.5"/>')
        b.append(T(x, 124, num, 64, 600, c["text"], ls=-2.6))
        b.append(T(x, 154, l1, 19, 500, c["text"]))
        b.append(T(x, 178, l2, 17, 400, c["muted"]))

    # --- mapa de contribuciones
    y0 = 236
    b.append(f'<line x1="64" x2="{W-64}" y1="{y0}" y2="{y0}" stroke="{c["line"]}" stroke-width="1.5"/>')
    b += eyebrow(64, y0 + 52, "Contribuciones del último año", c)
    first = days[0][0] - dt.timedelta(days=(days[0][0].weekday() + 1) % 7)   # domingo
    nz = sorted(n for _, n in days if n > 0)
    cuts = [nz[int(len(nz) * q)] for q in (0.25, 0.5, 0.75)] if nz else [1, 2, 3]
    cell, step = 15, 19
    gx, gy = 64 + 44, y0 + 102
    col_month = {}
    for d, _ in days:
        col_month.setdefault((d - first).days // 7, d.month)
    last_lbl = -9
    for col in sorted(col_month):
        prev = col_month.get(col - 1)
        if (prev is None or prev != col_month[col]) and col - last_lbl >= 3 and col <= 51:
            if prev is None and col_month.get(col + 2) != col_month[col]:
                continue   # mes cortado al principio: no cabe la etiqueta
            b.append(T(gx + col * step, gy - 14, MESES[col_month[col] - 1], 15, 400, c["muted"]))
            last_lbl = col
    for d, n in days:
        col, row = (d - first).days // 7, (d.weekday() + 1) % 7
        x, y = gx + col * step, gy + row * step
        b.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{c["heat"][level(n, cuts)]}"/>')
    for row, lbl in ((1, "lun"), (3, "mié"), (5, "vie")):
        b.append(T(64, gy + row * step + 12, lbl, 14, 400, c["muted"]))
    gb = gy + 7 * step + 14
    upd = dt.date.fromisoformat(data["updated"])
    b.append(T(64, gb + 18, f"Actualizado el {upd.day} de {MESES_LARGO[upd.month-1]} de {upd.year}", 15, 400, c["muted"]))
    lx = W - 64
    b.append(T(lx, gb + 18, "Más", 15, 400, c["muted"], anchor="end"))
    lx -= measure("Más", 15, 400) + 10 + cell
    for i in range(4, -1, -1):
        b.append(f'<rect x="{lx}" y="{gb+5}" width="{cell}" height="{cell}" rx="4" fill="{c["heat"][i]}"/>')
        lx -= step
    b.append(T(lx + step - 8, gb + 18, "Menos", 15, 400, c["muted"], anchor="end"))

    # --- lenguajes
    y1 = gb + 64
    b.append(f'<line x1="64" x2="{W-64}" y1="{y1}" y2="{y1}" stroke="{c["line"]}" stroke-width="1.5"/>')
    b += eyebrow(64, y1 + 52, "Lenguajes en mis repositorios", c)
    bx, by, bw, bh, gap = 64, y1 + 76, W - 128, 14, 2
    total = sum(p for *_, p in segs) or 1
    usable = bw - gap * (len(segs) - 1)
    x = bx
    for name, key, p in segs:
        w = usable * p / total
        b.append(f'<rect x="{x:.1f}" y="{by}" width="{w:.1f}" height="{bh}" rx="{min(4, w/2):.1f}" '
                 f'fill="{c[key] if key else c["muted"]}"/>')
        x += w + gap
    lx, ly = 64, by + bh + 44
    for name, key, p in segs:
        b.append(f'<circle cx="{lx+6}" cy="{ly-6}" r="6" fill="{c[key] if key else c["muted"]}"/>')
        b.append(T(lx + 20, ly, name, 18, 500, c["text"]))
        nx = lx + 20 + measure(name, 18, 500) + 8
        b.append(T(nx, ly, es_pct(p), 18, 400, c["muted"]))
        lx = nx + measure(es_pct(p), 18, 400) + 36
    H = int(ly + 52)
    b.insert(0, f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="{c["bg"]}" stroke="{c["line"]}" stroke-width="2"/>')
    alt = (f"Estadísticas de GitHub: {data['total']} contribuciones en el último año, {active} días con actividad, "
           f"racha más larga de {best} días, {data['public_repos']} repositorios públicos. Lenguajes: "
           + ", ".join(f"{n} {es_pct(p)}" for n, _, p in segs) + ".")
    return svg_doc(W, H, "\n".join(b), alt)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="JSON con los datos ya descargados (sin red)")
    ap.add_argument("--dump", help="guarda los datos descargados en este JSON")
    a = ap.parse_args()
    if a.data:
        data = json.load(open(a.data, encoding="utf-8"))
    else:
        token = os.environ.get("STATS_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("Falta GITHUB_TOKEN (o STATS_TOKEN) en el entorno.")
        data = fetch(token)
    if a.dump:
        json.dump(data, open(a.dump, "w", encoding="utf-8"), indent=1)
    for th in THEMES:
        write(f"stats-{th}.svg", render(th, data))
