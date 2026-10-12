#!/usr/bin/env python3
"""Генерує index.html (UA) і ru/index.html (RU) з одного шаблону.

Правте тексти тут (словники UA / RU нижче), потім: python3 scripts/build.py
Так обидві мови завжди залишаються дзеркальними.
"""
from html import escape
from hashlib import md5
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ver(rel):
    """Короткий хеш вмісту файлу — додається як ?v=… щоб телефони не показували стару версію з кешу."""
    return md5((ROOT / rel).read_bytes()).hexdigest()[:8]


SITE = "https://kossbarss.github.io/---14-mini-course-for-tattoo-artists-14-euros"

UA = dict(
    lang="uk", other_lang="ru", other_label="RU",
    title="Тату Старт: перші лінії за 5 днів — Вікторія Поникарова",
    desc="Онлайн-міні-курс від Вікторії Поникарової, засновниці VIP tattoo school: за 5 днів зробиш перші лінії на штучній шкірі й зрозумієш, чи готовий до першого клієнта. 14 € замість 99 €.",
    badge="Онлайн-міні-курс від Вікторії Поникарової",
    h1="Перші лінії <em>без страху</em> зіпсувати шкіру",
    sub="Хочеш у тату, але не знаєш, з чого почати, і боїшся дорогих помилок? За 5 днів ти зробиш перші лінії на штучній шкірі й зрозумієш, чи твоя це професія.",
    hero_list=[
        "Розберешся, яке обладнання справді потрібне на старті — без зайвих витрат",
        "Навчишся тримати машинку й вести рівні лінії",
        "Зрозумієш, коли можна переходити зі штучної шкіри на людину",
    ],
    cta="Забрати за 14 €", old="99 €", new="14 €",
    price_note="Доступ одразу після оплати · 14 днів гарантія повернення коштів",
    tags=["5 днів", "Онлайн", "Практика на штучній шкірі", "Зворотний зв'язок від Вікторії"],
    chip_b="Вікторія Поникарова", chip_s="Засновниця Sarna Tattoo і VIP tattoo school",
    stats=[("300+", "випускників школи"), ("22+", "країни, де цінують роботи учнів"),
           ("12", "студій-партнерів в Україні та Європі"), ("14", "днів гарантії повернення")],
    pain_eyebrow="Впізнаєш себе?", pain_title="Чому більшість новачків <em>застрягають</em> на старті",
    pain_lead="Якщо впізнав себе хоча б в одному пункті — цей міні-курс для тебе.",
    pains=[
        ("Мрієш, але відкладаєш", "Здається, що спершу треба ідеально малювати, купити дороге обладнання або «дочекатися моменту». Місяці йдуть, а першого кроку так і немає."),
        ("YouTube без системи", "Один майстер радить одне, інший — інше. Інформації багато, а розуміння, з чого починати, немає. Ментора теж немає."),
        ("Боїшся зіпсувати малюнок на шкірі", "Страх помилки й шкоди клієнту тримає на місці. Теорія є, а до практики справа не доходить."),
        ("«Без таланту нічого не вийде»", "Ти думаєш, що тату — лише для тих, хто малює від природи. Насправді це техніка і практика, а їх можна відпрацювати."),
    ],
    prog_eyebrow="Програма", prog_title="5 днів: від безпеки до <em>першого клієнта</em>",
    prog_lead="Кожного дня — новий урок і практичне завдання на штучній шкірі. 30–60 хвилин на день.",
    day_word="День",
    days=[
        ("Старт і безпека", ["Як насправді виглядає професія тату-майстра", "Стерилізація, гігієна і організація робочого місця", "Список обладнання для старту: що купувати, а що ні"], "Зрозумієш, з чого складається робота майстра, і не витратиш гроші даремно."),
        ("Машинка, голки і шкіра", ["Як працює тату-машинка і як її налаштувати", "Які бувають голки та для чого вони", "Глибина проколу й робота зі шкірою"], "Розберешся в обладнанні й принципі роботи зі шкірою."),
        ("Лінія і постановка руки", ["Як тримати машинку й натягувати шкіру", "Трафарети-прописі для твердої руки", "Рівні лінії та щільний закрас"], "Виконаєш свої перші лінії на штучній шкірі."),
        ("Ескіз і AI-асистент", ["Від ідеї до ескізу й трафарету", "Огляд тату-стилів: з чого обрати свій", "Особистий tattoo AI-асистент: ідеї, ескізи, робочі задачі"], "Створиш ескіз за допомогою AI і зробиш за ним практику."),
        ("Перший клієнт і що далі", ["Коли можна переходити зі штучної шкіри на людину", "Як рахувати вартість роботи й не працювати собі в збиток", "Портфоліо і шлях до перших клієнтів"], "Матимеш чіткий план: що відпрацьовувати далі."),
    ],
    bonus_eyebrow="У вартість входить", bonus_title="Бонуси до <em>міні-курсу</em>",
    bonuses=[
        ("Список обладнання для старту", "Перелік того, що справді потрібне на початку. Базовий набір для навчання на штучній шкірі коштує від 60–80 €."),
        ("Особистий tattoo AI-асистент", "Допомагає створювати й допрацьовувати ескізи, шукати ідеї та швидше вирішувати робочі задачі. Працює на даних курсу і студії Sarna."),
        ("Калькулятор вартості тату", "Шаблон для розрахунку ціни роботи, щоб не працювати собі в збиток."),
        ("Ескізи й трафарети для перших робіт", "Готові ескізи в різних стилях, з якими можна практикувати одразу."),
    ],
    instr_badge="Привіт, я Вікторія Поникарова",
    instr_h2="Чому моя методика працює, навіть якщо ти тримаєш машинку вперше",
    instr_p="Я не теоретик, а практикуюча майстриня, яка щодня працює з клієнтами і бачить, які помилки роблять новачки. У мене вища художня освіта і величезна насмотреність — перш ніж знайти свій стиль, я спробувала працювати в різних стилях, тому точно допоможу тобі знайти свою сильну сторону і опанувати всі технічні навички.",
    instr_list=[
        "Засновниця студії <strong>«Sarna Tattoo»</strong>, переможниця Personal Branding Awards Poland Ukraine та обличчя обкладинки Bomond VIP",
        "<strong>300+ випускників</strong> навчання, які вже працюють з клієнтами",
        "Учні VIP tattoo виконали <strong>2000+ робіт</strong> лише за 2025 рік",
        "Досвід навчання новачків у <strong>12 студіях-партнерах</strong> по Україні та Європі",
    ],
    instr_stats=[("instructorStatMakeup", "80%", "робіт з перманентного макіяжу — без жодної корекції"),
                 ("instructorStatGraduates", "300+", "випускників, які вже працюють з клієнтами"),
                 ("instructorStatWorks", "2000+", "робіт виконали учні тату-навчання за 2025 рік"),
                 ("instructorStatPartners", "12", "студій-партнерів визнають сертифікат навчання")],
    res_eyebrow="Результати", res_title="Роботи й учні <em>VIP tattoo school</em>",
    res_lead="Учні школи з різних країн. Усі почали з нуля.",
    how_eyebrow="Як проходить навчання", how_title="4 кроки до <em>перших ліній</em>",
    steps=[
        ("Оплачуєш за спеціальною ціною", "Stripe: безпечна оплата карткою. Одразу отримуєш доступ у Telegram."),
        ("Новий урок щодня", "Дивишся короткі відеоуроки у зручний час і одразу переходиш до практики."),
        ("Виконуєш завдання", "Практикуєшся на штучній шкірі й надсилаєш результат."),
        ("Отримуєш зворотний зв'язок", "Вікторія розбирає роботу: що зроблено правильно, де помилки й як їх виправити."),
    ],
    vs_title="Було / <em>Стане</em>", vs_was="Зараз", vs_will="Через 5 днів",
    vs_was_l=["Мрієш про тату-професію, але не знаєш, з чого почати", "Губишся в суперечливих порадах з інтернету", "Боїшся купити не те обладнання й витратити гроші даремно", "Відкладаєш перший крок через страх помилитися"],
    vs_will_l=["Знаєш, які голки обирати для різних ліній", "Вмієш налаштувати машинку й тримати її правильно", "Розумієш, чому лінії виходять кривими й розпливаються після загоєння", "Маєш свій ескіз, AI-асистента і чіткий план подальших кроків"],
    g_big="14", g_small="днів", g_title="Гарантія повернення коштів",
    g_text="Якщо протягом 14 днів зрозумієш, що курс не підходить, — поверну кошти без зайвих питань. Просто напиши мені. Ти нічим не ризикуєш.",
    faq_eyebrow="Питання й відповіді", faq_title="Відповіді на <em>сумніви</em>",
    faq=[
        ("А раптом у мене не вийде і я зрозумію, що це не моє?", "Саме для цього й існує міні-курс: зрозуміти, чи підходить тобі ця сфера, без великих вкладень. 14 € і 5 днів. Плюс є 14-денна гарантія повернення коштів."),
        ("Я не вмію малювати. Це проблема?", "Ні. Навички малювання не обов'язкові, хоча й вітаються. Тату — це техніка і практика, а не лише талант: постановка руки, контроль глибини, рівномірний рух відпрацьовуються."),
        ("Потрібно купувати обладнання до початку?", "Ні. У першому уроці ти отримаєш список обладнання для старту. Базовий набір для навчання на штучній шкірі коштує від 60–80 €."),
        ("Скільки часу потрібно на день?", "Орієнтовно 30–60 хвилин на день протягом 5 днів. Новий урок відкривається щодня."),
        ("Я боюся крові. Чи зможу працювати в цій сфері?", "При правильній техніці крові практично не видно. Усі вправи міні-курсу виконуються на штучній шкірі."),
        ("Чи потрібен ноутбук?", "Ні, достатньо смартфона: навчання проходить через Telegram, і дивитись уроки та надсилати завдання зручно з телефону."),
        ("Чи є вікові обмеження?", "Навчання доступне з 18 років — це стандартна вимога для роботи в тату-індустрії."),
        ("Після міні-курсу я буду готовий працювати з клієнтами?", "Ти матимеш правильну базу, розуміння принципів і чіткий план розвитку. Для роботи з реальними клієнтами потрібна додаткова практика, але ти знатимеш, що саме відпрацьовувати."),
    ],
    final_title="Зроби перший крок за ціну <em>однієї кави</em>",
    final_p="14 € замість 99 €. Доступ одразу після оплати, 14 днів гарантії повернення коштів.",
    final_note="Оплата через Stripe. Усі дані захищені.",
    sticky_small="14 днів гарантія повернення",
    f_about="VIP tattoo school", f_about_p="Онлайн-навчання для тату-майстрів від Вікторії Поникарової.",
    f_contacts="Контакти", f_tg="Telegram Вікторії", f_bot="Telegram-бот", f_ig="Instagram",
    f_more="Школа", f_site="Повний курс VIP tattoo school",
    legal="Firma Виктория Поникарова · NIP 6492327660. Курс має освітній та інформаційний характер. Результат залежить від твоєї практики й активності, тому ми не гарантуємо конкретного доходу чи кількості клієнтів. Навчання доступне з 18 років.",
    copyright="© 2026 VIP tattoo school. Усі права захищені.",
    alt_hero="Вікторія Поникарова з тату-машинкою",
    alt_case="Учень VIP tattoo school",
)

