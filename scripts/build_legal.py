#!/usr/bin/env python3
"""Генерує юридичні сторінки: privacy.html, offer.html (UA) і ru/privacy.html, ru/offer.html (RU).

Джерело — чинні документи школи VIP tattoo school (legal_src/: «Умови та положення (Публічна оферта)»
і «Політика конфіденційності» того ж продавця, Viktoria Ponikarova, NIP 6492327660). Скрипт переносить їх
на сторінку міні-курсу і вносить мінімальні точкові правки, щоб текст відповідав фактичній роботі
цього сайту (без cookie/аналітики/CRM, гарантія повернення 14 днів). Кожна правка перевіряється assert-ом.

Запуск: python3 scripts/build_legal.py
УВАГА: це робочий переклад існуючих документів, його має переглянути юрист продавця перед запуском реклами.
"""
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "legal_src"
DATE = "13.10.2026"
SITE = "https://kossbarss.github.io/---14-mini-course-for-tattoo-artists-14-euros"

CFG = {
    "ua": dict(
        lang="uk", og_locale="uk_UA", home="Назад на головну", brand_alt="VIP tattoo school",
        files=dict(terms="offer.html", privacy="privacy.html"),
        descs=dict(terms="Публічна оферта міні-курсу «Тату Старт: Перші лінії» (14 €): умови придбання, доступ до матеріалів, гарантія повернення коштів 14 днів, права й обов'язки сторін.", privacy="Політика конфіденційності міні-курсу «Тату Старт: Перші лінії»: які дані ми збираємо (email, телефон), навіщо, хто їх обробляє, як довго зберігаємо та які у вас права за GDPR."),
        titles=dict(terms="Умови та положення (Публічна оферта) — Тату Старт", privacy="Політика конфіденційності — Тату Старт"),
        dates=("Дата набрання чинності:", "Останнє оновлення:"),
        # --- offer (terms)
        t_website=("зі сторінками за доменом vip-tattoo-school.com", "зі сторінками, що ведуть до продажу курсів Компанії, та сторінкою продажу міні-курсу «Тату Старт: Перші лінії»"),
        t_31_marker="3.1.",
        t_310_marker="3.10.", t_310="3.10. «Політика конфіденційності» означає політику Компанії, опубліковану на Вебсайті. Посилання наведено в Розділі 14.",
        t_25_marker="2.5.",
        t_26="2.6. <strong>Умови міні-курсу «Тату Старт: Перші лінії».</strong> Для цього Цифрового продукту діють такі умови (вони є частиною Договору відповідно до п. 2.5): (a) ціна — 14 € (разовий платіж, оплата через Stripe); (b) формат — онлайн-навчання тривалістю 5 днів (5 відеоуроків, орієнтовно 30–60 хвилин на день); доступ до матеріалів діє 2 місяці з моменту оплати; (c) матеріали та доступ надаються після оплати через закритий Telegram-канал Компанії або особисте повідомлення від Компанії в Telegram; (d) для цього продукту діє гарантія повернення коштів протягом 14 календарних днів відповідно до п. 9.4.",
        t_76_old="(c) <strong>Реєстраційний номер платника ПДВ:</strong> [уточнити — чи зареєстрована Компанія платником ПДВ у Республіці Польща].",
        t_76_new="(c) Інформація про реєстрацію Компанії як платника ПДВ зазначається в документах про оплату (рахунок, чек).",
        t_94_marker="9.4.",
        t_94=("<p>9.4. <strong>Політика повернення коштів.</strong>\n"
              "(a) <strong>Міні-курс «Тату Старт: Перші лінії» — гарантія повернення коштів 14 днів.</strong> Якщо протягом 14 календарних днів з моменту оплати Користувач вирішить, що курс йому не підходить, він може звернутися до Компанії за адресою mentor@victoriaponikarova.online або в Telegram, і Компанія поверне сплачену суму без додаткових пояснень. Повернення здійснюється тим самим способом, яким було здійснено оплату. Ця гарантія діє на додачу до прав Споживача, що випливають з імперативних норм закону.\n"
              "(b) <strong>Інші Цифрові продукти — базова позиція (строга):</strong> після надання доступу до Цифрового контенту або після початку надання Послуги повернення коштів не здійснюється, за винятком випадків, коли обов'язкове законодавство вимагає іншого (наприклад, у разі ненадання, істотної невідповідності або застосування інших передбачених законом засобів захисту).\n"
              "(c) Для таких продуктів запити на повернення коштів приймаються лише до початку надання доступу до курсу, а запити після початку або під час надання не розглядаються, з урахуванням зазначених умов та вирахування фактичних витрат (у тому числі платіжних комісій).\n"
              "(d) Цей підхід узгоджується з обов'язковими нормами ЄС та Республіки Польща щодо цифрового контенту та послуг, включно із ситуаціями ненадання та засобами правового захисту у разі невідповідності.</p>"),
        t_142_marker="14.2.",
        t_142="14.2. <strong>Файли cookie.</strong> Сторінка міні-курсу не встановлює власні файли cookie і не використовує аналітичні скрипти. Сторонні сервіси (платіжна сторінка Stripe, Telegram, Google Fonts) можуть застосовувати власні технології відповідно до своїх політик.",
        t_143_marker="14.3.",
        t_143="14.3. <strong>Сторонні інструменти.</strong> Для роботи сторінки міні-курсу використовуються: обробка платежів — Stripe; збереження контактів із форми — Google Sheets; доставка доступу — Telegram; хостинг сторінки — GitHub Pages; шрифти — Google Fonts. Деталі, правові підстави та механізми відмови від обробки описані в Політиці конфіденційності.",
        # --- privacy
        p_intro=("сайтом https://vip-tattoo-school.com", "сторінкою міні-курсу «Тату Старт: Перші лінії»"),
        p_tech_marker="IP-адреса (використовується сервісом Cloudflare",
        p_tech="Технічні журнали, які ведуть хостинг-провайдер сторінки (GitHub Pages) та платіжний провайдер (Stripe) — зокрема IP-адреса, тип браузера, дата й час запиту; мова сторінки (українська/російська версія). Сторінка міні-курсу не веде власної аналітики.",
        p_src_old="(Stripe, Cloudflare)", p_src_new="(Stripe, Telegram)",
        p_analytics_marker="Аналітика та покращення Сервісів",
        p_analytics="<strong>Аналітика та покращення Сервісів:</strong> сторінка міні-курсу не використовує аналітичних скриптів; технічні журнали, які веде хостинг-провайдер, використовуються лише для безпеки та усунення помилок.\nПравова підстава: законні інтереси.",
        p_cookie_marker="Ми використовуємо файли cookie",
        p_cookie="Сторінка міні-курсу не встановлює власні файли cookie і не використовує cookie-банер. Сторонні сервіси (Stripe під час оплати, Telegram, Google Fonts) можуть застосовувати власні технології відповідно до своїх політик конфіденційності.",
        p_providers_remove=["KeyCRM", "Google Sheets", "Cloudflare", "Cookiebot", "Microsoft Clarity"],
        p_providers_add="<li><strong>Google (Google Sheets / Apps Script)</strong> — збереження контактів (email, телефон), які ви залишаєте у формі на сторінці міні-курсу;</li>\n<li><strong>GitHub Pages</strong> — хостинг сторінки;</li>\n<li><strong>Google Fonts</strong> — завантаження шрифтів;</li>",
        p_provider_anchor="<strong>Telegram</strong>",
        p_logs_marker="Технічні журнали та аналітичні дані",
        p_logs="Технічні журнали: зберігаються постачальниками послуг відповідно до їхніх політик та налаштувань.",
        post=[("доставка матеріалів через Telegram-бот або закритий Telegram-канал", "доставка матеріалів через закритий Telegram-канал або особисте повідомлення в Telegram")],
        post_p=[("доступ до курсу надається через Telegram-бот/закритий канал після оплати", "доступ до курсу надається через закритий Telegram-канал або особисте повідомлення в Telegram після оплати. На сторінці міні-курсу ви можете залишити email і номер телефону, щоб отримати доступ, підтвердження та підтримку"),
                ("доставка доступу до курсу через бот/закритий канал", "доставка доступу до курсу через закритий канал або особисте повідомлення"),
                ("- підтвердження платежів.", "- підтвердження платежів;\n- зв'язок з вами щодо доступу до курсу, якщо ви залишили email або номер телефону у формі на сторінці міні-курсу (дані зберігаються в таблиці Google, доступ до якої мають лише Компанія та уповноважені нею особи).")],
        p_forms=[("через форму замовлення, електронну пошту або Telegram", "через форму на сторінці міні-курсу (email і номер телефону), сторінку оплати Stripe, електронну пошту або Telegram"),
                 ("через форму замовлення на Сервісах", "через форму на сторінці міні-курсу, сторінку оплати Stripe або Telegram")],
    ),
    "ru": dict(
        lang="ru", og_locale="ru_RU", home="Назад на главную", brand_alt="VIP tattoo school",
        files=dict(terms="offer.html", privacy="privacy.html"),
        descs=dict(terms="Публичная оферта мини-курса «Тату Старт: Первые линии» (14 €): условия приобретения, доступ к материалам, гарантия возврата средств 14 дней, права и обязанности сторон.", privacy="Политика конфиденциальности мини-курса «Тату Старт: Первые линии»: какие данные мы собираем (email, телефон), зачем, кто их обрабатывает, как долго храним и какие у вас права по GDPR."),
        titles=dict(terms="Условия и положения (Публичная оферта) — Тату Старт", privacy="Политика конфиденциальности — Тату Старт"),
        dates=("Дата вступления в силу:", "Последнее обновление:"),
        t_website=("страницы по домену vip-tattoo-school.com", "страницы, ведущие к продаже курсов Компании, и страницу продажи мини-курса «Тату Старт: Первые линии»"),
        t_31_marker="3.1.",
        t_310_marker="3.10.", t_310="3.10. «Политика конфиденциальности» означает политику Компании, опубликованную на Вебсайте. Ссылка приведена в Разделе 14.",
        t_25_marker="2.5.",
        t_26="2.6. <strong>Условия мини-курса «Тату Старт: Первые линии».</strong> Для этого Цифрового продукта действуют следующие условия (они являются частью Договора в соответствии с п. 2.5): (a) цена — 14 € (разовый платёж, оплата через Stripe); (b) формат — онлайн-обучение продолжительностью 5 дней (5 видеоуроков, ориентировочно 30–60 минут в день); доступ к материалам действует 2 месяца с момента оплаты; (c) материалы и доступ предоставляются после оплаты через закрытый Telegram-канал Компании или личное сообщение от Компании в Telegram; (d) для этого продукта действует гарантия возврата средств в течение 14 календарных дней в соответствии с п. 9.4.",
        t_76_old="(c) <strong>Регистрационный номер плательщика НДС:</strong> [уточнить — зарегистрирована ли Компания плательщиком НДС в Республике Польша].",
        t_76_new="(c) Информация о регистрации Компании в качестве плательщика НДС указывается в платёжных документах (счёт, чек).",
        t_94_marker="9.4.",
        t_94=("<p>9.4. <strong>Политика возврата средств.</strong>\n"
              "(a) <strong>Мини-курс «Тату Старт: Первые линии» — гарантия возврата средств 14 дней.</strong> Если в течение 14 календарных дней с момента оплаты Пользователь решит, что курс ему не подходит, он может обратиться к Компании по адресу mentor@victoriaponikarova.online или в Telegram, и Компания вернёт уплаченную сумму без дополнительных объяснений. Возврат осуществляется тем же способом, которым была произведена оплата. Эта гарантия действует в дополнение к правам Потребителя, вытекающим из императивных норм закона.\n"
              "(b) <strong>Прочие Цифровые продукты — базовая позиция (строгая):</strong> после предоставления доступа к Цифровому контенту или после начала предоставления Услуги возврат средств не осуществляется, за исключением случаев, когда обязательное законодательство требует иного (например, в случае непредоставления, существенного несоответствия или применения иных предусмотренных законом средств защиты).\n"
              "(c) Для таких продуктов запросы на возврат средств принимаются только до начала предоставления доступа к курсу, а запросы после начала или во время предоставления не рассматриваются, с учётом указанных условий и вычета фактических расходов (в том числе платёжных комиссий).\n"
              "(d) Данный подход согласуется с обязательными нормами ЕС и Республики Польша относительно цифрового контента и услуг, включая ситуации непредоставления и средства правовой защиты в случае несоответствия.</p>"),
        t_142_marker="14.2.",
        t_142="14.2. <strong>Файлы cookie.</strong> Страница мини-курса не устанавливает собственные файлы cookie и не использует аналитические скрипты. Сторонние сервисы (платёжная страница Stripe, Telegram, Google Fonts) могут применять собственные технологии в соответствии со своими политиками.",
        t_143_marker="14.3.",
        t_143="14.3. <strong>Сторонние инструменты.</strong> Для работы страницы мини-курса используются: обработка платежей — Stripe; сохранение контактов из формы — Google Sheets; доставка доступа — Telegram; хостинг страницы — GitHub Pages; шрифты — Google Fonts. Детали, правовые основания и механизмы отказа от обработки описаны в Политике конфиденциальности.",
        p_intro=("сайтом https://vip-tattoo-school.com", "страницей мини-курса «Тату Старт: Первые линии»"),
        p_tech_marker="IP-адрес (используется сервисом Cloudflare",
        p_tech="Технические журналы, которые ведут хостинг-провайдер страницы (GitHub Pages) и платёжный провайдер (Stripe) — в частности IP-адрес, тип браузера, дата и время запроса; язык страницы (украинская/русская версия). Страница мини-курса не ведёт собственной аналитики.",
        p_src_old="(Stripe, Cloudflare)", p_src_new="(Stripe, Telegram)",
        p_analytics_marker="Аналитика и улучшение Сервисов",
        p_analytics="<strong>Аналитика и улучшение Сервисов:</strong> страница мини-курса не использует аналитических скриптов; технические журналы, которые ведёт хостинг-провайдер, используются только для безопасности и устранения ошибок.\nПравовое основание: законные интересы.",
        p_cookie_marker="Мы используем файлы cookie",
        p_cookie="Страница мини-курса не устанавливает собственные файлы cookie и не использует cookie-баннер. Сторонние сервисы (Stripe во время оплаты, Telegram, Google Fonts) могут применять собственные технологии в соответствии со своими политиками конфиденциальности.",
        p_providers_remove=["KeyCRM", "Google Sheets", "Cloudflare", "Cookiebot", "Microsoft Clarity"],
        p_providers_add="<li><strong>Google (Google Sheets / Apps Script)</strong> — сохранение контактов (email, телефон), которые вы оставляете в форме на странице мини-курса;</li>\n<li><strong>GitHub Pages</strong> — хостинг страницы;</li>\n<li><strong>Google Fonts</strong> — загрузка шрифтов;</li>",
        p_provider_anchor="<strong>Telegram</strong>",
        p_logs_marker="Технические журналы и аналитические данные",
        p_logs="Технические журналы: хранятся поставщиками услуг в соответствии с их политиками и настройками.",
        post=[("доставка материалов через Telegram-бот или закрытый Telegram-канал", "доставка материалов через закрытый Telegram-канал или личное сообщение в Telegram")],
        post_p=[("доступ к курсу предоставляется через Telegram-бот/закрытый канал после оплаты", "доступ к курсу предоставляется через закрытый Telegram-канал или личное сообщение в Telegram после оплаты. На странице мини-курса вы можете оставить email и номер телефона, чтобы получить доступ, подтверждение и поддержку"),
                ("доставка доступа к курсу через бот/закрытый канал", "доставка доступа к курсу через закрытый канал или личное сообщение"),
                ("- подтверждение платежей.", "- подтверждение платежей;\n- связь с вами по вопросам доступа к курсу, если вы оставили email или номер телефона в форме на странице мини-курса (данные хранятся в таблице Google, доступ к которой имеют только Компания и уполномоченные ею лица).")],
        p_forms=[("через форму заказа, электронную почту или Telegram", "через форму на странице мини-курса (email и номер телефона), страницу оплаты Stripe, электронную почту или Telegram"),
                 ("через форму заказа на Сервисах", "через форму на странице мини-курса, страницу оплаты Stripe или Telegram")],
    ),
}

