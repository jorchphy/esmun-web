# -*- coding: utf-8 -*-
"""Genera el sitio completo en ../_site. Uso: python3 src/build.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_final, build_pages
build_final.build()
build_pages.build()
print('listo:', build_final.OUT)
