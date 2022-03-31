from ast import expr_context
from aiogram import Dispatcher, types, exceptions
import aiogram
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


import cmd, logging, keyboards, sqlite3, cv2, os, exceptions
logger = logging.getLogger(__name__)


class Generate(StatesGroup):
    waiting_for_dictionary = State()
    waiting_for_id = State()
    waiting_for_size = State()

async def ask_dictionary(message:types.Message):
    await message.answer("Напишите, пожалуйста, какой размер маркера вы хотите использовать", reply_markup=keyboards.keyboard_dict())
    await Generate.waiting_for_dictionary.set()

async def dictionary_chosen(message:types.Message, state: FSMContext):
    await state.update_data(chosen_dictionary=message.text.lower())
    await message.answer("<i>Отлично!</i> Теперь напишите id\n<b>Внимание!</b> Это должно быть число от 0 до 249 ")
    await Generate.waiting_for_id.set()
    logger.info(f"DICTIONARY: {message.text.lower()}")

async def id_chosen(message:types.Message, state: FSMContext):
    try:
        if int(message.text.lower()) > 249:
            await message.answer("Пожалуйста, впишите значение <b>меньше</b> 249")
            return
    except ValueError:
        await message.answer("Введите, пожалуйста, целочисленное значение, которое меньше 249")
        return
    await state.update_data(chosen_id=message.text.lower())
    await message.answer("<i>Отлично!</i> Теперь напишите размер аруко-метки\n<b>Внимание!</b> Размер указывается в пикселях и не должен превышать 4999")
    await Generate.waiting_for_size.set()

    logger.info(f"ID: {message.text.lower()}")

async def size_chosen(message:types.Message, state:FSMContext):
    try:
        if int(message.text.lower()) < 6 or int(message.text.lower()) > 4999:
            await message.answer("Пожалуйста, впишите значение <b>больше</b> 5 и <b>меньше</b> 5000")
            return
    except ValueError:
        await message.answer("Введите, пожалуйста, целочисленное значение от 5 до 4999 без лишних знаков")
        return
    await state.update_data(chosen_size=message.text.lower())
    await message.answer("<i>Готово!</i> Вот ваша Aruco-метка")
    user_data = await state.get_data()

    logger.info(f"SIZE: {message.text.lower()}")

    chosen_dict = user_data["chosen_dictionary"]
    chosen_id = user_data["chosen_id"]
    chosen_size = user_data["chosen_size"]

    name=f"markers/"
    if chosen_dict == "dict_4x4":
        marker = cv2.aruco.DICT_4X4_1000
        name+=chosen_dict
    elif chosen_dict == "dict_5x5":
        marker = cv2.aruco.DICT_5X5_1000
        name+=chosen_dict
    elif chosen_dict == "dict_6x6":
        marker = cv2.aruco.DICT_6X6_1000
        name+=chosen_dict 
    elif chosen_dict == "dict_7x7":
        marker = cv2.aruco.DICT_7X7_1000
        name+=chosen_dict
    else:
        marker = cv2.aruco.DICT_ARUCO_ORIGINAL
        name+=chosen_dict
    name+= f"_{chosen_id}_{chosen_size}.jpg"

    if os.path.exists(name):
        logger.info("ALREADY EXISTS")
        photo = open(f"/Users/tomatocoder/Desktop/aruco_generate/{name}", 'rb')
        await message.answer_photo(photo=photo, reply_markup=keyboards.keyboard_main())
    else:
        dictionary =  cv2.aruco.Dictionary_get(marker)
        marker_image = cv2.aruco.drawMarker(dictionary, int(chosen_id), int(chosen_size))
        cv2.imwrite(name, marker_image)
        photo = open(f"/Users/tomatocoder/Desktop/aruco_generate/{name}", 'rb')
        await message.answer_photo(photo=photo, reply_markup=keyboards.keyboard_main())
    await state.finish()

def register_handlers_generate(dp:Dispatcher):
    dp.register_message_handler(ask_dictionary, Text(equals=cmd.generate_b))
    dp.register_message_handler(ask_dictionary, commands="new")
    dp.register_message_handler(dictionary_chosen, state=Generate.waiting_for_dictionary)
    dp.register_message_handler(id_chosen, state=Generate.waiting_for_id)
    dp.register_message_handler(size_chosen, state=Generate.waiting_for_size)