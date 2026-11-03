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
| Temporada en el logotipo de la cabecera (decoración sobre el edificio y partículas) | `src/content/site.json` → `temporada` (`modo`: auto, manual u off) |
| Fotos | `src/assets/img/real/` (fotos de mesa en `real/mesa/`) |
| Descargas para delegados (protocolo, ejemplos, carta) | `src/content/site.json` → `descargas`; archivos en `src/assets/docs/` |
| Patrocinios: niveles, beneficios, necesidades en especie, logotipos | `src/content/site.json` → `patrocinios` |
| Mesa directiva y tópico de cada comité | `src/content/comites.json` → `mesa`, `tema` |

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

## Documentos con membrete
`python3 tools/make_docs.py` regenera el membrete de la carta (DOCX y PDF) y los ejemplos de papel de posición y resolución en `src/assets/docs/`. Para publicar la carta real: pegar el texto en `Membrete_MUNMX_2027_carta.docx`, exportar a PDF como `Carta_bienvenida_MUNMX_2027.pdf` en `src/assets/docs/` y poner `"disponible": true` en `descargas`. El protocolo se publica igual: `Protocolo_MUNMX_2027.pdf` + `disponible: true`.

## Publicación por etapas

El sitio tiene dos modos. Se eligen en `src/content/site.json` → `publicacion.modo`:

| Modo | Qué se publica |
|---|---|
| `proximamente` | Solo la portada de "muy pronto": fechas de MUNMX 2027, cuenta regresiva y formulario de aviso por correo. Sin subpáginas. |
| `completo` | Todo el sitio. |

El modo también se puede forzar sin tocar el archivo, con la variable de entorno `ESMUN_MODO` (en GitHub: *Settings → Secrets and variables → Actions → Variables*; en Cloudflare Pages: *Settings → Environment variables*). Así, el dominio principal puede mostrar "próximamente" mientras una rama o entorno de vista previa publica el sitio completo en un subdominio temporal.

Para construir localmente un modo u otro: `python3 src/build.py completo` o `python3 src/build.py proximamente`.

Para abrir el sitio al público: cambiar `publicacion.modo` a `completo` (o la variable `ESMUN_MODO` en el hosting) y publicar.

## Dónde se publica

| Proyecto en Cloudflare | Rama | Qué muestra | URL |
|---|---|---|---|
| `esmun-web` | `main` | Lo que diga `publicacion.modo` (hoy, «Próximamente») | esmun-web.jorch-imr.workers.dev → esmun.com.mx |
| `esmun-vista` | `vista` | Sitio completo (variable `ESMUN_MODO=completo`) | esmun-vista.jorch-imr.workers.dev → vista.esmun.com.mx |

Cada *push* reconstruye el proyecto de su rama (`python3 src/build.py` → `_site/` → `npx wrangler deploy`). La configuración de Workers está en `wrangler.jsonc`; el proyecto `esmun-vista` usa `npx wrangler deploy --name esmun-vista` como comando de despliegue para no pisar a `esmun-web`.

## Panel de administración

En **/admin/** (por ejemplo https://vista.esmun.com.mx/admin/) está Sveltia CMS. Se entra con una cuenta de GitHub que sea colaboradora del repositorio. Lo que se edita ahí:

| Sección | Archivo | Qué se puede hacer |
|---|---|---|
| Noticias | `src/content/noticias/*.md` | Crear, editar, marcar como borrador, subir foto |
| Comités | `src/content/comites.json` | Nivel, idioma, tópico, mesa directiva con fotos, textos, color |
| Coaches y asesores | `src/content/staff.json` | Nombre, rol, descripción, foto |
| Sitio y ajustes | `src/content/site.json` | Textos del inicio, cifras, línea de tiempo, descargas, patrocinios, interruptor de publicación, temporada del logotipo, clave de formularios |

Cada guardado es un commit en `main`; Cloudflare reconstruye en uno o dos minutos. Las fotos subidas van a `src/assets/img/real/` (mesas en `real/mesa/`, logotipos en `real/patrocinadores/`) y los PDF a `src/assets/docs/`.

Inicio de sesión: el panel usa el Worker `sveltia-cms-auth` de la misma cuenta de Cloudflare (app OAuth de GitHub). Para dar acceso a alguien: GitHub → repositorio → Settings → Collaborators → Add people, con permiso *Write*.

