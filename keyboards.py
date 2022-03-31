from aiogram import types
import cmd 
def keyboard_main():
    buttons = types.KeyboardButton(cmd.generate_b)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(buttons)
    return keyboard

def keyboard_dict():
    buttons_1 = ["DICT_4X4", "DICT_5X5", "DICT_6X6", "DICT_7X7", "DICT_ARUCO_ORIGINAL"]
    keyboard_1 = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    keyboard_1.add(*buttons_1)
    return keyboard_1

def keyboard_git():
    button_g = types.InlineKeyboardButton(text="github", url="https://github.com/tomatoCoderq/aruco_generate")
    keyboard_g = types.InlineKeyboardMarkup(row_width=1)
    keyboard_g.add(button_g)
    return keyboard_g
