__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

from io import BytesIO

import httpx

from settings import TelegramSettings

settings = TelegramSettings()
client = httpx.Client(base_url='https://api.telegram.org', http2=True)


def send_message(message: str, preview: bool = False) -> bool:
    path = f'/bot{settings.bot_token}/sendMessage'
    payload = {
        'chat_id': settings.chat_id,
        'parse_mode': 'HTML',
        'text': message,
        'disable_web_page_preview': not preview,
    }
    resp = client.post(path, data=payload)
    return resp.is_success


def send_photo(photo: BytesIO, caption: str) -> bool:
    path = f'/bot{settings.bot_token}/sendPhoto'
    payload = {'chat_id': settings.chat_id, 'caption': caption, 'parse_mode': 'HTML'}
    files = {'photo': photo.read()}
    resp = client.post(path, data=payload, files=files)
    return resp.is_success
