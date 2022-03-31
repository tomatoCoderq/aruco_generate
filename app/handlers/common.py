from aiogram import types, Dispatcher
import keyboards


async def start(message:types.Message):
    await message.answer(f"""Привет, <b>{message.from_user.full_name}!</b>
На связи ArucoGeneratorBot. Ты можешь создать Aruco маркер, нажав на кнопку <u>Новая метка</u>.
Также работают команды /new и /newaruco. Приятного пользования!""", reply_markup=keyboards.keyboard_main())
    await message.answer("Репозиторий на <b>github</b>", reply_markup=keyboards.keyboard_git() )

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", "hello", "welcome", "about"])

