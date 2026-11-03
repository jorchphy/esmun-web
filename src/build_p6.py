# -*- coding: utf-8 -*-
"""P6 · Globo: propuesta arriesgada con globo terráqueo 3D en los colores de la identidad."""
import sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import build_sites as B
from build_sites import C, head, header, footer, contact_form, news_cards, scripts, comite_list, LOGO_P, LOGO_I, A, ROOT, esmun_logo_svg

CSS="""
html{background:var(--tinta)} body{overflow-x:clip} .wrap{min-width:0}
/* Capas: fondos de sección (opacos, por tema) → lienzo del globo (fijo, z2) → contenido (.wrap, z3) → cabecera (z50) */
#globe{position:fixed;inset:0;z-index:2;pointer-events:none} #globe canvas{width:100%!important;height:100%!important;display:block}
#globe.fallback{position:absolute;top:0;left:0;right:0;height:100svh;display:grid;align-items:center;justify-items:end;padding-right:4vw;overflow:hidden} #globe.fallback img{width:min(78vmin,760px);height:auto;opacity:.9} @media (max-width:900px){#globe.fallback{align-items:start;justify-items:center;padding:12vh 0 0}} #globe.webgl img{display:none} #globe.fallback~main .only-pointer{display:none}
#globe-tip{position:fixed;left:0;top:0;z-index:5;pointer-events:none;background:var(--tinta);color:#fff;font:600 11px/1 var(--body);letter-spacing:.14em;text-transform:uppercase;padding:8px 10px;border:1px solid rgba(255,255,255,.3)} #globe-tip[hidden]{display:none}
main section,.site-footer{position:relative} section>.wrap,.site-footer>.wrap{position:relative;z-index:3;width:100%}
.site-header{border-color:transparent;background:color-mix(in srgb,var(--bg) 97%,transparent)}
/* botón de la cabecera: contraste explícito sobre claro, oscuro y fondos teñidos */
.site-nav a{white-space:nowrap} .site-nav .cta{background:var(--azul);color:#fff;border-color:var(--azul)} .site-header[data-theme="dark"] .site-nav .cta{background:#fff;color:var(--azul);border-color:#fff}
/* titulares con interlineado apretado: aire para acentos y para el eyebrow de arriba */
.eyebrow+h1,.eyebrow+h2,.eyebrow+.display{margin-top:.18em} .display{padding-top:.04em}
.site-header[data-theme="dark"]{--bg:var(--tinta)} .site-header:not([data-theme="dark"]){--bg:var(--papel)}
section{min-height:100svh;display:grid;align-items:center;padding-block:clamp(72px,10vh,120px)} section:not(.hero,.panel,.page-hero,#munmx,#intro){min-height:min(100svh,880px)}
[id]{scroll-margin-top:84px} @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media (max-width:900px){.btn{min-height:44px} .faq summary{min-height:44px;align-items:center} .more{display:inline-block;padding:10px 0}} .sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
/* Composición: el globo ocupa siempre el lado opuesto al texto. Hero: texto izq. Quiénes: texto der. MUNMX: centrado con velo. Noticias: lista izq. Contacto: der. */
.hero .wrap{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr);gap:40px;align-items:center}
.hero h1{font-size:clamp(76px,13vw,220px);line-height:.8;color:#fff} .hero h1 em{font-style:normal;color:var(--oro,#FFD98A)}
.hero .lead{color:#DCE3F7;max-width:50ch} .hero .btn{background:#fff;color:var(--azul);border-color:#fff} .hero .btn.ghost{background:transparent;color:#fff}
.hero .legend{margin-top:34px;display:flex;gap:22px;flex-wrap:wrap;font-size:12px;color:#B9C6EE;letter-spacing:.08em} .hero .legend i{display:inline-block;width:10px;height:10px;border-radius:50%;background:#FFD98A;vertical-align:middle;margin-right:8px;box-shadow:0 0 10px #FFD98A} .hero .legend i.w{background:#B8B8BA;box-shadow:none}
@media (max-width:900px){.hero .wrap{grid-template-columns:1fr;align-content:end;min-height:100svh;padding-bottom:40px} .hero h1{font-size:clamp(64px,19vw,140px)}}
/* velo: halo del color del fondo detrás de un bloque de texto, por si el globo pasa por debajo */
.shield{position:relative;isolation:isolate} .shield::before{content:'';position:absolute;inset:-28px -40px;z-index:-1;background:radial-gradient(ellipse at center,var(--bgc,var(--papel)) 46%,transparent 100%);opacity:.92;pointer-events:none}
.q .wrap{display:grid;justify-items:end} .q .content{max-width:760px;width:100%} .q .lead{font-size:clamp(19px,1.8vw,26px);line-height:1.4;color:var(--fg)}
.que{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:40px} .que div{background:color-mix(in srgb,var(--papel) 70%,#fff 30%);border:1px solid var(--line);padding:22px;border-radius:3px} .que h3{font-family:var(--display);text-transform:uppercase;font-size:38px;color:var(--azul)} .que p{margin:8px 0 0;font-size:14.5px;color:var(--muted)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:40px} .stats .n{font-family:var(--display);font-size:clamp(56px,5.6vw,88px);line-height:.85;color:var(--azul)} .stats b{display:block;font-size:11px;letter-spacing:.18em;text-transform:uppercase;margin:6px 0 4px} .stats p{margin:0;font-size:13.5px;color:var(--muted)}
@media (max-width:900px){.q .wrap{justify-items:stretch} .stats{grid-template-columns:1fr 1fr} .que{grid-template-columns:1fr}}
#munmx .wrap{display:grid;grid-template-columns:minmax(0,1fr);justify-items:center;text-align:center;isolation:isolate} #munmx h2{font-size:clamp(90px,16vw,300px);line-height:.78;color:#fff}
#munmx .wrap::before{content:'';position:absolute;inset:-8% -14%;z-index:-1;pointer-events:none;background:radial-gradient(ellipse at 50% 55%,rgba(28,32,48,.86) 0%,rgba(28,32,48,.7) 32%,rgba(28,32,48,.3) 56%,rgba(28,32,48,0) 72%)}
#munmx .lockup{width:min(440px,86vw);height:auto;margin:28px auto 22px}
#munmx .lead{color:#C9D2F0;max-width:52ch} #munmx .btn{background:#fff;color:var(--azul);border-color:#fff} #munmx .btn.ghost{background:transparent;color:#fff}
.comites{list-style:none;margin:36px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:10px;justify-content:center} .com{display:inline-grid;grid-auto-flow:column;align-items:center;gap:12px;padding:10px 16px 10px 12px;border:1px solid rgba(255,255,255,.3);border-radius:999px;color:#fff;backdrop-filter:blur(6px);background:rgba(28,32,48,.55);max-width:100%} .com .sig{font-size:28px;line-height:1;color:var(--acc);filter:brightness(1.7)} .com .nm{font-size:13px;white-space:normal;text-align:left} .com .lv{display:none}
.news{display:grid;grid-template-columns:1fr;gap:18px;max-width:720px} .news-card a{text-decoration:none;display:grid;grid-template-columns:200px 1fr;gap:12px 22px;align-items:center;background:color-mix(in srgb,var(--papel) 70%,#fff 30%);border:1px solid var(--line);padding:14px;border-radius:3px} .news-card .thumb{aspect-ratio:4/3;grid-row:span 3} .news-card .meta,.news-card h3,.news-card p{grid-column:2} .news-card .meta{display:flex;gap:12px;font-size:12px;color:var(--muted)} .news-card h3{font-size:21px;font-weight:600;line-height:1.2} .news-card p{margin:0;font-size:14px;color:var(--muted)}
@media (max-width:640px){.news-card a{grid-template-columns:1fr} .news-card .thumb{grid-row:auto} .news-card .meta,.news-card h3,.news-card p{grid-column:1}}
#contacto .wrap{display:grid;justify-items:end} #contacto .content{max-width:820px;width:100%;display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:40px;align-items:start} #contacto h2.display{font-size:clamp(52px,6.5vw,110px);line-height:.9;overflow-wrap:anywhere} #contacto .form{background:color-mix(in srgb,var(--papel) 70%,#fff 30%);padding:24px;border:1px solid var(--line);border-radius:3px}
@media (max-width:900px){#contacto .content{grid-template-columns:1fr}}
h2.display{font-size:clamp(56px,8vw,130px)}
.site-footer .wrap::after{content:'';position:absolute;left:-50vw;right:-50vw;bottom:-28px;height:140px;z-index:-1;pointer-events:none;background:linear-gradient(to top,rgba(28,32,48,.92) 35%,rgba(28,32,48,0))}
.scrollcue{position:fixed;right:18px;top:50%;transform:translateY(-50%);z-index:3;display:grid;gap:10px} .scrollcue a{width:8px;height:8px;border-radius:50%;background:currentColor;opacity:.35;display:block} .scrollcue a.on{opacity:1;transform:scale(1.4)} @media (max-width:900px){.scrollcue{display:none}}
"""

