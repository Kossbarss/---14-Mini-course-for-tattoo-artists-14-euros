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
