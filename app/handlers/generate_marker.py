from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import cmd, logging, keyboards, sqlite3, cv2

logger = logging.getLogger(__name__)

# dictionaries = [DICT_4X4_50, DICT_4X4_100, DICT_4X4_250,
#         DICT_4X4_1000, DICT_5X5_50, DICT_5X5_100, DICT_5X5_250, DICT_5X5_1000,
#         DICT_6X6_50, DICT_6X6_100, DICT_6X6_250, DICT_6X6_1000, DICT_7X7_50,
#         DICT_7X7_100, DICT_7X7_250, DICT_7X7_1000, DICT_ARUCO_ORIGINAL]

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

async def id_chosen(message:types.Message, state: FSMContext):
    if int(message.text.lower()) > 249:
        await message.answer("Пожалуйста, впишите значение <b>меньше</b> 249")
        return
    await state.update_data(chosen_id=message.text.lower())
    await message.answer("<i>Отлично!</i> Теперь напишите размер аруко-метки\n<b>Внимание!</b> Размер указывается в пикселях")
    await Generate.waiting_for_size.set()

async def size_chosen(message:types.Message, state:FSMContext):
    if int(message.text.lower()) < 5:
        await message.answer("Пожалуйста, впишите значение <b>больше</b> 5")
        return
    await state.update_data(chosen_size=message.text.lower())
    await message.answer("<i>Готово!</i> Вот ваша Aruco-метка")
    user_data = await state.get_data()

    chosen_dict = user_data["chosen_dictionary"]
    chosen_id = user_data["chosen_id"]
    chosen_size = user_data["chosen_size"]


    # dictionary =  cv2.aruco.Dictionary_get()
    # marker_image = cv2.drawMarker(dictionary, chosen_id, chosen_size)
    # cv2.imshow("window", marker_image)

    await state.finish()

def register_handlers_generate(dp:Dispatcher):
    dp.register_message_handler(ask_dictionary, Text(equals=cmd.generate_b))
    dp.register_message_handler(dictionary_chosen, state=Generate.waiting_for_dictionary)
    dp.register_message_handler(id_chosen, state=Generate.waiting_for_id)
    dp.register_message_handler(size_chosen, state=Generate.waiting_for_size)