EL = re.compile(r"<(p|li)\b[^>]*>.*?</\1>", re.S)


def text_of(frag):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", frag))).strip()


def find_one(html, marker, tags=("p", "li")):
    numbered = re.fullmatch(r"\d+\.\d+\.", marker) is not None
    hits = [m for m in EL.finditer(html) if m.group(1) in tags and
            ((text_of(m.group(0)).startswith(marker)) if numbered else (marker in text_of(m.group(0))))]
    assert len(hits) == 1, f"маркер {marker!r}: знайдено {len(hits)}"
    return hits[0]


def replace_el(html, marker, new_inner_or_el, wrap="p"):
    m = find_one(html, marker)
    new = new_inner_or_el if new_inner_or_el.lstrip().startswith("<") else f"<{wrap}>{new_inner_or_el}</{wrap}>"
    return html[: m.start()] + new + html[m.end():]


def remove_el(html, marker):
    m = find_one(html, marker)
    return html[: m.start()] + html[m.end():].lstrip("\n")


def article_of(src):
    m = re.search(r'<article class="legal-content">(.*?)</article>', src, re.S)
    assert m, "немає <article>"
    return m.group(1)


def build_terms(lang):
    c = CFG[lang]
    html = article_of((SRC / f"terms-{lang}.html").read_text(encoding="utf-8"))
    html = re.sub(r'\s*<p class="legal-meta">.*?</p>', "", html, count=1, flags=re.S)
    d1, d2 = c["dates"]
    for lab in (d1, d2):
        pat = re.compile(r"(<strong>" + re.escape(lab) + r"</strong>)\s*\[[^\]]+\]")
        assert pat.search(html), lab
        html = pat.sub(lambda m: m.group(1) + " " + DATE, html, count=1)
    old, new = c["t_website"]; assert old in html; html = html.replace(old, new, 1)
    html = replace_el(html, c["t_310_marker"], c["t_310"])
    m = find_one(html, c["t_25_marker"]); html = html[: m.end()] + "\n" + f"<p>{c['t_26']}</p>" + html[m.end():]
    assert c["t_76_old"] in html; html = html.replace(c["t_76_old"], c["t_76_new"], 1)
    html = replace_el(html, c["t_94_marker"], c["t_94"])
    html = replace_el(html, c["t_142_marker"], c["t_142"])
    html = replace_el(html, c["t_143_marker"], c["t_143"])
    for o, n in c["post"]:
        assert o in html, o
        html = html.replace(o, n)
    return html


