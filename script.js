/* Мінімум JS: CTA → Stripe, sticky-панель, поява блоків при скролі. */
(function () {
  var cfg = window.SITE_CONFIG || {};
  var d = document;
  d.documentElement.classList.remove('no-js');

  // CTA: Stripe Payment Link, а якщо його ще не вказано — Telegram Вікторії.
  var pay = cfg.stripeLink || cfg.telegramPersonal || '#';
  d.querySelectorAll('[data-cta]').forEach(function (a) {
    a.href = pay;
    if (/^https?:/.test(pay)) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
  });
  d.querySelectorAll('[data-link]').forEach(function (a) {
    var url = cfg[a.getAttribute('data-link')];
    if (url) { a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; }
  });

  // Sticky-панель: з'являється після hero і ховається біля фінального CTA.
  var sticky = d.querySelector('.sticky');
  var hero = d.querySelector('.hero');
  var final = d.querySelector('#final');
  function toggleSticky() {
    if (!sticky || !hero) return;
    var y = window.scrollY, vh = window.innerHeight;
    var pastHero = y > hero.offsetHeight - 120;
    var atFinal = final && final.getBoundingClientRect().top < vh * 0.6;
    sticky.classList.toggle('show', pastHero && !atFinal);
  }
  window.addEventListener('scroll', toggleSticky, { passive: true });
  toggleSticky();

  // Попап (структура з лендингу VIP tattoo): відкривається з усіх CTA-кнопок і sticky-панелі.
  // Форма: email + телефон → заявка (за наявності formEndpoint) → Stripe Payment Link
  // (з підстановкою email), а поки його немає — Telegram-канал.
  var overlay = d.getElementById('popupOverlay');
  var card = d.getElementById('popupCard');
  var form = d.getElementById('popupForm');
  if (overlay && card && form) {
    var lastFocus = null;
    var setOpen = function (open) {
      overlay.classList.toggle('open', open);
      card.classList.toggle('open', open);
      d.body.classList.toggle('popup-open', open);
      overlay.setAttribute('aria-hidden', String(!open));
      card.setAttribute('aria-hidden', String(!open));
      if (open) {
        lastFocus = d.activeElement;
        setTimeout(function () { var c = d.getElementById('popupClose'); if (c) c.focus(); }, 0);
      } else if (lastFocus && lastFocus.focus) { lastFocus.focus(); }
    };
    setOpen(false);
    d.querySelectorAll('[data-cta]').forEach(function (a) {
      a.addEventListener('click', function (ev) {
        ev.preventDefault();
        try { sessionStorage.setItem('popup_source', (a.textContent || '').trim()); } catch (e) {}
        setOpen(true);
      });
    });
    d.getElementById('popupClose').addEventListener('click', function () { setOpen(false); });
    overlay.addEventListener('click', function () { setOpen(false); });
    d.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && card.classList.contains('open')) { setOpen(false); return; }
      if (ev.key === 'Tab' && card.classList.contains('open')) {
        var f = card.querySelectorAll('a[href],button:not([disabled]),input:not([disabled])');
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (ev.shiftKey && d.activeElement === first) { ev.preventDefault(); last.focus(); }
        else if (!ev.shiftKey && d.activeElement === last) { ev.preventDefault(); first.focus(); }
      }
    });

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!form.reportValidity()) return;
      var email = form.elements.email.value.trim(), phone = form.elements.phone.value.trim();
      var btn = form.querySelector('button[type=submit]'), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = form.getAttribute('data-loading');
      var src = ''; try { src = sessionStorage.getItem('popup_source') || ''; } catch (e) {}
      var go = function () {
        var url = cfg.stripeLink;
        if (url) {
          url += (url.indexOf('?') > -1 ? '&' : '?') + 'prefilled_email=' + encodeURIComponent(email);
        } else { url = cfg.telegramChannel || cfg.telegramPersonal; }
        if (!url) { btn.disabled = false; btn.innerHTML = label; alert(form.getAttribute('data-err')); return; }
        window.location.href = url;
      };
      if (cfg.formEndpoint) {
        // Заявку не чекаємо довше 2 с, щоб не гальмувати перехід до оплати.
        // text/plain + no-cors: Google Apps Script (Google-таблиця) не відповідає на CORS-preflight.
        var done = false, once = function () { if (!done) { done = true; go(); } };
        setTimeout(once, 2000);
        var qs = new URLSearchParams(window.location.search);
        fetch(cfg.formEndpoint, {
          method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: JSON.stringify({
            email: email, phone: phone, lang: form.getAttribute('data-lang'), source: src,
            utm_source: qs.get('utm_source') || '', utm_medium: qs.get('utm_medium') || '', utm_campaign: qs.get('utm_campaign') || '',
            page: window.location.pathname
          }),
          keepalive: true
        }).then(once, once);
      } else { go(); }
    });
  }

  // Таймер акції. cfg.promoEnd (ISO-дата) — реальний спільний дедлайн; інакше — індивідуальний
  // відлік cfg.promoHours годин від першого візиту (зберігається в localStorage), після нуля стартує знову.
  var tEls = { h: d.querySelectorAll('[data-timer="h"]'), m: d.querySelectorAll('[data-timer="m"]'), s: d.querySelectorAll('[data-timer="s"]') };
  if (tEls.s.length) {
    var span = (cfg.promoHours || 9) * 3600000, fixedEnd = cfg.promoEnd ? Date.parse(cfg.promoEnd) : NaN;
    var end = fixedEnd;
    if (isNaN(end)) {
      try { end = parseInt(localStorage.getItem('promoEnd'), 10); } catch (e) {}
      if (!end || end < Date.now() || end > Date.now() + span) {
        end = Date.now() + span;
        try { localStorage.setItem('promoEnd', String(end)); } catch (e) {}
      }
    }
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var tick = function () {
      var left = end - Date.now();
      if (left <= 0) {
        if (isNaN(fixedEnd)) { end = Date.now() + span; try { localStorage.setItem('promoEnd', String(end)); } catch (e) {} left = span; }
        else left = 0;
      }
      var sec = Math.floor(left / 1000), v = { h: pad(Math.floor(sec / 3600)), m: pad(Math.floor(sec % 3600 / 60)), s: pad(sec % 60) };
      ['h', 'm', 's'].forEach(function (k) { tEls[k].forEach(function (el) { el.textContent = v[k]; }); });
    };
    tick();
    setInterval(tick, 1000);
  }

  // «Роботи студентів»: безкінечна стрічка (авто-прокрутка + перетягування), пауза при наведенні.
  var wm = d.querySelector('[data-works-marquee]');
  var wt = wm && wm.querySelector('.works-track');
  if (wt && !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    var setHtml = wt.innerHTML; wt.insertAdjacentHTML('beforeend', setHtml);
    var half = 0, x = 0, speed = 36, hover = false, drag = false, startX = 0, startOff = 0, visible = true, last = 0;
    var measure = function () { half = wt.scrollWidth / 2; };
    var apply = function () { if (half) { x = ((x % half) + half) % half; } wt.style.transform = 'translate3d(' + (-x) + 'px,0,0)'; };
    measure(); window.addEventListener('resize', measure); window.addEventListener('load', measure);
    wm.addEventListener('mouseenter', function () { hover = true; });
    wm.addEventListener('mouseleave', function () { hover = false; });
    wt.addEventListener('pointerdown', function (ev) {
      drag = true; startX = ev.clientX; startOff = x; wt.classList.add('is-dragging'); wt.setPointerCapture(ev.pointerId);
    });
    wt.addEventListener('pointermove', function (ev) { if (drag) { x = startOff - (ev.clientX - startX); apply(); } });
    var endDrag = function () { drag = false; wt.classList.remove('is-dragging'); };
    wt.addEventListener('pointerup', endDrag); wt.addEventListener('pointercancel', endDrag);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(wm);
    }
    var frame = function (t) {
      if (last && visible && !hover && !drag) { x += speed * Math.min(t - last, 64) / 1000; apply(); }
      last = t; requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  }

  // Свайп по рамці відгуку (палець або миша): вліво — наступний кейс, вправо — попередній.
  // Працює через ті самі стрілки каруселі, тож індикатор і 3D-галерея синхронізуються.
  (function () {
    var sx = 0, sy = 0, st = 0, tracking = false;
    var inDetail = function (t) { return t && t.closest && t.closest('#caseFanLayout .case-carousel-detail'); };
    d.addEventListener('pointerdown', function (ev) {
      if (ev.pointerType === 'mouse' && ev.button !== 0) return;
      if (!inDetail(ev.target)) { tracking = false; return; }
      tracking = true; sx = ev.clientX; sy = ev.clientY; st = Date.now();
    }, { passive: true });
    d.addEventListener('pointerup', function (ev) {
      if (!tracking) return;
      tracking = false;
      var dx = ev.clientX - sx, dy = ev.clientY - sy;
      if (Date.now() - st > 800 || Math.abs(dx) < 45 || Math.abs(dx) < Math.abs(dy) * 1.4) return;
      var arrows = d.querySelectorAll('#caseFanLayout .case-carousel-dots-arrow');
      if (arrows.length < 2) return;
      arrows[dx < 0 ? 1 : 0].click();
    }, { passive: true });
    d.addEventListener('pointercancel', function () { tracking = false; }, { passive: true });
  })();

  // Поява при скролі.
  var items = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }
})();
