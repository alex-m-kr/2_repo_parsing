import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common import exceptions as se

client = MongoClient('localhost', 27017)
db = client['gb_email']
collection = db['mail.ru']

url = 'https://mail.ru/'
login = 'study.ai_172'
pswd = 'NextPassword172???'

chrome_options = Options()
chrome_options.add_argument("start-maximized")
# chrome_options.add_argument("--headless")  # Режим без интерфейса / сложно контролировать работу

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get(url)

elem = driver.find_element(By.CLASS_NAME, "email-input")
elem.send_keys(login)
elem.send_keys(Keys.ENTER)

# Да, я читал это в методичике:  Худший пример такого кода — использование команды time.sleep()
# Но здесь команда используется не в цикле, а однократно, поэтому, думаю, большого замедления не будет
time.sleep(2)

elem = driver.find_element(By.CLASS_NAME, "password-input")
elem.send_keys(pswd)
elem.send_keys(Keys.ENTER)
time.sleep(10)

# замысел такой - когда выделяем все письма ctrl + a, показывается их общее количество
# потом это значение можно использовать для остановки сбора ссылок на письма
actions = ActionChains(driver)
actions.key_down(Keys.LEFT_CONTROL).key_down('a')
actions.perform()
time.sleep(1)
elem = driver.find_elements(By.CLASS_NAME, "button2__txt")
cnt_let = int(elem[1].text)
print(cnt_let)
actions.perform()
# time.sleep(2)

set_of_link = set()

while len(set_of_link) < cnt_let:

    list_of_a = driver.find_elements(By.CLASS_NAME, "js-letter-list-item")
    for el in list_of_a:
        link = el.get_attribute('href')
        set_of_link.add(link)

    actions = ActionChains(driver)
    actions.move_to_element(list_of_a[-1])
    actions.perform()
    # time.sleep(1)

# print(len(set_of_link))

for el in set_of_link:
    dict_link = {}
    dict_link['link'] = el
    collection.update_one({'link': dict_link.get('link')}, {'$set': dict_link}, upsert=True)
print('ссылок в коллекции, шт.:', collection.count_documents({}))

# во время отладки после первого запуска закомментировал
# с 39 по 72 строчки кода, чтобы не ждать сбора данных с сайта
# запускал так и работал со ссылками из БД

time.sleep(2)
# cnt = 1
all_link = collection.find({})
for el in all_link:
    # cnt += 1
    # if cnt > 5: break
    link = el['link']
    # print(link)
    letter = {}
    driver.get(link)
    wait = WebDriverWait(driver, 8)
    text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "letter-body"))).text
    contact = driver.find_element(By.CLASS_NAME, "letter-contact").get_attribute('title')
    date = driver.find_element(By.CLASS_NAME, "letter__date").text
    subject = driver.find_element(By.CLASS_NAME, "thread__subject").text
    # print(f' {contact=}, {date=}, {subject=}, {text=}')
    letter['contact'] = contact
    letter['date'] = date
    letter['subject'] = subject
    letter['text'] = text
    collection.update_one({'link': link}, {'$set': letter}, upsert=True)

result = collection.find({}, {'_id': 0, 'contact': 1, 'date': 1, 'subject': 1, 'text': 1}).limit(10)
for el in result:
    print(el)
