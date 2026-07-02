import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os

TOKEN = os.getenv("VK_TOKEN")
if not TOKEN:
    raise ValueError("VK_TOKEN environment variable is not set")

GROUP_ID = int(os.getenv("VK_GROUP_ID", "237994824"))

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def send_message(user_id, text):
    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=0
    )

print("Бот запущен и слушает сообщения...")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        msg = event.text.lower().strip()
        
        if not msg:
            continue
        
        if msg in ("привет", "ку", "здравствуй", "хай"):
            send_message(user_id, "Привет! 👋 Чем помочь?")
        elif msg == "помощь":
            send_message(user_id, "Напиши:\n- привет\n- помощь")
        else:
            send_message(user_id, "Не понял. Напиши 'привет' или 'помощь'.")
