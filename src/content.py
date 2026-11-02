# -*- coding: utf-8 -*-
"""Contenido editable sin tocar Python.
- content/site.json      textos generales (intro, cifras, qué hacemos, línea de tiempo, comités, contacto)
- content/comites.json   fichas de los comités (sede, colores, textos)
- content/staff.json     coaches y asesores
- content/noticias/*.md  una noticia por archivo (cabecera entre --- y cuerpo en Markdown sencillo)
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
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\[(.+?)\]\((.+?)\)', lambda m: f'<a href="{m.group(2)}"' + (' rel="noopener" target="_blank"' if m.group(2).startswith('http') else '') + f'>{m.group(1)}</a>', t)
    return t

def md_to_html(md):
    out = []
    for block in re.split(r'\n\s*\n', md.strip()):
        b = block.strip()
        if not b: continue
        if b.startswith('## '): out.append(f'<h2 class="display">{md_inline(b[3:])}</h2>')
        elif b.startswith('- '): out.append('<ul>' + ''.join(f'<li>{md_inline(x[2:])}</li>' for x in b.split('\n') if x.startswith('- ')) + '</ul>')
        else: out.append(f'<p>{md_inline(b.replace(chr(10), " "))}</p>')
    return '\n'.join(out)

def read_post(path):
    txt = pathlib.Path(path).read_text(encoding='utf-8')
    m = re.match(r'---\s*\n(.*?)\n---\s*\n(.*)$', txt, re.S)
    if not m: raise ValueError(f'{path}: falta la cabecera entre ---')
    meta = {}
    for line in m.group(1).split('\n'):
        if ':' in line: k, v = line.split(':', 1); meta[k.strip()] = v.strip().strip('"')
    meta['body'] = md_to_html(m.group(2)); meta['slug'] = pathlib.Path(path).stem
    return meta

def load_content(cdir, C):
    cdir = pathlib.Path(cdir)
    site = load_json(cdir / 'site.json', None)
    if site:
        for k, v in site.items(): C[k] = v
    posts = {}
    nd = cdir / 'noticias'
    if nd.exists():
        items = []
        for f in sorted(nd.glob('*.md')):
            p = read_post(f)
            items.append((p['fecha'], p['etiqueta'], p['titulo'], p['resumen'], p['foto'], p['slug']))
            posts[p['slug']] = dict(alt=p.get('alt', ''), cap=p.get('pie', ''), body=p['body'])
        items.sort(key=lambda x: x[0], reverse=True)
        C['noticias'] = items
    return C, posts