'''
ссылок в коллекции, шт.: 582
{'contact': 'digest@email.wmj.ru', 'date': '9 июня, 10:36', 'subject': 'Как одежда может спровоцировать рак', 'text': 'Привет! Самые актуальные новости и любопытные темы для обсуждения — только на WMJ.ru!\nОбсуждаемые темы\nПродюсер Лободы покинула шоу-бизнес после скандала с Киркоровым\nНовости\nКак выглядят Валерия, Кудрявцева, Пересильд и другие на честных фото без макияжа\nЛицо\nКак одежда может спровоцировать рак\nНовости\nУ Нюши — Симба, а у Топурии — Адам: 8 самых необычных имен детей звезд\nКультура\nБатырев впервые объяснил, почему развелся с Лозой через полгода после женитьбы\nОтношения\nТренд: оптимистичные украшения. Чем пополнить свою шкатулку этим летом\nТенденции\nРабота вразрез с биоритмами приводит к депрессии\nНовости\n«История Лизи»: неудачная экранизация самого личного романа Стивена Кинга\nКино и сериалы\nБольше новостей\nМы отправили это письмо на study.ai_172@mail.ru\nПользовательское соглашение Отписаться\nКонтакты и реклама'}
{'contact': 'noreply@sidebar.io', 'date': '12 июля, 15:16', 'subject': 'Data Visualization for Kids, Motion Sickness, Text Hierarchy, SVG Favicons, Inspirational Websites', 'text': "Email not displaying properly? View browser version.\nJULY 12 2021\nData Visualization for Kids\nnightingaledvs.com\nIt all started when my nine-year-old son brought home his grade four math homework.\nData Visualization\nCredit: Data Visualization Society\nWeb Designers Grapple With Downside to Flashy Animation: Motion Sickness\nwsj.com\nWeb animations make some users sick. Companies are designing antidotes.\nAccessibility Animation\nCredit: The Wall Street Journal\nWhen Using Type Graphically, Avoid Text Hierarchy Disasters\nbaselinehq.com\nAfter all, you don't want your work to end up in an article like this.\nHumor Tutorials Typography\nCredit: Baseline, the free design bootcamp\nSVG Favicons in Action\ncss-tricks.com\nEver heard of favicons made with SVG? If you are a regular reader of CSS-Tricks, you probably have.\nSVG\nCredit: CSS-Tricks\nInspirational Websites Roundup #27\ntympanus.net\nA special selection of the most creative and interesting websites from the last weeks.\nInspiration\nCredit: Codrops\n  You’re receiving this email because you signed up on sidebar.io. Unsubscribe\nSacha Greif - Kyoto, Japan"}
{'contact': 'no-reply@webdesignernews.com', 'date': '5 июня, 20:35', 'subject': '✏ Fiendishly Hard Logo Quiz, Getting Started With Webpack, Beyond Triangles, and more...', 'text': '  ✨Grab a Free .design Domain Name for your Portfolio✨ [ad]\nPORKBUN.COM   \nFiendishly Hard Logo Quiz\nWEBDESIGNERDEPOT.COM    COMMENTS\nHow to Create a Disruptive Design (So it will Get Seen)\nDESIGNSHACK.NET    COMMENTS\nTrigonometry in CSS and JavaScript: Beyond Triangles\nTYMPANUS.NET    COMMENTS\nGetting Started with Webpack\nSMASHINGMAGAZINE.COM    COMMENTS\nDevelopers: Use Side Projects to Build a Career You Can Be Proud of\nTHENEXTWEB.COM    COMMENTS\n  See latest posts\n    Home   About   FAQs   Legal   Privacy   RSS   Update email frequency   Contact\n© 2021 All Rights Reserved - WebdesignerNews\n\nSent to study.ai_172@mail.ru\nunsubscribe from this list | update subscription preferences\nBuddy Industries Inc. · 1372 Seymour Street · Suite 3105 · Vancouver, BC V6B 0L1 · Canada'}
{'contact': 'no-reply@webdesignernews.com', 'date': '13 сентября, 20:35', 'subject': '✏ Top 10 Good Website Designs, Orchestrating Complexity, Pensieve AI, and more...', 'text': "  Orchestrating Complexity with Web Animations API\nSMASHINGMAGAZINE.COM    COMMENTS\nHow to Optimize your Site for Google's Core Web Vitals\nKINSTA.COM    COMMENTS\nTop 10 Good Website Designs\nUXPIN.COM    COMMENTS\n29 Projects Help You Practice HTML CSS Javascript 2021\nEN.NIEMVUILAPTRINH.COM    COMMENTS\nPensieve AI - Your Go-to User Research Platform\nPENSIEVEAI.COM    COMMENTS\n  See latest posts\n    Home   About   FAQs   Legal   Privacy   RSS   Update email frequency   Contact\n© 2021 All Rights Reserved - WebdesignerNews\n\nSent to study.ai_172@mail.ru\nunsubscribe from this list | update subscription preferences\nBuddy Industries Inc. · 1372 Seymour Street · Suite 3105 · Vancouver, BC V6B 0L1 · Canada"}
{'contact': 'noreply@pulse.mail.ru', 'date': '8 июля, 18:17', 'subject': 'Топ новостей за 24 часа для вас', 'text': '        Новости за 24 часа\n  Привет! Это ваша личная подборка новостей за последние 24 часа. Приятного чтения.\n        Дети Mail.ru\ndeti.mail.ru\n            Дмитрий Шепелев умилил сеть совместным кадром с 8-летним сыном\n  Читать →\n        Американка родила на приеме у врача\n        Сын пары появился на свет через 14 месяцев после смерти отца\n            Чемпионат.com\nchampionat.com\n            Евро-2020, Англия — Дания — 2:1, болельщики требуют переиграть матч из-за ослепления вратаря...\n  Читать →\n        Юрий Сёмин оценил скандальный пенальти в пользу Англии в полуфинале Евро-2020\n        УЕФА открыл дело против Англии после инцидента со Шмейхелем. Во вратаря светили лазером\n            Журнал Esquire\nesquire.ru\n            Петра Мамонова будут постепенно выводить из искусственной комы\n  Читать →\n        Wylsacom купил у Гусейна Гасанова курс «Мышление миллионера». Обучение закончилось, даже не...\n            AppleInsider.ru\nappleinsider.ru\n            Что Apple делает со старыми резервными копиями iPhone\n  Читать →\n        Apple Watch научили выявлять последствия болезни COVID-19\n            «Еда»\neda.ru\n            Как приготовить настоящую кюфту\n  Читать →\n        Яйца с двумя желтками\n            «Кино Mail.ru\nkino.mail.ru\n            Владимира Меньшова проводили в последний путь овациями\n  Читать →\n        Dava стал ведущим «Муз-ТВ»\n            Авто Mail.ru\nauto.mail.ru\n            Топ-5 интересных и необычных мест в Суздале\n  Читать →\n        Подростки скручивают колпачки с машин для ТikTok: теперь их ловит ГИБДД\n            Cybersport.ru\ncybersport.ru\n            Lil me alone: «Почему бы не сделать еще одну квалификацию и немного изменить формат The...\n  Читать →\n        Valve отложила The International 10 и назвала новое место проведения турнира\n            7я.ру\n7ya.ru\n            Что можно приготовить из ревеня?\n  Читать →\n        Дмитрий Шепелев запретил жалеть своего сына от Жанны Фриске\n                На этом все! Следующая подборка новостей придет завтра.\n                Copyright 2021 Mail.ru Group, Москва — Все права защищены.\nВы получили это письмо, потому что подписались на рассылку Пульса и являетесь пользователем сервиса Пульс Mail.ru на основании Пользовательского соглашения.\n    Отписаться     Служба поддержки\n       '}
{'contact': 'noreply@pulse.mail.ru', 'date': '19 июня, 18:17', 'subject': 'Топ новостей за 24 часа для вас', 'text': '        Новости за 24 часа\n  Привет! Это ваша личная подборка новостей за последние 24 часа. Приятного чтения.\n        Дети Mail.ru\ndeti.mail.ru\n            Экс-солистка группы Serebro Катя Кищук родила первенца\n  Читать →\n            Чемпионат.com\nchampionat.com\n            Обозреватель The Athletic — о Капризове в России: ЦСКА предложит Кириллу тонну долларов\n  Читать →\n        Деян Ловрен резко отреагировал на пенальти, назначенный после его контакта с соперником\n        Источник: Кирилл Капризов может вернуться в ЦСКА, чтобы сыграть на Олимпиаде-2022\n        Маттейс де Лигт ошибся в послематчевом интервью. Защитник забыл, за какой клуб играет\n            Журнал Esquire\nesquire.ru\n            При крушении самолета в Кемеровской области погибли четыре человека\n  Читать →\n        Криштиану Роналду первым в мире набрал 300 млн подписчиков в Instagram\n        Куда путешествовали герои классической литературы? Сложный тест Esquire\n        В Эквадоре новый вид лягушек назвали в честь британской рок-группы Led Zeppelin\n            AppleInsider.ru\nappleinsider.ru\n            Новое приложение Файлы и улучшенная многозадачность: что нового в iPadOS 15 beta 1\n  Читать →\n        Это самая важная функция iPadOS 15. Остальные не нужны\n            Авто Mail.ru\nauto.mail.ru\n            Посмотрите на уникальный 27-летний «Крузак» в идеальном состоянии (фото)\n  Читать →\n        10 самых популярных иномарок с пробегом в России (фото)\n        Нижний Новгород: что посмотреть и чем заняться\n            Cybersport.ru\ncybersport.ru\n            Twitch забанила каналы двух самых популярных «девушек в бассейне»\n  Читать →\n        NS про инцидент с gpK~ и Xiao8: «За такие выкрутасы игроков надо сурово наказывать»\n        За кого вы будете болеть в отборочных на The International 10 для СНГ? Опрос от Cybersport.ru\n            7я.ру\n7ya.ru\n            Если их посадить на даче, вас могут посадить. Надолго\n  Читать →\n        19 июня – День неспешной прогулки\n                На этом все! Следующая подборка новостей придет завтра.\n                Copyright 2021 Mail.ru Group, Москва — Все права защищены.\nВы получили это письмо, потому что подписались на рассылку Пульса и являетесь пользователем сервиса Пульс Mail.ru на основании Пользовательского соглашения.\n    Отписаться     Служба поддержки\n       '}
{'contact': 'noreply@pulse.mail.ru', 'date': '10 октября, 18:15', 'subject': 'Топ новостей за 24 часа для вас', 'text': '        Новости за 24 часа\n  Привет! Это ваша личная подборка новостей за последние 24 часа. Приятного чтения.\n        Чемпионат.com\nchampionat.com\n            Маркус Гисдоль новый тренер «Локомотива», мнения, Сёмин, Смородская\n  Читать →\n        Скандал вокруг фигуристки Алины Загитовой — инцидент на матче «Ак Барса», упрёки в грубости...\n        Словения — Россия, 11 октября 2021 года, прогноз и ставка на матч отбора ЧМ-2022, смотреть онлайн...\n        Тайсон Фьюри — Деонтей Уайлдер, слёзы Фьюри и жены Уайлдера после завершения боя за титул...\n            Журнал Esquire\nesquire.ru\n            В Британии создали трекер для гуляющих в одиночестве женщин\n  Читать →\n        Глава книги Дианы Вриланд "D.V."\n        В Большом театре актера насмерть придавило декорацией во время оперы "Садко"\n        WADA отозвало аккредитацию Московской антидопинговой лаборатории\n            AppleInsider.ru\nappleinsider.ru\n            Почему я не кастомизирую свой iPhone\n  Читать →\n        Функция «В центре внимания» на iPad: что это и как работает\n            Авто Mail.ru\nauto.mail.ru\n            Редкие классические автомобили на улицах города (фото)\n  Читать →\n        Производство «Шкод» может встать из-за дефицита чипов\n        5 новых кроссоверов Mazda появятся за два года\n            Cybersport.ru\ncybersport.ru\n            Team Spirit поддержала флешмоб OG и VP: «Хотим извиниться за керри Shadow Fiend в ваших пабликах»\n  Читать →\n        Virtus.pro прошла в верхнюю сетку плей-офф The International 2021\n        T1 гарантировала себе слот в переигровках группы A на The International 10\n        В Guardians of the Galaxy прозвучат песни Рика Эстли, a-ha и Def Leppard\n            7я.ру\n7ya.ru\n            Подросток, школа и помощь родителей: когда отойти в сторону\n  Читать →\n        5 причин сделать 12-часовой перерыв в еде\n        Домашний морковный торт: пошаговый рецепт\n                На этом все! Следующая подборка новостей придет завтра.\n                Copyright 2021 Mail.ru Group, Москва — Все права защищены.\nВы получили это письмо, потому что подписались на рассылку Пульса и являетесь пользователем сервиса Пульс Mail.ru на основании Пользовательского соглашения.\n    Отписаться     Служба поддержки\n       '}
{'contact': 'no-reply@webdesignernews.com', 'date': '17 июня, 20:35', 'subject': '✏ 3 Ways to Design More Inclusively, What is a Design System?2021 Fun Typefaces, and more...', 'text': '  3 Ways to Design More Inclusively\nWEBDESIGNERDEPOT.COM    COMMENTS\nWhat is a Design System?\nROBERTCREATIVE.COM    COMMENTS\nAnimal Crossing Font\nFONTSPANDA.COM    COMMENTS\nSome Fun Typefaces for 2021\nKOTTKE.ORG    COMMENTS\nGuiding Junior Developers Out of the Weeds\nBUTTERCMS.COM    COMMENTS\n  See latest posts\n    Home   About   FAQs   Legal   Privacy   RSS   Update email frequency   Contact\n© 2021 All Rights Reserved - WebdesignerNews\n\nSent to study.ai_172@mail.ru\nunsubscribe from this list | update subscription preferences\nBuddy Industries Inc. · 1372 Seymour Street · Suite 3105 · Vancouver, BC V6B 0L1 · Canada'}
{'contact': 'no-reply@mail.instagram.com', 'date': '8 марта, 14:33', 'subject': 'study.ai_172, посмотрите новости Angelababy и Lele Pons и других пользователей в своей ленте', 'text': '  Подпишитесь на обновления Angelababy, Lele Pons и других своих знакомых, чтобы видеть их фото и видео.\nОткрыть Instagram\nAngelababy\nРекомендации для вас\nПодписаться\nLele Pons\nРекомендации для вас\nПодписаться\nStar Wars\nРекомендации для вас\nПодписаться\nHouse of Highlights\nРекомендации для вас\nПодписаться\nBelieve\nРекомендации для вас\nПодписаться\nHrithik Roshan\nРекомендации для вас\nПодписаться\n1\nУ вас также есть 1 уведомлений, которые вы ещё не видели.\n     \n© Instagram. Facebook Inc., 1601 Willow Road, Menlo Park, CA 94025\nСообщение было отправлено для study.ai_172 на адрес study.ai_172@mail.ru. Instagram рассылает такие обновления, чтобы держать вас в курсе наших новостей. Вы можете отменить подписку на эти новости или удалить ваш эл. адрес, если этот аккаунт Instagram принадлежит не вам. Отмените подписку или удалите эл. адрес из этого аккаунта.\n     '}
{'contact': 'digest@email.wmj.ru', 'date': '6 октября, 10:35', 'subject': 'Покойная жена Прохора Шаляпина не была миллионершей?', 'text': 'Привет! Самые актуальные новости и любопытные темы для обсуждения — только на WMJ.ru!\nОбсуждаемые темы\nКарпович и Прилучный вместе пришли на мероприятие — но избегали друг друга\nНовости\nРомановы, Кеннеди и другие состоятельные семьи, которых преследовали родовые проклятия\nКультура\nЗвездный адвокат уверен, что покойная жена Прохора Шаляпина не была миллионершей\nНовости\nДевам — духи с запахом карамели, Весам — блеск для долгих поцелуев. Что надо знакам Зодиака в октябре\nБьюти-новинки\nКейт Миддлтон посетила институт в платье из масс-маркета. И она его уже надевала\nНовости\nПоиски бога и происки дьявола: почему сериал «Полуночная месса» — must see сезона\nКино и сериалы\nНайдите 5 отличий: как звезды выглядят на своих фото и на чужих\nНовости\nБыло — стало: как выглядит выросшая Анастасия Добрынина — малышка из «Куки»\nНовости\nБольше новостей\nМы отправили это письмо на study.ai_172@mail.ru\nПользовательское соглашение Отписаться\nКонтакты и реклама'}

Process finished with exit code 0
'''
