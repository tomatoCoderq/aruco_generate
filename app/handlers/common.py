from aiogram import types, Dispatcher
import keyboards


async def start(message:types.Message):
    await message.answer(f"""Привет, <b>{message.from_user.full_name}!</b>
НАПИСАТЬ ЧТО-НИБУДЬ""", reply_markup=keyboards.keyboard_main())

# async def cancel(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", "hello", "welcome", "about"])
    # dp.register_message_handler(cancel, commands="cancel", state="*")

