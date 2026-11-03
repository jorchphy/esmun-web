# -*- coding: utf-8 -*-
"""Genera el sitio en ../_site.
Uso:  python3 src/build.py             → según content/site.json → "publicacion": {"modo": "proximamente" | "completo"}
      python3 src/build.py completo    → fuerza el sitio completo (o variable de entorno ESMUN_MODO=completo)
      python3 src/build.py proximamente"""
import sys, os, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_sites as B
modo = (sys.argv[1] if len(sys.argv) > 1 else '') or os.environ.get('ESMUN_MODO', '') or (B.C.get('publicacion') or {}).get('modo', 'completo')
modo = modo.strip().lower()
if modo == 'proximamente':
    import build_pronto
    build_pronto.build()
else:
    import build_final, build_pages
    build_final.build()
    build_pages.build()
print('listo (modo %s):' % modo, pathlib.Path(__file__).resolve().parent.parent / '_site')
