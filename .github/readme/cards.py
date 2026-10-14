#!/usr/bin/env python3
"""Genera las piezas fijas del README: cabecera, contacto, proyectos y stack.

Uso:  python .github/readme/cards.py
"""
from design import THEMES, PLAT_NAME, T, begin, chips, measure, new_mark, svg_doc, wrap, write


# ---------------------------------------------------------------- cabecera
def hero(th):
    W, H = 1200, 460
    c = THEMES[th]
    begin()
    b = [f'<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse">'
         f'<circle cx="2" cy="2" r="1.3" fill="{c["grid"]}"/></pattern>'
         f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{c["bg"]}"/>'
         f'<stop offset=".55" stop-color="{c["bg"]}" stop-opacity="0"/></linearGradient></defs>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="{c["bg"]}" stroke="{c["line"]}" stroke-width="2"/>',
         f'<rect x="560" y="2" width="{W-562}" height="{H-4}" rx="26" fill="url(#g)"/>',
         f'<rect x="560" y="2" width="300" height="{H-4}" fill="url(#fade)"/>']
    x = 64
    b.append(T(x, 122, "Ontinyent, València", 20, 500, c["muted"]))
    b.append(T(x, 214, "Mauro Valdés", 88, 700, c["text"], ls=-2.6))
    b.append(T(x, 270, "Desarrollador multiplataforma", 30, 500, c["text"], ls=-0.4))
    for i, ln in enumerate(wrap("Construyo apps para móvil, web, escritorio y Odoo, y la API que las conecta.", 22, 400, 470)):
        b.append(T(x, 322 + i * 33, ln, 22, 400, c["muted"]))

    ox, oy, bw, bh, ex = 680, 240, 92, 48, 968
    ends = [("movil", 108, "React Native, Expo"), ("web", 196, "Angular, React, Vite"),
            ("escritorio", 284, "C#, WPF, .NET"), ("erp", 372, "Odoo, Python")]
    for i, (k, ey, sub) in enumerate(ends):
        d = f"M{ox+bw/2} {oy} C{ox+bw/2+120} {oy},{ex-140} {ey},{ex} {ey}"
        b.append(f'<path d="{d}" fill="none" stroke="{c["line"]}" stroke-width="2"/>')
        b.append(f'<path class="p" style="animation-delay:{i*0.35:.2f}s" d="{d}" pathLength="100" fill="none" '
                 f'stroke="{c[k]}" stroke-width="3" stroke-linecap="round"/>')
        b.append(f'<circle cx="{ex}" cy="{ey}" r="14" fill="{c[k]}" opacity=".16"/>')
        b.append(f'<circle cx="{ex}" cy="{ey}" r="6.5" fill="{c[k]}"/>')
        b.append(T(ex + 26, ey - 3, PLAT_NAME[k], 22, 700, c["text"], ls=-0.2))
        b.append(T(ex + 26, ey + 21, sub, 15, 400, c["muted"]))
    b.append(f'<rect x="{ox-bw/2}" y="{oy-bh/2}" width="{bw}" height="{bh}" rx="14" fill="{c["surface"]}" '
             f'stroke="{c["line"]}" stroke-width="2"/>')
    b.append(T(ox, oy + 6.5, "API", 19, 700, c["text"], anchor="middle", ls=0.5))
    css = (".p{stroke-dasharray:12 100;stroke-dashoffset:12;animation:flow 2.8s cubic-bezier(.55,.05,.25,1) infinite}"
           "@keyframes flow{0%{stroke-dashoffset:12;opacity:0}12%{opacity:1}78%{opacity:1}100%{stroke-dashoffset:-100;opacity:0}}"
           "@media (prefers-reduced-motion:reduce){.p{animation:none;opacity:0}}")
    return svg_doc(W, H, "\n".join(b),
                   "Mauro Valdés, desarrollador multiplataforma: apps para móvil, web, escritorio y Odoo", css)


