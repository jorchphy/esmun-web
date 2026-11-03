# -*- coding: utf-8 -*-
"""Documentos con membrete MUNMX Esmeralda 2027: membrete en blanco (DOCX), ejemplo de position paper y de resolución (PDF + DOCX).
PDF: HTML con las fuentes de la identidad renderizado con Playwright. DOCX: python-docx con cabecera y pie de página.
Uso: python3 tools/make_docs.py   → src/assets/docs/"""
import pathlib, base64, sys
from playwright.sync_api import sync_playwright
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'src' / 'assets' / 'docs'; OUT.mkdir(parents=True, exist_ok=True)
MARKS = pathlib.Path('/home/claude/munmx27/marks')
FONTS = ROOT / 'src' / 'assets' / 'fonts'
COFIRMA = MARKS / 'Cofirma_ESMUN_MUNMX_2027_color.png'
AZUL, TINTA, GRIS = '#253C82', '#1C2030', '#5B6075'

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def font(name): return f"url(data:font/woff2;base64,{b64(FONTS / name)}) format('woff2')"

CSS = f"""
@font-face{{font-family:'League Gothic';src:{font('league-gothic-400.woff2')}}}
@font-face{{font-family:Montserrat;font-weight:400;src:{font('montserrat-400.woff2')}}}
@font-face{{font-family:Montserrat;font-weight:600;src:{font('montserrat-600.woff2')}}}
@font-face{{font-family:Montserrat;font-weight:700;src:{font('montserrat-700.woff2')}}}
@page{{size:Letter;margin:0}}
body{{margin:0;font:11pt/1.5 Montserrat,sans-serif;color:{TINTA}}}
.page{{width:216mm;min-height:279mm;padding:18mm 22mm 24mm;box-sizing:border-box;position:relative;page-break-after:always}}
.head{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid {AZUL};padding-bottom:6mm;margin-bottom:9mm}}
.head img{{height:16mm}} .head .r{{text-align:right;font-size:8.5pt;letter-spacing:.14em;text-transform:uppercase;color:{GRIS};line-height:1.5}}
.foot{{position:absolute;left:22mm;right:22mm;bottom:12mm;display:flex;justify-content:space-between;font-size:8pt;color:{GRIS};letter-spacing:.06em;border-top:1px solid #DADCE5;padding-top:3mm}}
h1{{font:400 30pt/1 'League Gothic';text-transform:uppercase;margin:0 0 2mm;color:{TINTA}}}
h2{{font:700 10pt/1.4 Montserrat;letter-spacing:.14em;text-transform:uppercase;color:{AZUL};margin:7mm 0 2mm}}
.meta{{display:grid;grid-template-columns:auto 1fr;gap:1mm 6mm;font-size:10pt;margin:0 0 4mm}} .meta b{{font-size:8.5pt;letter-spacing:.12em;text-transform:uppercase;color:{GRIS};padding-top:1pt}}
p{{margin:0 0 3mm;text-align:justify}} .tag{{display:inline-block;background:{AZUL};color:#fff;font-size:8pt;letter-spacing:.14em;text-transform:uppercase;padding:2px 7px;border-radius:2px;margin-bottom:5mm}}
ol.op{{padding-left:7mm}} ol.op li{{margin-bottom:2mm}} .pre p{{margin-bottom:2mm}} em{{font-style:italic}}
.note{{font-size:8.5pt;color:{GRIS};border-left:3px solid #C8962E;padding-left:4mm;margin-top:6mm}}
"""

def page(title_block, body, foot_l='MUNMX Esmeralda 2027 · 11, 12 y 13 de marzo · PrepaTec Esmeralda', foot_r='esmun.com.mx · @esmunmx'):
    return f"""<div class="page"><div class="head"><img src="data:image/png;base64,{b64(COFIRMA)}" alt="ESMUN · MUNMX Esmeralda 2027"><div class="r">Modelo de Naciones Unidas<br>PrepaTec Esmeralda · 2027</div></div>{title_block}{body}<div class="foot"><span>{foot_l}</span><span>{foot_r}</span></div></div>"""

