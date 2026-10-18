#!/usr/bin/env python3
"""Genera las piezas fijas del README: cabecera, contacto, proyectos, stack,
cómo trabajo y certificación. Misma identidad que el portfolio
(https://mauro-vs.dev).

Uso:  python .github/readme/cards.py
"""
import base64, math, os

from design import HERE, THEMES, T, begin, chips, dots_wave, eyebrow, measure, svg_doc, wrap, write
from icons import ICONS


# ---------------------------------------------------------------- marca
def brand_mark(x, y, c, size=26):
    """La marca del portfolio: una ola en trama de semitono (3 × 3 puntos)."""
    s = size / 22
    out = []
    for cx, r, lift in ((4, 2.6, 0), (11, 2.0, 1.4), (18, 1.35, 2.4)):
        for cy in (4, 11, 18):
            out.append(f'<circle cx="{x + cx * s:.1f}" cy="{y + (cy - lift + 1.2) * s:.1f}" r="{r * s:.2f}" fill="{c["accent"]}"/>')
    return out


# ---------------------------------------------------------------- cabecera
NODES = [("Interfaz", 718, 214), ("API", 826, 150), ("Datos", 948, 196), ("Despliegue", 1070, 132)]


def ocean(c, x0, y0, w, h):
    """Océano de puntos en perspectiva, como la marea 3D del inicio (estático)."""
    out = []
    rows, cols = 24, 38
    cx = x0 + w / 2
    for i in range(rows):
        t = i / (rows - 1)
        y = y0 + (t ** 1.55) * h
        half = w * (0.32 + 0.62 * t)
        for j in range(cols):
            u = j / (cols - 1)
            x = cx + (u - 0.5) * 2 * half
            swell = math.sin(u * 7.5 + i * 0.42) * (2 + t * 9) + math.sin(u * 3.1 - i * 0.2) * (1 + t * 5)
            r = 0.7 + t * 2.3 + max(swell, 0) * 0.05
            o = 0.18 + 0.72 * t
            out.append(f'<circle cx="{x:.1f}" cy="{y - swell:.1f}" r="{r:.2f}" fill="{c["accent"]}" fill-opacity="{o:.2f}"/>')
    return out


