from aiogram import types, Dispatcher
import keyboards


async def start(message:types.Message):
    await message.answer(f"""Привет, <b>{message.from_user.full_name}!</b>
НАПИСАТЬ ЧТО-НИБУДЬ""", reply_markup=keyboards.keyboard_main())

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", "hello", "welcome", "about"])