# ---------------------------------------------------------------- contenido
PP = dict(
 comite='UNICEF · Fondo de las Naciones Unidas para la Infancia', pais='Estados Unidos Mexicanos', delegado='Nombre Apellido', escuela='PrepaTec Esmeralda',
 topico='Acceso a la educación de niñas, niños y adolescentes en contextos de desplazamiento forzado',
 secciones=[
  ('I. Antecedentes', 'Millones de niñas, niños y adolescentes en el mundo viven desplazados por conflictos, violencia o desastres, y una parte importante de ellos queda fuera de la escuela durante años. La Convención sobre los Derechos del Niño (1989) reconoce el derecho de toda persona menor de 18 años a la educación, sin distinción por su situación migratoria. UNICEF, con la Junta Ejecutiva y en coordinación con ACNUR, apoya programas de educación en emergencias, pero el financiamiento sigue por debajo de las necesidades.'),
  ('II. Postura del país', 'México ratificó la Convención sobre los Derechos del Niño en 1990 y reconoce en su Constitución el derecho a la educación. Como país de origen, tránsito, destino y retorno de personas migrantes, México sostiene que la educación no puede condicionarse a documentos de identidad o residencia y que la respuesta debe ser regional: ningún país de la ruta migratoria puede resolver el problema solo.'),
  ('III. Acciones previas', 'La delegación destaca las medidas que permiten inscribir a estudiantes sin documentación completa, el reconocimiento de estudios cursados en otros países y los programas de UNICEF México con autoridades estatales en entidades de alta movilidad. Reconoce, al mismo tiempo, que la cobertura es desigual y que faltan datos para saber cuántos estudiantes desplazados quedan fuera del sistema.'),
  ('IV. Propuestas', 'La delegación propone: (1) un fondo de respuesta rápida de UNICEF para educación en emergencias con desembolso en menos de 30 días; (2) un mecanismo regional de reconocimiento de estudios entre países de la ruta migratoria; (3) formación de docentes en atención a estudiantes desplazados, con materiales en lenguas indígenas y en español; y (4) un sistema común de registro que permita seguir la trayectoria escolar de cada estudiante entre países, con protección de datos.'),
 ])

RES = dict(
 comite='Asamblea General', topico='Fortalecimiento de la cooperación internacional para el acceso a la educación de niñas, niños y adolescentes desplazados',
 patrocinadores='México, Colombia, España, Kenia', firmantes='Argentina, Canadá, Chile, Costa Rica, Francia, Guatemala, Jordania, Noruega, Perú, Uruguay',
 pre=['<em>Reafirmando</em> la Convención sobre los Derechos del Niño, en particular sus artículos 28 y 29 sobre el derecho a la educación,',
      '<em>Recordando</em> la resolución 70/1 de la Asamblea General, "Transformar nuestro mundo: la Agenda 2030 para el Desarrollo Sostenible", y su Objetivo 4,',
      '<em>Profundamente preocupada</em> por el número de niñas, niños y adolescentes desplazados que permanecen fuera de la escuela durante periodos prolongados,',
      '<em>Reconociendo</em> la labor de UNICEF, ACNUR y las organizaciones de la sociedad civil en la educación en situaciones de emergencia,',
      '<em>Tomando nota</em> de que los países de origen, tránsito y destino comparten la responsabilidad de garantizar la continuidad educativa,'],
 op=['<em>Insta</em> a los Estados miembros a garantizar la inscripción escolar de toda persona menor de 18 años con independencia de su situación migratoria o de la documentación con que cuente;',
     '<em>Alienta</em> a los Estados a establecer mecanismos regionales de reconocimiento de estudios y de equivalencias, con plazos de respuesta no mayores a 60 días;',
     '<em>Solicita</em> a UNICEF que, en coordinación con ACNUR, presente a la Asamblea General un informe anual sobre la cobertura educativa de la población desplazada, desglosado por edad, sexo y país;',
     '<em>Invita</em> a los Estados donantes y a las instituciones financieras internacionales a destinar recursos adicionales a la educación en emergencias, con prioridad a los países que acogen a más personas desplazadas;',
     '<em>Recomienda</em> la formación de docentes en atención a estudiantes desplazados, incluida la enseñanza en lenguas maternas cuando sea posible;',
     '<em>Decide</em> seguir ocupándose de la cuestión.'])

