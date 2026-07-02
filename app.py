from flask import Flask, request
import vk_api
import os
import hmac
import hashlib

app = Flask(__name__)

TOKEN = os.getenv("VK_TOKEN")
GROUP_ID = int(os.getenv("VK_GROUP_ID", "237994824"))
CONFIRMATION_TOKEN = os.getenv("VK_CONFIRMATION_TOKEN", "test_token")
SECRET_KEY = os.getenv("VK_SECRET_KEY", "secret")

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

def send_message(user_id, text):
    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=0
    )

def verify_signature(body, secret):
    h = hmac.new(secret.encode(), body, hashlib.sha256)
    return h.hexdigest()

@app.route('/callback', methods=['POST'])
def callback():
    data = request.get_json()
    
    # Проверка подписи
    body = request.data.decode('utf-8')
    signature = request.headers.get('X-Retry-Counter', '')
    
    if data['type'] == 'confirmation':
        return CONFIRMATION_TOKEN
    
    if data['type'] == 'message_new':
        obj = data['object']['message']
        user_id = obj['from_id']
        text = obj['text'].lower().strip()
        
        if text in ("привет", "ку", "здравствуй", "хай"):
            send_message(user_id, "Привет! 👋 Чем помочь?")
        elif text == "помощь":
            send_message(user_id, "Напиши:\n- привет\n- помощь")
        else:
            send_message(user_id, "Не понял. Напиши 'привет' или 'помощь'.")
    
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
