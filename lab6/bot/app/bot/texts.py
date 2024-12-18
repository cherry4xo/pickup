def price(count: int, value: int) -> str:
    return f"{count} кружочков за {value} рублей"

def value(count: int) -> str:
    return f"{count} кружочков"

def buy_rounds(count: int, value: int) -> str:
    return f"Вы покупаете {count} кружочков за {value} рублей"

def got_payment(count: int, total: int) -> str:
    return f"Вы успешно приобрели подписку на {count} кружочков!\nВсего на вашем счету {total} кружочков"

def payment_answer(count: int) -> str:
    if count == -1:
        return f"У вас полный доступ. Вы точно хотите приобрести тариф?"
    if count == -2:
        return f"У вас безлимит на кружочки. Вы точно хотите приобрести тариф?"
    if count > 0:
        return f"У вас осталось кружочков: {count}. Укажите тариф для пополнения"
    else:
        return "Вы не можете создавать кружочки. Приобретите подписку для использования бота."    

def user_not_exist_alert(id: int) -> str:
    return f"Пользователь {id} не использует этого бота!"

def user_unlimited(id: int) -> str:
    return f"Пользователю {id} выдан доступ!"

def user_limited(id: int) -> str:
    return f"У пользователя {id} больше нет доступа!"

def user_set_sub(id: int) -> str:
    return f"Пользователю {id} выдана годовая подписка!"

def user_cancel_sub(id: int) -> str:
    return f"Пользователю {id} отменена годовая подписка!"

def users_count(count: int) -> str:
    return f"Количество пользователей: {count}"

def rounds_left(count: int) -> str:
    return f"Принял! Сейчас закруглю!\nОсталось кружочков: {count}"

def contour_saved(title: str) -> str:
    return f"Шаблон с названием {title} сохранен"

def watermark_sample_saved(title: str) -> str:
    return f"Шаблон с названием {title} сохранен"

def payment_url_and_test(url: str, count: int, total: int) -> str:
    return f"Перейдите по данной ссылке для оплаты покупки {count} кружочков за {total} рублей\n{url}"

def delete_sample_confirm(sample_name: str) -> str:
    return f"Вы точно хотите удалить шаблон \"{sample_name}\"?"

def delete_sample_menu_confirm(sample_name: str) -> str:
    return f"Да, удалить шаблон \"{sample_name}\""

def deleted_sample(sample_name: str) -> str:
    return f"Шаблон \"{sample_name}\" удален"

def delete_picture_confirm(picture_name: str) -> str:
    return f"Вы точно хотите удалить картинку \"{picture_name}\"?"

def delete_picture_menu_confirm(picture_name: str) -> str:
    return f"Да, удалить картинку \"{picture_name}\""

def deleted_picture(picutre_name: str) -> str:
    return f"Картинка \"{picutre_name}\" удалена"

sending_text = """Дорогие друзья! 

Я, Александр Арунов - визажист, парфюмерный стилист, основатель и генеральный директор компании [A7 community](https://a7community.ru/).

Рад сообщить, что мы с командой закончили работы по внедрению новых функций в бот [«Саня, закругляйся!»](https://t.me/arunov_round_bot):

- Брендирование. Функция с помощью которой можно наложить на видео логотип бренда, идеально подойдет компаниям, которые хотят сделать свой бренд более узнаваемым и запоминающимся. 

- Маркировка видео. Теперь бренды и блогеры могут размещать на видео-кружочках маркировочные данные рекламного креатива. Достаточно получить токен в сервисах ОРД и разместить его по кругу на видео. 

- Провести розыгрыш. Наш бот может провести до 5 разных видов розыгрышей и поднять активность на канале. 

Желаю приятных впечатлений и создания яркого, красивого контента на Вашем канале!"""

