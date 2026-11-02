# esmun-web

Sitio de ESMUN (Modelo de Naciones Unidas de la PrepaTec Esmeralda). Estático, generado con Python, publicado en GitHub Pages.

## Cómo se actualiza

Todo el contenido vive en `src/content/`. No hace falta tocar Python ni HTML.

| Qué cambiar | Archivo |
|---|---|
| Textos de la portada, cifras, línea de tiempo, comités (sigla, nombre, nivel, color), correo, Instagram, dominio, endpoints de formularios | `src/content/site.json` |
| Fichas de comités (sede, colores, descripción) | `src/content/comites.json` |
| Coaches y asesores | `src/content/staff.json` |
| Noticias (una por archivo; cabecera entre `---` y cuerpo en Markdown) | `src/content/noticias/*.md` |
| Fotos | `src/assets/img/real/` |

Al hacer push a `main`, GitHub Actions construye el sitio y lo publica (ver `.github/workflows/pages.yml`). También se puede construir en local:

```
python3 src/build.py      # genera _site/
```

y subir `_site/` a cualquier hosting estático.

## Puesta en marcha (una sola vez)
1. Crear el repositorio en GitHub y subir esta carpeta.
2. Settings → Pages → Source: **GitHub Actions**.
3. Esperar el primer workflow; el sitio queda en `https://<usuario>.github.io/<repo>/`.
4. Si el repo no se llama `<usuario>.github.io`, poner la URL completa en `dominio` dentro de `src/content/site.json` (sirve para el sitemap, canonical y datos estructurados).
5. Formularios: crear dos formularios en Formspree (contacto y pre-registro) y pegar sus URL en `formspree_contacto` y `formspree_registro` de `site.json`.

## Noticia nueva
Copiar cualquier archivo de `src/content/noticias/`, renombrarlo (el nombre es la URL), cambiar la cabecera y el texto. Se ordenan por fecha. Etiquetas usadas: Identidad, Reconocimiento, Historia, MUNMX 2027, Convocatoria.

## Estructura
- `src/build.py`: entrada. Llama a `build_final.py` (portada, blog, 404, sitemap…) y `build_pages.py` (subpáginas).
- `src/build_sites.py`: textos por defecto, cabecera, pie, formulario de contacto, noticias.
- `src/build_p6.py`: CSS y portada.
- `src/content.py`: carga de `content/`.
- `src/logo_svg.py` + `logo_cache.json`: logotipo inline (precalculado; la fuente está en `99 Archivos fuente/v3`).
- `src/assets/`: CSS, JS (globo 3D, comportamiento), fuentes, logotipos, fotos.