def build_privacy(lang):
    c = CFG[lang]
    html = article_of((SRC / f"privacy-{lang}.html").read_text(encoding="utf-8"))
    html = re.sub(r'\s*<p class="legal-meta">.*?</p>', "", html, count=1, flags=re.S)
    d1, d2 = c["dates"]
    for lab in (d1, d2):
        pat = re.compile(r"(<strong>" + re.escape(lab) + r"</strong>)\s*\[[^\]]+\]")
        assert pat.search(html), lab
        html = pat.sub(lambda m: m.group(1) + " " + DATE, html, count=1)
    old, new = c["p_intro"]; assert old in html; html = html.replace(old, new, 1)
    # технічні дані: у джерелі це «<p><strong>Заголовок</strong>\nТекст…</p>» — міняємо лише текстову частину
    m = find_one(html, c["p_tech_marker"])
    frag = m.group(0)
    head = re.match(r"(<p>\s*<strong>.*?</strong>)", frag, re.S)
    assert head, "тех. дані: немає заголовка"
    html = html[: m.start()] + head.group(1) + "\n" + c["p_tech"] + "</p>" + html[m.end():]
    assert c["p_src_old"] in html; html = html.replace(c["p_src_old"], c["p_src_new"], 1)
    for old, new in c["p_forms"]:
        assert old in html, old
        html = html.replace(old, new, 1)
    html = replace_el(html, c["p_analytics_marker"], "<p>" + c["p_analytics"] + "</p>")
    html = replace_el(html, c["p_cookie_marker"], c["p_cookie"])
    for prov in c["p_providers_remove"]:
        html = _rm_provider(html, prov)
    # додати GitHub Pages + Google Fonts перед Telegram (останній пункт списку закінчується крапкою)
    anchor = "<li>" + c["p_provider_anchor"]
    assert html.count(anchor) == 1, anchor
    html = html.replace(anchor, c["p_providers_add"] + "\n" + anchor, 1)
    html = re.sub(r";(\s*</li>\s*</ul>)", r".\1", html, count=1)
    for o, n in c["post_p"]:
        assert o in html, o
        html = html.replace(o, n)
    m = find_one(html, c["p_logs_marker"]); html = html[: m.start()] + replace_log(m.group(0), c["p_logs"]) + html[m.end():]
    return html


