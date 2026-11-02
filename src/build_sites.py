# -*- coding: utf-8 -*-
"""Cinco propuestas de portada para esmun (sitio del grupo con sección MUNMX 2027).
Salida: /home/claude/web/site/{index.html, p1-editorial/, …, noticias/, assets/}. Estático, listo para GitHub Pages."""
import sys, pathlib, json, html
SRC=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(SRC))
from logo_svg import esmun_logo_svg
from content import load_content

ROOT=SRC/'.build'   # intermedio (noticias); el sitio final lo arma build_final.py
ROOT.mkdir(exist_ok=True)
A='../assets'   # desde cada carpeta de propuesta

# ---------------------------------------------------------------- contenido real
C=dict(
 nombre='ESMUN', descriptor='PrepaTec Esmeralda', ciudad='Atizapán de Zaragoza, Estado de México',
 claim='Toma la palabra.', tagline='Debates. Liderazgo. Impacto.',
 intro='Somos el grupo de Modelo de Naciones Unidas de la PrepaTec Esmeralda. Desde 2019 preparamos delegados para representar a un país, defender su postura en comité y negociar resoluciones. También organizamos MUNMX Esmeralda, la conferencia de nuestra prepa dentro de la red PrepaTec.',
 ig='@esmunmx', ig_url='https://www.instagram.com/esmunmx/', mail='esmunze@outlook.com', mymun='https://mymun.com/conferences/esmun-2024',
 stats=[('2019','Fundación','Primer modelo propio, ESMUN jr, en noviembre de 2019.'),('120','Delegados','Convocados en ESMUN 2024, con seis comités en español e inglés.'),('11','Comités','En MUNMX Esmeralda 2026, del Consejo de Seguridad a Star Wars Rebellion.'),('2','Idiomas','Hay comités en español y en inglés. La conferencia también es bilingüe.')],
 que=[('Debate','Cada delegado representa a un país: investiga su postura sobre un tema y la defiende con datos frente a las demás delegaciones.'),('Negociación','Lo que cuenta es aprobar una resolución. Por eso aprendemos a ceder, a sumar aliados y a redactar textos que otros puedan firmar.'),('Liderazgo','Los alumnos llevan todo: las delegaciones, las mesas directivas y el secretariado que organiza la conferencia cada año.'),('Impacto','Hablar en público y argumentar con datos sirve en cualquier carrera. Aquí se practica cada semana, con gente que piensa distinto.')],
 timeline=[('2019','ESMUN jr, primer modelo propio, 22 y 23 de noviembre.'),('2020','ESMUN se registra como grupo estudiantil; ESMUN jr 2020 en formato remoto.'),('2023','ESMUN SR 2023 y participación en Change the World MUN, Nueva York: mención honorífica y mejor papel de posición.'),('2024','ESMUN 2024: 120 delegados, seis comités bilingües en Atizapán de Zaragoza.'),('2026','MUNMX Esmeralda 2026: once comités. Nueva identidad visual.'),('2027','MUNMX Esmeralda 2027: 11, 12 y 13 de marzo.')],
 comites=[('CS','Consejo de Seguridad','Experto · Inglés','#8A1C2B'),('AGNU','Asamblea General','Principiante · Español','#2E7D5B'),('IAEA','Organismo Internacional de Energía Atómica','Intermedio · Inglés','#C8962E'),('UNICEF','Fondo de las Naciones Unidas para la Infancia','Principiante · Inglés','#5B6EA6'),('OEA','Organización de los Estados Americanos','Intermedio · Español','#B4452E'),('OTAN','Organización del Tratado del Atlántico Norte','Experto · Inglés','#3E3E46')],
 noticias=[('2026-11-02','MUNMX 2027','MUNMX Esmeralda 2027 ya tiene fechas: 11, 12 y 13 de marzo','Tres días de comités en la PrepaTec Esmeralda. La lista de comités y la apertura del registro se anuncian con la convocatoria.','real/edificio_banner.jpg','munmx-2027-fechas'),
           ('2026-10-29','Identidad','ESMUN estrena identidad visual: el edificio de la prepa, hecho logotipo','El nuevo logotipo sale del edificio de la prepa. Con él llegan el emblema de MUNMX y un manual para que cualquiera del equipo haga piezas que se vean iguales.','real/edificio_4x3.jpg','identidad-visual-2026'),
           ('2023-05-30','Reconocimiento','Mención honorífica y mejor papel de posición en Nueva York','Luis Enrique Flores, de ESMUN, ganó dos reconocimientos en el Change the World MUN de la Associazione Diplomatici, entre unos cinco mil participantes de todo el mundo.','real/2023_luis_enrique_flores_asamblea.jpg','mencion-honorifica-nueva-york-2023'),
           ('2020-10-07','Historia','Un alumno de ESMUN, vicepresidente de la Asamblea General en el 75 YAMUN','Diego Zárate, fundador de ESMUN, fue a los 16 años el organizador más joven del primer Modelo de Naciones Unidas internacional respaldado por la ONU.','real/2020_diego_zarate_podio.jpg','75-yamun-2020')],
)

C, _POSTS_MD = load_content(SRC/'content', C)

# ---------------------------------------------------------------- formularios y analítica (configurados en content/site.json)
def form_attrs(nombre):
    """Atributos y campos ocultos del formulario según el proveedor."""
    f=C.get('formularios',{}) or {}
    if f.get('proveedor')=='web3forms':
        return 'data-endpoint="https://api.web3forms.com/submit"', f'<input type="hidden" name="access_key" value="{f.get("access_key","")}"><input type="hidden" name="subject" value="ESMUN web · {nombre}"><input type="hidden" name="from_name" value="Sitio ESMUN"><input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
    ep=f.get(nombre) or f.get('contacto') or 'https://formspree.io/f/TU_ID'
    return f'data-endpoint="{ep}"', '<input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'

def analytics():
    a=C.get('analitica',{}) or {}
    out=''
    if a.get('ga4'):
        out+=f'<script async src="https://www.googletagmanager.com/gtag/js?id={a["ga4"]}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{a["ga4"]}",{{anonymize_ip:true}});</script>'
    if a.get('cloudflare'):
        out+=f'<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{{"token": "{a["cloudflare"]}"}}\'></script>'
    return out

# ---------------------------------------------------------------- piezas comunes
def head(title, desc, css, path_prefix='..', extra=''):
    return f"""<!doctype html><html lang="es" class="no-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="website"><meta property="og:image" content="{path_prefix}/assets/img/photo_ceremony.jpg"><meta name="theme-color" content="#253C82">
<link rel="icon" href="{path_prefix}/assets/logo/ESMUN_favicon_32.png"><link rel="apple-touch-icon" href="{path_prefix}/assets/logo/ESMUN_favicon_180.png">
<link rel="stylesheet" href="{path_prefix}/assets/css/base.css"><link rel="stylesheet" href="{css}">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"Organization","name":"ESMUN · Modelo de Naciones Unidas PrepaTec Esmeralda","alternateName":"ESMUN","url":C.get("dominio","https://esmun.github.io")+"/","logo":C.get("dominio","https://esmun.github.io")+"/assets/logo/ESMUN_favicon_180.png","sameAs":[C['ig_url']],"email":C['mail'],"parentOrganization":{"@type":"EducationalOrganization","name":"PrepaTec Esmeralda"},"address":{"@type":"PostalAddress","addressLocality":"Atizapán de Zaragoza","addressRegion":"Estado de México","addressCountry":"MX"}},ensure_ascii=False)}</script>
{extra}{analytics()}<script>document.documentElement.classList.remove('no-js')</script></head><body>"""

NAV=[('#inicio','Inicio'),('#quienes','Quiénes somos'),('#munmx','MUNMX 2027'),('#noticias','Noticias'),('#contacto','Contacto')]
def header(logo_kind='horizontal', cta=('#munmx','Próximamente')):
    links=''.join(f'<a href="{h}">{t}</a>' for h,t in NAV)
    return f"""<header class="site-header" data-section-follow><div class="wrap"><a class="brand" href="#inicio" aria-label="ESMUN, inicio">{esmun_logo_svg(kind=logo_kind,mode='header')}</a>
<button class="menu-btn" aria-label="Menú" aria-expanded="false"><i></i><i></i><i></i></button>
<nav class="site-nav" aria-label="Principal">{links}<a class="btn cta" href="{cta[0]}">{cta[1]}</a></nav></div></header>"""

def footer(theme='dark'):
    return f"""<footer class="site-footer" data-section data-theme="{theme}" id="pie"><div class="wrap">
<div class="cols"><div style="max-width:300px">{esmun_logo_svg(kind='principal',mode='auto')}</div><p style="margin:14px 0 0;max-width:40ch">Grupo estudiantil de Modelo de Naciones Unidas de la PrepaTec Esmeralda. Organizador de MUNMX Esmeralda.</p></div>
<div class="cols"><b>Contacto</b><a href="mailto:{C['mail']}">{C['mail']}</a><br><a href="{C['ig_url']}" rel="noopener" target="_blank">Instagram {C['ig']}</a><br>{C['ciudad']}</div>
<div class="cols"><b>Enlaces</b><a href="#quienes">Quiénes somos</a><br><a href="#munmx">MUNMX Esmeralda 2027</a><br><a href="../noticias/">Noticias</a><br><a href="{C['mymun']}" rel="noopener" target="_blank">mymun</a></div>
<div class="legal"><span>© 2026 ESMUN · PrepaTec Esmeralda. Sitio del grupo estudiantil.</span><span class="ai-note">Fotografías: ESMUN y Conecta (Tecnológico de Monterrey). · <a href="../privacidad/">Aviso de privacidad</a></span></div>
</div></footer>"""

