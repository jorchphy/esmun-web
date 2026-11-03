# -*- coding: utf-8 -*-
"""Portada «Próximamente»: una sola página mientras el sitio completo no se publica.
Se activa con content/site.json → "publicacion": {"modo": "proximamente"} o con la variable de entorno ESMUN_MODO.
Salida: ../_site (index.html, 404.html, robots.txt, sitemap.xml, CNAME y solo los assets necesarios)."""
import sys, pathlib, shutil, json, html, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_sites as B
from logo_svg import esmun_logo_svg

SRC = pathlib.Path(__file__).resolve().parent
OUT = SRC.parent / '_site'
DOMAIN = B.C.get('dominio', 'https://esmun.github.io').rstrip('/')
MUNMX = datetime.date(2027, 3, 11)

CSS = """
html,body{min-height:100%} body{background:var(--tinta);color:#F2F3F8;margin:0;overflow-x:hidden}
.pronto{position:relative;min-height:100svh;display:grid;grid-template-rows:auto 1fr auto} .pronto>.site-header,.pronto>main,.pronto>footer{width:100%;box-sizing:border-box}
.pronto .site-header{position:relative;background:transparent;border-bottom:0}
.pronto .site-header .wrap{display:flex;align-items:center;justify-content:space-between;gap:18px;padding-block:22px}
.pronto .site-header .brand .esmun-logo{height:44px;width:auto}
.pronto .site-header .aux{display:flex;gap:22px;font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase}
.pronto .site-header .aux a{color:#F2F3F8;text-decoration:none;opacity:.85} .pronto .site-header .aux a:hover{opacity:1}
.globo{position:absolute;right:-18vw;top:50%;width:min(78vh,70vw);aspect-ratio:1;transform:translateY(-50%);pointer-events:none;opacity:.55;z-index:0}
.globo img{width:100%;height:100%;display:block;animation:giro 240s linear infinite}
@keyframes giro{to{transform:rotate(360deg)}}
.pronto main{position:relative;z-index:1;display:grid;align-content:center;gap:34px;padding-block:clamp(40px,8vh,96px)}
.pronto .eyebrow{color:#FFD98A}
.pronto .display{font-size:clamp(72px,13vw,196px);line-height:.84;margin:0;color:#fff}
.pronto .lead{color:#C9CDDC;max-width:52ch;font-size:clamp(17px,1.5vw,21px)}
.estado{display:inline-flex;align-items:center;gap:10px;font-size:12px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#C9CDDC}
.estado i{width:8px;height:8px;border-radius:50%;background:#FFD98A;box-shadow:0 0 0 0 rgba(255,217,138,.6);animation:late 2.4s ease-out infinite}
@keyframes late{to{box-shadow:0 0 0 12px rgba(255,217,138,0)}}
.fechas{display:grid;grid-template-columns:auto 1fr;gap:22px 32px;align-items:center;padding:26px 0;border-top:1px solid rgba(255,255,255,.14);border-bottom:1px solid rgba(255,255,255,.14);max-width:760px}
.fechas .lock{width:min(300px,52vw)} .fechas .lock img{width:100%;height:auto;display:block}
.fechas .dias{font-family:var(--display);text-transform:uppercase;font-size:clamp(40px,6vw,76px);line-height:.9;color:#fff}
.fechas .dias small{display:block;font:600 12px/1.4 var(--body);letter-spacing:.18em;color:#C9CDDC;margin-top:10px;text-transform:uppercase}
.fechas .dias b{color:#FFD98A;font-weight:400}
.aviso{max-width:560px} .aviso h2{font:700 12px/1 var(--body);letter-spacing:.18em;text-transform:uppercase;color:#FFD98A;margin:0 0 14px}
.aviso .form{--line:rgba(255,255,255,.28);--fg:#fff;--muted:#C9CDDC} .aviso .form input,.aviso .form select{background:rgba(255,255,255,.04)} .aviso .form select option{color:#1C2030}
.aviso .btn{--accent:#FFD98A;--bg:#1C2030;border-color:#FFD98A;background:#FFD98A;color:#1C2030}
.aviso details{margin-top:12px;color:#C9CDDC;font-size:12.5px;line-height:1.5} .aviso summary{cursor:pointer;text-decoration:underline;text-underline-offset:3px} .aviso details p{margin:8px 0 0;max-width:62ch}
.pronto footer{position:relative;z-index:1;display:flex;flex-wrap:wrap;gap:10px 28px;justify-content:space-between;padding-block:22px 28px;border-top:1px solid rgba(255,255,255,.14);font-size:13px;color:#C9CDDC}
.pronto footer a{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.3)} .pronto footer a:hover{border-color:#fff}
@media (max-width:760px){.globo{right:-45vw;top:auto;bottom:-10vh;transform:none;width:120vw;opacity:.35}.fechas{grid-template-columns:1fr}.pronto .site-header .aux{display:none}}
@media (prefers-reduced-motion:reduce){.globo img,.estado i{animation:none}}
"""

