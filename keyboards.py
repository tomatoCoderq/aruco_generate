from aiogram import types
import cmd 
def keyboard_main():
    buttons = types.KeyboardButton(cmd.generate_b)
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    keyboard.add(buttons)
    return keyboard

def keyboard_dict():
    buttons_1 = ["DICT_4X4_50", "DICT_4X4_100","DICT_4X4_250",
        "DICT_4X4_1000", "DICT_5X5_50","DICT_5X5_100", "DICT_5X5_250", "DICT_5X5_1000",
        "DICT_6X6_50", "DICT_6X6_100", "DICT_6X6_250", "DICT_6X6_1000", "DICT_7X7_50",
        "DICT_7X7_100", "DICT_7X7_250", "DICT_7X7_1000", "DICT_ARUCO_ORIGINAL"]
    keyboard_1 = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    keyboard_1.add(*buttons_1)
    return keyboard_1
