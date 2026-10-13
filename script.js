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
        var done = false, once = function () { if (!done) { done = true; go(); } };
        setTimeout(once, 2000);
        fetch(cfg.formEndpoint, {
          method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({ email: email, phone: phone, lang: form.getAttribute('data-lang'), source: src }),
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
      if (!end || end < Date.now()) {
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
