# -*- coding: utf-8 -*-
"""Logotipo ESMUN como SVG inline (ventanas individuales para que reaccionen al fondo).
Versión portable: lee los SVG precalculados de logo_cache.json. Para regenerar la caché hace falta la cadena de fuentes (99 Archivos fuente/v3)."""
import json, pathlib
_CACHE = json.loads((pathlib.Path(__file__).parent / 'logo_cache.json').read_text(encoding='utf-8'))
def esmun_logo_svg(cls='esmun-logo', kind='principal', pad=0, mode='auto'):
    key = f'{kind}|{mode}|{pad}'
    if key not in _CACHE: raise KeyError(f'logo no cacheado: {key}; regenerar logo_cache.json')
    svg = _CACHE[key]
    return svg if cls == 'esmun-logo' else svg.replace('class="esmun-logo', f'class="{cls}', 1)
