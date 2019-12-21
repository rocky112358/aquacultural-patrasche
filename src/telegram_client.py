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


async def _set_user_rank(chat_id, user_id, rank_text):
    res = await telegram_client.edit_admin(chat_id, user_id, delete_messages=False, ban_users=False, invite_users=False,
                                           add_admins=False, is_admin=True, title=rank_text)

    return res


def set_user_rank(chat_id, user_id, rank_text):
    with telegram_client:
        res = telegram_client.loop.run_until_complete(_set_user_rank(chat_id, user_id, rank_text))
        return res
