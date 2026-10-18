"""Tokens y utilidades compartidas para los SVG del README (claro y oscuro).

Es la misma identidad que el portfolio (https://mauro-vs.dev), «Marea + Sistema
vivo»: azul noche / niebla, un único acento cobalto y una señal ámbar para lo
que está vivo; Geist para el texto y Geist Mono para los rótulos y los datos.
"""
import base64, io, os
from fontTools.ttLib import TTFont
from fontTools import subset as ftsubset

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ASSETS = os.path.join(ROOT, "assets")

# (familia, peso) -> fichero. "sans" = Geist, "mono" = Geist Mono.
FONT_FILES = {
    **{("sans", w): os.path.join(HERE, "fonts", f"geist-latin-{w}-normal.woff2") for w in (400, 500, 600, 700)},
    **{("mono", w): os.path.join(HERE, "fonts", f"geist-mono-latin-{w}-normal.woff2") for w in (400, 500)},
}
_fonts = {k: TTFont(p) for k, p in FONT_FILES.items()}
FAMILY_CSS = {"sans": "FG", "mono": "FGM"}

# Mismos valores que src/styles/tokens.css del portfolio. Texto secundario y
# acento cumplen 4.5:1 sobre fondo y superficie en los dos temas.
THEMES = {
    "dark": dict(bg="#0A0E17", surface="#121826", raised="#182033", line="#232C3E", grid="#1C2435",
                 text="#E8ECF4", muted="#93A0B8", accent="#6E8BFF", signal="#FFB547",
                 lang3="#E8ECF4", lang4="#4A5878",
                 heat=["#161D2D", "#1F2F66", "#2E46A6", "#4A68E0", "#8EA6FF"]),
    "light": dict(bg="#F3F6F9", surface="#FFFFFF", raised="#E8EEF4", line="#D5DEE8", grid="#E1E8F0",
                  text="#0B1F3A", muted="#4A5B73", accent="#2350F5", signal="#E8961C",
                  lang3="#0B1F3A", lang4="#9DABC0",
                  heat=["#E6ECF5", "#BCCBF7", "#7E9CF4", "#3E66EE", "#1D3FB8"]),
}

_used = {k: set() for k in FONT_FILES}


def measure(s, size, weight, ls=0.0, mono=False):
    f = _fonts[("mono" if mono else "sans", weight)]
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    w = sum(hmtx[cmap[ord(ch)]][0] if ord(ch) in cmap else upm * 0.5 for ch in s)
    return w * size / upm + ls * max(len(s) - 1, 0)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size, weight, fill, ls=0, anchor="start", extra="", mono=False):
    fam = "mono" if mono else "sans"
    _used[(fam, weight)].update(s)
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    m = ' class="m"' if mono else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}"{l}{a}{m}{extra}>{esc(s)}</text>')


def wrap(s, size, weight, width):
    lines, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if measure(t, size, weight) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]


def chips(items, x, y, c, size=15, h=32, pad=12, gap=8, maxw=None, new=()):
    """Etiquetas de tecnología, como las del portfolio: mono y radio de 8 px.
    Las de `new` llevan un rombo delante (aprendido este curso)."""
    out, cx, cy = [], x, y
    for it in items:
        dot = 14 if it in new else 0
        w = measure(it, size, 400, mono=True) + pad * 2 + dot
        if maxw and cx + w > x + maxw:
            cx, cy = x, cy + h + gap
        out.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="{h}" rx="8" fill="{c["raised"]}" '
                   f'stroke="{c["line"]}" stroke-width="1"/>')
        if dot:
            out.append(new_mark(cx + pad + 4, cy + h / 2, c))
        out.append(T(cx + pad + dot, cy + h / 2 + size * 0.35, it, size, 400, c["text"], mono=True))
        cx += w + gap
    return out, cy + h


def new_mark(cx, cy, c):
    """Marca de 'aprendido este curso': rombo pequeño en tinta de texto (no depende del color)."""
    r = 4.2
    return f'<path d="M{cx} {cy-r} L{cx+r} {cy} L{cx} {cy+r} L{cx-r} {cy} Z" fill="{c["text"]}"/>'


def eyebrow(x, y, label, c, dot=None):
    """Antetítulo como el del portfolio: un punto y un rótulo en mono."""
    return [f'<circle cx="{x+4}" cy="{y-5}" r="4" fill="{dot or c["accent"]}"/>',
            T(x + 16, y, label, 15, 400, c["muted"], mono=True)]


def dots_wave(x0, y0, w, h, c, side="left", spacing=12, opacity=0.9):
    """Marea de puntos en semitono: el tamaño decrece hacia dentro y la frontera
    ondula, como el fondo del portfolio (versión estática)."""
    import math
    out = []
    cols, rows = int(w // spacing) + 1, int(h // spacing) + 1
    for r in range(rows):
        y = y0 + r * spacing
        edge = w * (0.62 + 0.22 * math.sin(y * 0.021 + (0 if side == "left" else 2.3))
                    + 0.12 * math.sin(y * 0.057 + (1.1 if side == "left" else 3.9)))
        for col in range(cols):
            depth = col * spacing + spacing / 2
            k = 1 - depth / max(edge, 1)
            if k <= 0:
                break
            k = k ** 1.3
            x = x0 + depth if side == "left" else x0 + w - depth
            yy = y + (spacing / 2 if col % 2 else 0)
            out.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="{spacing*0.42*k:.2f}" '
                       f'fill="{c["accent"]}" fill-opacity="{0.25 + 0.65 * k * opacity:.2f}"/>')
    return out


def _font_css():
    out = []
    for (fam, w), used in _used.items():
        if not used:
            continue
        opts = ftsubset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga", "calt"]
        f = TTFont(FONT_FILES[(fam, w)])
        s = ftsubset.Subsetter(opts); s.populate(text="".join(sorted(used)) + " "); s.subset(f)
        buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
        data = base64.b64encode(buf.getvalue()).decode()
        out.append(f"@font-face{{font-family:{FAMILY_CSS[fam]};font-weight:{w};"
                   f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return "".join(out)


def begin():
    """Empieza un SVG nuevo: cada archivo lleva solo los glifos que usa."""
    for s in _used.values():
        s.clear()


def svg_doc(w, h, body, title, extra_css=""):
    css = _font_css()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n'
            f'<style>{css}text{{font-family:FG,"Segoe UI",system-ui,-apple-system,sans-serif;'
            f'font-kerning:normal}}.m{{font-family:FGM,ui-monospace,Menlo,monospace}}{extra_css}</style>\n'
            f'{body}\n</svg>\n')


def write(name, svg):
    os.makedirs(ASSETS, exist_ok=True)
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"{name:32s} {len(svg)//1024:4d} KB")