def contact_form(dark=False, PRIV='../privacidad/'):
    return f"""<form class="form" {form_attrs("contacto")[0]} method="post">{form_attrs("contacto")[1]}
<div class="row"><label>Nombre<input name="nombre" type="text" autocomplete="name" required></label><label>Correo<input name="correo" type="email" autocomplete="email" required></label></div>
<label>Soy<select name="perfil"><option>Alumno de la PrepaTec Esmeralda</option><option>Alumno de otra escuela</option><option>Docente o advisor</option><option>Patrocinador o aliado</option></select></label>
<label>Mensaje<textarea name="mensaje" rows="4" placeholder="Quiero unirme al equipo / registrar a mi delegación en MUNMX 2027 / proponer una alianza"></textarea></label>
<label style="display:flex;gap:10px;align-items:center;text-transform:none;letter-spacing:0;font-weight:500;font-size:14px"><input type="checkbox" name="avisame" checked style="width:18px;height:18px"> Avísame cuando abra el registro de MUNMX 2027</label>
<div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap"><button class="btn" type="submit">Enviar</button><span class="form-msg" role="status" aria-live="polite" style="font-size:13px;color:var(--muted)"></span></div>
<small>Usamos tus datos solo para responderte (<a href="{PRIV}">aviso de privacidad</a>). Si eres menor de edad, necesitas autorización de tu madre, padre o tutor.</small></form>"""

def news_cards(cls='news-card', img=True):
    out=''
    for date,tag,title,desc,photo,slug in C['noticias']:
        out+=f"""<article class="{cls} reveal"><a href="../noticias/{slug}.html" aria-label="{html.escape(title)}">{'<div class="thumb duo"><img src="'+A+'/img/'+photo+'" alt="" loading="lazy"></div>' if img else ''}
<div class="meta"><time datetime="{date}">{date[8:]}·{date[5:7]}·{date[:4]}</time><span class="pill">{tag}</span></div><h3>{title}</h3><p>{desc}</p></a></article>"""
    return out

def scripts(prefix='..'): return f'<script src="{prefix}/assets/js/esmun.js" defer></script></body></html>'

def comite_list(cls='com'):
    return ''.join(f'<li class="{cls} reveal" style="--acc:{c[3]}"><span class="display sig">{c[0]}</span><span class="nm">{c[1]}</span><span class="lv">{c[2]}</span></li>' for c in C['comites'])

LOGO_P=lambda: esmun_logo_svg(kind='principal',mode='auto')
LOGO_I=lambda: esmun_logo_svg(kind='isotipo',mode='auto')
AI_NOTE='<p class="ai-note" style="margin-top:10px">Fotografía provisional generada por IA.</p>'

PROPS={}

# ======================================================================= P1 · Editorial
P1_CSS="""
body{background:var(--papel)} .hero{padding:clamp(40px,8vh,96px) 0 40px;overflow:hidden}
.hero .display{font-size:clamp(84px,17vw,300px);margin-left:-.03em;color:var(--azul);line-height:.8} .hero .display em{font-style:normal;color:var(--tinta)}
.hero .meta{display:grid;grid-template-columns:repeat(3,auto);gap:36px;justify-content:start;border-top:2px solid var(--tinta);margin-top:36px;padding-top:16px;font-size:13px}
.hero .meta b{display:block;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}
.hero-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:48px;align-items:end} .hero-grid figure{margin:0;aspect-ratio:4/5} .hero-grid figcaption{font-size:12px;color:var(--muted);margin-top:8px}
@media (max-width:900px){.hero-grid{grid-template-columns:1fr} .hero .meta{grid-template-columns:1fr 1fr}}
section{padding-block:clamp(56px,9vw,120px)} .sec-head{display:grid;grid-template-columns:1fr 2fr;gap:32px;align-items:start;border-top:1px solid var(--tinta);padding-top:20px;margin-bottom:40px}
.sec-head h2{font-size:clamp(44px,6vw,92px)} .sec-head .lead{margin:0}
@media (max-width:900px){.sec-head{grid-template-columns:1fr}}
.que{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-top:1px solid var(--tinta);border-bottom:1px solid var(--tinta)} .que div{padding:28px 24px 28px 0;border-right:1px solid var(--line)} .que div:last-child{border-right:0}
.que h3{font-size:clamp(28px,3vw,44px);margin-bottom:12px} .que p{margin:0;font-size:15px;color:var(--muted)}
@media (max-width:900px){.que{grid-template-columns:1fr 1fr}} @media (max-width:560px){.que{grid-template-columns:1fr}}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-top:48px} .stats .n{font-family:var(--display);font-size:clamp(64px,8vw,120px);line-height:.85;color:var(--azul)} .stats b{display:block;font-size:12px;letter-spacing:.16em;text-transform:uppercase;margin:8px 0 4px} .stats p{margin:0;font-size:14px;color:var(--muted)}
@media (max-width:900px){.stats{grid-template-columns:1fr 1fr}}
.timeline{list-style:none;margin:0;padding:0;columns:2;column-gap:48px} .timeline li{break-inside:avoid;display:grid;grid-template-columns:72px 1fr;gap:14px;padding:12px 0;border-bottom:1px dashed var(--line);font-size:15px} .timeline b{font-family:var(--display);font-size:28px;color:var(--azul);line-height:1}
@media (max-width:760px){.timeline{columns:1}}
#munmx{background:var(--tinta)} #munmx .wrap{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
#munmx .esmun-logo{max-width:520px} #munmx h2{font-size:clamp(64px,10vw,160px);color:#fff} #munmx .lockup{max-width:420px;margin:26px 0 30px}
@media (max-width:900px){#munmx .wrap{grid-template-columns:1fr}}
.comites{list-style:none;margin:40px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line)} .com{background:var(--tinta);padding:22px;display:grid;gap:6px;border-top:3px solid var(--acc)} .com .sig{font-size:56px;line-height:.9;color:#fff} .com .nm{font-size:14px;color:#E6E9F5} .com .lv{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#A6ADC6}
@media (max-width:760px){.comites{grid-template-columns:1fr 1fr}}
.news{display:grid;grid-template-columns:repeat(3,1fr);gap:32px} .news-card a{text-decoration:none;display:grid;gap:12px} .news-card .thumb{aspect-ratio:4/3} .news-card .meta{display:flex;gap:12px;align-items:center;font-size:12px;color:var(--muted)} .news-card h3{font-size:clamp(26px,2.4vw,34px);font-family:var(--display);text-transform:uppercase;line-height:.92} .news-card p{margin:0;font-size:14.5px;color:var(--muted)}
@media (max-width:900px){.news{grid-template-columns:1fr}}
#contacto .wrap{display:grid;grid-template-columns:1fr 1fr;gap:56px} #contacto h2{font-size:clamp(56px,8vw,120px)} #contacto .dl{font-size:15px;line-height:1.9;margin-top:24px} #contacto .dl b{display:block;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
@media (max-width:900px){#contacto .wrap{grid-template-columns:1fr}}
"""
def p1():
    body=header()+f"""
<main>
<section class="hero" id="inicio" data-section data-theme="paper"><div class="wrap hero-grid">
 <div><p class="eyebrow reveal">Modelo de Naciones Unidas · PrepaTec Esmeralda</p>
  <h1 class="display reveal d1">Toma la<br><em>palabra.</em></h1>
  <p class="lead reveal d2" style="margin-top:28px">{C['intro']}</p>
  <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:28px" class="reveal d3"><a class="btn" href="#contacto">Únete al equipo</a><a class="btn ghost" href="#munmx">MUNMX Esmeralda 2027</a></div>
  <div class="meta reveal d3"><div><b>Desde</b>2019</div><div><b>Sede</b>{C['ciudad']}</div><div><b>Instagram</b><a href="{C['ig_url']}" rel="noopener" target="_blank" style="text-decoration:none">{C['ig']}</a></div></div></div>
 <figure class="reveal d2"><div class="duo" style="aspect-ratio:4/5"><img src="{A}/img/photo_placard_hand.jpg" alt="Delegado levantando la placa en una sesión"></div><figcaption>Para pedir la palabra se levanta la placa. Fotografía provisional generada por IA.</figcaption></figure>
</div></section>

<section id="quienes" data-section data-theme="paper"><div class="wrap">
 <div class="sec-head"><h2 class="display reveal">Quiénes<br>somos</h2><p class="lead reveal d1">Un equipo de preparatoria que debate como una delegación. Nos preparamos durante el ciclo escolar, competimos en modelos de otras escuelas y organizamos el nuestro.</p></div>
 <div class="que">{''.join(f'<div class="reveal d{i%4}"><h3 class="display">{t}</h3><p>{p}</p></div>' for i,(t,p) in enumerate(C['que']))}</div>
 <div class="stats">{''.join(f'<div class="reveal d{i%4}"><div class="n num" {"data-count="+n if n.isdigit() and n!="2019" else ""}>{n}</div><b>{l}</b><p>{p}</p></div>' for i,(n,l,p) in enumerate(C['stats']))}</div>
 <h3 class="display reveal" style="font-size:clamp(36px,4vw,60px);margin:72px 0 20px">Línea de tiempo</h3>
 <ol class="timeline">{''.join(f'<li class="reveal"><b>{y}</b><span>{t}</span></li>' for y,t in C['timeline'])}</ol>
</div></section>

<section id="munmx" data-section data-theme="dark"><div class="wrap">
 <div class="reveal">{LOGO_P()}</div>
 <div><p class="eyebrow reveal">Nuestra conferencia</p><h2 class="display reveal d1">Próxima-<br>mente</h2>
  <img class="lockup reveal d2" src="{A}/logo/MUNMX_proximamente_lockup_horizontal_blanco.svg" alt="MUNMX Esmeralda · Próximamente">
  <p class="lead reveal d2" style="color:#C9D2F0">Estamos preparando MUNMX Esmeralda 2027. Comités en español e inglés, niveles de principiante a experto y registro de delegaciones en mymun. Las fechas se anuncian aquí y en {C['ig']}.</p>
  <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:26px" class="reveal d3"><a class="btn" href="#contacto">Avísame cuando haya fechas</a><a class="btn ghost" href="{C['mymun']}" rel="noopener" target="_blank">Edición 2026 en mymun</a></div>
 </div>
 <div style="grid-column:1/-1"><p class="eyebrow reveal" style="margin-top:40px">Comités de referencia (edición 2024-2026)</p><ul class="comites">{comite_list()}</ul></div>
</div></section>

<section id="noticias" data-section data-theme="paper"><div class="wrap">
 <div class="sec-head"><h2 class="display reveal">Noticias</h2><p class="lead reveal d1">Convocatorias, resultados y lo que pasa entre sesiones. <a href="../noticias/">Ver todas</a>.</p></div>
 <div class="news">{news_cards()}</div>
</div></section>

<section id="contacto" data-section data-theme="paper"><div class="wrap">
 <div><h2 class="display reveal">Hablemos</h2><p class="lead reveal d1" style="margin-top:20px">Para unirte al equipo, registrar a tu delegación o proponer una alianza.</p>
  <div class="dl reveal d2"><b>Correo</b><a href="mailto:{C['mail']}">{C['mail']}</a><b style="margin-top:12px">Instagram</b><a href="{C['ig_url']}" rel="noopener" target="_blank">{C['ig']}</a><b style="margin-top:12px">Dónde</b>PrepaTec Esmeralda · {C['ciudad']}</div></div>
 <div class="reveal d1">{contact_form()}</div>
</div></section>
</main>"""+footer()
    return body
