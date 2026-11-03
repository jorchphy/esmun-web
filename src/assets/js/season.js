/* ESMUN · temporada en el logotipo de la cabecera.
   Partículas discretas (hojas, pétalos, nieve, papel picado…) cayendo solo sobre el logotipo del header.
   Configuración en content/site.json → "temporada": { "modo": "auto" | "manual" | "off", "manual": "otono" }.
   En modo auto se elige por fecha (calendario de México y fechas de la ONU); un día señalado gana a una temporada larga. */
(function () {
  var brand = document.querySelector('.site-header .brand'); if (!brand) return;
  var cfgEl = document.getElementById('season-cfg'); var cfg = {};
  try { cfg = JSON.parse(cfgEl ? cfgEl.textContent : '{}') || {}; } catch (e) { cfg = {}; }
  if (cfg.modo === 'off') return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  // ---- catálogo: forma, colores, cantidad, velocidad, tamaño
  var KINDS = {
    otono:        { shape: 'leaf',   colors: ['#B4452E', '#C8962E', '#8A5A2B', '#A1A1A1'], n: 7, speed: [9, 16], size: [5, 8], sway: 1.2, spin: true },
    muertos:      { shape: 'petal',  colors: ['#E8871E', '#F2A541', '#C8962E'], n: 9, speed: [8, 14], size: [3.5, 5.5], sway: .8 },
    onu:          { shape: 'confetti', colors: ['#5B92E5', '#B9C6EE', '#FFFFFF'], n: 8, speed: [10, 18], size: [3, 5], sway: 1.4, spin: true },
    independencia:{ shape: 'confetti', colors: ['#2E7D5B', '#F3F1EC', '#B4452E'], n: 10, speed: [10, 18], size: [3, 5], sway: 1.4, spin: true },
    invierno:     { shape: 'snow',   colors: ['#FFFFFF', '#DCE3F7'], n: 12, speed: [12, 22], size: [2.5, 4.5], sway: 1.0 },
    primavera:    { shape: 'petal',  colors: ['#9B7FD1', '#B9A5E6', '#7B61B8'], n: 8, speed: [9, 16], size: [3.5, 5.5], sway: 1.3, spin: true },
    munmx:        { shape: 'spark',  colors: ['#FFD98A', '#FFE3A6'], n: 8, speed: [-14, -8], size: [1.5, 3], sway: .6 },
    mujer:        { shape: 'petal',  colors: ['#7B2D8E', '#B46AC8'], n: 8, speed: [9, 15], size: [3.5, 5.5], sway: 1.0 },
    // días internacionales (ONU) y fechas de México
    bandera:      { shape: 'confetti', colors: ['#2E7D5B', '#F3F1EC', '#B4452E'], n: 9, speed: [10, 18], size: [3, 5], sway: 1.2, spin: true },
    bosques:      { shape: 'leaf',   colors: ['#2E7D5B', '#4F9C6B', '#7FB77E'], n: 7, speed: [8, 14], size: [5, 8], sway: 1.2, spin: true },
    agua:         { shape: 'drop',   colors: ['#5B92E5', '#9CC3F5'], n: 8, speed: [16, 26], size: [2.5, 4], sway: .3 },
    tierra:       { shape: 'leaf',   colors: ['#2E7D5B', '#5B92E5', '#8A5A2B'], n: 7, speed: [8, 14], size: [5, 8], sway: 1.2, spin: true },
    ambiente:     { shape: 'leaf',   colors: ['#4F9C6B', '#7FB77E', '#B9D98C'], n: 7, speed: [8, 14], size: [5, 8], sway: 1.3, spin: true },
    oceanos:      { shape: 'bubble', colors: ['#5B92E5', '#9CC3F5', '#DCE3F7'], n: 8, speed: [-16, -8], size: [2, 4.5], sway: .8 },
    juventud:     { shape: 'confetti', colors: ['#FFD98A', '#5B92E5', '#B46AC8', '#2E7D5B'], n: 10, speed: [10, 18], size: [3, 5], sway: 1.4, spin: true },
    paz:          { shape: 'feather', colors: ['#FFFFFF', '#F3F1EC'], n: 7, speed: [6, 11], size: [4, 6.5], sway: 1.6, spin: true },
    infancia:     { shape: 'confetti', colors: ['#1CABE2', '#9CC3F5', '#FFFFFF'], n: 10, speed: [10, 18], size: [3, 5], sway: 1.4, spin: true },
    naranja:      { shape: 'petal',  colors: ['#F26B21', '#F7944D'], n: 8, speed: [9, 15], size: [3.5, 5.5], sway: 1.0 },
    ddhh:         { shape: 'spark',  colors: ['#5B92E5', '#FFFFFF'], n: 8, speed: [-14, -8], size: [1.5, 3], sway: .6 },
    navidad:      { shape: 'snow',   colors: ['#FFFFFF', '#B4452E', '#2E7D5B', '#FFD98A'], n: 12, speed: [12, 22], size: [2.5, 4.5], sway: 1.0 },
    anonuevo:     { shape: 'spark',  colors: ['#FFD98A', '#FFFFFF'], n: 10, speed: [-16, -9], size: [1.5, 3], sway: .8 }
  };
  // ---- calendario (mes, día). Rangos largos y días señalados; los días señalados tienen prioridad.
  function inRange(m, d, a, b) { var x = m * 100 + d, lo = a[0] * 100 + a[1], hi = b[0] * 100 + b[1]; return lo <= hi ? (x >= lo && x <= hi) : (x >= lo || x <= hi); }
  function auto(date) {
    var m = date.getMonth() + 1, d = date.getDate();
    if (inRange(m, d, [3, 11], [3, 13])) return 'munmx';      // MUNMX Esmeralda 2027
    // días señalados (tienen prioridad sobre las temporadas largas)
    if (m === 2 && d === 24) return 'bandera';                 // Día de la Bandera (México)
    if (m === 3 && d === 8) return 'mujer';                    // Día Internacional de la Mujer
    if (m === 3 && d === 21) return 'bosques';                 // Día Internacional de los Bosques
    if (m === 3 && d === 22) return 'agua';                    // Día Mundial del Agua
    if (m === 4 && d === 22) return 'tierra';                  // Día de la Madre Tierra
    if (m === 4 && d === 30) return 'infancia';                // Día del Niño (México)
    if (m === 6 && d === 5) return 'ambiente';                 // Día Mundial del Medio Ambiente
    if (m === 6 && d === 8) return 'oceanos';                  // Día Mundial de los Océanos
    if (m === 8 && d === 12) return 'juventud';                // Día Internacional de la Juventud
    if (m === 9 && d === 21) return 'paz';                     // Día Internacional de la Paz
    if (m === 10 && d === 24) return 'onu';                    // Día de las Naciones Unidas
    if (m === 11 && d === 20) return 'infancia';               // Día Mundial de la Infancia
    if (m === 11 && d === 25) return 'naranja';                // Eliminación de la violencia contra la mujer (Pinta el mundo de naranja)
    if (m === 12 && d === 10) return 'ddhh';                   // Día de los Derechos Humanos
    if (inRange(m, d, [12, 24], [12, 25])) return 'navidad';
    if (inRange(m, d, [12, 31], [1, 1])) return 'anonuevo';
    if (inRange(m, d, [10, 28], [11, 2])) return 'muertos';    // Día de Muertos
    if (inRange(m, d, [9, 1], [9, 16])) return 'independencia';
    if (inRange(m, d, [9, 17], [11, 30])) return 'otono';
    if (inRange(m, d, [12, 1], [1, 6])) return 'invierno';
    if (inRange(m, d, [3, 1], [4, 30])) return 'primavera';
    return null;
  }
  var key = cfg.modo === 'manual' ? cfg.manual : auto(new Date());
  var K = KINDS[key]; if (!K) return;

  // ---- lienzo sobre el logotipo
  var svg = brand.querySelector('svg') || brand; var cv = document.createElement('canvas'); cv.className = 'season'; cv.setAttribute('aria-hidden', 'true');
  brand.style.position = 'relative'; brand.appendChild(cv); var ctx = cv.getContext('2d'); var W = 0, H = 0, PR = Math.min(window.devicePixelRatio || 1, 2);
  function size() { var r = svg.getBoundingClientRect(); W = Math.max(40, r.width + 24); H = Math.max(24, r.height + 16); cv.width = W * PR; cv.height = H * PR; cv.style.width = W + 'px'; cv.style.height = H + 'px'; cv.style.left = (r.left - brand.getBoundingClientRect().left - 12) + 'px'; cv.style.top = (r.top - brand.getBoundingClientRect().top - 8) + 'px'; }
  size(); window.addEventListener('resize', size);
  var mob = window.innerWidth < 900; var N = mob ? Math.ceil(K.n * 0.6) : K.n;
  function rnd(a, b) { return a + Math.random() * (b - a); }
  function spawn(p, first) { p.x = rnd(0, W); p.y = first ? rnd(-H * .2, H) : (K.speed[0] < 0 ? H + 6 : -6); p.vy = rnd(K.speed[0], K.speed[1]); p.s = rnd(K.size[0], K.size[1]); p.c = K.colors[Math.floor(Math.random() * K.colors.length)]; p.ph = rnd(0, 6.28); p.sw = rnd(.5, 1) * K.sway; p.rot = rnd(0, 6.28); p.vr = K.spin ? rnd(-1.5, 1.5) : 0; p.a = rnd(.45, .8); return p; }
  var ps = []; for (var i = 0; i < N; i++) ps.push(spawn({}, true));

  function draw(p) {
    ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.globalAlpha = p.a; ctx.fillStyle = p.c; ctx.strokeStyle = p.c;
    var s = p.s;
    if (K.shape === 'leaf') { ctx.beginPath(); ctx.moveTo(0, -s); ctx.quadraticCurveTo(s * .9, -s * .2, 0, s); ctx.quadraticCurveTo(-s * .9, -s * .2, 0, -s); ctx.fill(); ctx.globalAlpha = p.a * .6; ctx.lineWidth = .6; ctx.beginPath(); ctx.moveTo(0, -s * .8); ctx.lineTo(0, s * .8); ctx.stroke(); }
    else if (K.shape === 'petal') { ctx.beginPath(); ctx.ellipse(0, 0, s * .55, s, 0, 0, 6.283); ctx.fill(); }
    else if (K.shape === 'snow') { ctx.beginPath(); ctx.arc(0, 0, s * .5, 0, 6.283); ctx.fill(); }
    else if (K.shape === 'drop') { ctx.beginPath(); ctx.moveTo(0, -s); ctx.quadraticCurveTo(s * .7, s * .1, 0, s * .6); ctx.quadraticCurveTo(-s * .7, s * .1, 0, -s); ctx.fill(); }
    else if (K.shape === 'bubble') { ctx.lineWidth = .9; ctx.beginPath(); ctx.arc(0, 0, s, 0, 6.283); ctx.stroke(); ctx.globalAlpha = p.a * .5; ctx.beginPath(); ctx.arc(-s * .35, -s * .35, s * .22, 0, 6.283); ctx.fill(); }
    else if (K.shape === 'feather') { ctx.beginPath(); ctx.moveTo(0, -s); ctx.quadraticCurveTo(s * .55, -s * .3, s * .15, s); ctx.quadraticCurveTo(-s * .25, 0, 0, -s); ctx.fill(); ctx.globalAlpha = p.a * .5; ctx.lineWidth = .5; ctx.beginPath(); ctx.moveTo(0, -s * .9); ctx.lineTo(s * .1, s * .9); ctx.stroke(); }
    else if (K.shape === 'spark') { ctx.beginPath(); ctx.arc(0, 0, s, 0, 6.283); ctx.fill(); ctx.globalAlpha = p.a * .35; ctx.beginPath(); ctx.arc(0, 0, s * 2.2, 0, 6.283); ctx.fill(); }
    else { ctx.fillRect(-s * .5, -s * .3, s, s * .6); }
    ctx.restore();
  }
  var last = 0, hidden = false;
  document.addEventListener('visibilitychange', function () { hidden = document.hidden; if (!hidden) { last = performance.now(); requestAnimationFrame(tick); } });
  function tick(t) {
    if (hidden) return; var dt = Math.min(.05, (t - last) / 1000 || .016); last = t;
    ctx.setTransform(PR, 0, 0, PR, 0, 0); ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < ps.length; i++) { var p = ps[i]; p.y += p.vy * dt; p.ph += dt * 1.3; p.x += Math.sin(p.ph) * p.sw * 12 * dt; p.rot += p.vr * dt;
      if ((p.vy > 0 && p.y > H + 8) || (p.vy < 0 && p.y < -8) || p.x < -10 || p.x > W + 10) spawn(p, false);
      draw(p); }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();