RU = dict(
    lang="ru", other_lang="", other_label="UA",
    title="Тату Старт: первые линии за 5 дней — Виктория Поникарова",
    desc="Онлайн-мини-курс от Виктории Поникаровой, основательницы VIP tattoo school: за 5 дней сделаешь первые линии на искусственной коже и поймёшь, готов ли к первому клиенту. 14 € вместо 99 €.",
    badge="Онлайн-мини-курс от Виктории Поникаровой",
    h1="Первые линии <em>без страха</em> испортить кожу",
    sub="Хочешь в тату, но не знаешь, с чего начать, и боишься дорогих ошибок? За 5 дней ты сделаешь первые линии на искусственной коже и поймёшь, твоя ли это профессия.",
    hero_list=[
        "Разберёшься, какое оборудование действительно нужно на старте — без лишних трат",
        "Научишься держать машинку и вести ровные линии",
        "Поймёшь, когда можно переходить с искусственной кожи на человека",
    ],
    cta="Забрать за 14 €", old="99 €", new="14 €",
    price_note="Доступ сразу после оплаты · 14 дней гарантия возврата средств",
    tags=["5 дней", "Онлайн", "Практика на искусственной коже", "Обратная связь от Виктории"],
    chip_b="Виктория Поникарова", chip_s="Основательница Sarna Tattoo и VIP tattoo school",
    stats=[("300+", "выпускников школы"), ("22+", "страны, где ценят работы учеников"),
           ("12", "студий-партнёров в Украине и Европе"), ("14", "дней гарантии возврата")],
    pain_eyebrow="Узнаёшь себя?", pain_title="Почему большинство новичков <em>застревают</em> на старте",
    pain_lead="Если узнал себя хотя бы в одном пункте — этот мини-курс для тебя.",
    pains=[
        ("Мечтаешь, но откладываешь", "Кажется, что сначала надо идеально рисовать, купить дорогое оборудование или «дождаться момента». Месяцы идут, а первого шага так и нет."),
        ("YouTube без системы", "Один мастер советует одно, другой — другое. Информации много, а понимания, с чего начинать, нет. Наставника тоже нет."),
        ("Боишься испортить рисунок на коже", "Страх ошибки и вреда клиенту держит на месте. Теория есть, а до практики дело не доходит."),
        ("«Без таланта ничего не выйдет»", "Ты думаешь, что тату — только для тех, кто рисует от природы. На самом деле это техника и практика, а их можно отработать."),
    ],
    prog_eyebrow="Программа", prog_title="5 дней: от безопасности до <em>первого клиента</em>",
    prog_lead="Каждый день — новый урок и практическое задание на искусственной коже. 30–60 минут в день.",
    day_word="День",
    days=[
        ("Старт и безопасность", ["Как на самом деле выглядит профессия тату-мастера", "Стерилизация, гигиена и организация рабочего места", "Список оборудования для старта: что покупать, а что нет"], "Поймёшь, из чего состоит работа мастера, и не потратишь деньги зря."),
        ("Машинка, иглы и кожа", ["Как работает тату-машинка и как её настроить", "Какие бывают иглы и для чего они", "Глубина прокола и работа с кожей"], "Разберёшься в оборудовании и принципе работы с кожей."),
        ("Линия и постановка руки", ["Как держать машинку и натягивать кожу", "Трафареты-прописи для твёрдой руки", "Ровные линии и плотный закрас"], "Выполнишь свои первые линии на искусственной коже."),
        ("Эскиз и AI-ассистент", ["От идеи до эскиза и трафарета", "Обзор тату-стилей: из чего выбрать свой", "Личный tattoo AI-ассистент: идеи, эскизы, рабочие задачи"], "Создашь эскиз с помощью AI и сделаешь по нему практику."),
        ("Первый клиент и что дальше", ["Когда можно переходить с искусственной кожи на человека", "Как считать стоимость работы и не работать себе в убыток", "Портфолио и путь к первым клиентам"], "Будет чёткий план: что отрабатывать дальше."),
    ],
    bonus_eyebrow="Входит в стоимость", bonus_title="Бонусы к <em>мини-курсу</em>",
    bonuses=[
        ("Список оборудования для старта", "Перечень того, что действительно нужно в начале. Базовый набор для обучения на искусственной коже стоит от 60–80 €."),
        ("Личный tattoo AI-ассистент", "Помогает создавать и дорабатывать эскизы, искать идеи и быстрее решать рабочие задачи. Работает на данных курса и студии Sarna."),
        ("Калькулятор стоимости тату", "Шаблон для расчёта цены работы, чтобы не работать себе в убыток."),
        ("Эскизы и трафареты для первых работ", "Готовые эскизы в разных стилях, с которыми можно практиковаться сразу."),
    ],
    instr_badge="Привет, я Виктория Поникарова",
    instr_h2="Почему моя методика работает, даже если ты держишь машинку первый раз",
    instr_p="Я не теоретик, а практикующий мастер, который каждый день работает с клиентами и видит, какие ошибки совершают новички. У меня высшее художественное образование и огромная насмотренность — прежде чем найти свой стиль, я попробовала работать в разных стилях, поэтому точно помогу тебе найти свою сильную сторону и овладеть всеми техническими навыками.",
    instr_list=[
        "Основательница студии <strong>«Sarna Tattoo»</strong>, победительница Personal Branding Awards Poland Ukraine и лицо обложки Bomond VIP",
        "<strong>300+ выпускников</strong> обучения, которые уже работают с клиентами",
        "Ученики VIP tattoo выполнили <strong>2000+ работ</strong> только за 2025 год",
        "Опыт обучения новичков в <strong>12 студиях-партнёрах</strong> по Украине и Европе",
    ],
    instr_stats=[("instructorStatMakeup", "80%", "работ по перманентному макияжу — без единой коррекции"),
                 ("instructorStatGraduates", "300+", "выпускников, которые уже работают с клиентами"),
                 ("instructorStatWorks", "2000+", "работ выполнили ученики тату-обучения за 2025 год"),
                 ("instructorStatPartners", "12", "студий-партнёров признают сертификат обучения")],
    res_eyebrow="Результаты", res_title="Работы и ученики <em>VIP tattoo school</em>",
    res_lead="Ученики школы из разных стран. Все начинали с нуля.",
    how_eyebrow="Как проходит обучение", how_title="4 шага к <em>первым линиям</em>",
    steps=[
        ("Оплачиваешь по специальной цене", "Stripe: безопасная оплата картой. Сразу получаешь доступ в Telegram."),
        ("Новый урок каждый день", "Смотришь короткие видеоуроки в удобное время и сразу переходишь к практике."),
        ("Выполняешь задания", "Практикуешься на искусственной коже и отправляешь результат."),
        ("Получаешь обратную связь", "Виктория разбирает работу: что сделано правильно, где ошибки и как их исправить."),
    ],
    vs_title="Было / <em>Станет</em>", vs_was="Сейчас", vs_will="Через 5 дней",
    vs_was_l=["Мечтаешь о тату-профессии, но не знаешь, с чего начать", "Теряешься в противоречивых советах из интернета", "Боишься купить не то оборудование и потратить деньги зря", "Откладываешь первый шаг из-за страха ошибиться"],
    vs_will_l=["Знаешь, какие иглы выбирать для разных линий", "Умеешь настроить машинку и правильно держать её", "Понимаешь, почему линии выходят кривыми и расплываются после заживления", "Есть свой эскиз, AI-ассистент и чёткий план дальнейших шагов"],
    g_big="14", g_small="дней", g_title="Гарантия возврата средств",
    g_text="Если в течение 14 дней поймёшь, что курс не подходит, — верну деньги без лишних вопросов. Просто напиши мне. Ты ничем не рискуешь.",
    faq_eyebrow="Вопросы и ответы", faq_title="Ответы на <em>сомнения</em>",
    faq=[
        ("А вдруг у меня не получится и я пойму, что это не моё?", "Именно для этого и существует мини-курс: понять, подходит ли тебе эта сфера, без больших вложений. 14 € и 5 дней. Плюс есть 14-дневная гарантия возврата средств."),
        ("Я не умею рисовать. Это проблема?", "Нет. Навыки рисования не обязательны, хотя и приветствуются. Тату — это техника и практика, а не только талант: постановка руки, контроль глубины, равномерное движение отрабатываются."),
        ("Нужно покупать оборудование до начала?", "Нет. В первом уроке ты получишь список оборудования для старта. Базовый набор для обучения на искусственной коже стоит от 60–80 €."),
        ("Сколько времени нужно в день?", "Ориентировочно 30–60 минут в день в течение 5 дней. Новый урок открывается каждый день."),
        ("Я боюсь крови. Смогу ли я работать в этой сфере?", "При правильной технике крови практически не видно. Все упражнения мини-курса выполняются на искусственной коже."),
        ("Нужен ли ноутбук?", "Нет, достаточно смартфона: обучение проходит через Telegram, и смотреть уроки и отправлять задания удобно с телефона."),
        ("Есть ли возрастные ограничения?", "Обучение доступно с 18 лет — это стандартное требование для работы в тату-индустрии."),
        ("После мини-курса я буду готов работать с клиентами?", "У тебя будет правильная база, понимание принципов и чёткий план развития. Для работы с реальными клиентами нужна дополнительная практика, но ты будешь знать, что именно отрабатывать."),
    ],
    final_title="Сделай первый шаг по цене <em>одной чашки кофе</em>",
    final_p="14 € вместо 99 €. Доступ сразу после оплаты, 14 дней гарантии возврата средств.",
    final_note="Оплата через Stripe. Все данные защищены.",
    sticky_small="14 дней гарантия возврата",
    f_about="VIP tattoo school", f_about_p="Онлайн-обучение для тату-мастеров от Виктории Поникаровой.",
    f_contacts="Контакты", f_tg="Telegram Виктории", f_bot="Telegram-бот", f_ig="Instagram",
    f_more="Школа", f_site="Полный курс VIP tattoo school",
    legal="Firma Виктория Поникарова · NIP 6492327660. Курс носит образовательный и информационный характер. Результат зависит от твоей практики и активности, поэтому мы не гарантируем конкретного дохода или количества клиентов. Обучение доступно с 18 лет.",
    copyright="© 2026 VIP tattoo school. Все права защищены.",
    alt_hero="Виктория Поникарова с тату-машинкой",
    alt_case="Ученик VIP tattoo school",
)