# ---------------------------------------------------------------- tarjeta de proyecto
def card(th, name, plats, desc, stack, badge=None):
    W, H = 600, 296
    c = THEMES[th]
    begin()
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22" fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="2"/>']
    x, ty = 36, 58
    for k in plats:
        b.append(f'<circle cx="{x+6}" cy="{ty-6}" r="6" fill="{c[k]}"/>')
        b.append(T(x + 20, ty, PLAT_NAME[k], 17, 500, c["muted"]))
        x += 20 + measure(PLAT_NAME[k], 17, 500) + 22
    if badge:
        bw = measure(badge, 14, 700) + 18
        b.append(f'<rect x="{x}" y="{ty-20}" width="{bw:.1f}" height="26" rx="7" fill="none" stroke="{c["line"]}" stroke-width="1.5"/>')
        b.append(T(x + 9, ty - 2, badge, 14, 700, c["muted"], ls=0.3))
    ax, ay = W - 50, 48
    b.append(f'<circle cx="{ax}" cy="{ay}" r="18" fill="none" stroke="{c["line"]}" stroke-width="1.5"/>')
    b.append(f'<path d="M{ax-5} {ay+5} L{ax+5} {ay-5} M{ax-3} {ay-5} H{ax+5} V{ay+3}" fill="none" '
             f'stroke="{c["text"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(T(36, 122, name, 36, 700, c["text"], ls=-0.8))
    for i, ln in enumerate(wrap(desc, 20, 400, W - 72)[:2]):
        b.append(T(36, 164 + i * 29, ln, 20, 400, c["muted"]))
    ch, _ = chips(stack, 36, 228, c)
    return svg_doc(W, H, "\n".join(b + ch), f"{name}: {desc}")


# ---------------------------------------------------------------- stack
# Lo marcado con * lo he aprendido este curso (2º DAW).
STACK = [
    ("movil", "Móvil", ["React Native", "Expo", "Expo Router", "Zustand", "React Query"]),
    ("web", "Web", ["Angular", "Signals*", "React", "Vite*", "JavaScript", "TypeScript", "Tailwind CSS", "Canvas API*"]),
    ("api", "API", ["Node.js", "NestJS", "Express*", "TypeORM", "Mongoose*", "Zod*", "Swagger", "Flask*"]),
    ("escritorio", "Escritorio", ["C#", ".NET", "WPF", "MVVM", "Entity Framework"]),
    ("erp", "ERP", ["Odoo 18", "Python", "ORM de Odoo", "Vistas XML", "Roles y seguridad"]),
]
INFRA = ["PostgreSQL", "MongoDB*", "MariaDB", "MySQL", "SQL Server", "SQLite*", "Supabase", "Docker",
         "Docker Compose*", "GitHub Actions", "GitHub Pages*", "PM2", "Linux / VPS", "Git", "Claude Code*"]


def stack(th):
    W = 1200
    c = THEMES[th]
    begin()
    b = []
    colw = (W - 128) / len(STACK)
    rows = max(len(i) for *_, i in STACK)
    # leyenda de lo nuevo
    lg = "Aprendido este curso"
    lw = measure(lg, 16, 500)
    b.append(new_mark(W - 64 - lw - 14, 54, c))
    b.append(T(W - 64, 59.5, lg, 16, 500, c["muted"], anchor="end"))
    top = 112
    for ci, (k, label, items) in enumerate(STACK):
        x = 64 + ci * colw
        if k == "api":   # el nodo central de la cabecera: neutro
            b.append(f'<rect x="{x}" y="{top-14}" width="14" height="14" rx="4" fill="none" stroke="{c["text"]}" stroke-width="2"/>')
            rule = c["line"]
        else:
            b.append(f'<circle cx="{x+7}" cy="{top-7}" r="7" fill="{c[k]}"/>')
            rule = c[k]
        b.append(T(x + 24, top, label, 24, 700, c["text"], ls=-0.3))
        b.append(f'<line x1="{x}" x2="{x+colw-30}" y1="{top+22}" y2="{top+22}" stroke="{rule}" stroke-width="2" opacity=".6"/>')
        for i, it in enumerate(items):
            y = top + 62 + i * 36
            if it.endswith("*"):
                it = it[:-1]
                b.append(new_mark(x + 5, y - 6.5, c))
                b.append(T(x + 18, y, it, 19, 500, c["text"]))
            else:
                b.append(T(x, y, it, 19, 400, c["text"]))
    sep = top + 62 + (rows - 1) * 36 + 38
    b.append(f'<line x1="64" x2="{W-64}" y1="{sep}" y2="{sep}" stroke="{c["line"]}" stroke-width="1.5"/>')
    b.append(T(64, sep + 48, "Datos, despliegue y herramientas", 18, 500, c["muted"]))
    names = [i.rstrip("*") for i in INFRA]
    new = {i.rstrip("*") for i in INFRA if i.endswith("*")}
    ch, bottom = chips(names, 64, sep + 70, c, size=17, h=38, pad=16, gap=10, maxw=W - 128, new=new)
    H = int(bottom + 56)
    b.insert(0, f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="{c["bg"]}" stroke="{c["line"]}" stroke-width="2"/>')
    alt = ("Stack. Móvil: React Native, Expo. Web: Angular, React, Vite, JavaScript, TypeScript. API: Node.js, NestJS, Express, "
           "Mongoose, Zod, Flask. Escritorio: C#, WPF. ERP: Odoo, Python. Nuevo este curso: Signals, Vite, "
           "Canvas API, Express, Mongoose, Zod, Flask, MongoDB, SQLite, Docker Compose, GitHub Pages, Claude Code.")
    return svg_doc(W, H, "\n".join(b + ch), alt)


# ---------------------------------------------------------------- botones de contacto
def pill(th, label, icon):
    c = THEMES[th]
    begin()
    size = 18
    W, H = int(28 + 30 + 14 + measure(label, size, 500) + 22 + 34 + 10), 60
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{(H-2)/2}" fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="2"/>']
    ix, iy = 30, H / 2
    if icon == "mail":
        b.append(f'<rect x="{ix-11}" y="{iy-8}" width="22" height="16" rx="3" fill="none" stroke="{c["text"]}" stroke-width="2"/>')
        b.append(f'<path d="M{ix-10} {iy-6} L{ix} {iy+1} L{ix+10} {iy-6}" fill="none" stroke="{c["text"]}" stroke-width="2" stroke-linejoin="round"/>')
    else:
        b.append(f'<circle cx="{ix}" cy="{iy-4}" r="4.5" fill="none" stroke="{c["text"]}" stroke-width="2"/>')
        b.append(f'<path d="M{ix-9} {iy+10} C{ix-8} {iy+2},{ix+8} {iy+2},{ix+9} {iy+10}" fill="none" stroke="{c["text"]}" stroke-width="2" stroke-linecap="round"/>')
    b.append(T(ix + 22, iy + size * 0.36, label, size, 500, c["text"]))
    ax = W - 31
    b.append(f'<circle cx="{ax}" cy="{iy}" r="17" fill="{c["movil"]}"/>')
    b.append(f'<path d="M{ax-5} {iy+5} L{ax+5} {iy-5} M{ax-3} {iy-5} H{ax+5} V{iy+3}" fill="none" stroke="#FFFFFF" '
             f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg_doc(W, H, "\n".join(b), label)


PROJECTS = [
    ("respi-app", "Respi", ["movil", "web"],
     "Reserva de pistas deportivas con roles de cliente y administrador, pagos con Stripe e i18n.",
     ["React Native", "Expo Router", "Zustand", "Stripe"], "TFG"),
    ("respi-api", "Respi API", ["web"],
     "API REST modular con autenticación JWT, Swagger y despliegue con Docker Compose y PM2.",
     ["NestJS", "TypeORM", "MariaDB", "Docker"], "TFG"),
    ("gestilibro", "GestiLibro", ["erp"],
     "Módulo de Odoo para una cadena de librerías: stock por tienda, ventas y facturación automática.",
     ["Odoo 18", "Python", "PostgreSQL"], None),
    ("hakuna-mamoto", "Hakuna-MaMoto", ["movil"],
     "App móvil con datos y autenticación en Supabase, subida de imágenes y notificaciones push.",
     ["React Native", "Supabase", "React Query"], None),
    ("club-padel", "Club Pádel", ["escritorio"],
     "Gestión de un club: socios, reservas que no se solapan y cuotas que se generan solas.",
     ["C#", "WPF", "MVVM", "EF6"], None),
    ("motogp", "MotoGP Dashboard", ["escritorio"],
     "Estadísticas de MotoGP en tiempo real desde la API de Sportradar, con carga asíncrona.",
     ["C#", "WPF", "REST API"], None),
]

if __name__ == "__main__":
    for th in THEMES:
        write(f"hero-{th}.svg", hero(th))
        write(f"stack-{th}.svg", stack(th))
        write(f"linkedin-{th}.svg", pill(th, "LinkedIn", "user"))
        write(f"email-{th}.svg", pill(th, "maurovs19@gmail.com", "mail"))
        for slug, *args in PROJECTS:
            write(f"{slug}-{th}.svg", card(th, *args))
