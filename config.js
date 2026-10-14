/* Налаштування лендингу. Змінюйте тільки тут — обидві мови (UA/RU) читають цей файл. */
window.SITE_CONFIG = {
  // Stripe Payment Link (Dashboard → Payment Links → Create → скопіювати https://buy.stripe.com/...).
  // У налаштуваннях лінка: «After payment» → Redirect → https://t.me/mentor_tatoo_Viktoria_bot,
  // щоб бот одразу видав доступ до курсу.
  // Поки порожньо — кнопки ведуть у Telegram Вікторії (запасний варіант).
  stripeLink: '',

  // Адреса для заявок з попапу: URL веб-застосунку Google Apps Script (заявки потрапляють у Google-таблицю).
  // Інструкція і код: docs/google-sheets-apps-script.gs. Необов'язково: без нього форма просто переадресовує на оплату (Stripe) або в Telegram-канал.
  formEndpoint: '',

  // Таймер акції. promoEnd — реальний кінець акції (напр. '2026-11-01T23:59:00+01:00'), спільний для всіх.
  // Якщо порожньо — кожному відвідувачу іде власний відлік promoHours годин від першого візиту (і так по колу).
  promoEnd: '',
  promoHours: 4,

  telegramPersonal: 'https://t.me/+48733341364',
  telegramChannel: 'https://t.me/+SpNU4aTMO28xYzY0',
  instagram: 'https://www.instagram.com/viktoriia_ponikarova',
  fullCourse: 'https://vip-tattoo-school.com/'
};
