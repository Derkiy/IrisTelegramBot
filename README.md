# IrisTelegramBot
Код телеграм бота ирис переписанный на питоне, некоторые функции изменены, все подробно расписано ниже 
Если есть вопросы пишите в дс rostmoment#0 либо тг @Rostmoment

# Файлы бота
main.py - основной файл, его нужно запускать

settings.json - файл настроек бота, в нем прописаны название админов, лммит символов на ник и тд

emojis.py - файл где смайлики котлрфй использует ирис

functions.py - файл где написание все функции которые используются в коде

commands.py - файл где прописаны команлы и их синонимы

# Префиксы
Все команды ниже буду писать с префиксом !, доступные префиксы: "!", ".", "/"

Менять их на 84 строке в main.py
# Команды расписанны ниже
# +ник
Ставит ник пользователю, ирис к пользователю будет обращаться по установленному нику, работает только без префикса

Пример: +ник {ваш ник}

# -ник
Удаляет кастомный ник и ставит ник из телеграма, работает только без префикса

# !снять всех
Опасная команда, работает только с префиксом, снимает админку со всех админов

# ПИУ/ПИНГ/КИНГ/БОТ
Команды для проверки работы бота

# Ид
Синонимы: id

Выводит айди пользователя

Пример: 

!ид @юзер

# Кто админ
Синонимы: админы, кто здесь власть, управляющие, а судьи кто

# Мут
Синонимы: заткунть

Минимальное время мута - 1 минута

Максимальное: 365 дней

Если мутить больше то замутит навсегда

Примеры:

Мутит пользователя на указанное время

Замутит до 16:00:00 23 октября 2023 года

Мут до 2023.10.23 16:00:00 @юзер/айди

Причина с новой строки

Мут на час

!Мут 1 час @юзер/айди

Причина c новой строки

Можно не писать @юзер/айди а отвечать на сообщения пользователя которого нужно мутить

# Варн
Синонимы: пред, предупреждения

Выдает пред. пользователю, если будет достигнут лимит он получит бан навсегда

Пример:

!Варн {количество варнов} @юзер/айди

Причина с новой строки

Чтобы снять варн:

Варн -{количество варнов которое нужно снять} @юзер/айди

Причина c новой строки

Можно не писать @юзер/айди а ответить на сообщения пользователя которому нужно выдать варн

# Варн лимит 
Меняет лимит предупреждений при котором банит пользователя

пример:

!Варн лимит {новый лимит}

# Рандом
Очень кривой код, выберает рандомное число в диапазоне

Пример:

!Рандом {минимальное число} {максимальное число}

# Повысить
Повышает ранг пользователя в админах, чем больше ранг тем больше команд доступно

Пример: 

Повысить {ранг от 1 до 5} @юзер/айди

Можно также в ответ на сообщения


# Планируется
Бан

Кик

Понизить

Правила

Заметки
