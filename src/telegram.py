__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

import re
from typing import Any, Literal, Self

from httpx import Client

from settings import TelegramSettings


class Telegram:
    escape_pattern = re.compile(rf'([{re.escape(r'\_*[]()~`>#+-=|{}.!')}])')

    def __init__(self) -> None:
        self._settings = TelegramSettings()

    def __enter__(self) -> Self:
        self._client = Client(base_url='https://api.telegram.org', http2=True)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._client.close()

    def send_message(
        self,
        text: str,
        *,
        parse_mode: Literal['HTML', 'MarkdownV2'] | None = None,
        preview: bool = False,
    ) -> Any:
        if parse_mode == 'MarkdownV2':
            text = re.sub(self.escape_pattern, r'\\\1', text)
        path = f'/bot{self._settings.bot_token}/sendMessage'
        payload = {
            'chat_id': self._settings.chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': not preview,
        }
        resp = self._client.post(path, data=payload)
        if not resp.is_success:
            resp.raise_for_status()
        return resp.json()

    def send_photo(
        self,
        photo: bytes,
        caption: str,
        *,
        parse_mode: Literal['HTML', 'MarkdownV2'] | None = None,
    ) -> Any:
        if parse_mode == 'MarkdownV2':
            caption = re.sub(self.escape_pattern, r'\\\1', caption)
        path = f'/bot{self._settings.bot_token}/sendPhoto'
        payload = {
            'chat_id': self._settings.chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
        }
        files = {'photo': photo}
        resp = self._client.post(path, data=payload, files=files)
        if not resp.is_success:
            resp.raise_for_status()
        return resp.json()