CASES = ["case-amira-vancouver", "case-anna-nice", "case-nika-oslo", "case-polina-milan",
         "case-olya-gdansk", "case-criss-rotterdam", "case-edvard-massachusetts", "case-adam-rotterdam"]


def e(s):
    return escape(s, quote=True)


def build(t, ua):
    p = "" if ua else "../"           # префікс до спільних файлів
    self_url = f"{SITE}/" if ua else f"{SITE}/ru/"
    ua_url, ru_url = f"{SITE}/", f"{SITE}/ru/"
    lang_ua = ("#" if ua else p + "index.html")
    lang_ru = ("ru/index.html" if ua else "#")
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    days = "".join(
        f'<article class="day reveal"><div class="day-n">{t["day_word"]}<b>{i}</b></div>'
        f'<div><h3>{h}</h3><ul>{li(items)}</ul><p class="outcome">{out}</p></div></article>'
        for i, (h, items, out) in enumerate(t["days"], 1))
    pains = "".join(f'<div class="card reveal"><h3>{h}</h3><p>{b}</p></div>' for h, b in t["pains"])
    bonuses = "".join(
        f'<div class="card bonus reveal"><div class="n">0{i}</div><div><h3>{h}</h3><p>{b}</p></div></div>'
        for i, (h, b) in enumerate(t["bonuses"], 1))
    steps = "".join(f'<div class="step reveal"><h3>{h}</h3><p>{b}</p></div>' for h, b in t["steps"])
    stats = "".join(f"<div><b>{n}</b><span>{l}</span></div>" for n, l in t["stats"])
    tags = "".join(f'<span class="tag">{x}</span>' for x in t["tags"])
    gallery = "".join(
        f'<figure class="reveal"><img src="{p}assets/{c}.jpg" alt="{t["alt_case"]}" loading="lazy" width="1000" height="1333"></figure>'
        for c in CASES)
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in t["faq"])
    instr_list = "".join(f'<li><span class="check">✓</span><span>{x}</span></li>' for x in t["instr_list"])
    instr_stats = "".join(f'<div class="stat-item"><div id="{i}" class="stat-value">{v}</div><div class="stat-label">{l}</div></div>' for i, v, l in t["instr_stats"])
    cta = lambda cls="": f'<a class="btn {cls}" data-cta href="#">{t["cta"]}</a>'

    faq_ld = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (
            q.replace('"', "'"), a.replace('"', "'")) for q, a in t["faq"])

    return f"""<!DOCTYPE html>
<html lang="{t['lang']}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{e(t['desc'])}">
<link rel="canonical" href="{self_url}">
<link rel="alternate" hreflang="uk" href="{ua_url}">
<link rel="alternate" hreflang="ru" href="{ru_url}">
<link rel="alternate" hreflang="x-default" href="{ua_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(t['title'])}">
<meta property="og:description" content="{e(t['desc'])}">
<meta property="og:image" content="{SITE}/assets/og-cover.jpg">
<meta property="og:url" content="{self_url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}assets/favicon-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Roboto:wght@400;700&family=Poppins:wght@400;500;600;700&family=Roboto+Flex:wght@700&display=swap&subset=cyrillic,latin" rel="stylesheet">
<link rel="stylesheet" href="{p}style.css?v={ver('style.css')}">
<script>document.documentElement.classList.remove('no-js')</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@graph":[{{"@type":"Course","name":"{e(t['title'])}","description":"{e(t['desc'])}","provider":{{"@type":"Organization","name":"VIP tattoo school"}},"offers":{{"@type":"Offer","price":"14","priceCurrency":"EUR"}}}},{{"@type":"FAQPage","mainEntity":[{faq_ld}]}}]}}</script>
</head>
<body>

<header class="header">
  <div class="container">
    <a class="brand" href="#top"><img src="{p}assets/logo-mark.png" alt="VIP tattoo school" width="56" height="56">VIP tattoo school</a>
    <nav class="lang" aria-label="Language">
      <a href="{lang_ua}" {'aria-current="true"' if ua else ''} hreflang="uk">UA</a>
      <a href="{lang_ru}" {'' if ua else 'aria-current="true"'} hreflang="ru">RU</a>
    </nav>
  </div>
</header>

<main id="top">
<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="badge">{t['badge']}</span>
      <h1>{t['h1']}</h1>
      <p class="sub">{t['sub']}</p>
      <ul class="hero-list">{li(t['hero_list'])}</ul>
      <div class="price-row"><span class="price-old">{t['old']}</span><span class="price-new">{t['new']}</span></div>
      {cta()}
      <p class="price-note">{t['price_note']}</p>
      <div class="tags">{tags}</div>
    </div>
    <div class="hero-photo">
      <div class="frame"><img src="{p}assets/instructor-tattoo-machine.jpg" alt="{t['alt_hero']}" width="1000" height="1250" fetchpriority="high"></div>
      <div class="hero-chip"><b>{t['chip_b']}</b><span>{t['chip_s']}</span></div>
    </div>
  </div>
</section>

<div class="stats"><div class="container stats-grid">{stats}</div></div>

<section class="pain">
  <div class="container">
    <div class="head center reveal"><span class="eyebrow">{t['pain_eyebrow']}</span><h2 class="title">{t['pain_title']}</h2><p class="lead">{t['pain_lead']}</p></div>
    <div class="cards cards-2">{pains}</div>
  </div>
</section>

<section class="alt" id="program">
  <div class="container">
    <div class="head center reveal"><span class="eyebrow">{t['prog_eyebrow']}</span><h2 class="title">{t['prog_title']}</h2><p class="lead">{t['prog_lead']}</p></div>
    <div class="days">{days}</div>
    <div class="center" style="margin-top:36px">{cta()}</div>
  </div>
</section>

<section class="dark">
  <div class="container">
    <div class="head center reveal"><span class="eyebrow">{t['bonus_eyebrow']}</span><h2 class="title">{t['bonus_title']}</h2></div>
    <div class="cards cards-2">{bonuses}</div>
  </div>
</section>

<section class="instructor-wrap instructor-wrap--light" id="instructor">
  <div class="container">
    <div class="instructor-section">
      <img src="{p}assets/logo-mark-black.png" class="section-watermark" alt="" aria-hidden="true">
      <div class="instructor-layout">
        <div id="instructorCarousel" class="instructor-carousel-mount"></div>

        <div class="instructor-identity">
          <span class="instructor-name-badge">{t['instr_badge']}</span>
        </div>

        <div class="instructor-copy">
          <h2 class="title">{t['instr_h2']}</h2>
          <p class="instructor-text">{t['instr_p']}</p>
          <ul class="instructor-checklist">{instr_list}</ul>
          <div class="stats-row">{instr_stats}</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="container">
    <div class="head center reveal"><span class="eyebrow">{t['res_eyebrow']}</span><h2 class="title">{t['res_title']}</h2><p class="lead">{t['res_lead']}</p></div>
    <div class="gallery">{gallery}</div>
  </div>
</section>

<section>
  <div class="container">
    <div class="head center reveal"><span class="eyebrow">{t['how_eyebrow']}</span><h2 class="title">{t['how_title']}</h2></div>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="alt">
  <div class="container">
    <div class="head center reveal"><h2 class="title">{t['vs_title']}</h2></div>
    <div class="vs">
      <div class="card was reveal"><h3>{t['vs_was']}</h3><ul>{li(t['vs_was_l'])}</ul></div>
      <div class="card will reveal"><h3>{t['vs_will']}</h3><ul>{li(t['vs_will_l'])}</ul></div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="guarantee reveal">
      <div class="big">{t['g_big']}<small>{t['g_small']}</small></div>
      <div><h3>{t['g_title']}</h3><p>{t['g_text']}</p></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="container">
    <div class="head center reveal"><span class="eyebrow">{t['faq_eyebrow']}</span><h2 class="title">{t['faq_title']}</h2></div>
    <div class="faq reveal">{faq}</div>
  </div>
</section>

<section class="final" id="final">
  <div class="container">
    <div class="reveal">
      <h2 class="title">{t['final_title']}</h2>
      <p class="lead">{t['final_p']}</p>
      <div class="price-row" style="margin-top:22px"><span class="price-old" style="color:var(--muted)">{t['old']}</span><span class="price-new" style="color:var(--blood)">{t['new']}</span></div>
      {cta('btn-wide')}
      <p class="price-note" style="color:var(--muted)">{t['final_note']}</p>
    </div>
  </div>
</section>
</main>

<footer class="footer">
  <div class="container">
    <div><h4>{t['f_about']}</h4><p>{t['f_about_p']}</p></div>
    <div><h4>{t['f_contacts']}</h4>
      <a data-link="telegramPersonal" href="https://t.me/+48733341364">{t['f_tg']}</a>
      <a data-link="telegramBot" href="https://t.me/mentor_tatoo_Viktoria_bot">{t['f_bot']}</a>
      <a data-link="instagram" href="https://www.instagram.com/viktoriia_ponikarova">{t['f_ig']}</a></div>
    <div><h4>{t['f_more']}</h4><a data-link="fullCourse" href="https://vip-tattoo-school.com/">{t['f_site']}</a></div>
    <div class="legal"><p>{t['legal']}</p><p style="margin-top:8px">{t['copyright']}</p></div>
  </div>
</footer>

<div class="sticky" role="region" aria-label="{e(t['cta'])}">
  <div class="p"><s>{t['old']}</s><b>{t['new']}</b><small>{t['sticky_small']}</small></div>
  <a class="btn" data-cta href="#">{t['cta']}</a>
</div>

<script>window.VIP_TATTOO_ASSET_BASE = "{p}assets/";</script>
<script src="{p}vendor/instructor-carousel.js?v={ver('vendor/instructor-carousel.js')}" defer></script>
<script src="{p}config.js?v={ver('config.js')}"></script>
<script src="{p}script.js?v={ver('script.js')}"></script>
</body>
</html>
"""


(ROOT / "ru").mkdir(exist_ok=True)
(ROOT / "index.html").write_text(build(UA, True), encoding="utf-8")
(ROOT / "ru" / "index.html").write_text(build(RU, False), encoding="utf-8")
print("built index.html, ru/index.html")