PROPS['p1-editorial']=dict(title='Editorial',css=P1_CSS,body=p1,desc='Papel, titulares gigantes recortados al borde y retícula editorial. La portada más cercana al manual.')

# ======================================================================= P2 · Cinemático
P2_CSS="""
.site-header{position:fixed;left:0;right:0;background:transparent;border-color:transparent} .site-header[data-theme="dark"]{background:linear-gradient(rgba(28,32,48,.65),rgba(28,32,48,0));backdrop-filter:none}
.site-header:not([data-theme]){background:color-mix(in srgb,var(--bg) 88%,transparent);border-color:var(--line)}
.hero{position:relative;min-height:100svh;display:grid;align-items:end;color:#fff;overflow:hidden;background:var(--tinta)}
.hero .bg{position:absolute;inset:0} .hero .bg img{width:100%;height:100%;object-fit:cover;object-position:50% 35%;filter:saturate(.8) brightness(.72);transform:scale(1.08);animation:kb 24s ease-out both}
@keyframes kb{from{transform:scale(1.18) translateY(2%)}to{transform:scale(1.04) translateY(0)}}
.hero .bg::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(28,32,48,.96) 0%,rgba(28,32,48,.35) 50%,rgba(28,32,48,.25) 100%)}
.hero .wrap{position:relative;padding-bottom:clamp(40px,8vh,90px);display:grid;grid-template-columns:1.3fr .7fr;gap:40px;align-items:end;width:100%}
.hero h1{font-size:clamp(72px,12vw,210px);color:#fff} .hero .lead{color:#DCE3F7} .hero .side{text-align:right;font-size:13px;color:#C9D2F0} .hero .side .esmun-logo{max-width:220px;margin-left:auto;margin-bottom:18px}
@media (max-width:900px){.hero .wrap{grid-template-columns:1fr} .hero .side{text-align:left} .hero .side .esmun-logo{margin-left:0}}
section{padding-block:clamp(56px,9vw,120px)} h2.display{font-size:clamp(48px,7vw,110px)}
.quehacemos .wrap{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start} .nums{display:grid;grid-template-columns:1fr 1fr;gap:28px} .nums .n{font-family:var(--display);font-size:clamp(80px,9vw,150px);line-height:.85;color:var(--azul)} .nums b{display:block;font-size:12px;letter-spacing:.16em;text-transform:uppercase;margin:6px 0 4px} .nums p{margin:0;font-size:14px;color:var(--muted)}
.que{display:grid;gap:18px;margin-top:28px} .que div{display:grid;grid-template-columns:120px 1fr;gap:18px;padding-top:14px;border-top:1px solid var(--line)} .que h3{font-family:var(--display);font-size:34px;text-transform:uppercase;color:var(--azul)} .que p{margin:0;color:var(--muted);font-size:15px}
@media (max-width:900px){.quehacemos .wrap{grid-template-columns:1fr}}
.strip{padding-block:0} .strip .rail{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;padding:8px var(--gutter) 28px;scrollbar-width:thin} .strip .rail::-webkit-scrollbar{height:6px}
.com{list-style:none;scroll-snap-align:start;flex:0 0 min(78vw,340px);aspect-ratio:3/4;background:var(--acc);color:#fff;padding:24px;display:grid;align-content:end;gap:8px;position:relative;overflow:hidden;transition:transform .4s var(--ease)} .com:hover{transform:translateY(-6px)}
.com .sig{font-size:120px;line-height:.8;position:absolute;top:18px;left:18px;opacity:.9} .com .nm{font-weight:600;font-size:16px} .com .lv{font-size:11px;letter-spacing:.16em;text-transform:uppercase;opacity:.8}
#munmx{background:var(--tinta);position:relative;overflow:hidden} #munmx .bg{position:absolute;inset:0;opacity:.35} #munmx .bg img{width:100%;height:100%;object-fit:cover;filter:grayscale(1)} #munmx .wrap{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
#munmx h2{font-size:clamp(72px,11vw,180px);color:#fff} #munmx .esmun-logo{max-width:460px;margin-left:auto}
@media (max-width:900px){#munmx .wrap{grid-template-columns:1fr} #munmx .esmun-logo{margin-left:0}}
.news{display:grid;gap:0;border-top:1px solid var(--line)} .news-card a{display:grid;grid-template-columns:120px 1fr 2fr;gap:24px;align-items:center;padding:22px 0;border-bottom:1px solid var(--line);text-decoration:none} .news-card .thumb{aspect-ratio:1} .news-card .meta{display:grid;gap:8px;font-size:12px;color:var(--muted)} .news-card h3{font-size:clamp(22px,2.2vw,30px);font-weight:600;line-height:1.15} .news-card p{margin:6px 0 0;color:var(--muted);font-size:14px}
@media (max-width:760px){.news-card a{grid-template-columns:80px 1fr} .news-card p{display:none}}
#contacto{background:var(--papel)} #contacto .wrap{display:grid;grid-template-columns:1fr 1fr;gap:56px} @media (max-width:900px){#contacto .wrap{grid-template-columns:1fr}}
"""
def p2():
    body=header()+f"""
<main>
<section class="hero" id="inicio" data-section data-theme="dark"><div class="bg"><img src="{A}/img/photo_ceremony.jpg" alt=""></div>
 <div class="wrap"><div><p class="eyebrow reveal" style="color:#B9C6EE">Modelo de Naciones Unidas · PrepaTec Esmeralda</p><h1 class="display reveal d1">Debates.<br>Liderazgo.<br>Impacto.</h1>
  <p class="lead reveal d2" style="margin-top:24px">{C['intro']}</p>
  <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:28px" class="reveal d3"><a class="btn" href="#contacto" style="background:#fff;color:var(--azul);border-color:#fff">Únete al equipo</a><a class="btn ghost" href="#munmx" style="color:#fff">MUNMX 2027</a></div></div>
  <div class="side reveal d2">{LOGO_P()}Las ventanas del edificio se encienden sobre fondo oscuro.<br>Fotografía provisional generada por IA.</div></div>
</section>

<section class="quehacemos" id="quienes" data-section><div class="wrap">
 <div><p class="eyebrow reveal">Quiénes somos</p><h2 class="display reveal d1">Un equipo que<br>debate como<br>una delegación</h2>
  <div class="que">{''.join(f'<div class="reveal"><h3>{t}</h3><p>{p}</p></div>' for t,p in C['que'])}</div></div>
 <div class="nums">{''.join(f'<div class="reveal d{i%4}"><div class="n num" {"data-count="+n if n.isdigit() and n!="2019" else ""}>{n}</div><b>{l}</b><p>{p}</p></div>' for i,(n,l,p) in enumerate(C['stats']))}</div>
</div></section>

<section class="strip" data-section><div class="wrap" style="padding-bottom:10px"><p class="eyebrow">Comités de referencia · 2024-2026</p></div><ul class="rail" style="margin:0;padding-left:var(--gutter)">{comite_list()}</ul></section>

<section id="munmx" data-section data-theme="dark"><div class="bg"><img src="{A}/img/photo_placard_hand.jpg" alt=""></div><div class="wrap">
 <div><p class="eyebrow reveal" style="color:#B9C6EE">MUNMX Esmeralda 2027</p><h2 class="display reveal d1">Próxima-<br>mente</h2>
  <img class="reveal d2" style="max-width:420px;margin:24px 0" src="{A}/logo/MUNMX_proximamente_lockup_horizontal_blanco.svg" alt="MUNMX Esmeralda · Próximamente">
  <p class="lead reveal d2" style="color:#C9D2F0">Fechas, comités y registro de delegaciones se anuncian aquí y en {C['ig']}.</p>
  <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:26px" class="reveal d3"><a class="btn" href="#contacto" style="background:#fff;color:var(--azul);border-color:#fff">Avísame</a><a class="btn ghost" href="{C['mymun']}" rel="noopener" target="_blank" style="color:#fff">Edición 2026 en mymun</a></div></div>
 <div class="reveal d1">{LOGO_P()}</div>
</div></section>

<section id="noticias" data-section><div class="wrap"><p class="eyebrow reveal">Noticias</p><h2 class="display reveal d1" style="margin-bottom:32px">Entre sesiones</h2><div class="news">{news_cards()}</div><p style="margin-top:24px"><a class="btn ghost" href="../noticias/">Todas las noticias</a></p></div></section>

<section id="contacto" data-section data-theme="paper"><div class="wrap"><div><p class="eyebrow reveal">Contacto</p><h2 class="display reveal d1">Hablemos</h2><p class="lead reveal d2" style="margin-top:20px">Para unirte al equipo, registrar a tu delegación o proponer una alianza.</p><p class="reveal d2" style="margin-top:20px;line-height:1.9"><a href="mailto:{C['mail']}">{C['mail']}</a><br><a href="{C['ig_url']}" rel="noopener" target="_blank">Instagram {C['ig']}</a><br>PrepaTec Esmeralda · {C['ciudad']}</p></div><div class="reveal d1">{contact_form()}</div></div></section>
</main>"""+footer()
    return body
