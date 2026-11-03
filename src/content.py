# -*- coding: utf-8 -*-
"""Contenido editable sin tocar Python (y desde el panel /admin/, Sveltia CMS).
- content/site.json      textos generales, cifras, qué hacemos, línea de tiempo, descargas, patrocinios, ajustes
- content/comites.json   lista de comités (sigla, nombre, nivel, idioma, color, sede, textos, tópico, mesa)
- content/staff.json     coaches y asesores
- content/noticias/*.md  una noticia por archivo (cabecera YAML entre --- y cuerpo en Markdown sencillo)
Si un archivo no existe, se usan los valores por defecto que traen los generadores."""
import json, pathlib, re, html

def load_json(path, default):
    path = pathlib.Path(path)
    if not path.exists(): return default
    data = json.loads(path.read_text(encoding='utf-8'))
    # listas de tuplas en los generadores → listas de listas en JSON
    return data

def md_inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'!\[(.*?)\]\((.+?)\)', lambda m: f'<img src="{m.group(2) if m.group(2).startswith(("http", "/", "../")) else "../assets/img/" + m.group(2)}" alt="{m.group(1)}" loading="lazy">', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])', r'<i>\1</i>', t)
    t = re.sub(r'\[(.+?)\]\((.+?)\)', lambda m: f'<a href="{m.group(2)}"' + (' rel="noopener" target="_blank"' if m.group(2).startswith('http') else '') + f'>{m.group(1)}</a>', t)
    return t

def md_to_html(md):
    out = []
    for block in re.split(r'\n\s*\n', md.strip()):
        b = block.strip()
        if not b: continue
        if b.startswith('## '): out.append(f'<h2 class="display">{md_inline(b[3:])}</h2>')
        elif b.startswith('### '): out.append(f'<h3>{md_inline(b[4:])}</h3>')
        elif b.startswith('# '): out.append(f'<h2 class="display">{md_inline(b[2:])}</h2>')
        elif b.startswith('> '): out.append('<blockquote>' + md_inline(' '.join(x[2:] for x in b.split(chr(10)))) + '</blockquote>')
        elif b.startswith('- '): out.append('<ul>' + ''.join(f'<li>{md_inline(x[2:])}</li>' for x in b.split('\n') if x.startswith('- ')) + '</ul>')
        else: out.append(f'<p>{md_inline(b.replace(chr(10), " "))}</p>')
    return '\n'.join(out)

def parse_front_matter(txt):
    """YAML sencillo: clave: valor, comillas simples o dobles, y bloques | o > con líneas indentadas (lo que escribe el panel)."""
    meta = {}; lines = txt.split('\n'); i = 0
    while i < len(lines):
        line = lines[i]; i += 1
        if not line.strip() or line.startswith('#') or line.startswith(' ') or ':' not in line: continue
        k, v = line.split(':', 1); k = k.strip(); v = v.strip()
        if v in ('|', '|-', '>', '>-', '|+', '>+'):
            block = []
            while i < len(lines) and (lines[i].startswith(' ') or not lines[i].strip()):
                block.append(lines[i].strip()); i += 1
            while block and not block[-1]: block.pop()
            meta[k] = '\n'.join(block) if v.startswith('|') else ' '.join(x for x in block if x)
            continue
        if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
            v = v[1:-1]; v = v.replace('\\"', '"') if line.strip().endswith('"') else v.replace("''", "'")
        meta[k] = v
    return meta

def read_post(path):
    txt = pathlib.Path(path).read_text(encoding='utf-8')
    m = re.match(r'---\s*\n(.*?)\n---\s*\n(.*)$', txt, re.S)
    if not m: raise ValueError(f'{path}: falta la cabecera entre ---')
    meta = parse_front_matter(m.group(1))
    meta['borrador'] = str(meta.get('borrador', '')).lower() in ('true', 'sí', 'si', 'yes', '1')
    meta['body'] = md_to_html(m.group(2)); meta['slug'] = pathlib.Path(path).stem
    return meta

def load_content(cdir, C):
    cdir = pathlib.Path(cdir)
    site = load_json(cdir / 'site.json', None)
    if site:
        for k, v in site.items(): C[k] = v
    # objetos del panel → tuplas que esperan los generadores
    if C.get('stats') and isinstance(C['stats'][0], dict): C['stats'] = [(x['cifra'], x['titulo'], x['texto']) for x in C['stats']]
    if C.get('que') and isinstance(C['que'][0], dict): C['que'] = [(x['titulo'], x['texto']) for x in C['que']]
    if C.get('timeline') and isinstance(C['timeline'][0], dict): C['timeline'] = [(x['anio'], x['texto']) for x in C['timeline']]
    com = load_comites(cdir / 'comites.json')
    if com: C['comites'] = [(c['sigla'], c['nombre'], nivel_txt(c), c['color']) for c in com]
    posts = {}
    nd = cdir / 'noticias'
    if nd.exists():
        items = []
        for f in sorted(nd.glob('*.md')):
            p = read_post(f)
            if p.get('borrador'): continue
            items.append((p['fecha'], p['etiqueta'], p['titulo'], p['resumen'], p['foto'], p['slug']))
            posts[p['slug']] = dict(alt=p.get('alt', ''), cap=p.get('pie', ''), body=p['body'])
        items.sort(key=lambda x: x[0], reverse=True)
        C['noticias'] = items
    return C, posts

# ---------------------------------------------------------------- comités
CITY_LON = {'Nueva York · ONU': -74, 'Ginebra': 6, 'Viena · OIEA': 16, 'Bruselas · OTAN': 4, 'Washington': -77, 'Ciudad de México · Senado': -99, 'Nairobi': 37, 'Tokio': 140, 'Buenos Aires': -58, 'Nueva Delhi': 77}

def nivel_txt(c):
    n = (c.get('nivel') or 'Por confirmar').strip(); i = (c.get('idioma') or '').strip()
    n = 'Nivel por confirmar' if n.lower() == 'por confirmar' else n
    return f'{n} · {i}' if i else n

def mix(hexcol, with_, t):
    h = hexcol.lstrip('#'); w = with_.lstrip('#')
    a = [int(h[i:i+2], 16) for i in (0, 2, 4)]; b = [int(w[i:i+2], 16) for i in (0, 2, 4)]
    return '#%02X%02X%02X' % tuple(round(x + (y - x) * t) for x, y in zip(a, b))

def load_comites(path):
    """Lista de comités del panel. Devuelve la lista (o None si no existe el archivo)."""
    data = load_json(path, None)
    if not data: return None
    if isinstance(data, dict): return None   # formato antiguo (dict por sigla): lo manejan los generadores
    return data

def comites_dict(path):
    """Dict por sigla con la forma que usan los generadores (sede, focus, lon, bg, dots, light, txt, facultades, tema, mesa, delegaciones)."""
    data = load_comites(path)
    if not data: return None
    out = {}
    for c in data:
        light = bool(c.get('claro')); bg = c.get('color', '#253C82')
        out[c['sigla']] = dict(sede=c.get('sede', ''), focus=c.get('foco', 'Nueva York · ONU'), lon=CITY_LON.get(c.get('foco'), -74), bg=bg,
                               dots=mix(bg, '#2A2210' if light else '#FFFFFF', 0.72), light=light,
                               txt=[c.get('que', ''), c.get('trata', '')], facultades=c.get('facultades', ''), tema=c.get('tema') or 'Por confirmar',
                               mesa=c.get('mesa') or [], delegaciones=c.get('delegaciones') or [])
    return out
