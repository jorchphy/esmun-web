# -*- coding: utf-8 -*-
"""Sitio final de ESMUN: la propuesta P6 (globo) pasa a la raíz. Salida: /home/claude/web/final/
Estático, listo para GitHub Pages: index.html, noticias/, assets/, 404.html, robots.txt, sitemap.xml, site.webmanifest."""
import sys, pathlib, shutil, json, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_sites as B
import build_p6 as P6

SRC = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(__file__).resolve().parent.parent / '_site'
DOMAIN = B.C.get('dominio', 'https://esmun.github.io').rstrip('/')   # se cambia en content/site.json

SKIP = '<a class="skip" href="#inicio">Saltar al contenido</a>'
EXTRA_CSS = """
.skip{position:absolute;left:12px;top:-60px;z-index:60;background:var(--azul);color:#fff;padding:10px 14px;border-radius:3px;font-weight:600} .skip:focus{top:12px}
@media (hover:none){.only-pointer{display:none}}
.news-card .thumb img{width:100%;height:100%;object-fit:cover}
"""

def rootify(html_):
    """Rutas de carpeta de propuesta (../assets) a raíz (assets)."""
    html_ = html_.replace('"../assets/', '"assets/').replace("'../assets/", "'assets/").replace('(../assets/', '(assets/')
    html_ = html_.replace('href="../noticias/"', 'href="noticias/"').replace('href="../noticias/', 'href="noticias/').replace('href="../privacidad/"', 'href="privacidad/"')
    html_ = html_.replace('content="../assets/', 'content="assets/')
    return html_

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    # assets completos (fuentes, logos, fotos, css, js)
    shutil.copytree(SRC / 'assets', OUT / 'assets', ignore=shutil.ignore_patterns('photo_*.jpg', 'merch_*.jpg', 'situ_*.jpg', '.DS_Store'))
    # CSS de la portada
    (OUT / 'style.css').write_text(P6.CSS + EXTRA_CSS, encoding='utf-8')
    # portada = P6
    head = B.head('ESMUN · Modelo de Naciones Unidas PrepaTec Esmeralda',
                  'Grupo estudiantil de Modelo de Naciones Unidas de la PrepaTec Esmeralda. Formamos delegados desde 2019 y organizamos MUNMX Esmeralda.',
                  'style.css', path_prefix='.',
                  extra=f'<link rel="canonical" href="{DOMAIN}/"><link rel="manifest" href="site.webmanifest">'
                        '<link rel="preload" href="assets/fonts/league-gothic-400.woff2" as="font" type="font/woff2" crossorigin>'
                        '<link rel="preload" href="assets/fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>'
                        f'<meta property="og:url" content="{DOMAIN}/"><meta name="twitter:card" content="summary_large_image">')
    head = head.replace('href="./assets/', 'href="assets/').replace('content="./assets/img/photo_ceremony.jpg"', f'content="{DOMAIN}/assets/img/og.jpg"')
    body = P6.p6()
    body = body.replace('<header class="site-header"', SKIP + '<header class="site-header"', 1)
    body = body.replace('<div id="globe" aria-hidden="true">', '<div id="globe" aria-hidden="true" data-three="assets/js/three.min.js">')
    html_ = head + body + '<script src="assets/js/land.js" defer></script><script src="assets/js/esmun.js" defer></script><script src="assets/js/season.js" defer></script><script src="assets/js/globe.js" defer></script></body></html>'
    (OUT / 'index.html').write_text(rootify(html_), encoding='utf-8')

    # blog: regenerar en site/ y copiar, apuntando la cabecera a la raíz
    B.noticias()
    (OUT / 'noticias').mkdir()
    for f in (B.ROOT / 'noticias').iterdir():
        t = f.read_text(encoding='utf-8')
        if f.suffix == '.html':
            t = t.replace('href="../p1-editorial/"', 'href="../"').replace('href="../p1-editorial/#', 'href="../#')
            t = t.replace('<header class="site-header">', SKIP.replace('#inicio', '#main') + '<header class="site-header">', 1).replace('<main class="wrap">', '<main class="wrap" id="main">', 1)
            t = t.replace('<link rel="stylesheet" href="style.css">', '<link rel="stylesheet" href="style.css"><style>.skip{position:absolute;left:12px;top:-60px;z-index:60;background:var(--azul);color:#fff;padding:10px 14px;border-radius:3px;font-weight:600} .skip:focus{top:12px}</style>')
        (OUT / 'noticias' / f.name).write_text(t, encoding='utf-8')

    # redirección de la URL antigua de ejemplo
    (OUT / 'noticias' / 'convocatoria-delegados-2026-27.html').write_text('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=./"><title>Noticias · ESMUN</title></head><body><a href="./">Noticias</a></body></html>', encoding='utf-8')
    # 404
    h404 = B.head('Página no encontrada · ESMUN', 'Esta página no existe.', 'style.css', path_prefix='.').replace('href="./assets/', 'href="assets/')
    h404 += f'''<main class="wrap" style="min-height:70vh;display:grid;align-content:center;gap:18px;padding-block:80px"><p class="eyebrow">Error 404</p><h1 class="display" style="font-size:clamp(64px,12vw,180px);line-height:.85">Sin quórum.</h1><p class="lead" style="max-width:48ch">Esta página no existe o cambió de lugar. Vuelve al inicio o escríbenos a <a href="mailto:{B.C['mail']}">{B.C['mail']}</a>.</p><p><a class="btn" href="./">Ir al inicio</a></p></main>''' + B.footer('dark').replace('href="../noticias/"', 'href="noticias/"') + '<script src="assets/js/esmun.js" defer></script><script src="assets/js/season.js" defer></script></body></html>'
    (OUT / '404.html').write_text(h404, encoding='utf-8')

    # robots, sitemap, manifest
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n', encoding='utf-8')
    pages = ['/', '/noticias/'] + ['/noticias/' + n[5] + '.html' for n in B.C['noticias']]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}{p}</loc><changefreq>{"weekly" if p=="/" else "monthly"}</changefreq></url>\n' for p in pages) + '</urlset>\n'
    (OUT / 'sitemap.xml').write_text(sm, encoding='utf-8')
    (OUT / 'site.webmanifest').write_text(json.dumps({"name": "ESMUN · PrepaTec Esmeralda", "short_name": "ESMUN", "start_url": "/", "display": "standalone", "background_color": "#1C2030", "theme_color": "#253C82",
        "icons": [{"src": "assets/logo/ESMUN_favicon_180.png", "sizes": "180x180", "type": "image/png"}]}, ensure_ascii=False, indent=1), encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')
    (OUT / 'README.md').write_text(README, encoding='utf-8')
    print('final ok', sum(1 for _ in OUT.rglob('*') if _.is_file()), 'archivos')

README = """# Sitio web de ESMUN

Estático: HTML + CSS + JS. Sin build, sin dependencias de servidor. Listo para GitHub Pages.

## Qué hay
- `index.html` + `style.css`: portada (propuesta "Globo"). Secciones: Inicio, Quiénes somos, MUNMX 2027, Noticias, Contacto.
- `quienes/`, `comites/`, `munmx/`, `contacto/`: subpáginas. Cada sección declara `data-globe` o `data-kf` (JSON) para colocar y colorear el globo; los paneles de comités usan `data-kf` con `bg`, `dots` y `focus` (la sede que se destaca) y `data-bg` para teñir la cabecera.
- `noticias/`: blog. `index.html` lista las entradas; cada artículo es un HTML con datos estructurados `NewsArticle`.
- `assets/css/base.css`: tokens de la identidad (colores, tipografías, temas claro/oscuro/azul) y componentes.
- `assets/js/esmun.js`: logotipo reactivo (ventanas que se encienden sobre fondo oscuro), revelados, menú, contadores, formulario.
- `assets/js/globe.js` + `land.js` + `three.min.js`: globo 3D. Se descarga solo si el navegador tiene WebGL y el usuario no pidió "reducir movimiento"; si no, se ve `assets/img/globo_fallback.svg`.
- `404.html`, `robots.txt`, `sitemap.xml`, `site.webmanifest`, `.nojekyll`.

## Publicar en GitHub Pages
1. Crea el repositorio (`esmun.github.io` en una cuenta u organización `esmun`, o `esmun-web` en cualquier cuenta).
2. Sube todo el contenido de esta carpeta a la raíz del repo, rama `main`.
3. Settings → Pages → Deploy from a branch → `main` / `/ (root)`. En unos minutos queda en `https://<usuario>.github.io/<repo>/`.
4. Si el repo no se llama `<usuario>.github.io`, las rutas absolutas del `sitemap.xml`, el `canonical` y `og:url` deben llevar el nombre del repo. Edita `DOMAIN` en `build_final.py` o a mano.
5. Dominio propio (opcional): archivo `CNAME` con el dominio y un registro CNAME en el DNS apuntando a `<usuario>.github.io`.

## Antes de publicar (pendientes)
- Formulario: crea un formulario en Formspree (gratis hasta 50 envíos al mes) y sustituye `https://formspree.io/f/TU_ID` en `index.html`. Alternativas: Getform, Web3Forms.
- Fotografías: las del sitio son reales (`assets/img/real/`): el edificio (fotos propias) y dos notas de Conecta (Tec de Monterrey), cuyos derechos son del Tec; confirmar con Comunicación del campus y con las personas retratadas antes de publicar. Faltan fotos propias de sesiones y conferencias.
- Imagen para redes: `assets/img/og.jpg` (1200×630). Se genera con `make_og.py`.
- MUNMX 2027: cuando haya fechas, cambiar el texto "Próximamente" de la sección y el logotipo `MUNMX_proximamente_lockup_horizontal_blanco.svg` por `MUNMX_2027_lockup_horizontal_color.svg` (versión blanca en el manual).
- Noticias: las tres entradas son reales (identidad 2026, Nueva York 2023, 75 YAMUN 2020). Para añadir una, copiar `noticias/plantilla-articulo.html` y añadirla a la lista `C['noticias']` de `build_sites.py` (o a mano en `noticias/index.html`, la portada y `sitemap.xml`).
- Analítica (opcional): Plausible o Google Analytics, una etiqueta en `<head>`.

## Editar el globo
Al inicio de `assets/js/globe.js`: `CITIES` (sedes marcadas) y `KF` (keyframes con nombre). Cada sección declara `data-globe="nombre"` y, si hace falta, `data-kf='{...}'` con cualquiera de: `x`, `y` (posición), `s` (escala), `lon` (longitud que mira a cámara), `dark` (true/false), `glow` (0..1, ventanas doradas), `bg` y `dots` (colores), `focus` (nombre exacto de una sede en `CITIES`). Para un comité nuevo: copiar un panel de `comites/index.html`, cambiar color, textos y `focus`; si la sede no existe, añadirla a `CITIES`.

## Generar
`python3 build_final.py && python3 build_pages.py` (requiere `build_sites.py`, `build_p6.py`, `logo_svg.py` en la carpeta superior). Los textos viven en `C` dentro de `build_sites.py`; los de comités en `COM` dentro de `build_pages.py`.

## Rendimiento
Portada: ~120 KB sin el globo (HTML + CSS + fuentes + logotipos). El globo añade ~640 KB (three.js + puntos), descargados en segundo plano tras la primera pintura y solo cuando se van a usar. En móvil dibuja la mitad de los puntos y baja la resolución del lienzo. Se pausa al cambiar de pestaña.
"""

if __name__ == '__main__':
    build()