PROPS['p2-cinematico']=dict(title='Cinemático',css=P2_CSS,body=p2,desc='Portada fotográfica a pantalla completa con movimiento lento, cabecera transparente, carril horizontal de comités y bandas oscuras.')

# ======================================================================= P3 · Retícula suiza
P3_CSS="""
body{background-image:linear-gradient(to right,rgba(37,60,130,.07) 1px,transparent 1px);background-size:calc(100%/12) 100%;background-attachment:fixed}
[data-theme="dark"]{background-image:linear-gradient(to right,rgba(255,255,255,.07) 1px,transparent 1px);background-size:calc(100%/12) 100%}
section{padding-block:clamp(56px,9vw,120px)} .lbl{font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);display:flex;justify-content:space-between;border-top:1px solid var(--fg);padding-top:10px;margin-bottom:28px}
.hero{min-height:88svh;display:grid;align-items:center} .hero .wrap{display:grid;grid-template-columns:repeat(12,1fr);gap:16px;align-items:end}
.hero h1{grid-column:1/13;font-size:clamp(80px,19vw,330px);line-height:.78;letter-spacing:-.005em;color:var(--azul)} .hero h1 span{display:block;padding-left:calc(100%/12*4)}
.hero .intro{grid-column:1/6;margin-top:28px} .hero .iso{grid-column:9/13;max-width:360px;justify-self:end} .hero .cta{grid-column:6/9;display:flex;gap:12px;flex-wrap:wrap;align-self:end;margin-top:28px}
@media (max-width:900px){.hero .wrap>*{grid-column:1/13!important} .hero .iso{justify-self:start} .hero h1 span{padding-left:0}}
.g12{display:grid;grid-template-columns:repeat(12,1fr);gap:16px} .c3{grid-column:span 3} .c4{grid-column:span 4} .c6{grid-column:span 6} .c8{grid-column:span 8} .c12{grid-column:span 12}
@media (max-width:900px){.c3,.c4{grid-column:span 6}} @media (max-width:600px){.c3,.c4,.c6,.c8{grid-column:span 12}}
.stat{border-top:2px solid var(--azul);padding-top:12px} .stat .n{font-family:var(--display);font-size:clamp(64px,8vw,124px);line-height:.85} .stat b{display:block;font-size:11px;letter-spacing:.18em;text-transform:uppercase;margin:6px 0 4px} .stat p{margin:0;font-size:14px;color:var(--muted)}
.que h3{font-family:var(--display);text-transform:uppercase;font-size:40px;color:var(--azul)} .que p{margin:6px 0 0;font-size:15px;color:var(--muted)} .que{border-top:1px solid var(--line);padding-top:14px}
.pattern{aspect-ratio:1;background:var(--azul);position:relative;overflow:hidden} .pattern i{position:absolute;background:#fff;opacity:.9;animation:blink 6s ease-in-out infinite;animation-delay:calc(var(--d)*1s)} @keyframes blink{0%,100%{opacity:.25}50%{opacity:.95}}
#munmx{background:var(--tinta)} #munmx .lbl{color:#A6ADC6;border-color:#fff} #munmx h2{font-size:clamp(72px,12vw,200px);color:#fff;grid-column:1/9} #munmx .esmun-logo{grid-column:9/13;max-width:380px;justify-self:end;align-self:start}
#munmx .com{list-style:none;grid-column:span 4;border-top:2px solid var(--acc);padding-top:12px;display:grid;gap:4px;color:#fff} #munmx .com .sig{font-size:44px;line-height:.9} #munmx .com .nm{font-size:13px;color:#DCE3F7} #munmx .com .lv{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#A6ADC6}
@media (max-width:900px){#munmx h2,#munmx .esmun-logo{grid-column:1/13;justify-self:start} #munmx .com{grid-column:span 6}}
.news-card{grid-column:span 4} .news-card a{text-decoration:none;display:grid;gap:10px;border-top:1px solid var(--fg);padding-top:12px} .news-card .thumb{aspect-ratio:3/2} .news-card .meta{display:flex;justify-content:space-between;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)} .news-card h3{font-size:22px;font-weight:600;line-height:1.2} .news-card p{margin:0;font-size:14px;color:var(--muted)}
@media (max-width:900px){.news-card{grid-column:span 6}} @media (max-width:600px){.news-card{grid-column:span 12}}
"""
def p3():
    import random; r=random.Random(5)
    pat=''.join(f'<i style="left:{r.randint(4,88)}%;top:{r.randint(4,88)}%;width:{r.choice([5,7,9])}%;aspect-ratio:1;--d:{r.random()*4:.2f}"></i>' for _ in range(22))
    body=header()+f"""
<main>
<section class="hero" id="inicio" data-section><div class="wrap">
 <h1 class="display reveal">ESMUN<span>Toma la palabra.</span></h1>
 <p class="intro lead reveal d1">{C['intro']}</p>
 <div class="cta reveal d2"><a class="btn" href="#contacto">Únete</a><a class="btn ghost" href="#munmx">MUNMX 2027</a></div>
 <div class="iso reveal d2">{LOGO_I()}</div>
</div></section>

<section id="quienes" data-section><div class="wrap">
 <div class="lbl"><span>01 · Quiénes somos</span><span>PrepaTec Esmeralda · desde 2019</span></div>
 <div class="g12">
  <div class="c4 pattern reveal" aria-hidden="true">{pat}</div>
  <div class="c8 g12" style="gap:16px 16px">{''.join(f'<div class="c6 que reveal d{i%4}"><h3>{t}</h3><p>{p}</p></div>' for i,(t,p) in enumerate(C['que']))}</div>
  {''.join(f'<div class="c3 stat reveal d{i%4}"><div class="n num" {"data-count="+n if n.isdigit() and n!="2019" else ""}>{n}</div><b>{l}</b><p>{p}</p></div>' for i,(n,l,p) in enumerate(C['stats']))}
  <div class="c12 lbl" style="margin-top:40px"><span>Línea de tiempo</span><span>2019 → 2027</span></div>
  {''.join(f'<div class="c4 reveal"><b class="display" style="font-size:40px;color:var(--azul)">{y}</b><p style="margin:6px 0 0;font-size:14px;color:var(--muted)">{t}</p></div>' for y,t in C['timeline'])}
 </div></div></section>

<section id="munmx" data-section data-theme="dark"><div class="wrap">
 <div class="lbl"><span>02 · MUNMX Esmeralda 2027</span><span>Próximamente</span></div>
 <div class="g12"><h2 class="display reveal">Próxima-<br>mente</h2><div class="reveal d1">{LOGO_P()}</div>
  <div class="c6 reveal d1"><img style="max-width:420px" src="{A}/logo/MUNMX_proximamente_lockup_horizontal_blanco.svg" alt="MUNMX Esmeralda · Próximamente"><p class="lead" style="color:#C9D2F0;margin-top:20px">Comités en español e inglés, niveles de principiante a experto y registro de delegaciones en mymun. Las fechas se publican aquí y en {C['ig']}.</p><div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:22px"><a class="btn" href="#contacto" style="background:#fff;color:var(--azul);border-color:#fff">Avísame</a><a class="btn ghost" href="{C['mymun']}" rel="noopener" target="_blank" style="color:#fff">Edición 2026</a></div></div>
  <div class="c12 lbl" style="margin-top:36px;color:#A6ADC6"><span>Comités de referencia</span><span>2024-2026</span></div>{comite_list()}
 </div></div></section>

<section id="noticias" data-section><div class="wrap"><div class="lbl"><span>03 · Noticias</span><a href="../noticias/" style="text-decoration:none">Ver todas →</a></div><div class="g12">{news_cards()}</div></div></section>

<section id="contacto" data-section data-theme="paper"><div class="wrap"><div class="lbl"><span>04 · Contacto</span><span>{C['mail']}</span></div>
 <div class="g12"><div class="c5 reveal" style="grid-column:span 5"><h2 class="display" style="font-size:clamp(56px,8vw,120px)">Hablemos</h2><p class="lead" style="margin-top:18px">Para unirte al equipo, registrar a tu delegación o proponer una alianza.</p><p style="line-height:1.9;margin-top:18px"><a href="{C['ig_url']}" rel="noopener" target="_blank">Instagram {C['ig']}</a><br>PrepaTec Esmeralda · {C['ciudad']}</p></div><div class="reveal d1" style="grid-column:7/13">{contact_form()}</div></div></div></section>
</main>"""+footer()
    return body
