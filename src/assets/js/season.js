/* ESMUN · temporada en el logotipo de la cabecera.
   Dos capas: (1) decoración dibujada sobre el edificio del logotipo (luces, papel picado, bandera, árbol…)
   y (2) partículas discretas cayendo (hojas, pétalos, nieve…). Cada fecha usa una, otra o ambas.
   Configuración en content/site.json → "temporada": { "modo": "auto" | "manual" | "off", "manual": "navidad" }.
   En modo auto se elige por fecha (calendario de México y días internacionales de la ONU). */
(function () {
  var brand = document.querySelector('.site-header .brand'); if (!brand) return;
  var cfgEl = document.getElementById('season-cfg'); var cfg = {};
  try { cfg = JSON.parse(cfgEl ? cfgEl.textContent : '{}') || {}; } catch (e) { cfg = {}; }
  if (cfg.modo === 'off') return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // paleta
  var VERDE = '#2E7D5B', ROJO = '#B4452E', ORO = '#FFD98A', AZULONU = '#5B92E5', CIAN = '#1CABE2', CREMA = '#F3F1EC', NIEVE = '#DCE3F7';

  // ---- catálogo. fall: partículas (o null); deco: piezas sobre el edificio
  var KINDS = {
    otono:        { fall: { shape: 'leaf', colors: ['#B4452E', '#C8962E', '#8A5A2B', '#A1A1A1'], n: 7, speed: [9, 16], size: [5, 8], sway: 1.2, spin: true }, deco: [['hojas']] },
    muertos:      { fall: { shape: 'petal', colors: ['#E8871E', '#F2A541'], n: 6, speed: [8, 14], size: [3.5, 5.5], sway: .8 }, deco: [['picado', ['#E8871E', '#D63384', '#6B3D7A', '#1CABE2', '#F2A541']], ['cempasuchil'], ['velas']] },
    onu:          { fall: { shape: 'confetti', colors: [AZULONU, '#B9C6EE', '#FFFFFF'], n: 7, speed: [10, 18], size: [3, 5], sway: 1.4, spin: true }, deco: [['bandera', 'onu']] },
    independencia:{ fall: { shape: 'confetti', colors: [VERDE, CREMA, ROJO], n: 8, speed: [10, 18], size: [3, 5], sway: 1.4, spin: true }, deco: [['bandera', 'mx'], ['picado', [VERDE, CREMA, ROJO]]] },
    bandera:      { fall: null, deco: [['bandera', 'mx']] },
    invierno:     { fall: { shape: 'snow', colors: ['#FFFFFF', NIEVE], n: 12, speed: [12, 22], size: [2.5, 4.5], sway: 1.0 }, deco: [['nieve']] },
    navidad:      { fall: { shape: 'snow', colors: ['#FFFFFF', NIEVE], n: 8, speed: [12, 22], size: [2.5, 4.5], sway: 1.0 }, deco: [['nieve'], ['luces', [ROJO, ORO, VERDE, AZULONU]], ['arbol'], ['estrella']] },
    anonuevo:     { fall: { shape: 'spark', colors: [ORO, '#FFFFFF'], n: 10, speed: [-16, -9], size: [1.5, 3], sway: .8 }, deco: [['luces', [ORO, '#FFFFFF']]] },
    primavera:    { fall: { shape: 'petal', colors: ['#9B7FD1', '#B9A5E6'], n: 6, speed: [9, 16], size: [3.5, 5.5], sway: 1.3, spin: true }, deco: [['arboles', ['#9B7FD1', '#B9A5E6', '#7B61B8']]] },
    munmx:        { fall: { shape: 'spark', colors: [ORO, '#FFE3A6'], n: 8, speed: [-14, -8], size: [1.5, 3], sway: .6 }, deco: [['bandera', 'onu'], ['bandera', 'mx', 2]] },
    mujer:        { fall: { shape: 'petal', colors: ['#7B2D8E', '#B46AC8'], n: 6, speed: [9, 15], size: [3.5, 5.5], sway: 1.0 }, deco: [['lazo', '#7B2D8E']] },
    naranja:      { fall: { shape: 'petal', colors: ['#F26B21', '#F7944D'], n: 6, speed: [9, 15], size: [3.5, 5.5], sway: 1.0 }, deco: [['lazo', '#F26B21']] },
    bosques:      { fall: { shape: 'leaf', colors: [VERDE, '#4F9C6B', '#7FB77E'], n: 5, speed: [8, 14], size: [5, 8], sway: 1.2, spin: true }, deco: [['arboles', [VERDE, '#4F9C6B', '#7FB77E']]] },
    ambiente:     { fall: { shape: 'leaf', colors: ['#4F9C6B', '#7FB77E', '#B9D98C'], n: 5, speed: [8, 14], size: [5, 8], sway: 1.3, spin: true }, deco: [['arboles', ['#4F9C6B', '#7FB77E', '#B9D98C']]] },
    tierra:       { fall: { shape: 'leaf', colors: [VERDE, AZULONU, '#8A5A2B'], n: 5, speed: [8, 14], size: [5, 8], sway: 1.2, spin: true }, deco: [['arboles', [VERDE, '#4F9C6B']], ['olas', AZULONU]] },
    agua:         { fall: { shape: 'drop', colors: [AZULONU, '#9CC3F5'], n: 8, speed: [16, 26], size: [2.5, 4], sway: .3 }, deco: [['olas', AZULONU]] },
    oceanos:      { fall: { shape: 'bubble', colors: [AZULONU, '#9CC3F5', NIEVE], n: 8, speed: [-16, -8], size: [2, 4.5], sway: .8 }, deco: [['olas', '#2F5D6E']] },
    juventud:     { fall: { shape: 'confetti', colors: [ORO, AZULONU, '#B46AC8', VERDE], n: 8, speed: [10, 18], size: [3, 5], sway: 1.4, spin: true }, deco: [['globos', [ORO, AZULONU, '#B46AC8', ROJO, VERDE]]] },
    infancia:     { fall: { shape: 'confetti', colors: [CIAN, '#9CC3F5', '#FFFFFF'], n: 8, speed: [10, 18], size: [3, 5], sway: 1.4, spin: true }, deco: [['globos', [CIAN, '#9CC3F5', '#FFFFFF']]] },
    paz:          { fall: { shape: 'feather', colors: ['#FFFFFF', CREMA], n: 5, speed: [6, 11], size: [4, 6.5], sway: 1.6, spin: true }, deco: [['paloma']] },
    ddhh:         { fall: { shape: 'spark', colors: [AZULONU, '#FFFFFF'], n: 8, speed: [-14, -8], size: [1.5, 3], sway: .6 }, deco: [['velas']] }
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

  /* =========================================================
     1) Decoración sobre el edificio (SVG dentro del logotipo).
     Geometría del logotipo (viewBox 0 -109.7 536.86 89.7): suelo y=-20; bloque x0-75 (techo -97);
     torre x75-118.6 (techo -109.7); bloque chico x127-142 (techo -100); marquesina x75-272, y -77..-56.5;
     pilares x75-88, 158-170, 257-272; huecos entre pilares 88-158 y 170-257.
     ========================================================= */
  var SVGNS = 'http://www.w3.org/2000/svg';
  function qb(p0, p1, p2, t) { var u = 1 - t; return [u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]]; }
  function star(cx, cy, r) { var pts = []; for (var i = 0; i < 10; i++) { var a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * .45 : r; pts.push((cx + rr * Math.cos(a)).toFixed(2) + ',' + (cy + rr * Math.sin(a)).toFixed(2)); } return pts.join(' '); }
  var SPANS = [[[88, -56.5], [123, -46], [158, -56.5]], [[170, -56.5], [213.5, -46], [257, -56.5]]];
  var D = {
    luces: function (cols) { // serie de luces colgando bajo la marquesina
      var s = ''; SPANS.forEach(function (sp, k) {
        s += '<path d="M' + sp[0] + ' Q' + sp[1] + ' ' + sp[2] + '" fill="none" stroke="#3E3E46" stroke-width=".7"/>';
        for (var i = 1; i < 10; i++) { var p = qb(sp[0], sp[1], sp[2], i / 10); s += '<circle class="blink" style="animation-delay:' + ((i * 7 + k * 3) % 10) / 4 + 's" cx="' + p[0].toFixed(1) + '" cy="' + (p[1] + 2.2).toFixed(1) + '" r="2" fill="' + cols[(i + k) % cols.length] + '"/>'; }
      }); return s;
    },
    picado: function (cols) { // papel picado bajo la marquesina
      var s = ''; SPANS.forEach(function (sp, k) {
        s += '<path d="M' + sp[0] + ' Q' + sp[1] + ' ' + sp[2] + '" fill="none" stroke="#3E3E46" stroke-width=".7"/>';
        for (var i = 0; i < 7; i++) { var t = (i + .5) / 7, p = qb(sp[0], sp[1], sp[2], t), x = p[0] - 4, y = p[1]; var c = cols[(i + k * 3) % cols.length];
          s += '<g class="sway" style="animation-delay:' + (i * .4) + 's"><path d="M' + x.toFixed(1) + ' ' + y.toFixed(1) + 'h8v5.2l-1.35 1.6-1.3-1.6-1.35 1.6-1.3-1.6-1.35 1.6-1.35-1.6z" fill="' + c + '"/><circle cx="' + (x + 2.6).toFixed(1) + '" cy="' + (y + 2).toFixed(1) + '" r=".8" fill="rgba(0,0,0,.35)"/><circle cx="' + (x + 5.4).toFixed(1) + '" cy="' + (y + 2).toFixed(1) + '" r=".8" fill="rgba(0,0,0,.35)"/><circle cx="' + (x + 4).toFixed(1) + '" cy="' + (y + 4).toFixed(1) + '" r=".7" fill="rgba(0,0,0,.35)"/></g>'; }
      }); return s;
    },
    bandera: function (tipo, pos) { // asta sobre la torre (pos 1) o sobre el bloque chico (pos 2)
      var x = pos === 2 ? 134.5 : 96.8, top = pos === 2 ? -100.2 : -109.7, h = pos === 2 ? 10 : 12, w = pos === 2 ? 10 : 12, fh = w * .62;
      var s = '<path d="M' + x + ' ' + top + 'V' + (top - h) + '" stroke="#3E3E46" stroke-width=".9"/><circle cx="' + x + '" cy="' + (top - h - .6) + '" r=".9" fill="#3E3E46"/>';
      var fx = x + .5, fy = top - h, g = '<g class="flag" style="transform-origin:' + fx + 'px ' + fy + 'px">';
      if (tipo === 'mx') { var t = w / 3; g += '<rect x="' + fx + '" y="' + fy + '" width="' + t + '" height="' + fh + '" fill="' + VERDE + '"/><rect x="' + (fx + t) + '" y="' + fy + '" width="' + t + '" height="' + fh + '" fill="' + CREMA + '"/><rect x="' + (fx + 2 * t) + '" y="' + fy + '" width="' + t + '" height="' + fh + '" fill="' + ROJO + '"/><circle cx="' + (fx + w / 2) + '" cy="' + (fy + fh / 2) + '" r="' + (fh * .18) + '" fill="#8A5A2B"/>'; }
      else { g += '<rect x="' + fx + '" y="' + fy + '" width="' + w + '" height="' + fh + '" fill="' + AZULONU + '"/><circle cx="' + (fx + w / 2) + '" cy="' + (fy + fh / 2) + '" r="' + (fh * .26) + '" fill="none" stroke="#FFFFFF" stroke-width=".6"/><circle cx="' + (fx + w / 2) + '" cy="' + (fy + fh / 2) + '" r="' + (fh * .1) + '" fill="#FFFFFF"/>'; }
      return s + g + '</g>';
    },
    nieve: function () { // nieve acumulada en los techos
      var r = function (x, y, w) { return '<rect x="' + x + '" y="' + (y - 2.4) + '" width="' + w + '" height="2.8" rx="1.2" fill="' + NIEVE + '" stroke="#9FB0DD" stroke-width=".45"/>'; };
      return r(-.6, -97.24, 76) + r(74.6, -109.7, 44.6) + r(126.8, -100.15, 15.6) + r(149.5, -77.31, 123);
    },
    arbol: function () { // árbol de Navidad en el hueco derecho
      var cx = 213.5, s = '<rect x="' + (cx - 2) + '" y="-25" width="4" height="5" fill="#8A5A2B"/>';
      [[-53, -39, 8], [-45, -31, 11], [-37, -24, 14]].forEach(function (L) { s += '<polygon points="' + cx + ',' + L[0] + ' ' + (cx - L[2]) + ',' + L[1] + ' ' + (cx + L[2]) + ',' + L[1] + '" fill="' + VERDE + '"/>'; });
      var orn = [[-41, -4, ROJO], [-36, 5, ORO], [-30, -8, AZULONU], [-27, 7, ROJO], [-33, 0, '#FFFFFF'], [-46, 3, ORO], [-27, -2, ORO]];
      orn.forEach(function (o, i) { s += '<circle class="blink" style="animation-delay:' + (i * .5) + 's" cx="' + (cx + o[1]) + '" cy="' + o[0] + '" r="1.3" fill="' + o[2] + '"/>'; });
      return s + '<polygon points="' + star(cx, -54.5, 2.8) + '" fill="' + ORO + '"/>';
    },
    estrella: function () { return '<path d="M96.8 -109.7V-118" stroke="#3E3E46" stroke-width=".9"/><polygon class="blink" points="' + star(96.8, -121, 3.6) + '" fill="' + ORO + '"/>'; },
    arboles: function (cols) { // arbolitos frente a la fachada (jacarandas, bosque…)
      var s = ''; [[104, 9, -36], [140, 6.5, -31], [228, 10, -38], [250, 6, -30]].forEach(function (t, i) {
        s += '<rect x="' + (t[0] - 1.3) + '" y="' + (t[2] + 2) + '" width="2.6" height="' + (-20 - t[2] - 2) + '" fill="#8A5A2B"/><circle cx="' + t[0] + '" cy="' + t[2] + '" r="' + t[1] + '" fill="' + cols[i % cols.length] + '"/><circle cx="' + (t[0] - t[1] * .45) + '" cy="' + (t[2] + t[1] * .35) + '" r="' + (t[1] * .6) + '" fill="' + cols[(i + 1) % cols.length] + '"/>';
      }); return s;
    },
    olas: function (col) { // agua al pie del edificio
      var d = 'M-6 -20', x = -6; while (x < 278) { d += ' q5 -4.5 10 0'; x += 10; } d += ' L284 -17 L-6 -17 Z';
      return '<path class="ola" d="' + d + '" fill="' + col + '" opacity=".75"/>';
    },
    globos: function (cols) { // globos amarrados al suelo entre los pilares
      var s = ''; [[100, -41], [109, -46], [118, -40], [228, -44], [237, -39], [246, -46]].forEach(function (b, i) {
        var c = cols[i % cols.length]; s += '<g class="bob" style="animation-delay:' + (i * .6) + 's"><path d="M' + b[0] + ' ' + (b[1] + 4.5) + ' Q' + (b[0] + 1.5) + ' ' + ((b[1] - 20) / 2) + ' ' + b[0] + ' -20" fill="none" stroke="#3E3E46" stroke-width=".5"/><ellipse cx="' + b[0] + '" cy="' + b[1] + '" rx="3.6" ry="4.4" fill="' + c + '"/><polygon points="' + b[0] + ',' + (b[1] + 4.2) + ' ' + (b[0] - 1) + ',' + (b[1] + 5.6) + ' ' + (b[0] + 1) + ',' + (b[1] + 5.6) + '" fill="' + c + '"/></g>';
      }); return s;
    },
    cempasuchil: function () { // flores de cempasúchil al pie de los pilares
      var s = ''; [[94, -26], [100, -24], [152, -25], [176, -25], [182, -27], [251, -25]].forEach(function (f) {
        s += '<path d="M' + f[0] + ' -20V' + f[1] + '" stroke="' + VERDE + '" stroke-width=".9"/>';
        for (var a = 0; a < 6; a++) s += '<circle cx="' + (f[0] + 2.1 * Math.cos(a * 1.047)).toFixed(1) + '" cy="' + (f[1] + 2.1 * Math.sin(a * 1.047)).toFixed(1) + '" r="1.5" fill="#F2A541"/>';
        s += '<circle cx="' + f[0] + '" cy="' + f[1] + '" r="1.6" fill="#E8871E"/>';
      }); return s;
    },
    velas: function () { // veladoras
      var s = ''; [[122, 8], [213.5, 10], [240, 7]].forEach(function (v, i) {
        s += '<rect x="' + (v[0] - 2) + '" y="' + (-20 - v[1]) + '" width="4" height="' + v[1] + '" rx=".6" fill="' + CREMA + '"/><path d="M' + v[0] + ' ' + (-20 - v[1] - 1) + 'V' + (-20 - v[1] - 2.5) + '" stroke="#3E3E46" stroke-width=".5"/><ellipse class="flame" style="animation-delay:' + (i * .3) + 's" cx="' + v[0] + '" cy="' + (-20 - v[1] - 4) + '" rx="1.3" ry="2.4" fill="' + ORO + '"/>';
      }); return s;
    },
    lazo: function (col) { // lazo de conciencia en la fachada del bloque
      return '<g fill="none" stroke="' + col + '" stroke-width="2.3" stroke-linecap="round"><path d="M8.5 -83C3.5 -77 2.5 -72 6 -66"/><path d="M8.5 -83C13.5 -77 14.5 -72 11 -66"/></g>';
    },
    paloma: function () { // paloma con rama de olivo junto a la torre
      return '<g transform="translate(128 -108)"><path d="M0 2c2.5-2.5 6-2.5 9.5-.5-1.5 1.2-3.5 1.4-5.5 2.6-1.4-.6-2.8-1.3-4-2.1z" fill="' + CREMA + '" stroke="#5B6075" stroke-width=".35"/><path d="M4 1.2c1-3.4 3.8-4.6 6.4-4.4-1.6 1.6-2.6 3.4-3.6 5.4z" fill="' + CREMA + '" stroke="#5B6075" stroke-width=".35"/><path d="M9.8 1.4l2.2 1.6" stroke="' + VERDE + '" stroke-width=".7" stroke-linecap="round"/><circle cx="8.6" cy="1.1" r=".35" fill="#1C2030"/></g>';
    },
    hojas: function () { // hojas acumuladas al pie de los pilares
      var s = '', cols = ['#B4452E', '#C8962E', '#8A5A2B']; [[91, -21, 20], [97, -22, -30], [154, -21, 45], [174, -22, -15], [253, -21, 30], [247, -22, -40]].forEach(function (h, i) {
        s += '<ellipse cx="' + h[0] + '" cy="' + h[1] + '" rx="3" ry="1.4" transform="rotate(' + h[2] + ' ' + h[0] + ' ' + h[1] + ')" fill="' + cols[i % 3] + '"/>';
      }); return s;
    }
  };
  function decorate() {
    var svg = brand.querySelector('svg.esmun-logo'); if (!svg || !K.deco || !K.deco.length) return;
    if (!document.getElementById('season-css')) {
      var st = document.createElement('style'); st.id = 'season-css';
      st.textContent = '.site-header .brand .esmun-logo{overflow:visible}.sd *{pointer-events:none}.sd .blink{animation:sdBlink 2.6s ease-in-out infinite}@keyframes sdBlink{0%,100%{opacity:1}50%{opacity:.35}}.sd .bob,.sd .sway,.sd .flame,.sd .flag{transform-box:fill-box}.sd .bob{animation:sdBob 3.4s ease-in-out infinite}@keyframes sdBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-1.6px)}}.sd .sway{transform-origin:top center;animation:sdSway 4s ease-in-out infinite}@keyframes sdSway{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(3deg)}}.sd .flame{transform-origin:center bottom;animation:sdFlame 1.1s ease-in-out infinite alternate}@keyframes sdFlame{from{transform:scaleY(1)}to{transform:scaleY(.78)}}.sd .flag{animation:sdFlag 2.8s ease-in-out infinite}@keyframes sdFlag{0%,100%{transform:skewY(0)}50%{transform:skewY(-4deg)}}@media(prefers-reduced-motion:reduce){.sd *{animation:none!important}}';
      document.head.appendChild(st);
    }
    var g = document.createElementNS(SVGNS, 'g'); g.setAttribute('class', 'sd'); g.setAttribute('aria-hidden', 'true');
    var html = ''; K.deco.forEach(function (d) { var fn = D[d[0]]; if (fn) html += fn(d[1], d[2]); });
    g.innerHTML = html; svg.appendChild(g);
  }
  decorate();

  /* =========================================================
     2) Partículas cayendo sobre el logotipo (lienzo).
     ========================================================= */
  var F = K.fall; if (!F || reduce) return;
  var svg = brand.querySelector('svg') || brand; var cv = document.createElement('canvas'); cv.className = 'season'; cv.setAttribute('aria-hidden', 'true');
  brand.style.position = 'relative'; brand.appendChild(cv); var ctx = cv.getContext('2d'); var W = 0, H = 0, PR = Math.min(window.devicePixelRatio || 1, 2);
  function size() { var r = svg.getBoundingClientRect(); W = Math.max(40, r.width + 24); H = Math.max(24, r.height + 16); cv.width = W * PR; cv.height = H * PR; cv.style.width = W + 'px'; cv.style.height = H + 'px'; cv.style.left = (r.left - brand.getBoundingClientRect().left - 12) + 'px'; cv.style.top = (r.top - brand.getBoundingClientRect().top - 8) + 'px'; }
  size(); window.addEventListener('resize', size);
  var mob = window.innerWidth < 900; var N = mob ? Math.ceil(F.n * 0.6) : F.n;
  function rnd(a, b) { return a + Math.random() * (b - a); }
  function spawn(p, first) { p.x = rnd(0, W); p.y = first ? rnd(-H * .2, H) : (F.speed[0] < 0 ? H + 6 : -6); p.vy = rnd(F.speed[0], F.speed[1]); p.s = rnd(F.size[0], F.size[1]); p.c = F.colors[Math.floor(Math.random() * F.colors.length)]; p.ph = rnd(0, 6.28); p.sw = rnd(.5, 1) * F.sway; p.rot = rnd(0, 6.28); p.vr = F.spin ? rnd(-1.5, 1.5) : 0; p.a = rnd(.45, .8); return p; }
  var ps = []; for (var i = 0; i < N; i++) ps.push(spawn({}, true));

  function draw(p) {
    ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.globalAlpha = p.a; ctx.fillStyle = p.c; ctx.strokeStyle = p.c;
    var s = p.s;
    if (F.shape === 'leaf') { ctx.beginPath(); ctx.moveTo(0, -s); ctx.quadraticCurveTo(s * .9, -s * .2, 0, s); ctx.quadraticCurveTo(-s * .9, -s * .2, 0, -s); ctx.fill(); ctx.globalAlpha = p.a * .6; ctx.lineWidth = .6; ctx.beginPath(); ctx.moveTo(0, -s * .8); ctx.lineTo(0, s * .8); ctx.stroke(); }
    else if (F.shape === 'petal') { ctx.beginPath(); ctx.ellipse(0, 0, s * .55, s, 0, 0, 6.283); ctx.fill(); }
    else if (F.shape === 'snow') { ctx.beginPath(); ctx.arc(0, 0, s * .5, 0, 6.283); ctx.fill(); }
    else if (F.shape === 'drop') { ctx.beginPath(); ctx.moveTo(0, -s); ctx.quadraticCurveTo(s * .7, s * .1, 0, s * .6); ctx.quadraticCurveTo(-s * .7, s * .1, 0, -s); ctx.fill(); }
    else if (F.shape === 'bubble') { ctx.lineWidth = .9; ctx.beginPath(); ctx.arc(0, 0, s, 0, 6.283); ctx.stroke(); ctx.globalAlpha = p.a * .5; ctx.beginPath(); ctx.arc(-s * .35, -s * .35, s * .22, 0, 6.283); ctx.fill(); }
    else if (F.shape === 'feather') { ctx.beginPath(); ctx.moveTo(0, -s); ctx.quadraticCurveTo(s * .55, -s * .3, s * .15, s); ctx.quadraticCurveTo(-s * .25, 0, 0, -s); ctx.fill(); ctx.globalAlpha = p.a * .5; ctx.lineWidth = .5; ctx.beginPath(); ctx.moveTo(0, -s * .9); ctx.lineTo(s * .1, s * .9); ctx.stroke(); }
    else if (F.shape === 'spark') { ctx.beginPath(); ctx.arc(0, 0, s, 0, 6.283); ctx.fill(); ctx.globalAlpha = p.a * .35; ctx.beginPath(); ctx.arc(0, 0, s * 2.2, 0, 6.283); ctx.fill(); }
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