def _rm_provider(html, prov):
    pat = re.compile(r"\s*<li><strong>" + re.escape(prov) + r"</strong>.*?</li>", re.S)
    assert len(pat.findall(html)) == 1, prov
    return pat.sub("", html, count=1)


def replace_log(frag, new_text):
    # у джерелі: «<p><strong>Технічні журнали…</strong>: …</p>» або «<li>Технічні журнали…: …</li>»
    tag = re.match(r"<(p|li)", frag).group(1)
    return f"<{tag}>{new_text}</{tag}>"


def fix_links(html, lang):
    """Підставляє наші відносні посилання замість {{…}} і прибирає посилання на неіснуючу cookie-політику."""
    html = re.sub(r'<a href="\{\{COOKIE_[A-Z]+_URL\}\}"[^>]*>(.*?)</a>', lambda m: m.group(1), html)
    html = html.replace("{{PRIVACY_UA_URL}}", "privacy.html").replace("{{PRIVACY_RU_URL}}", "privacy.html")
    html = html.replace("{{TERMS_UA_URL}}", "offer.html").replace("{{TERMS_RU_URL}}", "offer.html")
    assert "{{" not in html, re.findall(r"\{\{[^}]+\}\}", html)
    return html


def page(lang, kind, body):
    c = CFG[lang]
    p = "" if lang == "ua" else "../"
    title = c["titles"][kind]
    desc = c["descs"][kind].replace('"', "&quot;")
    fn = c["files"][kind]
    url_ua, url_ru = f"{SITE}/{fn}", f"{SITE}/ru/{fn}"
    url = url_ua if lang == "ua" else url_ru
    h1 = re.search(r"<h1>(.*?)</h1>", body, re.S).group(1)
    other = ("ru/" if lang == "ua" else "../") + c["files"][kind] if lang == "ua" else "../" + c["files"][kind]
    other_label = "RU" if lang == "ua" else "UA"
    return f"""<!DOCTYPE html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="index,follow">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="uk" href="{url_ua}">
<link rel="alternate" hreflang="ru" href="{url_ru}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="VIP tattoo school">
<meta property="og:locale" content="{c['og_locale']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-cover.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}assets/favicon-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Roboto+Flex:wght@700&display=swap&subset=cyrillic,latin" rel="stylesheet">
<link rel="stylesheet" href="{p}style.css?v=@@STYLE@@">
</head>
<body class="legal-body">
<header class="legal-header"><div class="container">
  <a class="brand" href="{p or './'}"><img src="{p}assets/logo-mark.png" alt="{c['brand_alt']}" width="56" height="56">VIP tattoo school</a>
  <a class="legal-back" href="{p or './'}">{c['home']}</a>
</div></header>
<main><article class="legal-content container">{body}</article></main>
<footer class="legal-foot"><div class="container">
  <a href="privacy.html">{"Політика конфіденційності" if lang == "ua" else "Политика конфиденциальности"}</a>
  <a href="offer.html">{"Договір оферти" if lang == "ua" else "Договор оферты"}</a>
  <a href="{other}">{other_label}</a>
  <span>Viktoria Ponikarova · NIP 6492327660</span>
</div></footer>
</body>
</html>
"""


def main():
    from hashlib import md5
    style_ver = md5((ROOT / "style.css").read_bytes()).hexdigest()[:8]
    for lang in ("ua", "ru"):
        outdir = ROOT if lang == "ua" else ROOT / "ru"
        outdir.mkdir(exist_ok=True)
        body = build_terms(lang)
        body = fix_links(body, lang)
        (outdir / "offer.html").write_text(page(lang, "terms", body).replace("@@STYLE@@", style_ver), encoding="utf-8")
        body = fix_links(build_privacy(lang), lang)
        (outdir / "privacy.html").write_text(page(lang, "privacy", body).replace("@@STYLE@@", style_ver), encoding="utf-8")
    print("built legal pages: offer.html, privacy.html (UA, RU)")


if __name__ == "__main__":
    main()