def p6():
    body=header()+f"""
<div id="globe" aria-hidden="true"><img src="{A}/img/globo_fallback.svg" alt=""></div>
<div id="globe-tip" hidden></div>
<nav class="scrollcue" aria-label="Secciones">{''.join(f'<a href="{h}" aria-label="{t}"></a>' for h,t in B.NAV)}</nav>
<main>
<section class="hero" id="inicio" data-section data-theme="dark" data-globe="hero"><div class="wrap">
 <div><p class="eyebrow reveal" style="color:#B9C6EE">Modelo de Naciones Unidas · PrepaTec Esmeralda</p>
  <h1 class="display reveal d1">Toma la<br>palabra<em>.</em></h1>
  <p class="lead reveal d2" style="margin-top:24px">{C['intro']}</p>
  <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:28px" class="reveal d3"><a class="btn" href="#contacto">Únete al equipo</a><a class="btn ghost" href="#munmx">MUNMX 2027</a></div>
</div>
 <div aria-hidden="true"></div>
</div></section>

<section class="q" id="quienes" data-section data-theme="paper" data-globe="quienes"><div class="wrap">
 <div class="content shield"><p class="eyebrow reveal">Quiénes somos</p><p class="lead reveal d1" style="margin-top:14px">{C['intro']}</p>
  <div class="stats">{''.join(f'<div class="reveal d{i%4}"><div class="n num" {"data-count="+n if n.isdigit() and n!="2019" else ""}>{n}</div><b>{l}</b><p>{p}</p></div>' for i,(n,l,p) in enumerate(C['stats']))}</div>
  <div class="que">{''.join(f'<div class="reveal d{i%4}"><h3>{t}</h3><p>{p}</p></div>' for i,(t,p) in enumerate(C['que']))}</div></div>
</div></section>

<section id="munmx" data-section data-theme="dark" data-globe="munmx"><div class="wrap">
 <p class="eyebrow reveal" style="color:#B9C6EE">MUNMX Esmeralda 2027 · PrepaTec Esmeralda</p><h2 class="display reveal d1">11 · 12 · 13<br>de marzo</h2>
 <img class="lockup reveal d2" src="{A}/logo/MUNMX_2027_lockup_horizontal_blanco.svg" alt="MUNMX Esmeralda 2027">
 <p class="lead reveal d2">El Modelo de Naciones Unidas de la PrepaTec Esmeralda: tres días y ocho comités, en inglés y en español. El registro abre con la convocatoria; mientras, las delegaciones pueden pre-registrarse.</p>
 <div style="display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin-top:26px" class="reveal d3"><a class="btn" href="#contacto">Avísame</a><a class="btn ghost" href="{C['mymun']}" rel="noopener" target="_blank">ESMUN 2024 en mymun</a></div>
 <ul class="comites">{comite_list()}</ul>
</div></section>

<section id="noticias" data-section data-theme="paper" data-globe="noticias"><div class="wrap"><div class="content shield" style="max-width:720px"><p class="eyebrow reveal">Noticias</p><h2 class="display reveal d1" style="margin-bottom:28px">Entre sesiones</h2><div class="news">{news_cards()}</div><p style="margin-top:24px"><a class="btn ghost" href="../noticias/">Todas las noticias</a></p></div></div></section>

<section id="contacto" data-section data-theme="paper" data-globe="contacto"><div class="wrap"><div class="content shield"><div><p class="eyebrow reveal">Contacto</p><h2 class="display reveal d1">Hablemos</h2><p class="lead reveal d2" style="margin-top:20px">Escríbenos si quieres entrar al equipo, registrar a tu delegación o proponer una alianza.</p><p class="reveal d2" style="line-height:1.9;margin-top:20px"><a href="mailto:{C['mail']}">{C['mail']}</a><br><a href="{C['ig_url']}" rel="noopener" target="_blank">Instagram {C['ig']}</a><br>PrepaTec Esmeralda · {C['ciudad']}</p></div><div class="reveal d1">{contact_form()}</div></div></div></section>
</main>"""+footer('dark').replace('<footer class="site-footer" data-section data-theme="dark" id="pie">','<footer class="site-footer" data-section data-theme="dark" data-globe="pie" id="pie">')
    return body

def build():
    d=ROOT/'p6-globo'; d.mkdir(exist_ok=True); (d/'style.css').write_text(CSS,encoding='utf-8')
    html_=head('ESMUN · Modelo de Naciones Unidas PrepaTec Esmeralda — Globo','Grupo estudiantil de Modelo de Naciones Unidas de la PrepaTec Esmeralda. Debates, liderazgo e impacto. Organizador de MUNMX Esmeralda 2027.','style.css')+p6()
    html_+=f'<script src="{A}/js/three.min.js" defer></script><script src="{A}/js/land.js" defer></script><script src="{A}/js/esmun.js" defer></script><script src="{A}/js/globe.js" defer></script></body></html>'
    (d/'index.html').write_text(html_,encoding='utf-8'); print('p6 ok')

if __name__=='__main__':
    build()
