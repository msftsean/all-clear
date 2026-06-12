/* All Clear — Participant Workbook
 * Theme toggle (persisted), scroll progress, section reveal, nav scroll-spy,
 * and a per-exercise "mark done" checklist with a sidebar counter.
 * Loaded as an external file so the strict CSP (script-src 'self') is satisfied.
 */
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');

  /* ---- Theme (dark default; persisted in localStorage) ---- */
  var THEME_KEY = 'allclear-participant-theme';
  try {
    var saved = localStorage.getItem(THEME_KEY);
    if (saved === 'light' || saved === 'dark') doc.setAttribute('data-theme', saved);
  } catch (e) {}

  var toggle = document.getElementById('themeToggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = doc.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      doc.setAttribute('data-theme', next);
      try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
    });
  }

  /* ---- Scroll progress bar ---- */
  var bar = document.querySelector('.progress');
  function onScroll() {
    var h = document.documentElement, max = h.scrollHeight - h.clientHeight;
    if (bar) bar.style.width = (max > 0 ? (h.scrollTop / max * 100) : 0) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- Section reveal + nav scroll-spy ---- */
  var links = [].slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  var map = {};
  links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
  var secs = [].slice.call(document.querySelectorAll('main section[id]'));

  if ('IntersectionObserver' in window) {
    var reveal = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) e.target.classList.add('in'); });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.01 });
    secs.forEach(function (s) { reveal.observe(s); });

    var spy = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) {
          var a = map[e.target.id];
          if (a) { links.forEach(function (l) { l.classList.remove('active'); }); a.classList.add('active'); }
        }
      });
    }, { rootMargin: '-22% 0px -70% 0px', threshold: 0 });
    secs.forEach(function (s) { spy.observe(s); });
  } else {
    secs.forEach(function (s) { s.classList.add('in'); });
  }

  /* ---- Exercise checklist (per-exercise "mark done", persisted) ---- */
  var EXERCISES = ['ex1', 'ex2', 'ex3', 'ex4', 'ex5'];
  var DONE_KEY = 'allclear-participant-done';
  var done = {};
  try { done = JSON.parse(localStorage.getItem(DONE_KEY) || '{}') || {}; } catch (e) { done = {}; }

  function save() { try { localStorage.setItem(DONE_KEY, JSON.stringify(done)); } catch (e) {} }

  function refreshCount() {
    var n = EXERCISES.filter(function (id) { return done[id]; }).length;
    var prog = document.getElementById('railProg');
    if (prog) prog.innerHTML = '<b>' + n + '</b> / ' + EXERCISES.length + ' exercises done';
  }

  EXERCISES.forEach(function (id) {
    var sec = document.getElementById(id);
    if (!sec) return;
    var navLink = map[id];

    var label = document.createElement('label');
    label.className = 'donebox';
    var box = document.createElement('input');
    box.type = 'checkbox';
    box.checked = !!done[id];
    var txt = document.createElement('span');
    txt.textContent = box.checked ? 'Completed' : 'Mark done';
    label.appendChild(box);
    label.appendChild(txt);

    function paint() {
      label.classList.toggle('checked', box.checked);
      txt.textContent = box.checked ? 'Completed' : 'Mark done';
      if (navLink) navLink.classList.toggle('is-done', box.checked);
    }

    box.addEventListener('change', function () {
      done[id] = box.checked;
      save();
      paint();
      refreshCount();
    });

    // Place the control right after the section's <h2>.
    var h2 = sec.querySelector('h2');
    if (h2 && h2.nextSibling) {
      sec.insertBefore(label, h2.nextSibling);
    } else {
      sec.appendChild(label);
    }
    paint();
  });

  refreshCount();
})();