def html_pp():
    meta = f"""<div class="meta"><b>Comité</b><span>{PP['comite']}</span><b>Delegación</b><span>{PP['pais']}</span><b>Delegado</b><span>{PP['delegado']} · {PP['escuela']}</span><b>Tópico</b><span>{PP['topico']}</span></div>"""
    body = ''.join(f'<h2>{h}</h2><p>{t}</p>' for h, t in PP['secciones'])
    body += '<div class="note"><b>Ejemplo.</b> Un papel de posición ocupa una página: antecedentes del tema, postura oficial del país, lo que ya ha hecho y lo que propone. Se escribe en tercera persona ("la delegación de…"), con datos verificables y sin opiniones personales. Se entrega antes de la primera sesión.</div>'
    return page('<span class="tag">Ejemplo</span><h1>Papel de posición</h1>' + meta, body)

def html_res():
    meta = f"""<div class="meta"><b>Comité</b><span>{RES['comite']}</span><b>Tópico</b><span>{RES['topico']}</span><b>Patrocinadores</b><span>{RES['patrocinadores']}</span><b>Firmantes</b><span>{RES['firmantes']}</span></div>"""
    body = '<p><b>La Asamblea General,</b></p><div class="pre">' + ''.join(f'<p>{x}</p>' for x in RES['pre']) + '</div><ol class="op">' + ''.join(f'<li>{x}</li>' for x in RES['op']) + '</ol>'
    body += '<div class="note"><b>Ejemplo.</b> Una resolución tiene dos partes. Las cláusulas preambulares (en cursiva, terminan en coma) explican por qué se actúa; las operativas (numeradas, terminan en punto y coma, la última en punto) dicen qué se hace. Los patrocinadores la redactan; los firmantes solo piden que se debata. Se presenta a la mesa para su aprobación antes de leerse en el pleno.</div>'
    return page('<span class="tag">Ejemplo</span><h1>Proyecto de resolución</h1>' + meta, body)

def html_carta():
    body = '<p>Estimadas y estimados delegados:</p><p>[Texto de la carta de bienvenida de la Presidencia y la Vicepresidencia. Se sustituye este párrafo por el texto que envíe la mesa.]</p><p>[Segundo párrafo.]</p><p style="margin-top:10mm">Atentamente,</p><p style="margin-top:12mm"><b>Nombre Apellido</b><br><span style="font-size:9pt;color:#5B6075;letter-spacing:.1em;text-transform:uppercase">Presidencia · MUNMX Esmeralda 2027</span></p><p style="margin-top:8mm"><b>Nombre Apellido</b><br><span style="font-size:9pt;color:#5B6075;letter-spacing:.1em;text-transform:uppercase">Vicepresidencia · MUNMX Esmeralda 2027</span></p>'
    return page('<h1>Carta de bienvenida</h1><p style="color:#5B6075;font-size:9.5pt">Atizapán de Zaragoza, Estado de México, a [día] de [mes] de 2027</p>', body)