upload_video = "📹 Загрузить видео"
upload_video_answer = """Отправь в бот любое видео, которое хочешь получить в формате кружочка. 

Для этого необходимо нажать на скрепку расположенную в левой части интерфейса,  выбрать видео из галереи телефона, обрезать его по квадрату и отправить боту. Через 10-15 секунд бот пришлет кружочек. Его можно переслать в канал, предварительно выключив во время отправки имя отправителя.

Длительность видео - до 60 сек.
"""
instruction = "📝 Инструкция"
instruction_answer = """
Инструкция по использованию бота:

https://a7community.ru/bot-sanya-zakruglyaysya
    """
null_rounds = "Кружочки закончились! Приобретите подписку, чтобы продолжить пользоваться ботом!"
unlimited_rounds = "Принял! Сейчас закруглю!\nУ вас неограниченное количество кружочков!"
payment = "💵 Оплата"
check_payment = "Проверить оплату"
payment_already_sent = "Вы уже оформили. Произведите оплату, чтобы создать новую"
payment_not_sent = "Нет оплат для подтверждения"
give_bot = "Бот [\"Халява, приди!\"](https://t.me/arunov_give_bot) поднимет активность среди аудитории канала и поможет провести пять разных видов розыгрыша."
technical_support = "🙋🛠 Техподдержка"
technical_support_answer = """
Инструкция по использованию бота:

https://a7community.ru/bot-sanya-zakruglyaysya

В случае возникновения вопросов пишите в поддержку: @faq_support_bot"""
is_not_admin_alert = "У вас нет доступа к данной команде!"
payment_error_message = "Произошла ошибка при оплате. Повторите попытку позже"
back_to_main_menu = "Назад"
main_menu = "Главное меню"
video_marking = "✍️ Маркировка видео"
create_marked_video = "Создать маркированное видео"
create_branded_video = "Создать брендированное видео"
video_labeling = "Брендирование видео"
contest = "🎲 Провести розыгрыш"
branding = "🖼 Брендирование"
round_samples = "Шаблоны обводки"
watermark_samples = "Шаблоны наложения картинки"
back_to_samples_menu = "Назад"
sample_type = "Выберите тип брендирования видео"
on_set_border_round_state = "Отлично!\nТеперь отправь мне видео, на которое хочешь наложить обводку"
on_set_watermark_round_state = "Отлично!\nТеперь отправь мне видео, на которое хочешь наложить картинку"
text_round_samples = "Здесь вы можете выбрать шаблон обводки"
text_watermark_samples = "Здесь вы можете выбрать шаблон наложения картинки"
text_pick_picture = "Выберете картинку, которую хотите наложить"
add_new_watermark = "Добавить новую картинку"
delete_picture = "Удалить картинку"
watermark_pictures_menu_text = "Выберете картинку для наложения или добавьте новую"
watermark_add_new_picture = "Отлично! Теперь отправь мне картинку файлом в формате png и название картинки"
watermark_added_picture = "Картинка добавлена! Выберете картинку для наложения или добавьте новую"
none_capture_error = "В сообщении ты не отправил название картинки!\nОтправь фото еще раз, написав название"
invalid_extention_error = "Ты неправильно отправил фотографию!\nОтправь фото файлом"
marking_menu = "Здесь вы можете наложить на видео обводку или картинку, а также управлять шаблонами наложения"
create_sample = "Создать шаблон"
delete_sample_marking = "Удаление шаблона маркировки"
delete_sample_branding = "Удаление шаблона брендирования"
delete_sample_menu_text = "Выберете шаблон, который хотите удалить"
delete_picture_menu_text = "Выберете картинку, которую хотите удалить"
samples_text = "Шаблоны"
watermark_menu_text = "Выберите шаблон брендирования или создайте новый"
round_menu_text = "С помощью этой функции можно разместить на кружочке маркировочные данные рекламного креатива или любой текст как показано на кружочках выше.\nВыберете шаблон маркировки видео или создайте новый"
cancelled_payment = "Платеж был отменен"
pending_payment = "Платеж еще не был произведен"
expired_payment = "Время платежа истекло"