PROPS['p3-reticula']=dict(title='Retícula',css=P3_CSS,body=p3,desc='Doce columnas visibles, etiquetas numeradas, cifras enormes y el patrón de ventanas como textura. Orden suizo.')

# ======================================================================= P4 · Bloques
P4_CSS="""
.site-header{border-bottom:2px solid var(--fg)} .hero{background:var(--azul);color:#fff;min-height:92svh;display:grid;grid-template-rows:1fr auto}
.hero .wrap{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;padding-block:48px} .hero h1{font-size:clamp(90px,15vw,260px);line-height:.8} .hero .esmun-logo{max-width:520px;justify-self:end} .hero .lead{color:#DCE3F7}
.hero .btn{background:#fff;color:var(--azul);border-color:#fff} .hero .btn.ghost{background:transparent;color:#fff}
.ticker{border-top:2px solid #fff;padding:14px 0;font-family:var(--display);font-size:clamp(28px,3.4vw,52px);text-transform:uppercase;letter-spacing:.02em}
@media (max-width:900px){.hero .wrap{grid-template-columns:1fr} .hero .esmun-logo{justify-self:start;max-width:380px}}
section{padding-block:clamp(56px,9vw,120px)} h2.display{font-size:clamp(56px,8vw,130px)}
.blocks{display:grid;grid-template-columns:repeat(4,1fr);border:2px solid var(--fg);margin-top:40px} .blocks div{padding:26px 22px;border-right:2px solid var(--fg);transition:background .25s,color .25s} .blocks div:last-child{border-right:0} .blocks div:hover{background:var(--azul);color:#fff} .blocks div:hover p{color:#DCE3F7}
.blocks h3{font-family:var(--display);text-transform:uppercase;font-size:44px} .blocks p{margin:10px 0 0;font-size:15px;color:var(--muted)}
@media (max-width:900px){.blocks{grid-template-columns:1fr 1fr} .blocks div:nth-child(2){border-right:0} .blocks div:nth-child(-n+2){border-bottom:2px solid var(--fg)}} @media (max-width:560px){.blocks{grid-template-columns:1fr} .blocks div{border-right:0;border-bottom:2px solid var(--fg)} .blocks div:last-child{border-bottom:0}}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:var(--fg);border:2px solid var(--fg);margin-top:2px} .stats div{background:var(--papel);padding:22px} .stats .n{font-family:var(--display);font-size:clamp(72px,9vw,140px);line-height:.85;color:var(--azul)} .stats b{display:block;font-size:11px;letter-spacing:.18em;text-transform:uppercase;margin:6px 0 4px} .stats p{margin:0;font-size:13.5px;color:var(--muted)}
@media (max-width:900px){.stats{grid-template-columns:1fr 1fr}}
#munmx{background:#000;color:#fff} #munmx .wrap{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center} #munmx h2{font-size:clamp(80px,13vw,220px);line-height:.8} #munmx .esmun-logo{max-width:520px} #munmx .btn{background:#fff;color:#000;border-color:#fff} #munmx .btn.ghost{background:transparent;color:#fff}
@media (max-width:900px){#munmx .wrap{grid-template-columns:1fr}}
.comites{list-style:none;margin:48px 0 0;padding:0;display:grid;grid-template-columns:repeat(6,1fr);border:2px solid #fff} .com{padding:18px 14px;border-right:2px solid #fff;display:grid;gap:4px;background:var(--acc)} .com:last-child{border-right:0} .com .sig{font-size:40px;line-height:.9} .com .nm{font-size:12px} .com .lv{font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.8}
@media (max-width:900px){.comites{grid-template-columns:repeat(3,1fr)} .com:nth-child(3){border-right:0} .com:nth-child(-n+3){border-bottom:2px solid #fff}} @media (max-width:560px){.comites{grid-template-columns:1fr 1fr} .com{border-right:2px solid #fff!important;border-bottom:2px solid #fff}}
.news{border-top:2px solid var(--fg)} .news-card a{display:grid;grid-template-columns:72px 1fr auto;gap:24px;align-items:center;padding:22px 0;border-bottom:2px solid var(--fg);text-decoration:none;transition:background .25s} .news-card a:hover{background:var(--papel)} .news-card .idx{font-family:var(--display);font-size:56px;line-height:.9;color:var(--azul)} .news-card h3{font-size:clamp(22px,2.4vw,34px);font-weight:700;line-height:1.1} .news-card p{margin:6px 0 0;color:var(--muted);font-size:14px} .news-card .meta{display:grid;gap:6px;text-align:right;font-size:12px;color:var(--muted)}
@media (max-width:700px){.news-card a{grid-template-columns:1fr} .news-card .meta{text-align:left}}
#contacto{background:var(--papel)} #contacto .wrap{display:grid;grid-template-columns:1fr 1fr;gap:56px} #contacto .form input,#contacto .form textarea,#contacto .form select{border:2px solid var(--fg);background:#fff}
@media (max-width:900px){#contacto .wrap{grid-template-columns:1fr}}
"""
def p4():
    news=''
    for i,(date,tag,title,desc,photo) in enumerate(C['noticias'],1):
        news+=f'<article class="news-card reveal"><a href="../noticias/"><span class="idx">0{i}</span><div><h3>{title}</h3><p>{desc}</p></div><div class="meta"><time datetime="{date}">{date}</time><span class="pill">{tag}</span></div></a></article>'
    body=header()+f"""
<main>
<section class="hero" id="inicio" data-section data-theme="blue"><div class="wrap">
 <div><p class="eyebrow reveal" style="color:#fff">Modelo de Naciones Unidas · PrepaTec Esmeralda</p><h1 class="display reveal d1">Toma la<br>palabra.</h1><p class="lead reveal d2" style="margin-top:24px">{C['intro']}</p>
  <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:28px" class="reveal d3"><a class="btn" href="#contacto">Únete al equipo</a><a class="btn ghost" href="#munmx">MUNMX 2027</a></div></div>
 <div class="reveal d2">{LOGO_P()}</div></div>
 <div class="ticker marquee" aria-hidden="true"><span>Debates · Liderazgo · Impacto · MUNMX Esmeralda 2027 · Próximamente · Convocatoria abierta · {C['ig']} · Debates · Liderazgo · Impacto · MUNMX Esmeralda 2027 · Próximamente · Convocatoria abierta · {C['ig']} · </span></div>
</section>

<section id="quienes" data-section><div class="wrap"><p class="eyebrow reveal">Quiénes somos</p><h2 class="display reveal d1">Un equipo, una<br>conferencia, un edificio</h2>
 <div class="blocks">{''.join(f'<div class="reveal d{i%4}"><h3>{t}</h3><p>{p}</p></div>' for i,(t,p) in enumerate(C['que']))}</div>
 <div class="stats">{''.join(f'<div class="reveal d{i%4}"><div class="n num" {"data-count="+n if n.isdigit() and n!="2019" else ""}>{n}</div><b>{l}</b><p>{p}</p></div>' for i,(n,l,p) in enumerate(C['stats']))}</div>
</div></section>

<section id="munmx" data-section data-theme="dark"><div class="wrap">
 <div><p class="eyebrow reveal" style="color:#B9C6EE">MUNMX Esmeralda 2027</p><h2 class="display reveal d1">Próxima-<br>mente</h2><img class="reveal d2" style="max-width:440px;margin:24px 0" src="{A}/logo/MUNMX_proximamente_lockup_horizontal_blanco.svg" alt="MUNMX Esmeralda · Próximamente"><p class="lead reveal d2" style="color:#C9D2F0">Fechas, comités y registro de delegaciones se anuncian aquí y en {C['ig']}.</p><div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:26px" class="reveal d3"><a class="btn" href="#contacto">Avísame</a><a class="btn ghost" href="{C['mymun']}" rel="noopener" target="_blank">Edición 2026 en mymun</a></div></div>
 <div class="reveal d1">{LOGO_P()}</div>
 <div style="grid-column:1/-1"><ul class="comites">{comite_list()}</ul></div>
</div></section>

<section id="noticias" data-section><div class="wrap"><p class="eyebrow reveal">Noticias</p><h2 class="display reveal d1" style="margin-bottom:28px">Entre sesiones</h2><div class="news">{news}</div><p style="margin-top:24px"><a class="btn" href="../noticias/">Todas las noticias</a></p></div></section>

<section id="contacto" data-section data-theme="paper"><div class="wrap"><div><p class="eyebrow reveal">Contacto</p><h2 class="display reveal d1">Hablemos</h2><p class="lead reveal d2" style="margin-top:20px">Para unirte al equipo, registrar a tu delegación o proponer una alianza.</p><p class="reveal d2" style="line-height:1.9;margin-top:20px"><a href="mailto:{C['mail']}">{C['mail']}</a><br><a href="{C['ig_url']}" rel="noopener" target="_blank">Instagram {C['ig']}</a><br>PrepaTec Esmeralda · {C['ciudad']}</p></div><div class="reveal d1">{contact_form()}</div></div></section>
</main>"""+footer()
    return body
