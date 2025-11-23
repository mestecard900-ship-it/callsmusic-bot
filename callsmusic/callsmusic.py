from typing import Dict
from typing import List

from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream

from . import client
from .. import queues

instances: Dict[int, PyTgCalls] = {}
active_chats: Dict[int, Dict[str, bool]] = {}


def init_instance(chat_id: int):
    if chat_id not in instances:
        instances[chat_id] = PyTgCalls(client)

    instance = instances[chat_id]

    @instance.on_update
    async def on_update(_, update: Update):
        # حدث انتهاء الأغنية
        if update and update.ended:
            queues.task_done(chat_id)

            if queues.is_empty(chat_id):
                await stop(chat_id)
            else:
                next_audio = queues.get(chat_id)[ file ]
                await set_stream(chat_id, next_audio)


def remove(chat_id: int):
    if chat_id in instances:
        del instances[chat_id]

    if not queues.is_empty(chat_id):
        queues.clear(chat_id)

    if chat_id in active_chats:
        del active_chats[chat_id]


def get_instance(chat_id: int) -> PyTgCalls:
    init_instance(chat_id)
    return instances[chat_id]


async def start(chat_id: int):
    instance = get_instance(chat_id)
    await instance.start(chat_id)
    active_chats[chat_id] = { playing : True,  muted : False}


async def stop(chat_id: int):
    instance = get_instance(chat_id)
    await instance.stop()

    if chat_id in active_chats:
        del active_chats[chat_id]


async def set_stream(chat_id: int, file: str):
    instance = get_instance(chat_id)

    if chat_id not in active_chats:
        await start(chat_id)

    await instance.change_stream(
        chat_id,
        InputAudioStream(
            file,
        )
    )
    active_chats[chat_id][ playing ] = True


def pause(chat_id: int) -> bool:
    if chat_id not in active_chats:
        return False
    elif not active_chats[chat_id][ playing ]:
        return False

    instance = get_instance(chat_id)
    instance.pause_stream(chat_id)
    active_chats[chat_id][ playing ] = False
    return True


def resume(chat_id: int) -> bool:
    if chat_id not in active_chats:
        return False
    elif active_chats[chat_id][ playing ]:
        return False

    instance = get_instance(chat_id)
    instance.resume_stream(chat_id)
    active_chats[chat_id][ playing ] = True
    return True


def mute(chat_id: int) -> int:
    if chat_id not in active_chats:
        return 2
    elif active_chats[chat_id][ muted ]:
        return 1

    instance = get_instance(chat_id)
    instance.mute_stream(chat_id)
    active_chats[chat_id][ muted ] = True
    return 0


def unmute(chat_id: int) -> int:
    if chat_id not in active_chats:
        return 2
    elif not active_chats[chat_id][ muted ]:
        return 1

    instance = get_instance(chat_id)
    instance.unmute_stream(chat_id)
    active_chats[chat_id][ muted ] = False
    return 0