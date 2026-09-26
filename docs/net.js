/* net.js — every moving picture on the site, drawn from the math in your browser.
   Each demo wakes up only when its canvas is on screen. */
(function () {
  "use strict";
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var HUES = ["#ffb347", "#8fd0ff", "#c8a6ff", "#ff6a5e", "#7fe0a8", "#ffd27a"];

  function $(id) { return document.getElementById(id); }
  function bind(id, fn) {
    var el = $(id), out = $(id + "-out");
    if (!el) return;
    var go = function () { if (out) out.textContent = el.value; fn(parseFloat(el.value)); };
    el.addEventListener("input", go); go();
  }
  function loop(canvas, step) {
    var on = false, raf = 0;
    function tick(t) { step(t / 1000); if (on && !still) raf = requestAnimationFrame(tick); }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting && !on) { on = true; raf = requestAnimationFrame(tick); }
        else if (!e.isIntersecting && on) { on = false; cancelAnimationFrame(raf); }
      });
    }, { threshold: 0.05 });
    io.observe(canvas);
    return function () { if (still || !on) step(performance.now() / 1000); };
  }
  function xy(canvas, ev) {
    var b = canvas.getBoundingClientRect();
    return [(ev.clientX - b.left) * canvas.width / b.width, (ev.clientY - b.top) * canvas.height / b.height];
  }

  /* ------------------------------------------------------------ 1. the jewel net
     Every jewel shows the whole last frame, shrunk and flipped. The last frame already
     had the net in every jewel, so the reflections nest, frame after frame. */
  function jewelNet() {
    var c = $("net-canvas"); if (!c) return;
    var W = c.width = 900, H = c.height = 560, g = c.getContext("2d");
    var prev = document.createElement("canvas"); prev.width = W; prev.height = H;
    var pg = prev.getContext("2d");
    var COLS = 9, ROWS = 6, R = 22;
    var z = [], v = [];
    for (var i = 0; i < COLS * ROWS; i++) { z.push(0); v.push(0); }
    function knot(i, j, t) {
      var x = 70 + i * (W - 140) / (COLS - 1), y = 60 + j * (H - 120) / (ROWS - 1);
      return [x + 6 * Math.sin(t * 0.7 + j * 0.9), y + 7 * Math.sin(t * 0.9 + i * 0.6) + z[j * COLS + i] * 10];
    }
    function wave() {
      var a = [];
      for (var j = 0; j < ROWS; j++) for (var i = 0; i < COLS; i++) {
        var k = j * COLS + i, s = 0, n = 0;
        if (i > 0) { s += z[k - 1]; n++; } if (i < COLS - 1) { s += z[k + 1]; n++; }
        if (j > 0) { s += z[k - COLS]; n++; } if (j < ROWS - 1) { s += z[k + COLS]; n++; }
        a.push(0.35 * (s - n * z[k]));
      }
      for (k = 0; k < z.length; k++) { v[k] = (v[k] + a[k]) * 0.985; }
      for (k = 0; k < z.length; k++) { z[k] += v[k]; }
    }
    var draw = loop(c, function (t) {
      var k, p, q, i, j;
      wave();
      pg.clearRect(0, 0, W, H); pg.drawImage(c, 0, 0);
      g.fillStyle = "#000"; g.fillRect(0, 0, W, H);
      var P = [];
      for (j = 0; j < ROWS; j++) for (i = 0; i < COLS; i++) P.push(knot(i, j, t));
      g.strokeStyle = "rgba(255,210,122,.38)"; g.lineWidth = 1.2; g.beginPath();
      for (j = 0; j < ROWS; j++) for (i = 0; i < COLS; i++) {
        p = P[j * COLS + i];
        if (i < COLS - 1) { q = P[j * COLS + i + 1]; g.moveTo(p[0], p[1]); g.quadraticCurveTo((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 8, q[0], q[1]); }
        if (j < ROWS - 1) { q = P[(j + 1) * COLS + i]; g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]); }
      }
      g.stroke();
      for (k = 0; k < P.length; k++) {
        p = P[k]; var hue = HUES[k % HUES.length], glow = Math.min(1, Math.abs(z[k]) * 1.4);
        g.save(); g.beginPath(); g.arc(p[0], p[1], R, 0, 7); g.clip();
        g.translate(p[0], p[1]); g.scale(-1, 1);
        g.drawImage(prev, -R, -R * H / W * 1.6, 2 * R, 2 * R * H / W * 1.6);
        g.restore();
        g.globalAlpha = 0.16 + 0.3 * glow; g.fillStyle = hue;
        g.beginPath(); g.arc(p[0], p[1], R, 0, 7); g.fill(); g.globalAlpha = 1;
        g.strokeStyle = hue; g.lineWidth = 1.6 + 2 * glow; g.stroke();
        g.fillStyle = "rgba(255,255,255,.75)"; g.beginPath(); g.arc(p[0] - R * 0.38, p[1] - R * 0.4, R * 0.13, 0, 7); g.fill();
      }
    });
    c.addEventListener("click", function (ev) {
      var m = xy(c, ev), best = 0, bd = 1e9, t = performance.now() / 1000;
      for (var j = 0; j < ROWS; j++) for (var i = 0; i < COLS; i++) {
        var p = knot(i, j, t), d = Math.hypot(p[0] - m[0], p[1] - m[1]);
        if (d < bd) { bd = d; best = j * COLS + i; }
      }
      v[best] += 2.2; draw();
    });
    var kick = $("net-pluck");
    if (kick) kick.addEventListener("click", function () { v[Math.floor(Math.random() * v.length)] += 2.2; draw(); });
    bind("net-size", function (val) {
      R = val;
      var d = Math.log(W) / Math.log(W / (2 * R));
      var r = $("net-read");
      if (r) r.innerHTML = "Jewel " + (2 * R) + " px across in a net " + W + " px wide: you can see about <b>" +
        d.toFixed(1) + "</b> reflections deep before a jewel inside a jewel gets smaller than one dot on your screen.";
      draw();
    });
    draw();
  }

  /* ------------------------------------------------------------ 2. the round mirrors
     Circle inversion: the circle (x, y, r) seen in the mirror (X, Y, R). */
  function invert(cx, cy, cr, X, Y, R) {
    var dx = cx - X, dy = cy - Y, s = R * R / (dx * dx + dy * dy - cr * cr);
    return [X + s * dx, Y + s * dy, Math.abs(s) * cr];
  }
  function pearls() {
    var c = $("pearl-canvas"); if (!c) return;
    var W = c.width = 760, H = c.height = 760, g = c.getContext("2d");
    var k = 4, size = 0.96, maxD = 9, breathe = false, start = 0;
    function mirrors(sz) {
      var r = Math.sin(Math.PI / k) * sz, out = [];
      for (var j = 0; j < k; j++) { var a = 2 * Math.PI * j / k - Math.PI / 2; out.push([Math.cos(a), Math.sin(a), r]); }
      return out;
    }
    var draw = loop(c, function (t) {
      if (!start) start = t;
      var sz = breathe ? 0.78 + 0.2 * (0.5 + 0.5 * Math.sin((t - start) * 0.6)) : size;
      var grow = still ? maxD : Math.min(maxD, Math.floor((t - start) * 1.6));
      var M = mirrors(sz), sc = W / 3.3, n = 0, minR = 0.4 / sc;
      g.fillStyle = "#000"; g.fillRect(0, 0, W, H);
      function walk(x, y, r, last, d) {
        n++;
        var px = W / 2 + x * sc, py = H / 2 + y * sc, pr = r * sc;
        g.strokeStyle = HUES[d % HUES.length];
        g.globalAlpha = d === 0 ? 0.95 : Math.max(0.35, 0.9 - 0.06 * d);
        g.lineWidth = d === 0 ? 2 : Math.max(0.5, 1.4 - 0.1 * d);
        g.beginPath(); g.arc(px, py, pr, 0, 7); g.stroke();
        if (d >= grow || r < minR) return;
        for (var j = 0; j < M.length; j++) if (j !== last) {
          var q = invert(x, y, r, M[j][0], M[j][1], M[j][2]);
          walk(q[0], q[1], q[2], j, d + 1);
        }
      }
      for (var j = 0; j < M.length; j++) walk(M[j][0], M[j][1], M[j][2], j, 0);
      g.globalAlpha = 1;
      var r = $("pearl-read");
      if (r) r.innerHTML = "<b>" + k + "</b> mirrors, <b>" + grow + "</b> bounces deep: <b>" +
        n.toLocaleString() + "</b> circles drawn. Without the too-small-to-see cutoff it would be " +
        k + " × " + (k - 1) + "<sup>" + grow + "</sup> = " + (k * Math.pow(k - 1, grow)).toLocaleString() + " at the last bounce alone.";
    });
    function restart() { start = 0; draw(); }
    bind("pearl-k", function (v) { k = v; restart(); });
    bind("pearl-size", function (v) { size = v; restart(); });
    bind("pearl-depth", function (v) { maxD = v; restart(); });
    var b = $("pearl-breathe");
    if (b) b.addEventListener("click", function () { breathe = !breathe; b.setAttribute("aria-pressed", breathe); restart(); });
  }

  /* ------------------------------------------------------------ 3. Fazang's room
     A square room with mirror walls, unfolded: the straight line out to any lamp in the
     grid is the same path, folded, that bounces around the one room. */
  function room() {
    var c = $("room-canvas"); if (!c) return;
    var W = c.width = 900, H = c.height = 620, g = c.getContext("2d");
    var N = 4, lamp = [0.38, 0.62], eye = [0.62, 0.3], target = null, auto = true;
    function img(i, j) { return [i + (i % 2 === 0 ? lamp[0] : 1 - lamp[0]), j + (j % 2 === 0 ? lamp[1] : 1 - lamp[1])]; }
    function fold(v) { var n = Math.floor(v), f = v - n; return (n % 2 === 0) ? f : 1 - f; }
    var sz, ox, oy;
    function P(x, y) { return [ox + x * sz, oy - y * sz]; }
    var order = [];
    var draw = loop(c, function (t) {
      var cells = 2 * N + 1; sz = Math.min(W, H) / cells * 0.96; ox = W / 2 - sz / 2; oy = H / 2 + sz / 2;
      if (auto) {
        order = [];
        for (var i = -N; i <= N; i++) for (var j = -N; j <= N; j++) if (Math.abs(i) + Math.abs(j) <= N && (i || j)) order.push([i, j]);
        order.sort(function (a, b) { return Math.atan2(a[1], a[0]) - Math.atan2(b[1], b[0]) || (Math.abs(a[0]) + Math.abs(a[1])) - (Math.abs(b[0]) + Math.abs(b[1])); });
        target = order[Math.floor(t * 0.7) % order.length];
      }
      g.fillStyle = "#000"; g.fillRect(0, 0, W, H);
      var count = 0;
      for (var i = -N; i <= N; i++) for (var j = -N; j <= N; j++) {
        var b = Math.abs(i) + Math.abs(j); if (b > N) continue; count++;
        var a = P(i, j + 1);
        g.strokeStyle = b === 0 ? "#ffd27a" : "#2a2a38"; g.lineWidth = b === 0 ? 2.5 : 1;
        g.strokeRect(a[0], a[1], sz, sz);
        var L = img(i, j), q = P(L[0], L[1]), op = Math.pow(0.82, b) * (0.85 + 0.15 * Math.sin(t * 9 + i * 3 + j * 5));
        g.globalAlpha = op * 0.2; g.fillStyle = "#ffb347"; g.beginPath(); g.arc(q[0], q[1], sz * 0.3, 0, 7); g.fill();
        g.globalAlpha = op; g.beginPath(); g.arc(q[0], q[1], sz * 0.12, 0, 7); g.fill(); g.globalAlpha = 1;
      }
      var e = P(eye[0], eye[1]);
      if (target) {
        var T = img(target[0], target[1]), tp = P(T[0], T[1]);
        g.setLineDash([6, 6]); g.strokeStyle = "rgba(143,208,255,.55)"; g.lineWidth = 1.4;
        g.beginPath(); g.moveTo(e[0], e[1]); g.lineTo(tp[0], tp[1]); g.stroke(); g.setLineDash([]);
        g.strokeStyle = "#8fd0ff"; g.lineWidth = 2.4; g.beginPath();
        var steps = 600, last = null;
        for (var s = 0; s <= steps; s++) {
          var x = eye[0] + (T[0] - eye[0]) * s / steps, y = eye[1] + (T[1] - eye[1]) * s / steps;
          var f = P(fold(x), fold(y));
          if (s === 0) g.moveTo(f[0], f[1]); else g.lineTo(f[0], f[1]);
        }
        g.stroke();
        var bounces = Math.abs(target[0]) + Math.abs(target[1]);
        var r = $("room-read");
        if (r) r.innerHTML = "The dashed line runs straight out to a lamp <b>" + bounces + "</b> bounce" + (bounces === 1 ? "" : "s") +
          " away. The solid blue line is that same path folded back into the one room — the way the light goes. <b>" + count +
          "</b> lamps within " + N + " bounces: 2 × " + N + "² + 2 × " + N + " + 1.";
      }
      g.fillStyle = "#8fd0ff"; g.beginPath(); g.arc(e[0], e[1], 6, 0, 7); g.fill();
    });
    c.addEventListener("click", function (ev) {
      var m = xy(c, ev), x = (m[0] - ox) / sz, y = (oy - m[1]) / sz, i = Math.floor(x), j = Math.floor(y);
      if (Math.abs(i) + Math.abs(j) <= N) { target = [i, j]; auto = false; draw(); }
    });
    bind("room-n", function (v) { N = v; draw(); });
    var a = $("room-auto");
    if (a) a.addEventListener("click", function () { auto = true; draw(); });
  }

  /* ------------------------------------------------------------ 4. touch one
     Watts–Strogatz: a ring of neighbours, a few hand-holds moved to strangers. Touch a
     knot and the news goes out one hop per tick. */
  function touch() {
    var c = $("touch-canvas"); if (!c) return;
    var W = c.width = 900, H = c.height = 620, g = c.getContext("2d");
    var n = 80, k = 4, p = 0.05, adj = [], seed = 1, dist = null, t0 = 0, src = 0;
    function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
    function build() {
      seed = 12345 + Math.round(p * 1000);
      adj = []; for (var i = 0; i < n; i++) adj.push({});
      for (i = 0; i < n; i++) for (var s = 1; s <= k / 2; s++) { var j = (i + s) % n; adj[i][j] = adj[j][i] = 1; }
      for (i = 0; i < n; i++) for (s = 1; s <= k / 2; s++) {
        j = (i + s) % n;
        if (rnd() < p && adj[i][j]) {
          var tgt; do { tgt = Math.floor(rnd() * n); } while (tgt === i || adj[i][tgt]);
          delete adj[i][j]; delete adj[j][i]; adj[i][tgt] = adj[tgt][i] = 1;
        }
      }
    }
    function bfs(s) {
      var d = []; for (var i = 0; i < n; i++) d.push(-1);
      d[s] = 0; var q = [s];
      while (q.length) { var a = q.shift(); for (var b in adj[a]) { b = +b; if (d[b] < 0) { d[b] = d[a] + 1; q.push(b); } } }
      return d;
    }
    function avgHops() {
      var tot = 0, cnt = 0;
      for (var s = 0; s < n; s++) { var d = bfs(s); for (var i = 0; i < n; i++) if (d[i] > 0) { tot += d[i]; cnt++; } }
      return tot / cnt;
    }
    function pos(i) { var a = 2 * Math.PI * i / n - Math.PI / 2, R = Math.min(W, H) * 0.42; return [W / 2 + R * Math.cos(a), H / 2 + R * Math.sin(a)]; }
    var hops = 0;
    var draw = loop(c, function (t) {
      if (!t0) t0 = t;
      var front = still ? 99 : (t - t0) * 2.2;
      g.fillStyle = "#000"; g.fillRect(0, 0, W, H);
      for (var i = 0; i < n; i++) for (var j in adj[i]) {
        j = +j; if (j < i) continue;
        var a = pos(i), b = pos(j), lit = dist && dist[i] >= 0 && dist[j] >= 0 && Math.max(dist[i], dist[j]) <= front && Math.abs(dist[i] - dist[j]) === 1;
        var far = Math.min((j - i + n) % n, (i - j + n) % n) > k / 2;
        g.strokeStyle = lit ? "rgba(255,210,122,.9)" : far ? "rgba(143,208,255,.45)" : "rgba(255,255,255,.14)";
        g.lineWidth = lit ? 2 : 1;
        g.beginPath(); g.moveTo(a[0], a[1]);
        if (far) g.quadraticCurveTo(W / 2 + (a[0] + b[0] - W) * 0.15, H / 2 + (a[1] + b[1] - H) * 0.15, b[0], b[1]); else g.lineTo(b[0], b[1]);
        g.stroke();
      }
      var reached = 0, maxd = 0;
      for (i = 0; i < n; i++) {
        var q = pos(i), on = dist && dist[i] >= 0 && dist[i] <= front;
        if (on) { reached++; maxd = Math.max(maxd, dist[i]); }
        g.fillStyle = on ? HUES[dist[i] % HUES.length] : "#3a3a4a";
        g.beginPath(); g.arc(q[0], q[1], i === src && dist ? 9 : 6, 0, 7); g.fill();
      }
      var r = $("touch-read");
      if (r) r.innerHTML = (dist ? "The news reached <b>" + reached + "</b> of " + n + " in <b>" + maxd + "</b> hops. " : "Tap any knot. ") +
        "With <b>" + Math.round(p * 100) + "%</b> of hand-holds moved to strangers, the average knot is <b>" + hops.toFixed(2) + "</b> hops from any other.";
    });
    function redo() { build(); hops = avgHops(); if (dist) dist = bfs(src); t0 = 0; draw(); }
    c.addEventListener("click", function (ev) {
      var m = xy(c, ev), best = 0, bd = 1e9;
      for (var i = 0; i < n; i++) { var q = pos(i), d = Math.hypot(q[0] - m[0], q[1] - m[1]); if (d < bd) { bd = d; best = i; } }
      src = best; dist = bfs(src); t0 = 0; draw();
    });
    bind("touch-p", function (v) { p = v / 100; redo(); });
    var b = $("touch-go");
    if (b) b.addEventListener("click", function () { src = Math.floor(Math.random() * n); dist = bfs(src); t0 = 0; draw(); });
  }

  jewelNet(); pearls(); room(); touch();
})();
