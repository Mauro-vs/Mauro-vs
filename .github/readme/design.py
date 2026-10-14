"""Tokens y utilidades compartidas para los SVG del README (claro y oscuro)."""
import base64, io, os
from fontTools.ttLib import TTFont
from fontTools import subset as ftsubset

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ASSETS = os.path.join(ROOT, "assets")

FONT_FILES = {w: os.path.join(HERE, "fonts", f"familjen-grotesk-latin-{w}-normal.woff2") for w in (400, 500, 700)}
_fonts = {w: TTFont(p) for w, p in FONT_FILES.items()}

# Colores de plataforma validados (ΔE CVD y lightness band) en ambos modos.
THEMES = {
    "dark": dict(bg="#0C1524", surface="#111D31", line="#22324B", grid="#1A2840",
                 text="#E9EEF6", muted="#8E9CB3",
                 movil="#4A8CF5", web="#1C9E8F", escritorio="#E0588A", erp="#C4861F",
                 heat=["#1A2840", "#1C3768", "#24509E", "#3570D6", "#6FA6FF"]),
    "light": dict(bg="#F5F7FB", surface="#FFFFFF", line="#D9E1EC", grid="#E4EAF2",
                  text="#0F1B2D", muted="#5A6A81",
                  movil="#2563EB", web="#0E8C7D", escritorio="#C2417A", erp="#B9740E",
                  heat=["#E9EEF5", "#BFD3FB", "#7FA6F4", "#3B72E8", "#1D47B0"]),
}
PLAT_NAME = {"movil": "Móvil", "web": "Web", "escritorio": "Escritorio", "erp": "ERP"}

_used = {400: set(), 500: set(), 700: set()}


def measure(s, size, weight, ls=0.0):
    f = _fonts[weight]
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    w = sum(hmtx[cmap[ord(ch)]][0] if ord(ch) in cmap else upm * 0.5 for ch in s)
    return w * size / upm + ls * max(len(s) - 1, 0)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size, weight, fill, ls=0, anchor="start", extra=""):
    _used[weight].update(s)
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}"{l}{a}{extra}>{esc(s)}</text>')


def wrap(s, size, weight, width):
    lines, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if measure(t, size, weight) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]


def chips(items, x, y, c, size=16, h=34, pad=15, gap=8, maxw=None, new=()):
    """Etiquetas en fila; las de `new` llevan un punto delante."""
    out, cx, cy = [], x, y
    for it in items:
        dot = 14 if it in new else 0
        w = measure(it, size, 500) + pad * 2 + dot
        if maxw and cx + w > x + maxw:
            cx, cy = x, cy + h + gap
        out.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="none" '
                   f'stroke="{c["line"]}" stroke-width="1.5"/>')
        if dot:
            out.append(new_mark(cx + pad + 4, cy + h / 2, c))
        out.append(T(cx + pad + dot, cy + h / 2 + size * 0.36, it, size, 500, c["text"]))
        cx += w + gap
    return out, cy + h


def new_mark(cx, cy, c):
    """Marca de 'aprendido este curso': rombo pequeño, en tinta de texto (sin color de serie)."""
    r = 4.2
    return f'<path d="M{cx} {cy-r} L{cx+r} {cy} L{cx} {cy+r} L{cx-r} {cy} Z" fill="{c["text"]}"/>'


def _font_css(weights):
    out = []
    for w in weights:
        if not _used[w]:
            continue
        opts = ftsubset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga", "calt"]
        f = TTFont(FONT_FILES[w])
        s = ftsubset.Subsetter(opts); s.populate(text="".join(sorted(_used[w])) + " "); s.subset(f)
        buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
        data = base64.b64encode(buf.getvalue()).decode()
        out.append(f"@font-face{{font-family:FG;font-weight:{w};src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return "".join(out)


def begin():
    """Empieza un SVG nuevo: cada archivo lleva solo los glifos que usa."""
    for s in _used.values():
        s.clear()


def svg_doc(w, h, body, title, extra_css=""):
    css = _font_css((400, 500, 700))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n'
            f'<style>{css}text{{font-family:FG,"Segoe UI",system-ui,-apple-system,sans-serif;'
            f'font-kerning:normal}}{extra_css}</style>\n{body}\n</svg>\n')


def write(name, svg):
    os.makedirs(ASSETS, exist_ok=True)
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"{name:28s} {len(svg)//1024:4d} KB")
