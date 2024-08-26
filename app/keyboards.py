from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import emoji

get_card = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = emoji.emojize(':joker: Claim a card'))]],
                               resize_keyboard = True,
                               input_field_placeholder = 'Press the button'
                               )

go_to_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Menu', callback_data = 'go_to_menu')]])

go_to_menu2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Menu', callback_data = 'go_to_menu2')]])

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = emoji.emojize(':card_file_box: My collection'), callback_data = 'collection')],
    [InlineKeyboardButton(text = emoji.emojize(':check_box_with_check: Tasks'), callback_data = 'tasks')],
    [InlineKeyboardButton(text = emoji.emojize('Friends :people_hugging:'), callback_data = 'refs'),
     InlineKeyboardButton(text = emoji.emojize('Trade :handshake:'), callback_data = 'trade')]
     #InlineKeyboardButton(text = 'Purchase', callback_data = 'donut')]
])

arrows = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = '<', callback_data = '<'),
     InlineKeyboardButton(text = '>', callback_data = '>')],
    [InlineKeyboardButton(text = 'Menu', callback_data = 'go_to_menu')]
])

top_refs = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = emoji.emojize(':crown: Check the TOP :crown:'), callback_data = 'top_refs')],
    [InlineKeyboardButton(text = emoji.emojize('Menu'), callback_data = 'go_to_menu')]
])











"""
settings = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Получить', url = 'https://youtube.com/@sudoteach')]
])



cars = ['Tesla', 'Mercedes', 'BMW']
async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text = car, url = 'https://google.com'))
    return keyboard.adjust(2).as_markup()
"""