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

  // Попап із формою: один раз за сесію (exit-intent на десктопі, ~45 с на мобільному).
  var pop = d.getElementById('leadPopup');
  var form = d.getElementById('leadForm');
  if (pop && form) {
    var seen = false, lastFocus = null;
    try { seen = sessionStorage.getItem('leadPopupSeen') === '1'; } catch (e) {}
    var openPop = function () {
      if (seen || !pop.hidden) return;
      seen = true;
      try { sessionStorage.setItem('leadPopupSeen', '1'); } catch (e) {}
      lastFocus = d.activeElement;
      pop.hidden = false;
      d.documentElement.classList.add('pop-open');
      var f = form.querySelector('input'); if (f) f.focus();
    };
    var closePop = function () {
      pop.hidden = true;
      d.documentElement.classList.remove('pop-open');
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    };
    pop.addEventListener('click', function (ev) {
      if (ev.target === pop || ev.target.hasAttribute('data-pop-close')) closePop();
    });
    d.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && !pop.hidden) closePop(); });
    var fine = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (fine) {
      d.addEventListener('mouseout', function (ev) { if (!ev.relatedTarget && ev.clientY <= 0) openPop(); });
    }
    setTimeout(openPop, fine ? 90000 : 45000);

    var status = form.querySelector('.popup-status');
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var name = form.elements.name.value.trim(), contact = form.elements.contact.value.trim();
      status.className = 'popup-status';
      if (!name || !contact || !form.elements.consent.checked) {
        status.textContent = form.getAttribute('data-req');
        status.classList.add('err');
        (!name ? form.elements.name : !contact ? form.elements.contact : form.elements.consent).focus();
        return;
      }
      var done = function () { status.textContent = form.getAttribute('data-ok'); status.classList.add('ok'); form.reset(); };
      var fail = function () { status.textContent = form.getAttribute('data-err'); status.classList.add('err'); };
      if (cfg.formEndpoint) {
        fetch(cfg.formEndpoint, {
          method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({ name: name, contact: contact, lang: d.documentElement.lang })
        }).then(function (r) { r.ok ? done() : fail(); }).catch(fail);
      } else if (cfg.telegramPersonal) {
        var text = form.getAttribute('data-msg').replace('{name}', name).replace('{contact}', contact);
        window.open(cfg.telegramPersonal + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
        done();
      } else { fail(); }
    });
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