PROPS['p4-bloques']=dict(title='Bloques',css=P4_CSS,body=p4,desc='Azul pleno, bordes gruesos, cinta de texto en movimiento y bloques que se invierten al pasar el cursor. Institucional con carácter.')

# ======================================================================= P5 · Inmersivo (scrollytelling)
P5_CSS="""
.scrolly{height:360vh;position:relative} .scrolly .stage{position:sticky;top:0;height:100svh;display:grid;place-items:center;overflow:hidden;transition:background .8s var(--ease),color .8s var(--ease)}
.scrolly .esmun-logo{height:min(52svh,38vw);width:auto;margin-top:4vh} .scrolly .bp,.scrolly .word,.scrolly .sub{opacity:0;transition:opacity .2s linear,transform .2s linear}
.scrolly .hint{position:absolute;bottom:28px;left:0;right:0;text-align:center;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);opacity:calc(1 - var(--p,0)*4)}
.scrolly .claim{position:absolute;left:var(--gutter);right:var(--gutter);top:12vh;font-size:clamp(32px,5vw,84px);color:#fff;opacity:calc((var(--p,0) - .86)*8);transform:translateY(calc((1 - min(1,max(0,(var(--p,0) - .86)*8)))*20px))}
.scrolly .hero-cta{position:absolute;right:var(--gutter);bottom:5vh;display:flex;gap:12px;opacity:calc((var(--p,0) - .9)*10)}
.scrolly .stage[data-theme="dark"] .btn{background:#fff;color:var(--azul);border-color:#fff} .scrolly .stage[data-theme="dark"] .btn.ghost{background:transparent;color:#fff}
section{padding-block:clamp(56px,9vw,120px)} h2.display{font-size:clamp(56px,8vw,130px)}
.intro .wrap{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start} .intro .lead{font-size:clamp(20px,2vw,28px);color:var(--fg);line-height:1.4}
.que{display:grid;gap:22px} .que div{display:grid;grid-template-columns:1fr;gap:6px;padding-top:12px;border-top:1px solid var(--line)} .que h3{font-family:var(--display);text-transform:uppercase;font-size:36px;color:var(--azul)} .que p{margin:0;color:var(--muted);font-size:15px}
@media (max-width:900px){.intro .wrap{grid-template-columns:1fr}}
.photos{display:grid;grid-template-columns:repeat(3,1fr);gap:16px} .photos figure{margin:0} .photos .duo{aspect-ratio:4/5} .photos figcaption{font-size:12px;color:var(--muted);margin-top:8px}
@media (max-width:700px){.photos{grid-template-columns:1fr}}
.stats{display:flex;gap:40px;flex-wrap:wrap;margin-top:40px} .stats div{flex:1 1 180px} .stats .n{font-family:var(--display);font-size:clamp(72px,9vw,140px);line-height:.85;color:var(--azul)} .stats b{display:block;font-size:11px;letter-spacing:.18em;text-transform:uppercase;margin:6px 0 4px} .stats p{margin:0;font-size:13.5px;color:var(--muted)}
#munmx{background:var(--tinta);min-height:100svh;display:grid;align-items:center;overflow:hidden;position:relative} #munmx .year{position:absolute;right:-2vw;top:50%;transform:translateY(-50%);font-size:clamp(200px,40vw,720px);line-height:.8;color:rgba(255,255,255,.06);pointer-events:none;user-select:none}
#munmx .wrap{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center} #munmx h2{font-size:clamp(72px,11vw,180px);color:#fff} #munmx .esmun-logo{max-width:440px}
@media (max-width:900px){#munmx .wrap{grid-template-columns:1fr}}
.comites{list-style:none;margin:40px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:10px} .com{display:inline-grid;grid-auto-flow:column;align-items:center;gap:12px;padding:10px 16px 10px 12px;border:1px solid rgba(255,255,255,.3);border-radius:999px;color:#fff} .com .sig{font-size:28px;line-height:1;color:var(--acc);filter:brightness(1.6)} .com .nm{font-size:13px} .com .lv{display:none}
.news{display:grid;grid-template-columns:repeat(3,1fr);gap:24px} .news-card a{text-decoration:none;display:grid;gap:12px} .news-card .thumb{aspect-ratio:1;border-radius:4px} .news-card .meta{display:flex;gap:12px;font-size:12px;color:var(--muted)} .news-card h3{font-size:22px;font-weight:600;line-height:1.2} .news-card p{margin:0;font-size:14px;color:var(--muted)}
@media (max-width:900px){.news{grid-template-columns:1fr}}
#contacto{background:var(--papel)} #contacto .wrap{display:grid;grid-template-columns:1fr 1fr;gap:56px} @media (max-width:900px){#contacto .wrap{grid-template-columns:1fr}}
"""
def p5():
    body=header()+f"""
<main>
<div class="scrolly" id="inicio" data-section data-theme="paper" data-scrolly><div class="stage" data-theme="paper">
 {esmun_logo_svg(kind='principal',mode='scrolly')}
 <p class="hint">Desplázate para construir el edificio</p>
 <h1 class="display claim">Toma la palabra.</h1>
 <div class="hero-cta"><a class="btn" href="#contacto">Únete al equipo</a><a class="btn ghost" href="#munmx">MUNMX 2027</a></div>
</div></div>

<section class="intro" id="quienes" data-section><div class="wrap">
 <div><p class="eyebrow reveal">Quiénes somos</p><p class="lead reveal d1" style="margin-top:14px">{C['intro']}</p>
  <div class="stats">{''.join(f'<div class="reveal d{i%4}"><div class="n num" {"data-count="+n if n.isdigit() and n!="2019" else ""}>{n}</div><b>{l}</b><p>{p}</p></div>' for i,(n,l,p) in enumerate(C['stats']))}</div></div>
 <div class="que">{''.join(f'<div class="reveal d{i%4}"><h3>{t}</h3><p>{p}</p></div>' for i,(t,p) in enumerate(C['que']))}</div>
</div>
<div class="wrap" style="margin-top:56px"><div class="photos">
 <figure class="reveal"><div class="duo"><img src="{A}/img/photo_gavel.jpg" alt="Mazo sobre mantel azul" loading="lazy"></div><figcaption>Sesiones de comité</figcaption></figure>
 <figure class="reveal d1"><div class="duo"><img src="{A}/img/photo_handshake.jpg" alt="Acuerdo entre delegaciones" loading="lazy"></div><figcaption>Negociación y consenso</figcaption></figure>
 <figure class="reveal d2"><div class="duo"><img src="{A}/img/photo_campus.jpg" alt="Campus" loading="lazy"></div><figcaption>PrepaTec Esmeralda · Fotografías provisionales generadas por IA</figcaption></figure>
</div></div></section>

<section id="munmx" data-section data-theme="dark"><div class="year display" aria-hidden="true">2027</div><div class="wrap">
 <div><p class="eyebrow reveal" style="color:#B9C6EE">MUNMX Esmeralda 2027</p><h2 class="display reveal d1">Próxima-<br>mente</h2><img class="reveal d2" style="max-width:420px;margin:24px 0" src="{A}/logo/MUNMX_proximamente_lockup_horizontal_blanco.svg" alt="MUNMX Esmeralda · Próximamente"><p class="lead reveal d2" style="color:#C9D2F0">Fechas, comités y registro de delegaciones se anuncian aquí y en {C['ig']}.</p><div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:26px" class="reveal d3"><a class="btn" href="#contacto" style="background:#fff;color:var(--azul);border-color:#fff">Avísame</a><a class="btn ghost" href="{C['mymun']}" rel="noopener" target="_blank" style="color:#fff">Edición 2026 en mymun</a></div>
  <ul class="comites">{comite_list()}</ul></div>
 <div class="reveal d1">{LOGO_P()}</div>
</div></section>

<section id="noticias" data-section><div class="wrap"><p class="eyebrow reveal">Noticias</p><h2 class="display reveal d1" style="margin-bottom:28px">Entre sesiones</h2><div class="news">{news_cards()}</div><p style="margin-top:24px"><a class="btn ghost" href="../noticias/">Todas las noticias</a></p></div></section>

<section id="contacto" data-section data-theme="paper"><div class="wrap"><div><p class="eyebrow reveal">Contacto</p><h2 class="display reveal d1">Hablemos</h2><p class="lead reveal d2" style="margin-top:20px">Para unirte al equipo, registrar a tu delegación o proponer una alianza.</p><p class="reveal d2" style="line-height:1.9;margin-top:20px"><a href="mailto:{C['mail']}">{C['mail']}</a><br><a href="{C['ig_url']}" rel="noopener" target="_blank">Instagram {C['ig']}</a><br>PrepaTec Esmeralda · {C['ciudad']}</p></div><div class="reveal d1">{contact_form()}</div></div></section>
</main>"""+footer()
    return body
PROPS['p5-inmersivo']=dict(title='Inmersivo',css=P5_CSS,body=p5,desc='El edificio se construye con el scroll, el fondo se vuelve tinta y las ventanas se encienden; después, el sitio.')

