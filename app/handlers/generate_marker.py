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

async def ask_dictionary(message:types.Message):
    await message.answer("Напишите, пожалуйста, какой размер маркера вы хотите использовать", reply_markup=keyboards.keyboard_dict())
    await Generate.waiting_for_dictionary.set()

async def dictionary_chosen(message:types.Message, state: FSMContext):
    await state.update_data(chosen_dictionary=message.text.lower())



def register_handlers_generate(dp:Dispatcher):
    dp.register_message_handler(ask_dictionary, Text(equals=cmd.generate_b))
    dp.register_message_handler(dictionary_chosen, state=Generate.waiting_for_dictionary)