def render_pdf(html_, out):
    doc = f"<!doctype html><html lang='es'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html_}</body></html>"
    tmp = OUT / (out.stem + '.html'); tmp.write_text(doc, encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.goto(tmp.as_uri()); pg.wait_for_timeout(600)
        pg.pdf(path=str(out), format='Letter', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'}); b.close()
    tmp.unlink(); print('pdf', out.name)

# ---------------------------------------------------------------- DOCX
def docx_base(title):
    d = Document(); s = d.sections[0]; s.page_height, s.page_width = Mm(279), Mm(216); s.left_margin = s.right_margin = Mm(22); s.top_margin = Mm(16); s.bottom_margin = Mm(20)
    st = d.styles['Normal']; st.font.name = 'Montserrat'; st.font.size = Pt(11); st.font.color.rgb = RGBColor(0x1C, 0x20, 0x30)
    hp = s.header.paragraphs[0]; hp.add_run().add_picture(str(COFIRMA), height=Mm(15)); hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hr = s.header.add_paragraph(); r = hr.add_run('Modelo de Naciones Unidas · PrepaTec Esmeralda · 2027'); r.font.size = Pt(8); r.font.color.rgb = RGBColor(0x5B, 0x60, 0x75); hr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp = s.footer.paragraphs[0]; r = fp.add_run('MUNMX Esmeralda 2027 · 11, 12 y 13 de marzo · PrepaTec Esmeralda · esmun.com.mx · @esmunmx'); r.font.size = Pt(8); r.font.color.rgb = RGBColor(0x5B, 0x60, 0x75)
    h = d.add_paragraph(); r = h.add_run(title.upper()); r.font.name = 'League Gothic'; r.font.size = Pt(28); r.font.color.rgb = RGBColor(0x1C, 0x20, 0x30)
    return d

def meta_table(d, rows):
    t = d.add_table(rows=0, cols=2); t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for k, v in rows:
        c = t.add_row().cells; r = c[0].paragraphs[0].add_run(k.upper()); r.font.size = Pt(8); r.font.bold = True; r.font.color.rgb = RGBColor(0x5B, 0x60, 0x75); c[1].paragraphs[0].add_run(v)
    d.add_paragraph()

def h2(d, txt):
    p = d.add_paragraph(); r = p.add_run(txt.upper()); r.font.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(0x25, 0x3C, 0x82)

def strip(x): return x.replace('<em>', '').replace('</em>', '')

def build_docx():
    d = docx_base('Carta de bienvenida'); d.add_paragraph('Atizapán de Zaragoza, Estado de México, a [día] de [mes] de 2027'); d.add_paragraph(); d.add_paragraph('Estimadas y estimados delegados:'); d.add_paragraph('[Texto de la carta de bienvenida de la Presidencia y la Vicepresidencia.]'); d.add_paragraph('[Segundo párrafo.]'); d.add_paragraph(); d.add_paragraph('Atentamente,'); d.add_paragraph(); p = d.add_paragraph(); p.add_run('Nombre Apellido').bold = True; d.add_paragraph('Presidencia · MUNMX Esmeralda 2027'); d.add_paragraph(); p = d.add_paragraph(); p.add_run('Nombre Apellido').bold = True; d.add_paragraph('Vicepresidencia · MUNMX Esmeralda 2027')
    d.save(OUT / 'Membrete_MUNMX_2027_carta.docx')
    d = docx_base('Papel de posición (ejemplo)'); meta_table(d, [('Comité', PP['comite']), ('Delegación', PP['pais']), ('Delegado', f"{PP['delegado']} · {PP['escuela']}"), ('Tópico', PP['topico'])])
    for h, t in PP['secciones']: h2(d, h); d.add_paragraph(t)
    d.save(OUT / 'Ejemplo_position_paper.docx')
    d = docx_base('Proyecto de resolución (ejemplo)'); meta_table(d, [('Comité', RES['comite']), ('Tópico', RES['topico']), ('Patrocinadores', RES['patrocinadores']), ('Firmantes', RES['firmantes'])])
    p = d.add_paragraph(); p.add_run('La Asamblea General,').bold = True
    for x in RES['pre']: p = d.add_paragraph(); first, rest = x.split('</em>', 1); r = p.add_run(first.replace('<em>', '')); r.italic = True; p.add_run(rest)
    for i, x in enumerate(RES['op'], 1): p = d.add_paragraph(); p.add_run(f'{i}. '); first, rest = x.split('</em>', 1); r = p.add_run(first.replace('<em>', '')); r.italic = True; p.add_run(rest)
    d.save(OUT / 'Ejemplo_resolucion.docx'); print('docx ok')

if __name__ == '__main__':
    render_pdf(html_pp(), OUT / 'Ejemplo_position_paper.pdf')
    render_pdf(html_res(), OUT / 'Ejemplo_resolucion.pdf')
    render_pdf(html_carta(), OUT / 'Membrete_MUNMX_2027_carta.pdf')
    build_docx()