# ======================================================================= Noticias (blog SEO)
POSTS={
 'munmx-2027-fechas': dict(alt='Fachada de la PrepaTec Esmeralda', cap='PrepaTec Esmeralda, sede de MUNMX Esmeralda 2027. Foto: ESMUN.', body="""
<p>MUNMX Esmeralda 2027 se celebra el jueves 11, el viernes 12 y el sábado 13 de marzo de 2027 en la PrepaTec Esmeralda, en Atizapán de Zaragoza.</p>
<h2 class="display">Qué sigue</h2><p>La lista de comités, con nivel e idioma de cada uno, y la fecha de apertura del registro se anuncian con la convocatoria. El registro será por mymun, como en ESMUN 2024.</p>
<h2 class="display">Si quieres venir</h2><p>Delegaciones de otras preparatorias: hagan el <a href="../registro/">pre-registro</a> y les escribimos el día que abra el registro oficial. Alumnos de la PrepaTec Esmeralda: la convocatoria de delegados y de secretariado sale antes, por {C['ig']}.</p>"""),
 'identidad-visual-2026': dict(alt='Fachada de la PrepaTec Esmeralda, con el bloque blanco de ventanas que inspira el logotipo', cap='El bloque de ventanas de la PrepaTec Esmeralda, origen del logotipo. Foto: ESMUN.', body="""
<p>ESMUN tiene identidad nueva. El logotipo es el edificio de la prepa: el bloque blanco con ventanas de distintos tamaños que se ve desde el estacionamiento, dibujado en geometría plana y con la palabra ESMUN en League Gothic. Sobre fondo oscuro, las ventanas se encienden.</p>
<h2 class="display">Qué cambia</h2><p>Se mantiene el emblema circular de MUNMX, ahora con una versión de una tinta y una variante para la edición 2027 con la leyenda "Próximamente". Los dos logotipos conviven en una cofirma para piezas de la conferencia.</p>
<h2 class="display">El manual</h2><p>Hay un manual de identidad con colores, tipografías, usos correctos del logotipo, plantillas para redes y los colores de cada comité. La idea es que cualquiera del equipo, en cualquier generación, pueda producir piezas que se vean iguales sin pedir permiso para cada una.</p>
<p>Este sitio es la primera aplicación completa de la identidad.</p>"""),
 'mencion-honorifica-nueva-york-2023': dict(alt='Luis Enrique Flores en la sala de la Asamblea General de la ONU, en Nueva York', cap='Luis Enrique Flores en la sala de la Asamblea General, Nueva York, mayo de 2023. Foto: Conecta, Tecnológico de Monterrey.', body="""
<p>Luis Enrique Flores, alumno de la PrepaTec Esmeralda e integrante de ESMUN, obtuvo mención honorífica en el congreso Change the World Model United Nations, organizado en Nueva York por la ONG Associazione Diplomatici. Además recibió el reconocimiento al mejor papel de posición de todo el congreso.</p>
<h2 class="display">El congreso</h2><p>Participaron unas cinco mil personas de todo el mundo, con estudiantes de Serbia, Jamaica, Italia, España, Francia, Brasil y Paraguay, entre otros países. El tema: bloquear la adquisición de armas de destrucción masiva por parte de actores no gubernamentales, simulando distintas agencias de la ONU.</p>
<h2 class="display">Lo que se llevó</h2><p>"Haber ganado dos premios en la Asamblea General, frente a miles de personas de todo el mundo, es una sensación indescriptible", dijo Luis a Conecta. Su mayor reto, contó, fue debatir en pareja con una delegada de otra cultura; sus mayores aprendizajes, la comunicación y el pensamiento crítico.</p>
<p>Fuente: <a href="https://conecta.tec.mx/es/noticias/estado-de-mexico/educacion/alumno-de-prepatec-esmeralda-recibe-mencion-honorifica-en-nueva" rel="noopener" target="_blank">Conecta, Tecnológico de Monterrey, 30 de mayo de 2023</a>.</p>"""),
 '75-yamun-2020': dict(alt='Diego Zárate hablando en un podio con banderas y el logotipo del Tecnológico de Monterrey', cap='Diego Zárate, presidente fundador de ESMUN. Foto: Conecta, Tecnológico de Monterrey.', body="""
<p>Diego Zárate, estudiante de la PrepaTec Esmeralda y presidente fundador de ESMUN, fue seleccionado como vicepresidente de la Asamblea General en el 75 YAMUN, el primer Modelo de Naciones Unidas internacional respaldado por la ONU, organizado en línea en octubre de 2020 por el 75 aniversario de la organización. A sus 16 años era el organizador más joven y el único alumno de PrepaTec en el evento.</p>
<h2 class="display">Cómo empezó ESMUN</h2><p>Diego entró a la prepa a los 15 años y, tras un proceso de selección abierto a todos los semestres, fue nombrado secretario general del primer modelo de la prepa: ESMUN jr 2019, el 22 y 23 de noviembre de 2019. Después se reunió con LiFE para convertir ESMUN en grupo estudiantil, encargado de organizar los modelos de la prepa y de representarla en eventos relacionados con la ONU. En enero de 2020 fue elegido presidente del grupo.</p>
<h2 class="display">Un modelo histórico</h2><p>A diferencia de la mayoría de los modelos, el 75 YAMUN no debatía temas actuales: cada comité simulaba momentos que marcaron a la ONU, como la firma de la Carta de San Francisco o la primera reunión de la Asamblea General.</p>
<p>Fuente: <a href="https://conecta.tec.mx/es/noticias/estado-de-mexico/educacion/de-prepatec-esmeralda-a-primer-mun-internacional-respaldado-por-la-ONU" rel="noopener" target="_blank">Conecta, Tecnológico de Monterrey, 7 de octubre de 2020</a>.</p>"""),
}

def noticias():
    POSTS.update(_POSTS_MD)
    css="""body{background:#fff} .wrap{max-width:900px} .site-header .wrap,.site-footer .wrap{max-width:var(--maxw)} .post{padding-block:48px} .post h1{font-size:clamp(44px,7vw,96px);margin:10px 0 18px} .post .meta{display:flex;gap:14px;align-items:center;font-size:12px;color:var(--muted)} .post figure{margin:28px 0} .post .duo{aspect-ratio:16/9} .post .duo img{width:100%;height:100%;object-fit:cover} .post figcaption{font-size:12px;color:var(--muted);margin-top:8px}
.post .body{font-size:18px;line-height:1.7;max-width:68ch} .post .body h2{font-size:34px;margin:36px 0 10px} .list{display:grid;gap:22px;padding-block:48px} .list article{border-top:1px solid var(--line);padding-top:18px} .list h3{font-size:26px;font-weight:600;line-height:1.2} .list p{color:var(--muted)} .list a{text-decoration:none}"""
    (ROOT/'noticias').mkdir(exist_ok=True); (ROOT/'noticias'/'style.css').write_text(css,encoding='utf-8')
    nav_home='<header class="site-header"><div class="wrap"><a class="brand" href="../p1-editorial/" aria-label="ESMUN, inicio">'+esmun_logo_svg(kind='horizontal',mode='header')+'</a><nav class="site-nav"><a href="../p1-editorial/#quienes">Quiénes somos</a><a href="../p1-editorial/#munmx">MUNMX 2027</a><a href="./">Noticias</a><a href="../p1-editorial/#contacto">Contacto</a></nav></div></header>'
    idx=head('Noticias · ESMUN PrepaTec Esmeralda','Convocatorias, resultados y novedades del grupo de Modelo de Naciones Unidas de la PrepaTec Esmeralda y de MUNMX Esmeralda.','style.css')+nav_home+'<main class="wrap"><section class="list"><p class="eyebrow">Noticias</p><h1 class="display" style="font-size:clamp(56px,9vw,120px)">Entre sesiones</h1>'
    for dd,tg,tt,ds,ph,slug in C['noticias']:
        idx+=f'<article><a href="{slug}.html"><div style="display:flex;gap:12px;font-size:12px;color:var(--muted)"><time datetime="{dd}">{dd}</time><span class="pill">{tg}</span></div><h3 style="margin-top:8px">{tt}</h3><p>{ds}</p></a></article>'
    idx+='</section></main>'+footer('dark').replace('href="../noticias/"','href="./"')+scripts('..')
    (ROOT/'noticias'/'index.html').write_text(idx,encoding='utf-8')
    for d,tag,title,desc,photo,slug in C['noticias']:
        P=POSTS[slug]
        ld=json.dumps({"@context":"https://schema.org","@type":"NewsArticle","headline":title,"datePublished":d,"dateModified":d,"author":{"@type":"Organization","name":"ESMUN"},"publisher":{"@type":"Organization","name":"ESMUN · PrepaTec Esmeralda"},"image":[C.get("dominio","https://esmun.github.io")+f"/assets/img/{photo}"],"description":desc,"inLanguage":"es-MX"},ensure_ascii=False)
        post=head(title+' · ESMUN',desc,'style.css',extra=f'<script type="application/ld+json">{ld}</script><meta property="article:published_time" content="{d}">')+nav_home+f"""<main class="wrap"><article class="post"><div class="meta"><a href="./">← Noticias</a><time datetime="{d}">{d}</time><span class="pill">{tag}</span></div><h1 class="display">{title}</h1><p class="lead">{desc}</p>
<figure><div class="duo"><img src="../assets/img/{photo}" alt="{P['alt']}"></div><figcaption>{P['cap']}</figcaption></figure>
<div class="body">{P['body']}</div></article></main>"""+footer('dark').replace('href="../noticias/"','href="./"')+scripts('..')
        (ROOT/'noticias'/f'{slug}.html').write_text(post,encoding='utf-8')
    # plantilla para nuevas entradas (no se enlaza ni se indexa)
    tpl=head('Plantilla de artículo · ESMUN','Plantilla.','style.css',extra='<meta name="robots" content="noindex">')+nav_home+f"""<main class="wrap"><article class="post"><div class="meta"><a href="./">← Noticias</a><time datetime="2027-01-01">2027-01-01</time><span class="pill">Etiqueta</span></div><h1 class="display">Título de la noticia</h1><p class="lead">Entradilla de una o dos frases.</p>
<figure><div class="duo"><img src="../assets/img/real/edificio_banner.jpg" alt="Describe la imagen"></div><figcaption>Pie de foto. Foto: autor.</figcaption></figure>
<div class="body"><p>Primer párrafo.</p><h2 class="display">Subtítulo</h2><p>Texto.</p><p class="ai-note" style="margin-top:36px">Plantilla: copiar este archivo, cambiar título, fecha, etiqueta, imagen y texto; añadir la entrada a index.html, a la lista de noticias de la portada y al sitemap.xml.</p></div></article></main>"""+footer('dark').replace('href="../noticias/"','href="./"')+scripts('..')
    (ROOT/'noticias'/'plantilla-articulo.html').write_text(tpl,encoding='utf-8')