def hero(th):
    W, H = 1200, 460
    c = THEMES[th]
    begin()
    b = [f'<defs><clipPath id="panel"><rect x="636" y="34" width="530" height="392" rx="24"/></clipPath>'
         f'<clipPath id="card"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28"/></clipPath>'
         f'<radialGradient id="glow" cx=".5" cy="0" r=".9"><stop offset="0" stop-color="{c["accent"]}" stop-opacity=".16"/>'
         f'<stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/></radialGradient></defs>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="{c["bg"]}" stroke="{c["line"]}" stroke-width="2"/>',
         '<g clip-path="url(#card)">', *dots_wave(0, 0, 54, H, c, "left", spacing=11, opacity=0.8), '</g>']

    # Texto: marca, titular de dos líneas y estado.
    x = 92
    b += brand_mark(x, 62, c)
    b.append(T(x + 38, 82, "Mauro Valdes", 22, 600, c["text"], ls=-0.5))
    size = 86
    b.append(T(x - 3, 214, "De la interfaz", size, 600, c["text"], ls=-4.6))
    al_w = measure("al ", size, 600, ls=-4.6)
    serv_w = measure("servidor", size, 600, ls=-4.6)
    b.append(T(x - 3, 296, "al", size, 600, c["text"], ls=-4.6))
    b.append(T(x - 3 + al_w, 296, "servidor", size, 600, c["accent"], ls=-4.6))
    # Punto final en ámbar, cuadrado como el de Geist.
    px = x - 3 + al_w + serv_w - 12   # el tracking negativo deja aire tras la "r"
    b.append(f'<rect x="{px:.1f}" y="280" width="15" height="16" rx="1.5" fill="{c["signal"]}"/>')
    # Subrayado de puntos bajo "servidor".
    for k in range(int(serv_w // 13)):
        b.append(f'<circle cx="{x - 3 + al_w + 6 + k * 13:.1f}" cy="318" r="3" fill="{c["accent"]}" fill-opacity=".85"/>')
    b.append(T(x, 372, "Desarrollador full-stack · React Native, NestJS y PostgreSQL", 19, 400, c["muted"]))
    b += eyebrow(x, 414, "Disponible: remoto, híbrido o presencial", c, dot=c["signal"])

    # Escena: panel con la marea y las cuatro capas enlazadas.
    b.append(f'<rect x="636" y="34" width="530" height="392" rx="24" fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="1.5"/>')
    b.append('<g clip-path="url(#panel)">')
    b.append('<rect x="636" y="34" width="530" height="200" fill="url(#glow)"/>')
    b += ocean(c, 636, 236, 530, 196)
    chain = " ".join(f"{'M' if i == 0 else 'L'}{nx} {ny}" for i, (_, nx, ny) in enumerate(NODES))
    for _, nx, ny in NODES:
        b.append(f'<line x1="{nx}" y1="{ny}" x2="{nx}" y2="{ny + 70 + (ny % 30)}" stroke="{c["signal"]}" stroke-opacity=".35" stroke-width="1.2"/>')
    b.append(f'<path d="{chain}" fill="none" stroke="{c["signal"]}" stroke-width="2" stroke-linejoin="round"/>')
    for name, nx, ny in NODES:
        b.append(f'<circle cx="{nx}" cy="{ny}" r="11" fill="{c["signal"]}" fill-opacity=".22"/>')
        b.append(f'<circle cx="{nx}" cy="{ny}" r="5.5" fill="{c["signal"]}"/>')
        lw = measure(name, 13, 400, mono=True) + 16
        b.append(f'<rect x="{nx - lw / 2:.1f}" y="{ny - 44}" width="{lw:.1f}" height="24" rx="6" fill="{c["surface"]}" '
                 f'stroke="{c["line"]}" stroke-width="1"/>')
        b.append(T(nx, ny - 27.5, name, 13, 400, c["text"], anchor="middle", mono=True))
    # La petición recorre las capas (animación CSS; quieta si se pide menos movimiento).
    b.append(f'<circle class="req" r="5" fill="{c["text"]}"/>')
    b.append('</g>')
    css = (f".req{{offset-path:path('{chain}');animation:req 4.2s cubic-bezier(.77,0,.175,1) infinite;opacity:0}}"
           "@keyframes req{0%{offset-distance:0%;opacity:0}8%{opacity:1}76%{offset-distance:100%;opacity:1}"
           "86%,100%{offset-distance:100%;opacity:0}}"
           "@media (prefers-reduced-motion:reduce){.req{animation:none;opacity:0}}")
    return svg_doc(W, H, "\n".join(b),
                   "Mauro Valdes. De la interfaz al servidor. Desarrollador full-stack con React Native, NestJS y "
                   "PostgreSQL. Disponible en remoto, híbrido o presencial.", css)


# ---------------------------------------------------------------- tarjeta de proyecto
def arrow(cx, cy, color):
    return (f'<path d="M{cx-5} {cy+5} L{cx+5} {cy-5} M{cx-3} {cy-5} H{cx+5} V{cy+3}" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')


def card(th, name, kicker, owner, desc, stack, link_label):
    W, H = 600, 300
    c = THEMES[th]
    begin()
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="20" fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="1.5"/>']
    b.append(T(34, 52, kicker, 15, 400, c["muted"], mono=True))
    ow = measure(owner, 13, 500) + 34
    b.append(f'<rect x="{W - 34 - ow:.1f}" y="32" width="{ow:.1f}" height="28" rx="14" fill="none" '
             f'stroke="{c["line"]}" stroke-width="1.2"/>')
    # Autoría: punto lleno = propio; medio punto = en equipo (no solo color).
    ox = W - 34 - ow + 12
    if owner.startswith("Propio"):
        b.append(f'<circle cx="{ox}" cy="46" r="4" fill="{c["text"]}"/>')
    else:
        b.append(f'<circle cx="{ox}" cy="46" r="4" fill="none" stroke="{c["text"]}" stroke-width="1.3"/>')
        b.append(f'<path d="M{ox} 42 A4 4 0 0 0 {ox} 50 Z" fill="{c["text"]}"/>')
    b.append(T(ox + 9, 50.5, owner, 13, 500, c["text"]))
    b.append(T(34, 112, name, 34, 600, c["text"], ls=-1.2))
    for i, ln in enumerate(wrap(desc, 18, 400, W - 68)[:2]):
        b.append(T(34, 152 + i * 27, ln, 18, 400, c["muted"]))
    ch, _ = chips(stack, 34, 214, c, size=14, h=30, pad=11)
    b += ch
    b.append(T(34, 274, link_label, 15, 500, c["accent"]))
    b.append(arrow(34 + measure(link_label, 15, 500) + 14, 269, c["accent"]))
    return svg_doc(W, H, "\n".join(b), f"{name}. {kicker}. {owner}. {desc} {link_label}.")


PROJECTS = [
    ("designo-crm", "Designo Studio CRM", "CRM interno · web · prácticas", "Equipo de 4",
     "CRM de una agencia de marketing: comercial, proyectos, tareas y presupuestos. Principal contribuidor del frontend.",
     ["React Native", "Expo", "NestJS", "PostgreSQL"], "Ver el caso de estudio"),
    ("respi", "Respi", "Reserva de pistas · móvil y web", "Equipo de 3",
     "Proyecto final de DAM con pago integrado. Mi parte: los pagos con Stripe de extremo a extremo.",
     ["React Native", "Expo", "NestJS", "Stripe"], "Ver el caso de estudio"),
    ("gestilibro", "GestiLibro", "Módulo de Odoo 18 · ERP", "Propio",
     "Cadena de librerías: catálogo, stock por tienda, ventas con validación de existencias y facturación.",
     ["Odoo 18", "Python", "PostgreSQL", "Docker"], "Ver el caso de estudio"),
    ("hakuna-mamoto", "Hakuna MaMoto", "Alquiler de motos · app móvil", "Propio",
     "Catálogo, favoritos, reservas por fechas y tres roles (administrador, mecánico y cliente), sobre Supabase.",
     ["React Native", "Expo", "Supabase", "TanStack Query"], "Ver el caso de estudio"),
    ("club-padel", "Club Pádel", "Gestión de club · escritorio", "Propio",
     "Socios, instalaciones, reservas sin solapamientos, cuotas automáticas e informes.",
     ["C#", "WPF", "MVVM", "SQL Server"], "Ver el caso de estudio"),
    ("motogp", "MotoGP Dashboard", "Estadísticas · escritorio", "Propio",
     "Estadísticas de MotoGP en tiempo real desde la API de Sportradar, con async/await y caché.",
     ["C#", "WPF", "API REST"], "Ver el repositorio"),
]


# ---------------------------------------------------------------- stack
# Las cuatro capas de la constelación del portfolio, con sus logos.
LAYERS = [
    ("Interfaz", ["TypeScript", "React Native + Expo", "React", "Angular", "C# / .NET + SQL Server"]),
    ("API", ["Node.js + NestJS", "Express", "Java + Spring Boot", "API REST + JWT", "Stripe"]),
    ("Datos", ["PostgreSQL", "MySQL / MariaDB", "MongoDB", "Odoo + Python"]),
    ("Despliegue", ["Docker, GitHub Actions y Azure", "Testing (Jest, MSTest)"]),
]
# Lo que también he usado en proyectos o en clase, sin entrar en las capas.
ALSO = ["FastAPI", "Flask", "WPF", "WinForms", "MVVM", "Entity Framework", "Supabase", "Zustand",
        "TanStack Query", "Vite", "Tailwind CSS", "Zod", "Swagger", "TypeORM", "Mongoose", "SQLAlchemy",
        "Flyway", "Alembic", "SQLite", "Linux / VPS", "Git", "Claude Code"]


def logo(x, y, name, c, size=22):
    """Logo de Simple Icons (24 × 24) en una burbuja, como en la constelación."""
    _, d = ICONS[name]
    s = size / 24
    return [f'<circle cx="{x + 18}" cy="{y}" r="18" fill="{c["raised"]}" stroke="{c["line"]}" stroke-width="1"/>',
            f'<path transform="translate({x + 18 - size / 2:.1f} {y - size / 2:.1f}) scale({s:.4f})" d="{d}" '
            f'fill="{c["text"]}"/>']


def stack(th):
    W = 1200
    c = THEMES[th]
    begin()
    b = []
    b += eyebrow(64, 64, "16 tecnologías en cuatro capas, cada una con un proyecto real detrás", c)
    colw = (W - 128) / len(LAYERS)
    top = 122
    for ci, (layer, items) in enumerate(LAYERS):
        x = 64 + ci * colw
        b.append(T(x, top, layer, 24, 600, c["text"], ls=-0.5))
        b.append(f'<line x1="{x}" x2="{x + colw - 28}" y1="{top + 18}" y2="{top + 18}" stroke="{c["accent"]}" '
                 f'stroke-width="2" stroke-opacity=".7"/>')
        for i, name in enumerate(items):
            y = top + 62 + i * 54
            b += logo(x, y, name, c)
            lines = wrap(name, 16, 500, colw - 80)
            for k, ln in enumerate(lines[:2]):
                b.append(T(x + 48, y + 5 - (len(lines[:2]) - 1) * 9 + k * 19, ln, 16, 500, c["text"]))
    rows = max(len(items) for _, items in LAYERS)
    sep = top + 62 + (rows - 1) * 54 + 44
    b.append(f'<line x1="64" x2="{W - 64}" y1="{sep}" y2="{sep}" stroke="{c["line"]}" stroke-width="1.5"/>')
    b.append(T(64, sep + 44, "También he trabajado con", 17, 500, c["muted"]))
    ch, bottom = chips(ALSO, 64, sep + 66, c, maxw=W - 128)
    H = int(bottom + 52)
    b.insert(0, f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="{c["bg"]}" stroke="{c["line"]}" stroke-width="2"/>')
    alt = ("Stack por capas. " + " ".join(f"{layer}: {', '.join(items)}." for layer, items in LAYERS)
           + " También he trabajado con " + ", ".join(ALSO) + ".")
    return svg_doc(W, H, "\n".join(b + ch), alt)


# ---------------------------------------------------------------- cómo trabajo
FRAMEWORKS = [("Express", "Node.js", "Routly"), ("NestJS", "TypeScript", "Respi"),
              ("FastAPI", "Python", "Polideportivo"), ("Spring Boot", "Java", "Ticketmaster"),
              ("Flask", "Python", "Calculadora")]
PRACTICES = [
    ("API REST por capas",
     "La ruta valida y delega, el servicio decide y el repositorio habla con la base de datos. "
     "MVVM y MVC en escritorio, y el frontend organizado por features."),
    ("Autenticación y roles",
     "JWT con access y refresh token, accesos separados para admin y cliente, contraseñas con bcrypt, "
     "cookies seguras, Helmet y CORS."),
    ("Validación en los bordes",
     "Nada llega a la lógica sin pasar por un esquema: Zod, Pydantic, class-validator o Bean Validation, "
     "y un mismo formato de error en toda la API."),
    ("Pagos con Stripe",
     "Integrado en Node, Python y Java: carrito, pedidos, PaymentIntents y pedidos que caducan si no se pagan."),
    ("Datos y migraciones",
     "Seis motores, de PostgreSQL a MongoDB, casi siempre a través de un ORM. Migraciones versionadas "
     "con Flyway, Alembic y TypeORM."),
    ("Tests y documentación",
     "MSTest en .NET, Jest con Supertest en NestJS y Karma con Jasmine en Angular. Swagger en las APIs "
     "y Doxygen en escritorio."),
    ("Contenedores y despliegue",
     "Docker Compose para app y base de datos, GitHub Actions hasta Azure App Service, y un VPS con PM2 "
     "para Respi."),
    ("Desarrollo con IA",
     "Claude Code y Copilot en el día a día, modelos locales con Ollama y aplicaciones completas "
     "construidas por fases guiando a la IA."),
]


def practices(th):
    W = 1200
    c = THEMES[th]
    begin()
    b = []
    b += eyebrow(64, 64, "APIs REST en cinco frameworks", c)
    fw = (W - 128) / len(FRAMEWORKS)
    for i, (name, lang, proj) in enumerate(FRAMEWORKS):
        x = 64 + i * fw
        if i:
            b.append(f'<line x1="{x - 22}" x2="{x - 22}" y1="98" y2="182" stroke="{c["line"]}" stroke-width="1.5"/>')
        b.append(T(x, 128, name, 28, 600, c["text"], ls=-0.8))
        b.append(T(x, 156, lang, 15, 400, c["accent"], mono=True))
        b.append(T(x, 180, proj, 16, 400, c["muted"]))
    y = 222
    b.append(f'<line x1="64" x2="{W - 64}" y1="{y}" y2="{y}" stroke="{c["line"]}" stroke-width="1.5"/>')
    b += eyebrow(64, y + 50, "Lo que aplico en cada proyecto", c)
    gap = 56
    colw = (W - 128 - gap) / 2
    y += 82
    for r in range(0, len(PRACTICES), 2):
        row_h = 0
        for k in range(2):
            title, body = PRACTICES[r + k]
            x = 64 + k * (colw + gap)
            b.append(f'<line x1="{x}" x2="{x + colw}" y1="{y}" y2="{y}" stroke="{c["line"]}" stroke-width="1"/>')
            b.append(T(x, y + 38, title, 21, 600, c["text"], ls=-0.4))
            lines = wrap(body, 17, 400, colw)
            for i, ln in enumerate(lines):
                b.append(T(x, y + 70 + i * 26, ln, 17, 400, c["muted"]))
            row_h = max(row_h, 70 + (len(lines) - 1) * 26 + 32)
        y += row_h
    H = int(y + 24)
    b.insert(0, f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="{c["bg"]}" stroke="{c["line"]}" stroke-width="2"/>')
    alt = ("APIs REST en cinco frameworks: Express, NestJS, FastAPI, Spring Boot y Flask. "
           + " ".join(f"{t}: {d}" for t, d in PRACTICES))
    return svg_doc(W, H, "\n".join(b), alt)


# ---------------------------------------------------------------- certificación
def certification(th):
    W, H = 1200, 176
    c = THEMES[th]
    begin()
    with open(os.path.join(HERE, "aws-academy-cloud-foundations.png"), "rb") as fh:
        badge = base64.b64encode(fh.read()).decode()
    b = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24" fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="1.5"/>',
         f'<rect x="36" y="28" width="120" height="120" rx="14" fill="#FFFFFF" stroke="{c["line"]}" stroke-width="1"/>',
         f'<image x="42" y="34" width="108" height="108" href="data:image/png;base64,{badge}"/>']
    b += eyebrow(190, 58, "Certificación", c)
    b.append(T(190, 100, "AWS Academy Graduate: Cloud Foundations", 30, 600, c["text"], ls=-0.8))
    b.append(T(190, 132, "Amazon Web Services · AWS Academy · 25 nov 2025 · 20 horas", 17, 400, c["muted"]))
    label = "Verificar en Credly"
    lw = measure(label, 16, 500)
    b.append(f'<rect x="{W - 64 - lw - 48:.1f}" y="66" width="{lw + 48:.1f}" height="44" rx="22" fill="none" '
             f'stroke="{c["accent"]}" stroke-width="1.5"/>')
    b.append(T(W - 64 - lw - 26, 93.5, label, 16, 500, c["accent"]))
    b.append(arrow(W - 64 - 18, 88, c["accent"]))
    return svg_doc(W, H, "\n".join(b),
                   "Certificación AWS Academy Graduate: Cloud Foundations, de Amazon Web Services, "
                   "emitida el 25 de noviembre de 2025 (20 horas). Verificable en Credly.")


# ---------------------------------------------------------------- botones de contacto
ICON_PATHS = {
    "web": lambda x, y, col: [f'<circle cx="{x}" cy="{y}" r="10" fill="none" stroke="{col}" stroke-width="2"/>',
                              f'<path d="M{x-10} {y}H{x+10}M{x} {y-10}C{x-5} {y-4},{x-5} {y+4},{x} {y+10}'
                              f'M{x} {y-10}C{x+5} {y-4},{x+5} {y+4},{x} {y+10}" fill="none" stroke="{col}" stroke-width="1.6"/>'],
    "mail": lambda x, y, col: [f'<rect x="{x-11}" y="{y-8}" width="22" height="16" rx="3" fill="none" stroke="{col}" stroke-width="2"/>',
                               f'<path d="M{x-10} {y-6} L{x} {y+1} L{x+10} {y-6}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>'],
    "user": lambda x, y, col: [f'<circle cx="{x}" cy="{y-4}" r="4.5" fill="none" stroke="{col}" stroke-width="2"/>',
                               f'<path d="M{x-9} {y+10} C{x-8} {y+2},{x+8} {y+2},{x+9} {y+10}" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round"/>'],
    "down": lambda x, y, col: [f'<path d="M{x} {y-9}V{y+5}M{x-6} {y-1}L{x} {y+5}L{x+6} {y-1}M{x-9} {y+10}H{x+9}" fill="none" '
                               f'stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'],
}


def pill(th, label, icon, solid=False):
    c = THEMES[th]
    begin()
    size = 18
    W, H = int(28 + 30 + 14 + measure(label, size, 500) + 22 + 34 + 10), 60
    fill, ink, edge = (c["accent"], c["bg"] if th == "dark" else "#FFFFFF", c["accent"]) if solid else (c["surface"], c["text"], c["line"])
    b = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="{(H - 2) / 2}" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>']
    ix, iy = 30, H / 2
    b += ICON_PATHS[icon](ix, iy, ink)
    b.append(T(ix + 22, iy + size * 0.36, label, size, 500, ink))
    ax = W - 31
    b.append(f'<circle cx="{ax}" cy="{iy}" r="16" fill="{ink if solid else c["accent"]}" fill-opacity="{0.18 if solid else 1}"/>')
    b.append(arrow(ax, iy, ink if solid else ("#FFFFFF" if th == "light" else c["bg"])))
    return svg_doc(W, H, "\n".join(b), label)


if __name__ == "__main__":
    for th in THEMES:
        write(f"hero-{th}.svg", hero(th))
        write(f"stack-{th}.svg", stack(th))
        write(f"practices-{th}.svg", practices(th))
        write(f"certification-{th}.svg", certification(th))
        write(f"portfolio-{th}.svg", pill(th, "mauro-vs.dev", "web", solid=True))
        write(f"email-{th}.svg", pill(th, "hello@mauro-vs.dev", "mail"))
        write(f"linkedin-{th}.svg", pill(th, "LinkedIn", "user"))
        write(f"cv-{th}.svg", pill(th, "Descargar CV", "down"))
        for slug, *args in PROJECTS:
            write(f"{slug}-{th}.svg", card(th, *args))