def page():
    C = B.C
    faltan = (MUNMX - datetime.date.today()).days
    attrs, hidden = B.form_attrs('aviso')
    head = B.head('ESMUN · Modelo de Naciones Unidas PrepaTec Esmeralda',
                  'Muy pronto, el nuevo sitio de ESMUN, el grupo de Modelo de Naciones Unidas de la PrepaTec Esmeralda, y la convocatoria de MUNMX Esmeralda 2027 (11, 12 y 13 de marzo).',
                  'style.css', path_prefix='.',
                  extra=f'<link rel="canonical" href="{DOMAIN}/"><meta property="og:url" content="{DOMAIN}/"><meta name="twitter:card" content="summary_large_image">'
                        '<link rel="preload" href="assets/fonts/league-gothic-400.woff2" as="font" type="font/woff2" crossorigin>')
    head = head.replace('href="./assets/', 'href="assets/').replace('content="./assets/img/photo_ceremony.jpg"', f'content="{DOMAIN}/assets/img/og.jpg"')
    body = f"""<div class="pronto" data-theme="dark">
<header class="site-header" data-theme="dark"><div class="wrap"><a class="brand" href="./" aria-label="ESMUN">{esmun_logo_svg(kind='horizontal', mode='header')}</a>
<nav class="aux" aria-label="Contacto"><a href="{C['ig_url']}" rel="noopener" target="_blank">Instagram {C['ig']}</a><a href="mailto:{C['mail']}">{C['mail']}</a></nav></div></header>
<div class="globo" aria-hidden="true"><img src="assets/img/globo_fallback.svg" alt="" width="1000" height="1000"></div>
<main class="wrap" id="main">
<div><p class="eyebrow">ESMUN · PrepaTec Esmeralda · Modelo de Naciones Unidas</p>
<h1 class="display">Toma la<br>palabra.</h1></div>
<p class="estado"><i></i> Nuevo sitio en construcción</p>
<p class="lead">Estamos terminando el sitio de ESMUN y la convocatoria de MUNMX Esmeralda 2027. Mientras tanto, lo importante ya está aquí: las fechas del modelo y una forma de avisarte cuando abra el registro.</p>
<div class="fechas"><div class="lock"><img src="assets/logo/MUNMX_proximamente_lockup_horizontal_blanco.svg" alt="MUNMX Esmeralda 2027, próximamente" width="826" height="240"></div>
<p class="dias" data-munmx="2027-03-11">11 · 12 · 13 <b>de marzo</b><small>Faltan <span class="faltan">{faltan}</span> días · {C['ciudad']}</small></p></div>
<section class="aviso" aria-labelledby="aviso-t"><h2 id="aviso-t">Avísame cuando abra el registro</h2>
<form class="form" {attrs} method="post">{hidden}
<div class="row"><label>Correo<input name="correo" type="email" autocomplete="email" required placeholder="nombre@correo.com"></label>
<label>Soy<select name="perfil"><option>Alumno de la PrepaTec Esmeralda</option><option>Alumno de otra escuela</option><option>Docente o advisor</option><option>Patrocinador o aliado</option></select></label></div>
<div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap"><button class="btn" type="submit">Avisarme</button><span class="form-msg" role="status" aria-live="polite" style="font-size:13px;color:#C9CDDC"></span></div>
<details><summary>Aviso de privacidad</summary><p>ESMUN, grupo estudiantil de la PrepaTec Esmeralda, usa tu correo solo para avisarte de la convocatoria y el registro de MUNMX Esmeralda 2027. No lo compartimos con terceros ni lo usamos para publicidad. Puedes pedir que lo borremos en cualquier momento escribiendo a <a href="mailto:{C['mail']}" style="color:#fff">{C['mail']}</a>.</p></details>
</form></section>
</main>
<footer class="wrap"><span>© 2026 ESMUN · PrepaTec Esmeralda. Sitio del grupo estudiantil.</span><span><a href="{C['ig_url']}" rel="noopener" target="_blank">Instagram</a> · <a href="mailto:{C['mail']}">Correo</a> · <a href="{C['mymun']}" rel="noopener" target="_blank">mymun</a></span></footer>
</div>
<script>(function(){{var el=document.querySelector('.dias');if(!el)return;var d=new Date(el.getAttribute('data-munmx')+'T00:00:00');var n=Math.max(0,Math.ceil((d-new Date())/864e5));var s=el.querySelector('.faltan');if(s)s.textContent=n;}})();</script>
<script src="assets/js/esmun.js" defer></script><script src="assets/js/season.js" defer></script></body></html>"""
    return head + body

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / 'assets').mkdir(parents=True)
    for sub in ('fonts', 'css', 'logo'):
        shutil.copytree(SRC / 'assets' / sub, OUT / 'assets' / sub, ignore=shutil.ignore_patterns('.DS_Store'))
    (OUT / 'assets' / 'js').mkdir(); (OUT / 'assets' / 'img').mkdir()
    for f in ('esmun.js', 'season.js'): shutil.copy(SRC / 'assets' / 'js' / f, OUT / 'assets' / 'js' / f)
    for f in ('globo_fallback.svg', 'og.jpg'): shutil.copy(SRC / 'assets' / 'img' / f, OUT / 'assets' / 'img' / f)
    (OUT / 'style.css').write_text(CSS, encoding='utf-8')
    (OUT / 'index.html').write_text(page(), encoding='utf-8')
    h404 = page().replace('<h1 class="display">Toma la<br>palabra.</h1>', '<h1 class="display">Sin<br>quórum.</h1>').replace('<p class="estado"><i></i> Nuevo sitio en construcción</p>', '<p class="estado"><i></i> Error 404 · esta página no existe</p>')
    h404 = h404.replace('<title>ESMUN · Modelo de Naciones Unidas PrepaTec Esmeralda</title>', '<title>Página no encontrada · ESMUN</title>').replace('<head>', '<head><meta name="robots" content="noindex">', 1)
    (OUT / '404.html').write_text(h404, encoding='utf-8')
    # panel de administración (Sveltia CMS)
    shutil.copytree(SRC / 'admin', OUT / 'admin')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {DOMAIN}/sitemap.xml\n', encoding='utf-8')
    (OUT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{DOMAIN}/</loc><changefreq>weekly</changefreq></url>\n</urlset>\n', encoding='utf-8')
    (OUT / 'site.webmanifest').write_text(json.dumps({"name": "ESMUN · PrepaTec Esmeralda", "short_name": "ESMUN", "start_url": "/", "display": "standalone", "background_color": "#1C2030", "theme_color": "#253C82",
        "icons": [{"src": "assets/logo/ESMUN_favicon_180.png", "sizes": "180x180", "type": "image/png"}]}, ensure_ascii=False, indent=1), encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')
    host = DOMAIN.replace('https://', '').replace('http://', '')
    if host and 'github.io' not in host: (OUT / 'CNAME').write_text(host + '\n', encoding='utf-8')
    print('próximamente ok', sum(1 for _ in OUT.rglob('*') if _.is_file()), 'archivos')

if __name__ == '__main__':
    build()