# ======================================================================= Índice selector
EXTRA={'p6-globo':dict(title='Globo',desc='La arriesgada: un globo terráqueo 3D en los colores de la identidad que gira, se mueve y cambia de color con el scroll; sedes de los comités conectadas por arcos desde la PrepaTec Esmeralda. Fondo que pasa de papel a tinta. Requiere WebGL (con alternativa estática).',tag='Nueva')}
def index(shots):
    cards=''
    items=list(PROPS.items())+[(k,v) for k,v in EXTRA.items() if (ROOT/k/'index.html').exists()]
    for k,p in items:
        tag=f' <b class="tag">{p["tag"]}</b>' if p.get('tag') else ''
        cards+=f'<a class="prop reveal" href="{k}/"><img src="preview/{k}.jpg" alt="Vista previa de la propuesta {p["title"]}" loading="lazy"><div><span class="eyebrow">{k[:2].upper()}{tag}</span><h2 class="display">{p["title"]}</h2><p>{p["desc"]}</p></div></a>'
    css=""".props{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:28px;padding-block:40px 80px} .prop{text-decoration:none;display:grid;gap:14px;border:1px solid var(--line);padding:14px;border-radius:4px;background:#fff;transition:transform .3s var(--ease),box-shadow .3s} .prop:hover{transform:translateY(-4px);box-shadow:0 16px 40px rgba(28,32,48,.12)} .prop img{width:100%;aspect-ratio:4/3;object-fit:cover;object-position:top;border:1px solid var(--line)} .prop h2{font-size:44px;margin:4px 0 8px} .prop p{margin:0;font-size:14px;color:var(--muted)}
.top{padding-block:64px 20px} .top h1{font-size:clamp(56px,9vw,130px)} .tag{display:inline-block;margin-left:8px;padding:3px 8px;background:var(--azul);color:#fff;font-size:10px;letter-spacing:.14em;border-radius:2px;vertical-align:middle}"""
    (ROOT/'index.css').write_text(css,encoding='utf-8')
    h=head('Propuestas de sitio web · ESMUN','Seis direcciones de arte para el sitio de ESMUN con sección MUNMX 2027.','index.css',path_prefix='.')
    h=h.replace('href="./assets/css/base.css"','href="assets/css/base.css"')
    body=h+f"""<header class="site-header"><div class="wrap"><a class="brand" href="./">{esmun_logo_svg(kind='horizontal',mode='header')}</a><nav class="site-nav"><a href="noticias/">Noticias (blog)</a><a href="README.html">Cómo publicar</a></nav></div></header>
<main class="wrap"><section class="top"><p class="eyebrow">ESMUN · sitio web · ronda 1</p><h1 class="display">Seis<br>propuestas</h1><p class="lead" style="margin-top:18px">Mismo contenido, misma cabecera y mismo pie; cinco direcciones de arte más una arriesgada con globo terráqueo 3D. En todas, el logotipo es normal sobre fondo claro y, al entrar en una sección oscura, las ventanas del edificio se encienden una a una hasta quedar encendidas. Prueba a hacer scroll en cada una y mira también la cabecera.</p></section>
<section class="props">{cards}</section></main>"""+footer('dark').replace('href="../noticias/"','href="noticias/"')+'<script src="assets/js/esmun.js" defer></script></body></html>'
    (ROOT/'index.html').write_text(body,encoding='utf-8')

README="""# Sitio ESMUN · propuestas (ronda 1)

Estático: HTML + CSS + JS sin dependencias. Listo para GitHub Pages.

## Estructura
- `index.html` — selector de propuestas (solo para esta ronda; al elegir una, su carpeta pasa a ser la raíz).
- `p1-editorial/ … p5-inmersivo/` — cinco portadas con las secciones Inicio, Quiénes somos, MUNMX 2027, Noticias y Contacto.
- `p6-globo/` — propuesta arriesgada: globo terráqueo 3D (Three.js, `assets/js/three.min.js` + `globe.js` + `land.js`) que reacciona al scroll y al cursor. Si el navegador no tiene WebGL, muestra `assets/img/globo_fallback.svg`. Sedes y keyframes por sección se editan al inicio de `globe.js` (`CITIES`, `KF`).
- `noticias/` — blog: listado y un artículo de ejemplo con datos estructurados `NewsArticle` (SEO).
- `assets/` — fuentes (woff2), fotografías provisionales, logotipos SVG, `css/base.css` (tokens y componentes), `js/esmun.js` (logotipo reactivo, revelados, cabecera, formulario, scrollytelling).

## Publicar en GitHub Pages
1. Crea un repositorio (por ejemplo `esmun.github.io` en una cuenta/organización `esmun`, o `esmun-web` en la tuya).
2. Copia el contenido de la propuesta elegida a la raíz (`index.html` + `assets/` + `noticias/`) y ajusta las rutas `../assets` → `assets`.
3. Settings → Pages → Deploy from branch → `main` / root. En unos minutos queda en `https://<usuario>.github.io/<repo>/`.
4. Dominio propio (opcional): añade un archivo `CNAME` con el dominio y un registro CNAME en el DNS apuntando a `<usuario>.github.io`.

## Formulario sin backend
El formulario usa `data-endpoint`. Crea un formulario en Formspree (gratis hasta 50 envíos/mes) y sustituye `https://formspree.io/f/TU_ID`. Alternativas: Getform, Web3Forms o Netlify Forms si se publica en Netlify.

## SEO
- Títulos y descripciones por página, Open Graph, `theme-color`, favicon.
- JSON-LD `Organization` en todas las páginas y `NewsArticle` en los artículos.
- HTML semántico (`header`, `main`, `section`, `article`, `time`), un solo `h1` por página, imágenes con `alt` y `loading="lazy"`.
- Pendiente al publicar: `sitemap.xml`, `robots.txt`, URL canónica real, y sustituir las fotografías generadas por IA por fotografías propias.

## El logotipo reactivo
`assets/js/esmun.js` busca `.esmun-logo` dentro de secciones `[data-theme="dark"]`: al entrar en pantalla enciende las 12 ventanas en secuencia y las deja encendidas. El logotipo de la cabecera sigue la sección que tiene debajo: sobre oscuro se enciende progresivamente con el scroll; sobre claro vuelve al estado normal. Los colores salen de variables CSS (`--lg-main`, `--lg-win`, `--lg-lit`).
"""

def build():
    for k,p in PROPS.items():
        d=ROOT/k; d.mkdir(exist_ok=True)
        (d/'style.css').write_text(p['css'],encoding='utf-8')
        html_=head(f'ESMUN · Modelo de Naciones Unidas PrepaTec Esmeralda — {p["title"]}', 'Grupo estudiantil de Modelo de Naciones Unidas de la PrepaTec Esmeralda. Debates, liderazgo e impacto. Organizador de MUNMX Esmeralda 2027.','style.css')+p['body']()+scripts('..')
        (d/'index.html').write_text(html_,encoding='utf-8')
    noticias()
    (ROOT/'README.md').write_text(README,encoding='utf-8')

    # README.html sencillo
    import re
    body=README
    body=re.sub(r'^### (.*)$',r'<h3>\1</h3>',body,flags=re.M); body=re.sub(r'^## (.*)$',r'<h2>\1</h2>',body,flags=re.M); body=re.sub(r'^# (.*)$',r'<h1 class="display" style="font-size:72px">\1</h1>',body,flags=re.M)
    body=re.sub(r'`([^`]+)`',r'<code>\1</code>',body); body=re.sub(r'^- (.*)$',r'<li>\1</li>',body,flags=re.M); body=re.sub(r'^(\d+)\. (.*)$',r'<li>\2</li>',body,flags=re.M)
    body=re.sub(r'(<li>.*</li>\n?)+',lambda m:'<ul>'+m.group(0)+'</ul>',body); body=re.sub(r'\n\n([^<\n][^\n]+)',r'\n\n<p>\1</p>',body)
    (ROOT/'README.html').write_text(head('Cómo publicar · ESMUN web','Instrucciones para publicar el sitio en GitHub Pages.','index.css',path_prefix='.').replace('href="./assets/css/base.css"','href="assets/css/base.css"')+'<main class="wrap" style="max-width:820px;padding-block:48px;line-height:1.7">'+body+'</main></body></html>',encoding='utf-8')
    print('built',list(PROPS))

if __name__=='__main__':
    build()
    if 'index' in sys.argv: index(None)
