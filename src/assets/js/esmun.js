/* ESMUN · comportamiento compartido: logotipo reactivo al fondo, revelados, cabecera, formulario. Sin dependencias. */
(function () {
  document.documentElement.classList.remove('no-js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Logotipo: ventanas que se encienden sobre fondo oscuro ----------
     Reglas: sobre fondo claro, logotipo normal (ventanas grises).
     Dentro de una sección [data-theme="dark"], al entrar en pantalla las ventanas se encienden una a una y quedan encendidas.
     El logotipo de la cabecera sigue la sección que tiene debajo: sobre oscuro se enciende progresivamente con el scroll;
     al volver a un fondo claro vuelve al estado normal. */
  function windowsOf(svg) { return Array.prototype.slice.call(svg.querySelectorAll('.win')); }
  function setLit(svg, n) {
    var ws = windowsOf(svg);
    ws.forEach(function (w, i) { w.classList.toggle('on', i < n); });
    svg.dataset.lit = n;
  }
  function lightUp(svg, stagger) {
    var ws = windowsOf(svg); if (svg.dataset.playing === '1') return; svg.dataset.playing = '1';
    var order = ws.map(function (_, i) { return i; }).sort(function (a, b) { return ((a * 7) % 12) - ((b * 7) % 12); });
    order.forEach(function (idx, k) { setTimeout(function () { ws[idx].classList.add('on'); }, reduce ? 0 : 120 * k + 150); });
    setTimeout(function () { svg.dataset.playing = ''; svg.dataset.lit = ws.length; }, reduce ? 0 : 120 * order.length + 200);
  }
  function reset(svg) { windowsOf(svg).forEach(function (w) { w.classList.remove('on'); }); svg.dataset.lit = 0; svg.dataset.playing = ''; }
  // Apagado progresivo: las ventanas se apagan una a una (orden inverso al encendido)
  function lightDown(svg) {
    var ws = windowsOf(svg).filter(function (w) { return w.classList.contains('on'); }); if (!ws.length) return;
    if (svg.dataset.playing === '1') { reset(svg); return; }
    var order = ws.map(function (_, i) { return i; }).sort(function (a, b) { return ((b * 7) % 12) - ((a * 7) % 12); });
    svg.dataset.playing = '1';
    order.forEach(function (idx, k) { setTimeout(function () { ws[idx].classList.remove('on'); }, reduce ? 0 : 90 * k); });
    setTimeout(function () { svg.dataset.playing = ''; svg.dataset.lit = 0; }, reduce ? 0 : 90 * order.length + 50);
  }

  // Logotipos dentro de secciones oscuras
  var darkLogos = document.querySelectorAll('[data-theme="dark"] .esmun-logo[data-mode="auto"]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { lightUp(e.target); } else if (parseInt(e.target.dataset.lit || '0', 10) > 0 || e.target.dataset.playing === '1') { lightDown(e.target); } });
    }, { threshold: 0.2 });
    darkLogos.forEach(function (s) { io.observe(s); });
  } else { darkLogos.forEach(function (s) { setLit(s, 12); }); }

  // Logotipo de cabecera: sigue el fondo
  var header = document.querySelector('.site-header'); var hLogo = header && header.querySelector('.esmun-logo');
  var sections = Array.prototype.slice.call(document.querySelectorAll('[data-section]'));
  function sectionUnderHeader() {
    var y = (header ? header.getBoundingClientRect().bottom : 0) + 1; var best = null;
    sections.forEach(function (s) { var r = s.getBoundingClientRect(); if (r.top <= y && r.bottom > y) best = s; });
    return best;
  }
  var lastTheme = null, lastBg = null;
  function syncHeader() {
    if (!header) return; var s = sectionUnderHeader(); var theme = s ? (s.getAttribute('data-theme') || 'light') : 'light';
    if (theme !== lastTheme) { header.setAttribute('data-theme', theme === 'dark' ? 'dark' : (theme === 'blue' ? 'blue' : '')); if (theme !== 'dark' && hLogo) lightDown(hLogo); lastTheme = theme; }
    var bgc = s && s.getAttribute('data-bg'); if (bgc !== lastBg) { header.style.setProperty('--bg', bgc || ''); lastBg = bgc; } // secciones teñidas (p. ej. color de comité) tiñen también la cabecera
    if (theme === 'dark' && hLogo && s) {
      var r = s.getBoundingClientRect(); var hb = header.getBoundingClientRect().bottom; var span = Math.min(r.height / 2, window.innerHeight * 0.7);
      var pin = Math.min(1, Math.max(0, (hb - r.top) / span));            // entrando: se encienden
      var pout = Math.min(1, Math.max(0, (r.bottom - hb) / span));        // saliendo: se apagan
      var n = Math.round(Math.min(pin, pout) * 12); setLit(hLogo, n);
    }
  }
  var ticking = false;
  window.addEventListener('scroll', function () { if (!ticking) { requestAnimationFrame(function () { syncHeader(); ticking = false; }); ticking = true; } }, { passive: true });
  window.addEventListener('resize', syncHeader); syncHeader();

  /* ---------- Revelado ---------- */
  var rev = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io2 = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io2.unobserve(e.target); } }); }, { rootMargin: '0px 0px -10% 0px' });
    rev.forEach(function (el) { io2.observe(el); });
  } else { rev.forEach(function (el) { el.classList.add('in'); }); }

  /* ---------- Navegación activa + menú móvil ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.site-nav a[href^="#"]'));
  if ('IntersectionObserver' in window) {
    var io3 = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { links.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id); }); } }); }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { if (s.id) io3.observe(s); });
  }
  var mb = document.querySelector('.menu-btn'); if (mb) { mb.addEventListener('click', function () { header.classList.toggle('open'); mb.setAttribute('aria-expanded', header.classList.contains('open')); }); links.forEach(function (a) { a.addEventListener('click', function () { header.classList.remove('open'); }); }); document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && header.classList.contains('open')) { header.classList.remove('open'); mb.setAttribute('aria-expanded', 'false'); mb.focus(); } }); }

  /* ---------- Contadores ---------- */
  var counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && !reduce) {
    var io4 = new IntersectionObserver(function (es) { es.forEach(function (e) { if (!e.isIntersecting) return; var el = e.target, to = parseInt(el.getAttribute('data-count'), 10), t0 = null; io4.unobserve(el);
      function step(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / 1400); p = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(to * p); if (p < 1) requestAnimationFrame(step); }
      requestAnimationFrame(step); }); }, { threshold: 0.6 });
    counters.forEach(function (c) { io4.observe(c); });
  } else { counters.forEach(function (c) { c.textContent = c.getAttribute('data-count'); }); }

  /* ---------- Formulario (Formspree u otro endpoint sin backend) ---------- */
  var form = document.querySelector('form[data-endpoint]');
  if (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault(); var ep = form.getAttribute('data-endpoint'); var msg = form.querySelector('.form-msg');
      var ak = form.querySelector('input[name=access_key]'); if (!ep || ep.indexOf('TU_ID') !== -1 || (ak && ak.value.indexOf('PEGAR') === 0)) { msg.textContent = 'Formulario de demostración: configura el endpoint (Formspree, Getform o Netlify Forms) en data-endpoint.'; return; }
      var data = new FormData(form); msg.textContent = 'Enviando…';
      fetch(ep, { method: 'POST', body: data, headers: { Accept: 'application/json' } }).then(function (r) { msg.textContent = r.ok ? 'Gracias. Te respondemos por correo en menos de 48 horas.' : 'No se pudo enviar. Escríbenos a esmunze@outlook.com.'; if (r.ok) form.reset(); }).catch(function () { msg.textContent = 'Sin conexión. Escríbenos a esmunze@outlook.com.'; });
    });
  }

  /* ---------- Scrollytelling (propuesta 5): progreso 0..1 de un contenedor fijo ---------- */
  var scrolly = document.querySelector('[data-scrolly]');
  if (scrolly) {
    var pieces = Array.prototype.slice.call(scrolly.querySelectorAll('.bp')); var word = scrolly.querySelector('.word'); var sub = scrolly.querySelector('.sub'); var stage = scrolly.querySelector('.stage');
    var order = ['pilar_izq', 'pilar_centro', 'pilar_der', 'lado_pilar', 'marquesina', 'bloque', 'sombra', 'torre', 'triangulo', 'lado_torre', 'bloque_chico', 'lado_chico'];
    pieces.sort(function (a, b) { return order.indexOf(a.className.baseVal.replace('bp bp-', '')) - order.indexOf(b.className.baseVal.replace('bp bp-', '')); });
    var svg = scrolly.querySelector('.esmun-logo');
    function update() {
      var r = scrolly.getBoundingClientRect(); var total = r.height - window.innerHeight; var p = Math.min(1, Math.max(0, -r.top / total));
      scrolly.style.setProperty('--p', p.toFixed(4));
      var build = Math.min(1, p / 0.55); var n = pieces.length;
      pieces.forEach(function (el, i) { var t = Math.min(1, Math.max(0, (build * (n + 2) - i) / 2)); el.style.opacity = t; el.style.transform = 'translateY(' + ((1 - t) * 16) + 'px)'; });
      var bi = pieces.findIndex(function (el) { return el.classList.contains('bp-bloque'); }); var tb = Math.min(1, Math.max(0, (build * (n + 2) - bi) / 2));
      scrolly.querySelectorAll('.win').forEach(function (w) { w.style.opacity = tb; });
      var tw = Math.min(1, Math.max(0, (p - 0.5) / 0.18)); if (word) { word.style.opacity = tw; word.style.transform = 'translateY(' + ((1 - tw) * 24) + 'px)'; }
      var ts = Math.min(1, Math.max(0, (p - 0.62) / 0.12)); if (sub) { sub.style.opacity = ts; }
      var dark = p > 0.72; stage.setAttribute('data-theme', dark ? 'dark' : 'paper'); scrolly.setAttribute('data-theme', dark ? 'dark' : 'paper'); if (typeof syncHeader === 'function') syncHeader();
      if (svg) { var lit = Math.round(Math.min(1, Math.max(0, (p - 0.74) / 0.22)) * 12); setLit(svg, dark ? lit : 0); }
      scrolly.classList.toggle('done', p >= 0.999);
    }
    window.addEventListener('scroll', function () { requestAnimationFrame(update); }, { passive: true }); window.addEventListener('resize', update); update();
    if (reduce) { pieces.forEach(function (el) { el.style.opacity = 1; el.style.transform = 'none'; }); scrolly.querySelectorAll('.win').forEach(function (w) { w.style.opacity = 1; }); if (word) word.style.opacity = 1; if (sub) sub.style.opacity = 1; }
  }
})();
