import os

from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline

API_ID = os.getenv('TELEGRAM_CORE_API_ID')
API_HASH = os.getenv('TELEGRAM_CORE_API_HASH')
telegram_client = TelegramClient('anon', API_ID, API_HASH)


async def _get_online_users(chat_id):
    users = await telegram_client.get_participants(chat_id)
    return users


def get_online_users(chat_id):
    with telegram_client:
        users = telegram_client.loop.run_until_complete(_get_online_users(chat_id))
        return_list = list()
        for user in users:
            if isinstance(user.status, UserStatusOnline):
                return_list.append(user.id)
        return return_list
