/* ESMUN · Globo 3D (Three.js). Puntos de tierra en los colores de la identidad, arcos desde la PrepaTec Esmeralda,
   ventanas doradas en las sedes; reacciona al cursor (inclinación), al scroll (posición, escala, zoom, color) y al tema de la sección.
   Carga: three.js (≈600 KB) solo se descarga si hay WebGL, el usuario no pidió "reducir movimiento" y no activó ahorro de datos.
   En cualquier otro caso se muestra el SVG estático. */
(function () {
  var holder = document.getElementById('globe'); if (!holder) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var saveData = navigator.connection && navigator.connection.saveData;
  var test = document.createElement('canvas'); var glOk = !!(test.getContext('webgl2') || test.getContext('webgl'));
  if (!glOk || reduce || saveData) { holder.classList.add('fallback'); return; }
  var src = holder.getAttribute('data-three') || 'assets/js/three.min.js';
  var load = function () { var sc = document.createElement('script'); sc.src = src; sc.onload = init; sc.onerror = function () { holder.classList.add('fallback'); }; document.head.appendChild(sc); };
  if ('requestIdleCallback' in window) requestIdleCallback(load, { timeout: 1200 }); else setTimeout(load, 1);

  function init() {
  if (!window.THREE) { holder.classList.add('fallback'); return; }
  var canvas = document.createElement('canvas'); canvas.setAttribute('aria-hidden', 'true');
  holder.appendChild(canvas); holder.classList.add('webgl');
  var mobile = window.innerWidth < 900;

  var THREE = window.THREE;
  var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, mobile ? 1.25 : 1.6)); renderer.setClearColor(0x000000, 0);
  var scene = new THREE.Scene(); var camera = new THREE.PerspectiveCamera(32, 1, 0.1, 50); camera.position.set(0, 0, 4.2);
  var world = new THREE.Group(); var globe = new THREE.Group(); world.add(globe); scene.add(world);

  // ---- colores de identidad
  var C = { azul: new THREE.Color('#253C82'), azul2: new THREE.Color('#1B477A'), tinta: new THREE.Color('#1C2030'), papel: new THREE.Color('#F3F1EC'), blanco: new THREE.Color('#ffffff'), gris: new THREE.Color('#B8B8BA'), oro: new THREE.Color('#FFD98A'), lila: new THREE.Color('#8FA6E6') };

  // ---- puntos de tierra (Int16 lat*100, lon*100 en base64)
  function decode(b64) { var bin = atob(b64); var n = bin.length / 4; var out = new Float32Array(n * 3); var meta = new Float32Array(n);
    for (var i = 0; i < n; i++) { var la = ((bin.charCodeAt(i * 4) | (bin.charCodeAt(i * 4 + 1) << 8)) << 16 >> 16) / 100; var lo = ((bin.charCodeAt(i * 4 + 2) | (bin.charCodeAt(i * 4 + 3) << 8)) << 16 >> 16) / 100;
      var v = ll(la, lo, 1); out[i * 3] = v.x; out[i * 3 + 1] = v.y; out[i * 3 + 2] = v.z; meta[i] = Math.random(); } return { pos: out, meta: meta, n: n }; }
  function ll(lat, lon, r) { var phi = (90 - lat) * Math.PI / 180, th = (lon + 180) * Math.PI / 180; return new THREE.Vector3(-r * Math.sin(phi) * Math.cos(th), r * Math.cos(phi), r * Math.sin(phi) * Math.sin(th)); }
  var land = decode(window.ESMUN_LAND || '');
  if (mobile) { // móvil: uno de cada dos puntos (los puntos van ordenados por latitud, así que se filtra alternando, no recortando)
    var n2 = Math.floor(land.n / 2), pos2 = new Float32Array(n2 * 3), meta2 = new Float32Array(n2);
    for (var k2 = 0; k2 < n2; k2++) { pos2[k2 * 3] = land.pos[k2 * 6]; pos2[k2 * 3 + 1] = land.pos[k2 * 6 + 1]; pos2[k2 * 3 + 2] = land.pos[k2 * 6 + 2]; meta2[k2] = land.meta[k2 * 2]; }
    land = { pos: pos2, meta: meta2, n: n2 }; }
  var geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(land.pos, 3)); geo.setAttribute('seed', new THREE.BufferAttribute(land.meta, 1));
  // Uniformes compartidos. La página es opaca por secciones y el lienzo del globo va ENCIMA de los fondos y DEBAJO del contenido;
  // el color de cada píxel del globo se decide según el lado de la frontera entre secciones (uSplit, en píxeles GL desde abajo):
  // gris sobre tinta, azul sobre papel. Así el globo nunca contradice el fondo que tiene detrás, ni siquiera a media transición.
  var U = { uLit: { value: C.oro }, uTime: { value: 0 }, uSize: { value: 1 }, uGlow: { value: 0 }, uPR: { value: renderer.getPixelRatio() },
    uSplit: { value: -1e6 }, uColA: { value: C.gris.clone() }, uColB: { value: C.gris.clone() }, uBgA: { value: C.tinta.clone() }, uBgB: { value: C.tinta.clone() }, uDarkA: { value: 1 }, uDarkB: { value: 1 } };
  var SPLIT = 'uniform float uSplit,uDarkA,uDarkB; uniform vec3 uColA,uColB,uBgA,uBgB; float upSide(){ return step(uSplit,gl_FragCoord.y); } float darkAt(){ return mix(uDarkB,uDarkA,upSide()); } vec3 colAt(){ return mix(uColB,uColA,upSide()); } vec3 bgAt(){ return mix(uBgB,uBgA,upSide()); }\n';
  var dots = new THREE.Points(geo, new THREE.ShaderMaterial({ transparent: true, depthWrite: false, uniforms: U,
    vertexShader: 'attribute float seed; uniform float uTime,uSize,uGlow,uPR; varying float vA; varying float vL;\n' +
      'void main(){ vec4 mv=modelViewMatrix*vec4(position,1.); vec3 n=normalize(normalMatrix*position); float facing=max(0.,dot(n,vec3(0.,0.,1.)));\n' +
      ' vA=smoothstep(0.0,0.35,facing); float tw=0.5+0.5*sin(uTime*1.3+seed*40.); vL=uGlow*step(0.72,seed)*tw;\n' +
      ' gl_Position=projectionMatrix*mv; gl_PointSize=(2.6+1.6*facing+vL*2.0)*uSize*uPR*(4.2/-mv.z); }',
    fragmentShader: SPLIT + 'uniform vec3 uLit; varying float vA; varying float vL;\n' +
      'void main(){ vec2 c=gl_PointCoord-0.5; float d=dot(c,c); if(d>0.25) discard; float e=smoothstep(0.25,0.16,d); float dk=darkAt(); vec3 col=mix(colAt(),uLit,vL*dk); gl_FragColor=vec4(col,e*(0.55+0.45*vA)*(0.9+0.1*vL)*mix(0.85,1.0,dk)); }' }));
  globe.add(dots);
  // esfera interior: tinta sobre oscuro, papel sobre claro; oculta el hemisferio posterior y da cuerpo
  var inner = new THREE.Mesh(new THREE.SphereGeometry(0.985, 64, 48), new THREE.ShaderMaterial({ transparent: true, uniforms: U,
    vertexShader: 'void main(){ gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: SPLIT + 'void main(){ float dk=darkAt(); gl_FragColor=vec4(bgAt(),mix(0.86,0.92,dk)); }' })); globe.add(inner);
  // halo (fresnel por la cara interior)
  var halo = new THREE.Mesh(new THREE.SphereGeometry(1.0, 64, 48), new THREE.ShaderMaterial({ transparent: true, side: THREE.BackSide, depthWrite: false, uniforms: U,
    vertexShader: 'varying vec3 vN; varying vec3 vP; void main(){ vN=normalize(normalMatrix*normal); vP=(modelViewMatrix*vec4(position,1.)).xyz; gl_Position=projectionMatrix*vec4(vP,1.); }',
    fragmentShader: SPLIT + 'varying vec3 vN; varying vec3 vP; void main(){ float f=pow(1.0-abs(dot(normalize(-vP),vN)),3.0); float dk=darkAt(); gl_FragColor=vec4(mix(vec3(0.145,0.235,0.51),vec3(0.56,0.65,0.9),dk),f*mix(0.16,0.38,dk)); }' }));
  halo.scale.setScalar(1.18); globe.add(halo);

  // ---- sedes: Atizapán (PrepaTec Esmeralda) y ciudades de los comités de referencia
  var HOME = { name: 'PrepaTec Esmeralda', lat: 19.58, lon: -99.26 };
  var CITIES = [ { name: 'Nueva York · ONU', lat: 40.75, lon: -73.97 }, { name: 'Ginebra', lat: 46.2, lon: 6.15 }, { name: 'Viena · OIEA', lat: 48.21, lon: 16.37 }, { name: 'Bruselas · OTAN', lat: 50.85, lon: 4.35 }, { name: 'Washington · OEA', lat: 38.9, lon: -77.04 }, { name: 'Nairobi', lat: -1.29, lon: 36.82 }, { name: 'Tokio', lat: 35.68, lon: 139.69 }, { name: 'Buenos Aires', lat: -34.6, lon: -58.38 }, { name: 'Nueva Delhi', lat: 28.61, lon: 77.21 } ];
  var markers = new THREE.Group(); globe.add(markers);
  function marker(c, big) { var m = new THREE.Mesh(new THREE.SphereGeometry(big ? 0.022 : 0.012, 12, 12), new THREE.MeshBasicMaterial({ color: C.oro })); m.position.copy(ll(c.lat, c.lon, 1.004)); m.userData.city = c.name; markers.add(m);
    var ring = new THREE.Mesh(new THREE.RingGeometry(0.02, 0.028, 32), new THREE.MeshBasicMaterial({ color: C.oro, transparent: true, opacity: 0.7, side: THREE.DoubleSide })); ring.position.copy(m.position); ring.lookAt(new THREE.Vector3(0, 0, 0)); ring.userData.t = Math.random() * 6; markers.add(ring); return m; }
  marker(HOME, true); CITIES.forEach(function (c) { marker(c, false); });
  // arcos (Bézier cúbica elevada según la distancia): blancos sobre tinta, azul emblema sobre papel
  var arcs = [];
  function arcMaterial() { return new THREE.ShaderMaterial({ transparent: true, depthWrite: false, uniforms: { uSplit: U.uSplit, uColA: U.uColA, uColB: U.uColB, uBgA: U.uBgA, uBgB: U.uBgB, uDarkA: U.uDarkA, uDarkB: U.uDarkB, uA: { value: 0.5 } },
    vertexShader: 'void main(){ gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: SPLIT + 'uniform float uA; void main(){ float dk=darkAt(); gl_FragColor=vec4(mix(vec3(0.106,0.28,0.48),vec3(1.0),dk),uA); }' }); }
  function arc(a, b) { var p0 = ll(a.lat, a.lon, 1), p3 = ll(b.lat, b.lon, 1); var d = p0.distanceTo(p3); var h = 1 + 0.25 + d * 0.35;
    var mid = p0.clone().add(p3).multiplyScalar(0.5).normalize(); var p1 = p0.clone().lerp(mid, 0.35).normalize().multiplyScalar(h), p2 = p3.clone().lerp(mid, 0.35).normalize().multiplyScalar(h);
    var curve = new THREE.CubicBezierCurve3(p0, p1, p2, p3); var g = new THREE.TubeGeometry(curve, 64, 0.0045, 6, false); var m = new THREE.Mesh(g, arcMaterial()); m.userData = { total: g.index.count, t: Math.random() * 10, city: b.name }; g.setDrawRange(0, 0); globe.add(m); arcs.push(m); }
  CITIES.forEach(function (c) { arc(HOME, c); });

  // ---- estado dirigido por scroll y tema de sección
  var state = { x: 0.9, y: 0, s: 1, lonTarget: -99, glow: 0, opacity: 1, dark: 1, focus: null };
  var cur = { x: 0.9, y: 0, s: 1, rotY: 0, tiltX: 0, glow: 0, opacity: 1 };
  var mouse = { x: 0, y: 0 }; var spin = 0; var lastT = 0;
  window.addEventListener('pointermove', function (e) { mouse.x = (e.clientX / window.innerWidth) * 2 - 1; mouse.y = (e.clientY / window.innerHeight) * 2 - 1; }, { passive: true });

  // Keyframes por sección (data-globe): x,y en unidades de mundo (cámara z=4.2, FOV 32 → media altura visible ≈ 1.2), s escala, lon longitud a centrar.
  // Regla de composición: el globo ocupa siempre el lado OPUESTO al texto de la sección (o va detrás con velo, en MUNMX).
  var KF = {
    hero:     { x: 1.05, y: -0.05, s: 1.0,  lon: -99, dark: true,  glow: 0.35 }, // texto izq · globo der
    quienes:  { x: -1.65, y: 0.05, s: 0.82, lon: -30, dark: false, glow: 0 },    // texto der · globo izq
    munmx:    { x: 0.0,  y: -0.1,  s: 1.3,  lon: -99, dark: true,  glow: 1 },    // centrado detrás, con velo
    noticias: { x: 1.6,  y: 0.1,   s: 0.8,  lon: 20,  dark: false, glow: 0 },    // lista izq · globo der
    contacto: { x: -1.65, y: -0.1, s: 0.82, lon: -99, dark: false, glow: 0 },   // texto y formulario der · globo izq
    pie:      { x: 0.0,  y: -2.05, s: 1.3,  lon: -99, dark: true,  glow: 0.6 }   // horizonte por abajo
  };
  var sections = Array.prototype.slice.call(document.querySelectorAll('[data-globe]'));
  var header = document.querySelector('.site-header');
  function lerp(a, b, t) { return a + (b - a) * t; } function sm(t) { t = Math.min(1, Math.max(0, t)); return t * t * (3 - 2 * t); }
  var kfCache = [];
  function kf(i) { if (kfCache[i]) return kfCache[i]; var el = sections[i]; var k = KF[el.getAttribute('data-globe')] || KF.hero;
    if (el.hasAttribute('data-kf')) { try { var o = JSON.parse(el.getAttribute('data-kf')); k = Object.assign({}, k, o); } catch (e) {} }
    k = Object.assign({}, k); k.bgC = new THREE.Color(k.bg || (k.dark ? '#1C2030' : '#F3F1EC')); k.dotC = new THREE.Color(k.dots || (k.dark ? '#B8B8BA' : '#253C82'));
    kfCache[i] = k; return k; }
  function update() {
    var vh = window.innerHeight, mid = vh * 0.5, mob = window.innerWidth < 900, aspect = window.innerWidth / vh, xs = mob ? 0 : Math.min(1, aspect / 1.6);
    // posición: se interpola entre keyframes en una ventana de ±0.3vh centrada en el momento en que la frontera pasa por el centro de la pantalla
    var a = kf(0), x = a.x, y = a.y, s = a.s, lon = a.lon, glow = a.glow, dark = a.dark ? 1 : 0, dip = 0, ride = 0, yB = 0;
    var endT = sm((window.scrollY + vh - (document.documentElement.scrollHeight - 0.6 * vh)) / (0.6 * vh)); // final de página: la última transición se completa aunque el pie sea corto
    for (var i = 1; i < sections.length; i++) {
      var top = sections[i].getBoundingClientRect().top; var t = sm((mid - top) / (0.5 * vh) + 0.5); if (i === sections.length - 1) t = Math.max(t, endT); if (t <= 0) break; var b = kf(i);
      if (t < 1) { // al cruzar la pantalla: se encoge, se atenúa y viaja montado en la frontera entre secciones (la franja sin texto)
        var last = i === sections.length - 1; var amp = last ? 0.8 : Math.min(1, Math.abs(b.x - x) / 2.2); dip = Math.sin(Math.PI * t) * amp; ride = last ? 0 : dip; /* hacia el pie se hunde por abajo: atenúa pero no viaja en la frontera */ yB = ((mid - top) / mid) * 1.2; }
      x = lerp(x, b.x, t); y = lerp(y, b.y, t); s = lerp(s, b.s, t); lon = lerp(lon, b.lon, t); glow = lerp(glow, b.glow, t); dark = lerp(dark, b.dark ? 1 : 0, t);
    }
    y = lerp(y, yB, ride);
    // frontera visible entre secciones → colores por píxel
    var split = -1e6, dA = dark, dB = dark, kA = kf(0), kB = kf(0), focus = null;
    for (var j = 1; j < sections.length; j++) { var tj = sections[j].getBoundingClientRect().top; if (tj > 0 && tj < vh) { split = (vh - tj) * renderer.getPixelRatio(); kA = kf(j - 1); kB = kf(j); dA = kA.dark ? 1 : 0; dB = kB.dark ? 1 : 0; break; } }
    if (split === -1e6) { var k = -1; for (var q = 0; q < sections.length; q++) { var r = sections[q].getBoundingClientRect(); if (r.top <= mid && r.bottom > mid) k = q; } if (k >= 0) { kA = kB = kf(k); dA = dB = kA.dark ? 1 : 0; } }
    U.uSplit.value = split; U.uDarkA.value = dA; U.uDarkB.value = dB; U.uColA.value.copy(kA.dotC); U.uColB.value.copy(kB.dotC); U.uBgA.value.copy(kA.bgC); U.uBgB.value.copy(kB.bgC);
    // foco: la sección bajo el centro manda qué sede se destaca (sus arcos quedan; los demás se atenúan)
    for (var f = 0; f < sections.length; f++) { var rf = sections[f].getBoundingClientRect(); if (rf.top <= mid && rf.bottom > mid) { focus = kf(f).focus || null; break; } }
    state.focus = focus;
    // móvil: sobre fondo claro el globo se desplaza a la derecha y se atenúa para no competir con el texto
    state.x = mob ? lerp(1.0, 0, dark) : x * xs; state.y = y + (mob ? lerp(-0.2, 0.55, dark) : 0); state.s = s * (mob ? 0.78 : 1) * (1 - 0.5 * dip);
    state.glow = glow; state.lonTarget = lon; state.dark = dark; state.opacity = (mob ? lerp(0.22, 1, dark) : 1) * (1 - 0.65 * dip);
    document.documentElement.style.setProperty('--darkT', dark.toFixed(3));
  }
  window.addEventListener('scroll', update, { passive: true }); window.addEventListener('resize', function () { resize(); update(); }); update();

  function resize() { var w = window.innerWidth, h = window.innerHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); U.uPR.value = renderer.getPixelRatio(); }
  resize();

  function frame(tms) { var dt = Math.min(0.05, (tms - lastT) / 1000 || 0.016); lastT = tms; var k = 1 - Math.pow(0.001, dt);
    cur.x = lerp(cur.x, state.x, k); cur.y = lerp(cur.y, state.y, k); cur.s = lerp(cur.s, state.s, k); cur.glow = lerp(cur.glow, state.glow, k); cur.opacity = lerp(cur.opacity, state.opacity, k);
    renderer.domElement.style.opacity = cur.opacity.toFixed(3);
    world.position.set(cur.x, cur.y, 0); world.scale.setScalar(cur.s);
    if (!reduce) spin += dt * 0.08;
    // longitud objetivo: giramos el globo para que esa longitud mire a la cámara, más el giro libre acotado
    var targetRot = -(state.lonTarget + 90) * Math.PI / 180 + Math.sin(spin) * 0.35 + (reduce ? 0 : mouse.x * 0.25);
    cur.rotY = lerp(cur.rotY, targetRot, k); cur.tiltX = lerp(cur.tiltX, 0.28 + (reduce ? 0 : mouse.y * 0.18), k);
    globe.rotation.set(cur.tiltX, cur.rotY, 0);
    U.uTime.value = tms / 1000; U.uGlow.value = cur.glow;
    // arcos: dibujo cíclico
    arcs.forEach(function (m) { m.userData.t += dt * 0.35; var ph = m.userData.t % 4; var total = m.userData.total; var dr;
      if (ph < 1.4) dr = [0, Math.floor(total * (ph / 1.4))]; else if (ph < 2.4) dr = [0, total]; else if (ph < 3.4) { var p = (ph - 2.4) / 1.0; dr = [Math.floor(total * p), total - Math.floor(total * p)]; } else dr = [0, 0];
      m.geometry.setDrawRange(dr[0], dr[1]); var fm = state.focus ? (m.userData.city === state.focus ? 1.6 : 0.12) : 1; m.material.uniforms.uA.value = Math.min(1, (0.55 * (0.35 + 0.65 * cur.glow) + 0.15) * fm); });
    markers.children.forEach(function (o) { if (o.geometry.type === 'SphereGeometry' && o.userData.city) { var want = state.focus === o.userData.city ? 2.2 : 1; o.scale.setScalar(lerp(o.scale.x, want, k)); } if (o.geometry.type === 'RingGeometry') { o.userData.t += dt; var p = (o.userData.t % 2.4) / 2.4; o.scale.setScalar(1 + p * 2.2); o.material.opacity = (1 - p) * 0.7; } });
    renderer.render(scene, camera); if (!document.hidden) requestAnimationFrame(frame); }
  requestAnimationFrame(frame);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) { lastT = performance.now(); requestAnimationFrame(frame); } });

  // etiqueta de sede al pasar el cursor (desktop)
  var tip = document.getElementById('globe-tip'); var ray = new THREE.Raycaster(); var v2 = new THREE.Vector2(); var spheres = markers.children.filter(function (o) { return o.geometry.type === 'SphereGeometry'; });
  var names = [HOME].concat(CITIES);
  if (tip && !('ontouchstart' in window)) { window.addEventListener('pointermove', function (e) { v2.set((e.clientX / window.innerWidth) * 2 - 1, -(e.clientY / window.innerHeight) * 2 + 1); ray.setFromCamera(v2, camera); var hit = ray.intersectObjects(spheres, false)[0];
    if (hit) { var i = spheres.indexOf(hit.object); tip.textContent = names[i] ? names[i].name : ''; tip.style.transform = 'translate(' + (e.clientX + 14) + 'px,' + (e.clientY + 14) + 'px)'; tip.hidden = false; } else { tip.hidden = true; } }, { passive: true }); }
  } // init
})();
