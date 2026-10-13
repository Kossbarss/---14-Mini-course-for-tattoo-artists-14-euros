/* Налаштування лендингу. Змінюйте тільки тут — обидві мови (UA/RU) читають цей файл. */
window.SITE_CONFIG = {
  // Stripe Payment Link (Dashboard → Payment Links → Create → скопіювати https://buy.stripe.com/...).
  // У налаштуваннях лінка: «After payment» → Redirect → https://t.me/mentor_tatoo_Viktoria_bot,
  // щоб бот одразу видав доступ до курсу.
  // Поки порожньо — кнопки ведуть у Telegram Вікторії (запасний варіант).
  stripeLink: '',

  // Адреса для заявок з попапу (напр. Formspree: https://formspree.io/f/xxxx). Приймає POST JSON {name, contact, lang}.
  // Поки порожньо — після відправки відкривається Telegram Вікторії з готовим повідомленням.
  formEndpoint: '',

  telegramPersonal: 'https://t.me/+48733341364',
  telegramBot: 'https://t.me/mentor_tatoo_Viktoria_bot',
  instagram: 'https://www.instagram.com/viktoriia_ponikarova',
  fullCourse: 'https://vip-tattoo-school.com/'
};
