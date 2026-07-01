import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import os
import json

# Токен из переменной окружения
TOKEN = os.getenv("VK_TOKEN")
if not TOKEN:
    raise ValueError("VK_TOKEN environment variable is not set")

GROUP_ID = int(os.getenv("VK_GROUP_ID", "237994824"))

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Функция для отправки сообщения
def send_message(user_id, text, keyboard=None):
    params = {
        "user_id": user_id,
        "message": text,
        "random_id": random.randint(1, 2**31)
    }
    if keyboard:
        params["keyboard"] = json.dumps(keyboard)
    vk.messages.send(**params)

# Клавиатура для главного меню (кнопки)
def get_main_keyboard():
    return {
        "one_time": False,
        "buttons": [
            [
                {"action": {"type": "text", "label": "📖 О сообществе"}, "color": "primary"},
                {"action": {"type": "text", "label": "📚 Наши рубрики"}, "color": "primary"}
            ],
            [
                {"action": {"type": "text", "label": "✏️ Как участвовать?"}, "color": "positive"},
                {"action": {"type": "text", "label": "📩 Связаться с админом"}, "color": "negative"}
            ]
        ]
    }

print("Бот запущен и слушает сообщения...")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        msg = event.text.lower().strip()
        
        if not msg:
            continue
        
        if msg in ("привет", "ку", "здравствуй", "хай"):
            send_message(
                user_id,
                f"Привет-привет! 👋 Рад снова тебя видеть в «Скетче Путешественника». Чем могу помочь? Нажми на кнопку или напиши вопрос.",
                keyboard=get_main_keyboard()
            )
        elif msg == "о сообществе" or msg == "📖 о сообществе":
            send_message(
                user_id,
                "«Скетч Путешественника» — это место для тех, кто замечает красоту в обыденном. Мы делимся зарисовками, лайфхаками для творческих поездок и вдохновляем на новые маршруты. Присоединяйся к нашему творческому сообществу! 🎨",
                keyboard=get_main_keyboard()
            )
        elif msg == "наши рубрики" or msg == "📚 наши рубрики":
            send_message(
                user_id,
                "🗺️ Записки путешественника — короткие истории о встречах и открытиях.\n✍️ Лайфхаки для скетчинга — как выбрать блокнот и успеть запечатлеть главное.\n🎨 Маршруты для творчества — подборки живописных локаций.\n🏆 Челленджи — тематические недели, где можно участвовать и делиться работами.\n\nХочешь узнать о какой-то рубрике подробнее? Напиши её название.",
                keyboard=get_main_keyboard()
            )
        elif msg == "как участвовать?" or msg == "✏️ как участвовать?":
            send_message(
                user_id,
                "Мы рады каждому! Чтобы стать частью сообщества:\n1. Подпишись на наш паблик.\n2. Следи за анонсами челленджей.\n3. Делись своими работами в обсуждениях или отмечай нас в своих постах. Твои зарисовки могут вдохновить других путешественников!",
                keyboard=get_main_keyboard()
            )
        elif msg == "связаться с админом" or msg == "📩 связаться с админом":
            send_message(
                user_id,
                "Хотите задать вопрос или предложить идею? Напишите нам в личные сообщения, и мы обязательно ответим. А пока вы ждёте, возможно, вас заинтересует наша новая рубрика «Маршруты для творчества».",
                keyboard=get_main_keyboard()
            )
        elif "скетч" in msg or "рисовать" in msg or "блокнот" in msg:
            send_message(
                user_id,
                "О, ты по адресу! У нас есть отличные лайфхаки для скетчинга в путешествиях. Например, советую всегда носить с собой небольшой блокнот и линер — так ты не упустишь вдохновение. Хочешь узнать больше полезных советов? Напиши «лайфхак».",
                keyboard=get_main_keyboard()
            )
        elif "лайфхак" in msg:
            send_message(
                user_id,
                "Вот мой любимый лайфхак: рисуй по 5 минут каждый день, даже если просто линию или пятно. Это развивает насмотренность и помогает не бояться чистого листа. А ты пробовал вести скетч-дневник в поездках?",
                keyboard=get_main_keyboard()
            )
        else:
            send_message(
                user_id,
                "Я не совсем понял ваш запрос, но я здесь, чтобы помочь! Выберите один из вариантов ниже или напишите свой вопрос.",
                keyboard=get_main_keyboard()
            )
