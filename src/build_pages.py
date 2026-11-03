# -*- coding: utf-8 -*-
"""Subpáginas del sitio final de ESMUN: quienes/, comites/, munmx/, contacto/ (+ portada con la navegación nueva).
Todas comparten cabecera, pie, base.css, el CSS de la portada (P6) y el globo. Salida en /home/claude/web/final/."""
import sys, pathlib, json, html, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_sites as B
import build_p6 as P6
from build_sites import C, esmun_logo_svg
from content import load_json

OUT = pathlib.Path(__file__).resolve().parent.parent / '_site'
DOMAIN = B.C.get('dominio', 'https://esmun.github.io').rstrip('/')   # se cambia en content/site.json
SKIP = '<a class="skip" href="#main">Saltar al contenido</a>'

# Navegación del sitio (rutas relativas; prefix = '' en la raíz, '../' en subpáginas)
NAV = [('quienes/', 'Quiénes somos'), ('munmx/', 'MUNMX 2027'), ('comites/', 'Comités'), ('delegados/', 'Delegados'), ('patrocinios/', 'Patrocinios'), ('noticias/', 'Noticias'), ('contacto/', 'Contacto')]

def header(prefix, active):
    links = ''.join(f'<a href="{prefix}{h}"{" class=on aria-current=page" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f"""{SKIP}<header class="site-header" data-section-follow><div class="wrap"><a class="brand" href="{prefix}" aria-label="ESMUN, inicio">{esmun_logo_svg(kind='horizontal', mode='header')}</a>
<button class="menu-btn" aria-label="Menú" aria-expanded="false"><i></i><i></i><i></i></button>
<nav class="site-nav" aria-label="Principal">{links}<a class="btn cta" href="{prefix}contacto/">Únete</a></nav></div></header>"""

def footer(prefix):
    return B.footer('dark').replace('href="../privacidad/"', f'href="{prefix}privacidad/"').replace('href="../noticias/"', f'href="{prefix}noticias/"').replace('href="#quienes"', f'href="{prefix}quienes/"').replace('href="#munmx"', f'href="{prefix}munmx/"')

def scrollcue(ids):
    return '<nav class="scrollcue" aria-label="Secciones">' + ''.join(f'<a href="#{i}" aria-label="{t}"></a>' for i, t in ids) + '</nav>'

def globe_div(prefix):
    return f'<div id="globe" aria-hidden="true" data-three="{prefix}assets/js/three.min.js"><img src="{prefix}assets/img/globo_fallback.svg" alt=""></div><div id="globe-tip" hidden></div>'

def head(title, desc, prefix, path, extra=''):
    h = B.head(title, desc, f'{prefix}style.css', path_prefix=prefix.rstrip('/') or '.',
               extra=f'<link rel="canonical" href="{DOMAIN}/{path}"><meta property="og:url" content="{DOMAIN}/{path}"><meta name="twitter:card" content="summary_large_image">' + extra)
    h = h.replace('href="./assets/', 'href="assets/').replace('content="./assets/img/photo_ceremony.jpg"', f'content="{DOMAIN}/assets/img/og.jpg"').replace('content="../assets/img/photo_ceremony.jpg"', f'content="{DOMAIN}/assets/img/og.jpg"')
    return h

def scripts(prefix):
    return f'<script src="{prefix}assets/js/land.js" defer></script><script src="{prefix}assets/js/esmun.js" defer></script><script src="{prefix}assets/js/globe.js" defer></script></body></html>'

def slug(s): return s.lower().replace(' ', '-')

def kf(**k): return html.escape(json.dumps(k), quote=True)

# ---------------------------------------------------------------- CSS adicional de las subpáginas
PAGES_CSS = """
.skip{position:absolute;left:12px;top:-60px;z-index:60;background:var(--azul);color:#fff;padding:10px 14px;border-radius:3px;font-weight:600} .skip:focus{top:12px}
@media (hover:none){.only-pointer{display:none}}
.news-card .thumb img{width:100%;height:100%;object-fit:cover}
/* subpáginas: dos layouts, texto a la izquierda (globo der) o texto a la derecha (globo izq) */
.tl .wrap,.tr .wrap{display:grid;gap:48px;align-items:center} .tl .wrap{grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr)} .tr .wrap{grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr)} .tr .wrap>.content{grid-column:2}
.content{max-width:720px} .content .lead{font-size:clamp(18px,1.6vw,24px);line-height:1.45}
@media (max-width:900px){.tl .wrap,.tr .wrap{grid-template-columns:1fr} .tr .wrap>.content{grid-column:1}}
.page-hero h1{font-size:clamp(64px,10vw,170px);line-height:.82}
[data-theme="dark"] .content,.hero .content{color:#F2F3F8} [data-theme="dark"] .lead{color:#DCE3F7}
/* historia */
.timeline{list-style:none;margin:36px 0 0;padding:0;display:grid;gap:0} .timeline li{display:grid;grid-template-columns:110px 1fr;gap:18px;padding:16px 0;border-top:1px solid var(--line)} .timeline b{font-family:var(--display);font-size:40px;line-height:1;color:var(--accent)} .timeline p{margin:0;font-size:15px}
/* comités: paneles teñidos */
.panel{min-height:100svh;color:#fff} .panel .sig{font-family:var(--display);text-transform:uppercase;font-size:clamp(120px,22vw,360px);line-height:.8;letter-spacing:-.01em;color:#fff;opacity:.96} .panel .nm{font-size:clamp(26px,2.6vw,40px);font-weight:600;line-height:1.15;margin:10px 0 6px} .panel .lv{font-size:12px;letter-spacing:.18em;text-transform:uppercase;opacity:.85} .panel .sede{display:inline-flex;align-items:center;gap:8px;margin-top:18px;font-size:13px;letter-spacing:.08em;text-transform:uppercase;opacity:.9} .panel .sede i{width:10px;height:10px;border-radius:50%;background:#FFD98A;box-shadow:0 0 10px #FFD98A;display:inline-block}
.panel .lead{color:inherit;opacity:.92;max-width:52ch;margin-top:18px} .panel .btn{border-color:currentColor;color:inherit;background:transparent} .panel.light{color:var(--tinta)} .panel.light .sig{color:var(--tinta)} .panel.light .sede i{background:var(--tinta);box-shadow:none}
.panel .shield::before{background:radial-gradient(ellipse at center,var(--bgc) 42%,transparent 100%);opacity:.9}
.ficha{margin-top:16px;max-width:60ch} .ficha .lv{display:block;margin-bottom:4px} .ficha p{margin:0;font-size:15px;line-height:1.5;opacity:.95}
.mesa-grid li{grid-template-columns:56px 1fr;grid-template-rows:auto auto;column-gap:12px;align-items:center} .mesa-grid .mav{grid-row:span 2;width:56px;height:56px;border-radius:50%;overflow:hidden;background:rgba(255,255,255,.18);display:grid;place-items:center;font-family:var(--display);font-size:24px} .mesa-grid .mav img{width:100%;height:100%;object-fit:cover} .panel.light .mesa-grid .mav{background:rgba(28,32,48,.15)}
.mesa{margin-top:22px} .mesa ul{list-style:none;margin:8px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px 18px} .mesa li{display:grid;line-height:1.3} .mesa .nm2{font-weight:600;font-size:15px} .mesa .cg{font-size:12px;opacity:.8} .mesa ul.dl{grid-template-columns:repeat(auto-fill,minmax(160px,1fr))}
.com-index{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px} .com-index a{display:inline-grid;grid-auto-flow:column;align-items:center;gap:10px;padding:8px 14px 8px 10px;border:1px solid rgba(255,255,255,.3);border-radius:999px;color:#fff;text-decoration:none;font-size:13px;background:rgba(28,32,48,.4)} .com-index a b{font-family:var(--display);font-size:24px;line-height:1;color:var(--acc);filter:brightness(1.7)}
/* preguntas */
.faq{display:grid;gap:0;margin-top:28px;max-width:720px} .faq details{border-top:1px solid var(--line);padding:14px 0} .faq summary{cursor:pointer;font-weight:600;font-size:17px;list-style:none;display:flex;justify-content:space-between;gap:16px} .faq summary::after{content:'+';font-family:var(--display);font-size:28px;line-height:1;color:var(--accent)} .faq details[open] summary::after{content:'–'} .faq p{margin:10px 0 0;color:var(--muted);max-width:60ch}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin-top:32px} .cards div{background:color-mix(in srgb,var(--papel) 70%,#fff 30%);border:1px solid var(--line);padding:22px;border-radius:3px} .cards h3{font-family:var(--display);text-transform:uppercase;font-size:34px;color:var(--azul);margin:0 0 6px} .cards p{margin:0;font-size:14.5px;color:var(--muted)}
[data-theme="dark"] .cards div{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.18)} [data-theme="dark"] .cards h3{color:#fff} [data-theme="dark"] .cards p{color:#C9D2F0}
.staff-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px;margin-top:30px} .staff{display:grid;grid-template-columns:64px 1fr;gap:6px 16px;align-items:center;padding:18px;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.06);border-radius:3px} .staff .av{grid-row:span 3;width:64px;height:64px;border-radius:50%;overflow:hidden;background:var(--azul);display:grid;place-items:center} .staff .av img{width:100%;height:100%;object-fit:cover} .staff .ini{font-family:var(--display);font-size:30px;color:#fff;letter-spacing:.02em} .staff h3{font-size:17px;font-weight:600;line-height:1.2;margin:0;color:#fff} .staff b{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#FFD98A} .staff p{margin:0;font-size:13.5px;color:#C9D2F0;line-height:1.5}
.dl-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-top:30px} .dl-card{background:color-mix(in srgb,var(--papel) 70%,#fff 30%);border:1px solid var(--line);padding:22px;border-radius:3px;display:grid;gap:10px;align-content:start} .dl-card h3{font-size:19px;font-weight:600;line-height:1.2;margin:0} .dl-card p{margin:0;font-size:14px;color:var(--muted)} .dl-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}
.tiers{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin-top:30px} .tier{background:color-mix(in srgb,var(--papel) 70%,#fff 30%);border:1px solid var(--line);padding:22px;border-radius:3px} .tier h3{font-family:var(--display);text-transform:uppercase;font-size:38px;color:var(--azul);margin:4px 0 6px} .tier p{margin:0 0 10px;font-size:14px;color:var(--muted)} .tier ul{margin:0;padding-left:18px;font-size:14px} .tier li{margin:4px 0}
.needs{list-style:none;margin:28px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px 18px} .needs li{padding:12px 0;border-top:1px solid rgba(255,255,255,.2);font-size:16px}
.logos{list-style:none;margin:14px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:18px;align-items:center} .logos img{height:44px;width:auto;filter:brightness(0) invert(1);opacity:.9}
.more{display:inline-block;margin-top:22px;font-weight:600;text-decoration:none;border-bottom:2px solid var(--accent);padding-bottom:2px}
"""

# ---------------------------------------------------------------- Comités: datos
# (sigla, nombre, nivel · idioma, acento) desde C['comites']; sede, coordenadas de foco (nombre tal cual en CITIES de globe.js), fondo, puntos, descripción
COM = {
 'CS':    dict(sede='Nueva York', focus='Nueva York · ONU', lon=-74, bg='#8A1C2B', dots='#D3A9AE',
              txt=['El órgano de la ONU responsable de la paz y la seguridad internacionales. Lo forman quince Estados: cinco permanentes con derecho de veto (China, Estados Unidos, Francia, Reino Unido y Rusia) y diez electos por dos años.',
                   'Sus resoluciones son vinculantes para todos los miembros de la ONU, así que cada palabra se negocia. En el modelo es el comité de nivel experto, con pocas delegaciones y crisis que cambian a mitad de sesión.']),
 'AGNU':  dict(sede='Nueva York', focus='Nueva York · ONU', lon=-74, bg='#2C7457', dots='#B0CEC1',
              txt=['La asamblea donde están representados los 193 Estados miembros de la ONU, cada uno con un voto. Debate cualquier asunto de la Carta, aprueba el presupuesto y elige a los miembros no permanentes del Consejo de Seguridad.',
                   'Sus resoluciones son recomendaciones, no obligaciones, y por eso el trabajo es sumar mayorías. Es el comité por el que casi todos empiezan: muchas delegaciones, procedimiento clásico, en español.']),
 'IAEA':  dict(sede='Viena', focus='Viena · OIEA', lon=16, bg='#C8962E', dots='#3E2F10', light=True,
              txt=['El Organismo Internacional de Energía Atómica promueve el uso pacífico de la energía nuclear y verifica, con inspecciones y salvaguardias, que los programas nucleares no se desvíen a fines militares.',
                   'Un comité técnico: se debate con informes, datos y tratados (el TNP ante todo). Nivel intermedio, en inglés.']),
 'UNICEF':dict(sede='Nueva York', focus='Nueva York · ONU', lon=-74, bg='#55669A', dots='#C1C8DD',
              txt=['El Fondo de las Naciones Unidas para la Infancia trabaja por los derechos de niñas, niños y adolescentes: salud, nutrición, educación y protección, en más de 190 países y territorios.',
                   'Un comité de programas y cooperación: aquí se discute qué se puede financiar y ejecutar, más que quién tiene razón. Nivel principiante, en inglés.']),
 'OEA':   dict(sede='Washington', focus='Washington · OEA', lon=-77, bg='#AC432E', dots='#E2B8B0',
              txt=['La Organización de los Estados Americanos reúne a los 35 Estados del continente. Sus pilares son la democracia, los derechos humanos, la seguridad y el desarrollo.',
                   'Un comité regional en español: los temas son los de América Latina y el Caribe, y las alianzas se parecen mucho a las reales. Nivel intermedio.']),
 'OTAN':  dict(sede='Bruselas', focus='Bruselas · OTAN', lon=4, bg='#3E3E46', dots='#B6B6B9',
              txt=['La Organización del Tratado del Atlántico Norte es una alianza político-militar de 32 países de Europa y Norteamérica. Su artículo 5 establece que un ataque contra uno es un ataque contra todos.',
                   'En el modelo, el Consejo del Atlántico Norte decide por consenso: nadie vota, todos tienen que estar de acuerdo. Nivel experto, en inglés.']),
}


# ---------------------------------------------------------------- Coaches y asesores (editar aquí; foto opcional en assets/img/real/)
STAFF = [
 dict(nombre='Jubal Esteban Páez', rol='Coach de ESMUN', desc='Entrena a los delegados: procedimiento parlamentario, papeles de posición, oratoria y simulacros antes de cada modelo.', foto=None),
 dict(nombre='Jorge Alberto Ramírez Ochoa', rol='Advisor de ESMUN', desc='Profesor de la PrepaTec Esmeralda. Acompaña al secretariado en la organización de MUNMX Esmeralda y al grupo ante la prepa.', foto=None),
]

STAFF = load_json(pathlib.Path(__file__).resolve().parent/'content'/'staff.json', STAFF)
COM = load_json(pathlib.Path(__file__).resolve().parent/'content'/'comites.json', COM)

def staff_cards():
    out=''
    for s in STAFF:
        ini=''.join(w[0] for w in s['nombre'].split()[:2])
        av=f'<img src="{s["foto"]}" alt="">' if s.get('foto') else f'<span class="ini">{ini}</span>'
        out+=f'<div class="staff reveal"><div class="av">{av}</div><h3>{s["nombre"]}</h3><b>{s["rol"]}</b><p>{s["desc"]}</p></div>'
    return out

def ficha_html(d):
    out = ''
    if len(d.get('txt', [])) > 1: out += f'<div class="ficha reveal d2"><b class="lv">De qué trata</b><p>{d["txt"][1]}</p></div>'
    if d.get('facultades'): out += f'<div class="ficha reveal d3"><b class="lv">Facultades</b><p>{d["facultades"]}</p></div>'
    tema = d.get('tema') or 'Por confirmar'
    out += f'<div class="ficha reveal d3"><b class="lv">Tópico 2027</b><p>{tema}{"" if tema != "Por confirmar" else " · se anuncia con la convocatoria"}</p></div>'
    return out

def mesa_html(d):
    """Mesa directiva (y opcionalmente delegaciones) de un comité, si están en comites.json."""
    out = ''
    if d.get('mesa'):
        def av(m):
            if m.get('foto'): return f'<img src="../assets/img/{m["foto"]}" alt="" loading="lazy">'
            return '<span>' + ''.join(w[0] for w in m['nombre'].split()[:2]) + '</span>'
        out += '<div class="mesa reveal d3"><b class="lv">Mesa directiva</b><ul class="mesa-grid">' + ''.join(f'<li><div class="mav">{av(m)}</div><span class="nm2">{m["nombre"]}</span><span class="cg">{m.get("cargo","")}</span></li>' for m in d['mesa']) + '</ul></div>'
    if d.get('delegaciones'):
        out += '<div class="mesa reveal d3"><b class="lv">Delegaciones</b><ul class="dl">' + ''.join(f'<li><span class="nm2">{x["pais"]}</span><span class="cg">{x.get("escuela","")}</span></li>' for x in d['delegaciones']) + '</ul></div>'
    return out

def comites_page(prefix='../'):
    secs = [('intro', 'Comités')] + [(slug(c[0]), c[0]) for c in C['comites']]
    body = header(prefix, 'comites/') + globe_div(prefix) + scrollcue(secs) + '<main id="main">'
    body += f"""<section class="page-hero tl" id="intro" data-section data-theme="dark" data-globe="hero" data-kf="{kf(x=1.05, y=-.05, s=1.0, lon=-60, dark=True, glow=.35)}"><div class="wrap"><div class="content">
<p class="eyebrow reveal" style="color:#B9C6EE">MUNMX Esmeralda · Comités</p><h1 class="display reveal d1">Ocho<br>comités</h1>
<p class="lead reveal d2" style="margin-top:22px">Ocho comités para MUNMX Esmeralda 2027, en inglés y en español: desde la Asamblea General, donde se empieza, hasta el Consejo de Seguridad y la OTAN. Cada uno con qué es, de qué trata y qué puede decidir.</p>
<p class="reveal d2" style="font-size:14px;color:#B9C6EE;margin-top:14px">Niveles, tópicos y mesas directivas se publican conforme se confirman.</p>
<div class="com-index reveal d3">{''.join(f'<a href="#{slug(c[0])}" style="--acc:{c[3]}"><b>{c[0]}</b>{c[1]}</a>' for c in C['comites'])}</div></div><div aria-hidden="true"></div></div></section>"""
    for i, (sig, nm, lv, acc) in enumerate(C['comites']):
        d = COM[sig]; left = i % 2 == 0; light = d.get('light', False)
        theme = 'paper' if light else 'dark'
        body += f"""<section class="panel {'tl' if left else 'tr'}{' light' if light else ''}" id="{slug(sig)}" data-section data-theme="{theme}" data-bg="{d['bg']}" style="background:{d['bg']};--bgc:{d['bg']};--acc:{acc}" data-globe="hero" data-kf="{kf(x=(1.1 if left else -1.1), y=-.05, s=.95, lon=d['lon'], dark=(not light), glow=.5, bg=d['bg'], dots=d['dots'], focus=d['focus'])}"><div class="wrap"><div class="content shield">
<div class="sig reveal">{sig}</div><div class="nm reveal d1">{nm}</div><div class="lv reveal d1">{lv}</div>
<p class="sede reveal d2"><i></i>Sede real: {d['sede']}</p>
<p class="lead reveal d2">{d['txt'][0]}</p>{ficha_html(d)}{mesa_html(d)}
</div>{'<div aria-hidden="true"></div>' if left else ''}</div></section>"""
    body += f"""<section class="tl" id="unete" data-section data-theme="paper" data-globe="contacto" data-kf="{kf(x=1.6, y=-.1, s=.82, lon=-99, dark=False, glow=0)}"><div class="wrap"><div class="content"><p class="eyebrow reveal">Y después</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Elige tu comité</h2><p class="lead reveal d2" style="margin-top:18px">Si nunca has participado, empieza por la Asamblea General, UNICEF o el Senado. Si ya tienes un par de modelos, prueba ONU Mujeres, el FMI o la Comisión de Derecho Internacional. El Consejo de Seguridad y la OTAN son para quien ya sabe lo que es una sesión sin receso.</p><p class="reveal d3" style="margin-top:24px;display:flex;gap:14px;flex-wrap:wrap"><a class="btn" href="{prefix}contacto/">Únete al equipo</a><a class="btn ghost" href="{prefix}munmx/">MUNMX 2027</a></p></div><div aria-hidden="true"></div></div></section></main>"""
    return head('Comités · ESMUN PrepaTec Esmeralda', 'Los ocho comités de MUNMX Esmeralda 2027: Asamblea General, Consejo de Seguridad, UNICEF, ONU Mujeres, Comisión de Derecho Internacional, OTAN, FMI y Cámara de Senadores. Qué es, de qué trata y facultades de cada uno.', prefix, 'comites/') + body + footer(prefix) + scripts(prefix)

def quienes_page(prefix='../'):
    secs = [('intro', 'Quiénes somos'), ('hacemos', 'Qué hacemos'), ('coaches', 'Coaches y asesores'), ('historia', 'Historia'), ('cifras', 'Cifras')]
    body = header(prefix, 'quienes/') + globe_div(prefix) + scrollcue(secs) + '<main id="main">'
    body += f"""<section class="page-hero tl" id="intro" data-section data-theme="dark" data-globe="hero"><div class="wrap"><div class="content"><p class="eyebrow reveal" style="color:#B9C6EE">Quiénes somos</p><h1 class="display reveal d1">Un grupo<br>que debate</h1><p class="lead reveal d2" style="margin-top:22px">{C['intro']}</p><p class="lead reveal d3" style="margin-top:12px">Lo llevan alumnos de la prepa con el apoyo de un advisor docente. Hay delegados, mesas directivas y un secretariado, y cada año cambian las caras.</p></div><div aria-hidden="true"></div></div></section>
<section class="tr" id="hacemos" data-section data-theme="paper" data-globe="quienes"><div class="wrap"><div class="content"><p class="eyebrow reveal">Qué hacemos</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Cuatro cosas</h2>
<div class="cards">{''.join(f'<div class="reveal d{i%4}"><h3>{t}</h3><p>{p}</p></div>' for i,(t,p) in enumerate(C['que']))}</div></div></div></section>
<section class="tl" id="coaches" data-section data-theme="dark" data-globe="hero" data-kf="{kf(x=1.3, y=-.15, s=.95, lon=-99, dark=True, glow=.3)}"><div class="wrap"><div class="content"><p class="eyebrow reveal" style="color:#B9C6EE">Coaches y asesores</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Quién acompaña</h2><p class="lead reveal d2" style="margin-top:18px">ESMUN lo dirigen alumnos. Estas son las personas de la prepa que los asesoran: en el procedimiento, en la preparación de posturas y en la logística de la conferencia.</p>
<div class="staff-grid reveal d2">{staff_cards()}</div>
<p class="reveal d3" style="margin-top:22px;font-size:14px;color:#B9C6EE">Los coaches invitados de cada edición se anuncian con la convocatoria de MUNMX.</p></div><div aria-hidden="true"></div></div></section>
<section class="tl" id="historia" data-section data-theme="dark" data-globe="hero" data-kf="{kf(x=1.3, y=-.2, s=1.0, lon=-74, dark=True, glow=.5, focus='Nueva York · ONU')}"><div class="wrap"><div class="content"><p class="eyebrow reveal" style="color:#B9C6EE">Historia</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Desde 2019</h2>
<ol class="timeline reveal d2">{''.join(f'<li><b>{y}</b><p>{t}</p></li>' for y,t in C['timeline'])}</ol></div><div aria-hidden="true"></div></div></section>
<section class="tr" id="cifras" data-section data-theme="paper" data-globe="quienes"><div class="wrap"><div class="content"><p class="eyebrow reveal">En cifras</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Lo que se mide</h2>
<div class="stats">{''.join(f'<div class="reveal d{i%4}"><div class="n num" {"data-count="+n if n.isdigit() and n!="2019" else ""}>{n}</div><b>{l}</b><p>{p}</p></div>' for i,(n,l,p) in enumerate(C['stats']))}</div>
<p class="reveal d3" style="margin-top:28px;display:flex;gap:14px;flex-wrap:wrap"><a class="btn" href="{prefix}contacto/">Únete al equipo</a><a class="btn ghost" href="{prefix}comites/">Conoce los comités</a></p></div></div></section></main>"""
    return head('Quiénes somos · ESMUN PrepaTec Esmeralda', 'Qué es ESMUN, qué hacemos, nuestra historia desde 2019 y las cifras del grupo de Modelo de Naciones Unidas de la PrepaTec Esmeralda.', prefix, 'quienes/') + body + footer(prefix) + scripts(prefix)

def munmx_page(prefix='../'):
    secs = [('intro', 'MUNMX 2027'), ('mun', 'Qué es un MUN'), ('que', 'La conferencia'), ("edicion-2026", "Edición 2026"), ('delegaciones', 'Delegaciones')]
    body = header(prefix, 'munmx/') + globe_div(prefix) + scrollcue(secs) + '<main id="main">'
    body += f"""<section id="intro" data-section data-theme="dark" data-globe="munmx" style="text-align:center"><div class="wrap" style="display:grid;justify-items:center;isolation:isolate"><p class="eyebrow reveal" style="color:#B9C6EE">MUNMX Esmeralda 2027</p><h1 class="display reveal d1" style="font-size:clamp(90px,16vw,300px);line-height:.78;color:#fff">11 · 12 · 13<br>de marzo</h1>
<img class="lockup reveal d2" src="{prefix}assets/logo/MUNMX_2027_lockup_horizontal_blanco.svg" alt="MUNMX Esmeralda 2027" style="width:min(440px,86vw);height:auto;margin:28px auto 22px">
<p class="lead reveal d2" style="color:#C9D2F0;max-width:52ch">Jueves 11, viernes 12 y sábado 13 de marzo de 2027 en la PrepaTec Esmeralda, Atizapán de Zaragoza. Los comités y la apertura del registro se publican aquí y en {C['ig']}.</p>
<div style="display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin-top:26px" class="reveal d3"><a class="btn" href="{prefix}registro/" style="background:#fff;color:var(--azul);border-color:#fff">Pre-registro de delegaciones</a><a class="btn ghost" href="{C['mymun']}" rel="noopener" target="_blank" style="color:#fff">ESMUN 2024 en mymun</a></div></div></section>
<section class="tl" id="mun" data-section data-theme="paper" data-globe="noticias"><div class="wrap"><div class="content"><p class="eyebrow reveal">Qué es un Modelo de Naciones Unidas</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Un país,<br>una silla</h2>
<p class="lead reveal d2" style="margin-top:18px">Un Modelo de Naciones Unidas es una simulación: cada estudiante representa a un país (o a un senador, en el caso del Senado) dentro de un comité real, con sus reglas y sus temas. Durante dos o tres días investiga, redacta, negocia y vota como lo haría un diplomático.</p>
<div class="cards"><div class="reveal"><h3>Antes</h3><p>Recibes tu país y tu comité, estudias la guía del tópico y escribes un papel de posición: qué piensa tu país y qué propone.</p></div><div class="reveal d1"><h3>En sesión</h3><p>Discursos, listas de oradores, mociones y caucus. La mesa directiva modera con el protocolo del modelo; todo se decide por votación.</p></div><div class="reveal d2"><h3>Al final</h3><p>Los bloques redactan proyectos de resolución y el comité vota. Se reconoce a las mejores delegaciones y al mejor papel de posición.</p></div></div>
<p class="reveal d3" style="margin-top:24px"><a class="more" href="{prefix}delegados/">Guía para delegados: protocolo y ejemplos</a></p></div><div aria-hidden="true"></div></div></section>
<section class="tr" id="que" data-section data-theme="paper" data-globe="quienes"><div class="wrap"><div class="content"><p class="eyebrow reveal">Qué es</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">La conferencia<br>de la prepa</h2><p class="lead reveal d2" style="margin-top:18px">MUNMX es el Modelo de Naciones Unidas de la red PrepaTec. MUNMX Esmeralda es la edición que organiza nuestra prepa: durante dos días, delegaciones de la zona debaten en comités en español e inglés, con mesas directivas y un secretariado formados por alumnos de ESMUN.</p>
<div class="cards"><div class="reveal"><h3>Comités</h3><p>De nivel principiante a experto, en español o en inglés. La lista de 2027 se anuncia con la convocatoria.</p></div><div class="reveal d1"><h3>Delegaciones</h3><p>Alumnos de la PrepaTec Esmeralda y de otras escuelas, en equipos con su advisor.</p></div><div class="reveal d2"><h3>Registro</h3><p>Primero el <a href="{prefix}registro/">pre-registro</a> de delegaciones; el registro oficial por delegado se publica aquí cuando abre.</p></div></div></div></div></section>
<section class="tl" id="edicion-2026" data-section data-theme="dark" data-globe="hero" data-kf="{kf(x=1.2, y=-.1, s=1.0, lon=-99, dark=True, glow=.8)}"><div class="wrap"><div class="content"><p class="eyebrow reveal" style="color:#B9C6EE">Edición 2026</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Once comités<br>y una sala llena</h2><p class="lead reveal d2" style="margin-top:18px">MUNMX Esmeralda 2026 tuvo once comités, del Consejo de Seguridad a Star Wars Rebellion. La edición anterior, ESMUN 2024, convocó a 120 delegados en seis comités; su ficha sigue en mymun.</p>
<p class="reveal d3" style="margin-top:24px;display:flex;gap:14px;flex-wrap:wrap"><a class="btn" href="{C['mymun']}" rel="noopener" target="_blank" style="background:#fff;color:var(--azul);border-color:#fff">ESMUN 2024 en mymun</a><a class="btn ghost" href="{prefix}noticias/" style="color:#fff">Crónica en Noticias</a></p></div><div aria-hidden="true"></div></div></section>
<section class="tr" id="delegaciones" data-section data-theme="paper" data-globe="quienes"><div class="wrap"><div class="content"><p class="eyebrow reveal">Para delegaciones</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Cómo participar</h2>
<div class="faq reveal d2"><details open><summary>¿Quién puede registrarse?</summary><p>Delegaciones de preparatorias de la zona, con un docente o advisor responsable. También alumnos de la PrepaTec Esmeralda a título individual.</p></details><details><summary>¿Cuándo es y cuándo abre el registro?</summary><p>La conferencia es el 11, 12 y 13 de marzo de 2027. El registro oficial abre con la convocatoria; mientras tanto, el <a href="{prefix}registro/">pre-registro</a> nos dice cuántas delegaciones vienen y te avisa primero.</p></details><details><summary>¿Hay que saber inglés?</summary><p>No para todos los comités: hay comités en español y en inglés, y niveles de principiante a experto.</p></details><details><summary>¿Cómo elijo comité y país?</summary><p>Al registrarte indicas nivel e idioma; el secretariado asigna comité y país y te envía la guía de estudio.</p></details></div>
<p class="reveal d3" style="margin-top:28px"><a class="btn" href="{prefix}registro/">Pre-registrar a mi delegación</a></p></div></div></section></main>"""
    EVENT_LD='<script type="application/ld+json">{"@context": "https://schema.org", "@type": "Event", "name": "MUNMX Esmeralda 2027", "description": "Modelo de Naciones Unidas de la PrepaTec Esmeralda. Comités en español e inglés para delegaciones de preparatoria.", "startDate": "2027-03-11", "endDate": "2027-03-13", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled", "location": {"@type": "Place", "name": "PrepaTec Esmeralda", "address": {"@type": "PostalAddress", "addressLocality": "Atizapán de Zaragoza", "addressRegion": "Estado de México", "addressCountry": "MX"}}, "organizer": {"@type": "Organization", "name": "ESMUN", "url": "https://esmun.github.io/"}, "url": "https://esmun.github.io/munmx/"}</script>'
    return head('MUNMX Esmeralda 2027 · ESMUN', 'MUNMX Esmeralda 2027: 11, 12 y 13 de marzo de 2027 en la PrepaTec Esmeralda. Modelo de Naciones Unidas para delegaciones de preparatoria; comités y registro por anunciar.', prefix, 'munmx/', extra=EVENT_LD) + body + footer(prefix) + scripts(prefix)

def registro_page(prefix='../'):
    """Pre-registro de delegaciones (formulario provisional hasta que abra el registro oficial)."""
    secs = [('intro', 'Registro'), ('como', 'Cómo funciona')]
    form = f"""<form class="form" {B.form_attrs("registro")[0]} method="post">{B.form_attrs("registro")[1]}
<input type="hidden" name="formulario" value="pre-registro MUNMX 2027">
<div class="row"><label>Escuela<input name="escuela" type="text" autocomplete="organization" required></label><label>Ciudad<input name="ciudad" type="text" autocomplete="address-level2" required></label></div>
<div class="row"><label>Nombre del advisor o responsable<input name="responsable" type="text" autocomplete="name" required></label><label>Correo<input name="correo" type="email" autocomplete="email" required></label></div>
<div class="row"><label>Teléfono (opcional)<input name="telefono" type="tel" autocomplete="tel"></label><label>Delegados estimados<input name="delegados" type="number" min="1" max="60" inputmode="numeric" required></label></div>
<label>Idiomas de interés<select name="idiomas"><option>Español e inglés</option><option>Solo español</option><option>Solo inglés</option></select></label>
<label>Niveles de interés<select name="niveles"><option>Principiante e intermedio</option><option>Principiante</option><option>Intermedio</option><option>Experto</option><option>Todos</option></select></label>
<label>Comentarios<textarea name="mensaje" rows="3" placeholder="Comités que les interesan, experiencia previa, necesidades especiales"></textarea></label>
<label style="display:flex;gap:10px;align-items:center;text-transform:none;letter-spacing:0;font-weight:500;font-size:14px"><input type="checkbox" name="aviso" checked style="width:18px;height:18px"> Avísenme por correo el día que abra el registro oficial</label>
<div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap"><button class="btn" type="submit">Enviar pre-registro</button><span class="form-msg" role="status" aria-live="polite" style="font-size:13px;color:var(--muted)"></span></div>
<small>El pre-registro no compromete lugares ni tiene costo. Usamos los datos solo para organizar la conferencia y avisarles del registro (<a href="{prefix}privacidad/">aviso de privacidad</a>).</small></form>"""
    body = header(prefix, '') + globe_div(prefix) + scrollcue(secs) + '<main id="main">'
    body += f"""<section class="tr" id="intro" data-section data-theme="paper" data-globe="contacto"><div class="wrap"><div class="content"><p class="eyebrow reveal">MUNMX Esmeralda 2027 · 11, 12 y 13 de marzo</p><h1 class="display reveal d1" style="font-size:clamp(56px,8vw,130px);line-height:.88">Pre-registro<br>de delegaciones</h1>
<p class="lead reveal d2" style="margin-top:18px">El registro oficial abre con la convocatoria. Mientras tanto, las escuelas interesadas pueden dejar aquí sus datos: con eso calculamos cupos por comité y les avisamos primero.</p>
<div class="reveal d3" style="margin-top:28px;background:color-mix(in srgb,var(--papel) 70%,#fff 30%);padding:24px;border:1px solid var(--line);border-radius:3px">{form}</div></div></div></section>
<section class="tl" id="como" data-section data-theme="dark" data-globe="hero" data-kf="{kf(x=1.3, y=-.1, s=1.0, lon=-99, dark=True, glow=.5)}"><div class="wrap"><div class="content"><p class="eyebrow reveal" style="color:#B9C6EE">Cómo funciona</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Tres pasos</h2>
<div class="cards"><div class="reveal"><h3>1 · Pre-registro</h3><p>Este formulario. Nos dice cuántas delegaciones vienen y qué idiomas y niveles necesitan.</p></div><div class="reveal d1"><h3>2 · Registro</h3><p>Con la convocatoria abre el registro oficial, por delegado, con asignación de comité y país.</p></div><div class="reveal d2"><h3>3 · Guías y sesiones</h3><p>Cada delegado recibe la guía de estudio de su comité y el calendario de las sesiones de preparación.</p></div></div>
<p class="reveal d3" style="margin-top:28px;display:flex;gap:14px;flex-wrap:wrap"><a class="btn" href="{prefix}comites/" style="background:#fff;color:var(--azul);border-color:#fff">Ver los comités</a><a class="btn ghost" href="{prefix}munmx/" style="color:#fff">Sobre MUNMX 2027</a></p></div><div aria-hidden="true"></div></div></section></main>"""
    return head('Registro · MUNMX Esmeralda 2027', 'Pre-registro de delegaciones para MUNMX Esmeralda 2027 (11, 12 y 13 de marzo). El registro oficial abre con la convocatoria.', prefix, 'registro/') + body + footer(prefix) + scripts(prefix)

def privacidad_page(prefix='../'):
    org = 'ESMUN, grupo estudiantil de la PrepaTec Esmeralda (Tecnológico de Monterrey)'
    body = header(prefix, '') + globe_div(prefix) + '<main id="main">'
    body += f"""<section class="tr" id="aviso" data-section data-theme="paper" data-globe="quienes" style="min-height:auto"><div class="wrap"><div class="content"><p class="eyebrow reveal">Aviso de privacidad</p><h1 class="display reveal d1" style="font-size:clamp(56px,8vw,130px);line-height:.88">Tus datos</h1>
<div class="reveal d2" style="margin-top:18px;font-size:16px;line-height:1.7;max-width:68ch">
<p><b>Responsable.</b> {org}, con domicilio en {C['ciudad']}. Contacto: <a href="mailto:{C['mail']}">{C['mail']}</a>.</p>
<p><b>Qué datos recabamos.</b> Los que escribes en los formularios de este sitio: nombre, correo, escuela, ciudad, teléfono (opcional), número estimado de delegados y tus comentarios.</p>
<p><b>Para qué.</b> Responder a tu mensaje, organizar la conferencia MUNMX Esmeralda (cupos, comités, comunicación con delegaciones) y, si lo marcaste, avisarte de la apertura del registro. No usamos los datos para publicidad ni los vendemos.</p>
<p><b>Con quién se comparten.</b> Con el equipo organizador de ESMUN y su advisor. Los formularios se procesan con un servicio externo de recepción de formularios; si el sitio tiene analítica activada, se recogen estadísticas de uso anónimas.</p>
<p><b>Menores de edad.</b> Si tienes menos de 18 años, envía tus datos con autorización de tu madre, padre o tutor.</p>
<p><b>Tus derechos (ARCO).</b> Puedes pedir acceso, rectificación, cancelación u oposición escribiendo a <a href="mailto:{C['mail']}">{C['mail']}</a>. Respondemos en un máximo de 20 días hábiles.</p>
<p><b>Cambios.</b> Este aviso puede actualizarse; la versión vigente es la publicada en esta página. Última actualización: noviembre de 2026.</p>
<p class="ai-note" style="margin-top:28px">Borrador para revisión del advisor y de la prepa antes de publicar.</p></div></div></div></section></main>"""
    return head('Aviso de privacidad · ESMUN', 'Aviso de privacidad del sitio de ESMUN, grupo estudiantil de la PrepaTec Esmeralda.', prefix, 'privacidad/', extra='<meta name="robots" content="noindex">') + body + footer(prefix) + scripts(prefix)

def delegados_page(prefix='../'):
    secs = [('intro', 'Delegados'), ('descargas', 'Descargas'), ('consejos', 'Consejos')]
    cards = ''
    for d in C.get('descargas', []):
        if d.get('disponible'):
            links = f'<a class="btn" href="{prefix}assets/{d["archivo"]}" download>Descargar PDF</a>' + (f' <a class="btn ghost" href="{prefix}assets/{d["editable"]}" download>Word</a>' if d.get('editable') else '')
        else:
            links = f'<span class="pill">{d.get("nota", "Próximamente")}</span>'
        cards += f'<div class="dl-card reveal"><h3>{d["titulo"]}</h3><p>{d["desc"]}</p><div class="dl-actions">{links}</div></div>'
    body = header(prefix, 'delegados/') + globe_div(prefix) + scrollcue(secs) + '<main id="main">'
    body += f"""<section class="page-hero tl" id="intro" data-section data-theme="dark" data-globe="hero" data-kf="{kf(x=1.1, y=-.05, s=1.0, lon=-74, dark=True, glow=.4, focus='Nueva York · ONU')}"><div class="wrap"><div class="content"><p class="eyebrow reveal" style="color:#B9C6EE">Delegados</p><h1 class="display reveal d1">Antes de<br>la sesión</h1>
<p class="lead reveal d2" style="margin-top:22px">Lo que necesitas para llegar preparado a MUNMX Esmeralda 2027: el protocolo del modelo, un papel de posición y una resolución de ejemplo con el formato que se pide, y la carta de bienvenida de la mesa.</p>
<p class="reveal d3" style="margin-top:24px;display:flex;gap:14px;flex-wrap:wrap"><a class="btn" href="#descargas" style="background:#fff;color:var(--azul);border-color:#fff">Ir a las descargas</a><a class="btn ghost" href="{prefix}comites/" style="color:#fff">Ver los comités</a></p></div><div aria-hidden="true"></div></div></section>
<section class="tr" id="descargas" data-section data-theme="paper" data-globe="quienes"><div class="wrap"><div class="content"><p class="eyebrow reveal">Descargas</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Documentos</h2><div class="dl-grid">{cards}</div></div></div></section>
<section class="tl" id="consejos" data-section data-theme="dark" data-globe="hero" data-kf="{kf(x=1.3, y=-.15, s=.95, lon=-99, dark=True, glow=.3)}"><div class="wrap"><div class="content"><p class="eyebrow reveal" style="color:#B9C6EE">Consejos de la mesa</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Cómo se gana<br>un comité</h2>
<div class="faq reveal d2" style="--line:rgba(255,255,255,.2);--muted:#C9D2F0;--accent:#FFD98A"><details open><summary>Investiga a tu país, no solo el tema</summary><p>Qué ha votado, con quién se alía, qué le conviene. Un delegado que sabe por qué su país piensa lo que piensa negocia mejor que uno que solo conoce el problema.</p></details><details><summary>Habla pronto y habla corto</summary><p>Los primeros discursos fijan los bloques. Un minuto con una propuesta concreta vale más que tres de contexto.</p></details><details><summary>Escribe desde el primer caucus</summary><p>Las resoluciones que se aprueban son las que ya existían en papel cuando los demás seguían hablando.</p></details><details><summary>Cede en lo accesorio, nunca en la postura</summary><p>Firmar un proyecto ajeno es diplomacia; firmar uno que contradice a tu país es un error que la mesa nota.</p></details><details><summary>Respeta el protocolo y a la mesa</summary><p>Las mociones bien hechas, los puntos de orden justificados y el trato formal cuentan en la evaluación.</p></details></div></div><div aria-hidden="true"></div></div></section></main>"""
    return head('Delegados · MUNMX Esmeralda 2027', 'Protocolo del modelo, ejemplos de papel de posición y de resolución, y carta de bienvenida para las y los delegados de MUNMX Esmeralda 2027.', prefix, 'delegados/') + body + footer(prefix) + scripts(prefix)

def patrocinios_page(prefix='../'):
    P = C.get('patrocinios', {})
    secs = [('intro', 'Patrocinios'), ('niveles', 'Niveles'), ('especie', 'En especie'), ('contacto', 'Contacto')]
    niveles = ''.join(f'<div class="tier reveal d{i}"><b class="lv">Nivel {i+1}</b><h3>{n["nombre"]}</h3><p>{n["desc"]}</p><ul>{"".join(f"<li>{b}</li>" for b in n["beneficios"])}</ul></div>' for i, n in enumerate(P.get('niveles', [])))
    especie = ''.join(f'<li>{x}</li>' for x in P.get('en_especie', []))
    logos = ''.join(f'<li><img src="{prefix}assets/img/{l["logo"]}" alt="{l["nombre"]}"></li>' for l in P.get('logos', []))
    mail = C['mail']; asunto = P.get('contacto_asunto', 'Patrocinio')
    body = header(prefix, 'patrocinios/') + globe_div(prefix) + scrollcue(secs) + '<main id="main">'
    body += f"""<section class="page-hero tl" id="intro" data-section data-theme="dark" data-globe="hero" data-kf="{kf(x=1.1, y=-.05, s=1.0, lon=-99, dark=True, glow=.5)}"><div class="wrap"><div class="content"><p class="eyebrow reveal" style="color:#B9C6EE">Patrocinios · ESMUN y MUNMX Esmeralda 2027</p><h1 class="display reveal d1">Ponga su nombre<br>en la sala</h1>
<p class="lead reveal d2" style="margin-top:22px">MUNMX Esmeralda reúne durante tres días a delegaciones de preparatorias de la zona en ocho comités. Lo organizan alumnos; lo que cuesta (gafetes, placas, guías, coffee break, reconocimientos) sale de patrocinios. A cambio, su marca aparece donde están las familias, las escuelas y los jóvenes que debaten.</p>
<p class="reveal d3" style="margin-top:24px;display:flex;gap:14px;flex-wrap:wrap"><a class="btn" href="#niveles" style="background:#fff;color:var(--azul);border-color:#fff">Ver niveles</a><a class="btn ghost" href="mailto:{mail}?subject={asunto}" style="color:#fff">Escribirnos</a></p></div><div aria-hidden="true"></div></div></section>
<section class="tr" id="niveles" data-section data-theme="paper" data-globe="quienes"><div class="wrap"><div class="content"><p class="eyebrow reveal">Niveles</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Tres formas<br>de apoyar</h2><div class="tiers">{niveles}</div><p class="reveal d3" style="margin-top:18px;font-size:14px;color:var(--muted)">Los montos se acuerdan con cada patrocinador según el rubro; el advisor de ESMUN emite el reconocimiento correspondiente.</p></div></div></section>
<section class="tl" id="especie" data-section data-theme="dark" data-globe="hero" data-kf="{kf(x=1.3, y=-.1, s=.95, lon=-99, dark=True, glow=.3)}"><div class="wrap"><div class="content"><p class="eyebrow reveal" style="color:#B9C6EE">En especie</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Lo que hace falta</h2><ul class="needs reveal d2">{especie}</ul>
{'<p class="eyebrow reveal d3" style="color:#B9C6EE;margin-top:36px">Patrocinadores 2027</p><ul class="logos reveal d3">' + logos + '</ul>' if logos else '<p class="reveal d3" style="margin-top:28px;font-size:14px;color:#B9C6EE">Los patrocinadores de la edición 2027 se publican aquí conforme se confirman.</p>'}</div><div aria-hidden="true"></div></div></section>
<section class="tr" id="contacto" data-section data-theme="paper" data-globe="contacto"><div class="wrap"><div class="content"><p class="eyebrow reveal">Contacto</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Hablemos</h2><p class="lead reveal d2" style="margin-top:18px">Escriba a <a href="mailto:{mail}?subject={asunto}">{mail}</a> con el nombre de su empresa u organización y el rubro que le interesa; le respondemos con una propuesta en menos de una semana.</p><p class="reveal d3" style="margin-top:24px"><a class="btn" href="{prefix}contacto/">Formulario de contacto</a></p></div></div></section></main>"""
    return head('Patrocinios · ESMUN y MUNMX Esmeralda 2027', 'Cómo patrocinar MUNMX Esmeralda 2027 y a ESMUN: niveles, beneficios y apoyos en especie.', prefix, 'patrocinios/') + body + footer(prefix) + scripts(prefix)

def contacto_page(prefix='../'):
    secs = [('intro', 'Contacto'), ('faq', 'Preguntas')]
    body = header(prefix, 'contacto/') + globe_div(prefix) + scrollcue(secs) + '<main id="main">'
    body += f"""<section class="tr" id="intro" data-section data-theme="paper" data-globe="contacto"><div class="wrap"><div class="content"><p class="eyebrow reveal">Contacto</p><h1 class="display reveal d1" style="font-size:clamp(64px,9vw,150px);line-height:.85">Hablemos</h1><p class="lead reveal d2" style="margin-top:18px">Escríbenos si quieres entrar al equipo, registrar a tu delegación o proponer una alianza.</p>
<p class="reveal d2" style="line-height:1.9;margin-top:18px"><a href="mailto:{C['mail']}">{C['mail']}</a><br><a href="{C['ig_url']}" rel="noopener" target="_blank">Instagram {C['ig']}</a><br>PrepaTec Esmeralda · {C['ciudad']}</p>
<div class="reveal d3" style="margin-top:28px">{B.contact_form(PRIV=prefix+'privacidad/')}</div></div></div></section>
<section class="tl" id="faq" data-section data-theme="dark" data-globe="hero" data-kf="{kf(x=1.3, y=-.1, s=1.0, lon=-99, dark=True, glow=.4)}"><div class="wrap"><div class="content"><p class="eyebrow reveal" style="color:#B9C6EE">Preguntas frecuentes</p><h2 class="display reveal d1" style="font-size:clamp(56px,8vw,130px)">Antes de escribir</h2>
<div class="faq reveal d2" style="--line:rgba(255,255,255,.2);--muted:#C9D2F0;--accent:#FFD98A"><details open><summary>¿Necesito experiencia para entrar a ESMUN?</summary><p>No. Empiezas con sesiones de preparación y simulacros, y debutas en la conferencia de la prepa.</p></details><details><summary>¿Cuándo son las sesiones?</summary><p>Se acuerdan con el equipo cada semestre; te lo decimos al responder.</p></details><details><summary>¿Puede participar alguien de otra escuela?</summary><p>En MUNMX Esmeralda sí, como delegación con su advisor. ESMUN como grupo es de la PrepaTec Esmeralda.</p></details><details><summary>¿Cómo pueden apoyar las empresas o exalumnos?</summary><p>Con patrocinio de la conferencia, materiales o charlas. Escríbenos y te contamos qué hace falta este año.</p></details></div></div><div aria-hidden="true"></div></div></section></main>"""
    return head('Contacto · ESMUN PrepaTec Esmeralda', 'Escríbenos para unirte a ESMUN, registrar a tu delegación en MUNMX Esmeralda o proponer una alianza.', prefix, 'contacto/') + body + footer(prefix) + scripts(prefix)

def home():
    """Portada P6 con la navegación nueva y enlaces a las subpáginas."""
    import build_final as F
    html_ = F.rootify(P6.p6())
    # cabecera y scrollcue propios
    import re
    html_ = re.sub(r'<header class="site-header".*?</header>', lambda m: header('', ''), html_, count=1, flags=re.S)
    html_ = re.sub(r'<nav class="scrollcue".*?</nav>', scrollcue([('inicio', 'Inicio'), ('quienes', 'Quiénes somos'), ('munmx', 'MUNMX 2027'), ('noticias', 'Noticias'), ('contacto', 'Contacto')]), html_, count=1, flags=re.S)
    html_ = html_.replace('<div id="globe" aria-hidden="true">', '<div id="globe" aria-hidden="true" data-three="assets/js/three.min.js">')
    html_ = html_.replace('<main>', '<main id="main">')
    html_ = html_.replace('<p class="eyebrow reveal">Quiénes somos</p>', '<h2 class="sr-only">Quiénes somos</h2><p class="eyebrow reveal">Quiénes somos</p>', 1)
    # enlaces "más" en las secciones resumen
    html_ = html_.replace('</div></div>\n</div></section>\n\n<section id="munmx"', '<p class="reveal d3"><a class="more" href="quienes/">Más sobre nosotros</a> &nbsp;·&nbsp; <a class="more" href="quienes/#coaches">Coaches y asesores</a></p></div></div>\n</div></section>\n\n<section id="munmx"')
    html_ = html_.replace('<ul class="comites">', '<p class="reveal d3" style="margin-top:30px;font-size:13px;color:#B9C6EE">Los ocho comités de 2027 · <a href="comites/" style="color:#fff">qué es y de qué trata cada uno</a></p><ul class="comites">')
    html_ = html_.replace('<a class="btn" href="#contacto">Avísame</a>', '<a class="btn" href="registro/">Pre-registro de delegaciones</a>')
    head_ = head('ESMUN · Modelo de Naciones Unidas PrepaTec Esmeralda', 'Grupo estudiantil de Modelo de Naciones Unidas de la PrepaTec Esmeralda. Formamos delegados desde 2019 y organizamos MUNMX Esmeralda.', '', '',
                 extra='<script type="application/ld+json">{"@context": "https://schema.org", "@type": "Event", "name": "MUNMX Esmeralda 2027", "description": "Modelo de Naciones Unidas de la PrepaTec Esmeralda. Comités en español e inglés para delegaciones de preparatoria.", "startDate": "2027-03-11", "endDate": "2027-03-13", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled", "location": {"@type": "Place", "name": "PrepaTec Esmeralda", "address": {"@type": "PostalAddress", "addressLocality": "Atizapán de Zaragoza", "addressRegion": "Estado de México", "addressCountry": "MX"}}, "organizer": {"@type": "Organization", "name": "ESMUN", "url": "https://esmun.github.io/"}, "url": "https://esmun.github.io/munmx/"}</script><link rel="manifest" href="site.webmanifest"><link rel="preload" href="assets/fonts/league-gothic-400.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>')
    return head_ + html_ + scripts('')

def build():
    (OUT / 'style.css').write_text(P6.CSS + PAGES_CSS, encoding='utf-8')
    (OUT / 'index.html').write_text(home(), encoding='utf-8')
    for folder, fn in [('quienes', quienes_page), ('comites', comites_page), ('munmx', munmx_page), ('contacto', contacto_page), ('registro', registro_page), ('privacidad', privacidad_page), ('delegados', delegados_page), ('patrocinios', patrocinios_page)]:
        d = OUT / folder; d.mkdir(exist_ok=True); (d / 'index.html').write_text(fn('../'), encoding='utf-8')
    # pie y cabecera del blog con la navegación nueva
    for f in (OUT / 'noticias').glob('*.html'):
        t = f.read_text(encoding='utf-8')
        import re
        t = re.sub(r'<a class="skip"[^>]*>.*?</a><header class="site-header".*?</header>|<header class="site-header".*?</header>', lambda m: header('../', 'noticias/'), t, count=1, flags=re.S)
        t = t.replace('href="../#quienes"', 'href="../quienes/"').replace('href="../#munmx"', 'href="../munmx/"')
        f.write_text(t, encoding='utf-8')
    # sitemap con las subpáginas
    pages = ['/', '/quienes/', '/comites/', '/munmx/', '/noticias/'] + ['/noticias/' + n[5] + '.html' for n in C['noticias']] + ['/contacto/', '/registro/', '/delegados/', '/patrocinios/']
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}{p}</loc><changefreq>{"weekly" if p in ("/", "/noticias/") else "monthly"}</changefreq></url>\n' for p in pages) + '</urlset>\n'
    (OUT / 'sitemap.xml').write_text(sm, encoding='utf-8')
    host = re.sub(r'^https?://', '', DOMAIN).strip('/')
    if not host.endswith('github.io'): (OUT / 'CNAME').write_text(host + '\n', encoding='utf-8')
    print('pages ok')

if __name__ == '__main__':
    build()
