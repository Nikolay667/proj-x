import asyncio
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import random
import math
import emoji
import datetime

import app.keyboards as kb
import app.database.requests as rq
from app.database.requests import get_card

from app.middlewares import TestMiddleware

router = Router()

router.message.outer_middleware(TestMiddleware())

class Reg(StatesGroup):
    name = State()
    number = State()

#СТАРТ
@router.message(CommandStart())
async def cmd_start(message: Message):
    #await rq.set_user(message.from_user.id)
    await rq.create_points(message.from_user.id, int(0))

    msg = await message.answer(emoji.emojize('Welcome to Project X'))
    await asyncio.sleep(2)
    await msg.delete()
    msg = await message.answer_photo(photo = 'https://disk.yandex.ru/i/6Q4rDkTQ3ju7Xg', caption = emoji.emojize(':gem_stone: Collect cards, explore TON and receive rewards\n\nGet your _first card_ :backhand_index_pointing_down:'), parse_mode= "Markdown", reply_markup = kb.get_card)
    await asyncio.sleep(6)

users_cards = []
users_cards_links = []
cards_list = []

#получить карту
@router.message(F.text == emoji.emojize(':joker: Claim a card'))
async def get_the_card(message: Message):
    current_time = datetime.datetime.now()
    last_recieve = await rq.time_check2(message.from_user.id)

    if last_recieve == 0:
        msg = await message.answer('3.. 2.. 1..')
        await asyncio.sleep(2)
        await msg.delete()
        array_card = await get_card()
        card_link = array_card[0]
        card_name = array_card[1]
        card_rarity = array_card[2]
        card_points = array_card[3]
        card_description = array_card[4]
        card_id = array_card[5]
        proj_link = array_card[6]
        await rq.to_collection(card_id, message.from_user.id, card_link)
        await message.answer_photo(photo = card_link, caption = f'*{card_name}*\n\nRarity: _{card_rarity}_\nXStars: _+{card_points}_\nProject: [Click here]({proj_link})\n\nDescription: _{card_description}_', parse_mode = 'Markdown', reply_markup = kb.go_to_menu)
        
        points_before = await rq.view_points(message.from_user.id)
        points_all = points_before + card_points
        await rq.delete_points(message.from_user.id)
        #print(points_all)
        await rq.add_points(message.from_user.id, points_all)

        last_recieve = datetime.datetime.now()
        await rq.time_check(str(last_recieve), message.from_user.id)
        #print('true2')
    else:
        last_recieve = datetime.datetime.strptime(last_recieve, '%Y-%m-%d %H:%M:%S.%f')
        time_elapsed = current_time - last_recieve
        time_to_wait = 4 #как часто можно будет запршивать карточку в секундах
        if time_elapsed.total_seconds() < time_to_wait:
            time = math.ceil(int(time_to_wait-time_elapsed.total_seconds()))
            await message.answer(f'Next claim in _{time} second(s)_', parse_mode = 'Markdown', reply_markup = kb.go_to_menu2)
        else:
            msg = await message.answer('3.. 2.. 1..')
            await asyncio.sleep(2)
            await msg.delete()
            array_card = await get_card()
            card_link = array_card[0]
            card_name = array_card[1]
            card_rarity = array_card[2]
            card_points = array_card[3]
            card_description = array_card[4]
            card_id = array_card[5]
            proj_link = array_card[6]
            await rq.to_collection(card_id, message.from_user.id, card_link)
            await message.answer_photo(photo = card_link, caption = f'*{card_name}*\n\nRarity: _{card_rarity}_\nXStars: _+{card_points}_\nProject: [Click here]({proj_link})\n\nDescription: _{card_description}_', parse_mode = 'Markdown', reply_markup = kb.go_to_menu)
            
            points_before = await rq.view_points(message.from_user.id)
            points_all = points_before + card_points
            await rq.delete_points(message.from_user.id)
            #print(points_all)
            await rq.add_points(message.from_user.id, points_all)

            last_recieve = datetime.datetime.now()
            await rq.delete_time_check(message.from_user.id)
            await rq.time_check(str(last_recieve), message.from_user.id)
            #print('true2')

#меню
@router.callback_query(F.data == 'go_to_menu')
async def menu(callback: CallbackQuery):
    cards_counter = 0
    cards_list = []
    await callback.answer()
    #await callback.message.answer_photo(photo = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQq__sgD-quFzFtu4Qa2H_JeRW3sDwGI5Q4uA&s', caption = 'Добро пожаловать в меню :)', reply_markup = kb.menu)
    await callback.message.edit_media( InputMediaPhoto(media = 'https://disk.yandex.ru/i/xAW4O_iAwlYjNQ', caption = 'Welcome to the menu :)'), reply_markup = kb.menu )

#меню2 - из "time remaining"
@router.callback_query(F.data == 'go_to_menu2')
async def menu(callback: CallbackQuery):
    cards_counter = 0
    cards_list = []
    await callback.answer()
    #https://disk.yandex.ru/i/xAW4O_iAwlYjNQ
    #https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQq__sgD-quFzFtu4Qa2H_JeRW3sDwGI5Q4uA&s
    #await callback.message.answer_photo(photo = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQq__sgD-quFzFtu4Qa2H_JeRW3sDwGI5Q4uA&s', caption = 'Добро пожаловать в меню :)', reply_markup = kb.menu)
    await callback.message.answer_photo(photo = 'https://disk.yandex.ru/i/xAW4O_iAwlYjNQ', caption = 'Welcome to the menu :)', reply_markup = kb.menu )

#коллекция
@router.callback_query(F.data == 'collection')
async def collection(callback: CallbackQuery):
    await callback.answer()
    cards_list = await rq.collection_cards(callback.from_user.id)
    details_list = await rq.details_collection_cards(cards_list[0])

    points = await rq.view_points(callback.from_user.id)

    #rating_place = await rq.rating_place(callback.from_user.id)

    await callback.message.edit_media( InputMediaPhoto(media = details_list[0], caption = emoji.emojize(f':card_file_box: *Your collection* \n\n*Card number: {cards_counter}*\nProject: [{details_list[1]}]({details_list[6]})\n\nRarity: _{details_list[2]}_\nXStars: _+{details_list[3]}_\nCards description: _{details_list[4]}_\n\n*Your XStars: {points}:glowing_star:*'), parse_mode = 'Markdown'), reply_markup = kb.arrows )

cards_counter = 1
#листаем коллекцию
@router.callback_query(F.data == '>')
async def collection_swap(callback: CallbackQuery):
    await callback.answer()

    cards_list = await rq.collection_cards(callback.from_user.id)

    global cards_counter
    cards_counter += 1
    if cards_counter > len(cards_list):
        cards_counter = 1

    details_list = await rq.details_collection_cards(cards_list[cards_counter-1])

    points = await rq.view_points(callback.from_user.id)
    await callback.message.edit_media( InputMediaPhoto(media = details_list[0], caption = emoji.emojize(f':card_file_box: *Your collection* \n\n*Card number: {cards_counter}*\nProject: [{details_list[1]}]({details_list[6]})\n\nRarity: _{details_list[2]}_\nXStars: _+{details_list[3]}_\nCards description: _{details_list[4]}_\n\n*Your XStars: {points}:glowing_star:*'), parse_mode = 'Markdown'), reply_markup = kb.arrows )
@router.callback_query(F.data == '<')
async def collection_swap(callback: CallbackQuery):
    await callback.answer()

    cards_list = await rq.collection_cards(callback.from_user.id)
    global cards_counter
    cards_counter -= 1
    if cards_counter < 1:
        cards_counter = len(cards_list)
    details_list = await rq.details_collection_cards(cards_list[cards_counter-1])

    points = await rq.view_points(callback.from_user.id)

    await callback.message.edit_media( InputMediaPhoto(media = details_list[0], caption = emoji.emojize(f':card_file_box: *Your collection* \n\n*Card number: {cards_counter}*\nProject: [{details_list[1]}]({details_list[6]})\n\nRarity: _{details_list[2]}_\nXStars: _+{details_list[3]}_\nCards description: _{details_list[4]}_\n\n*Your XStars: {points}:glowing_star:*'), parse_mode = 'Markdown'), reply_markup = kb.arrows )

@router.callback_query(F.data == 'tasks')
async def collection_swap(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_caption( caption = emoji.emojize(f'Here you can earn more XStars :star: \n\n_This section of the bot is still under development..._'), parse_mode = 'Markdown', reply_markup = kb.go_to_menu)

@router.callback_query(F.data == 'refs')
async def collection_swap(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_caption( caption = emoji.emojize(f':loudspeaker: _Your referral link:_ https://t.me/the_project_x_bot/app?startapp=ref_wniwWin\n~\nInvited friends: \n~\nEarned from friends: '), parse_mode = 'Markdown', reply_markup = kb.top_refs)

@router.callback_query(F.data == 'top_refs')
async def collection_swap(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_caption( caption = emoji.emojize(f':crown: *The TOP ref-players:*\n\n:1st_place_medal: 1. ... \n:2nd_place_medal: 2. ... \n:3rd_place_medal: 3. ... \n\nYour position: 8'), parse_mode = 'Markdown', reply_markup = kb.go_to_menu)

@router.callback_query(F.data == 'trade')
async def collection_swap(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_caption( caption = emoji.emojize(f'Here you can trade your extra cards :joker: \n\n_This section of the bot is still under development..._'), parse_mode = 'Markdown', reply_markup = kb.go_to_menu)




































#ниже лишнее, не для бота
"""
@router.message(Command('test'))
async def test(message: Message):

@router.message(F.text == 'Получить')
async def get_the_card(message: Message):
    number_card = random.randint(0,9)
    await message.answer_photo(photo = cards[number_card])
    https://changelly.com/blog/wp-content/uploads/2023/09/ton_logo_light_background.png
https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQq__sgD-quFzFtu4Qa2H_JeRW3sDwGI5Q4uA&s

cards = [
    'https://disk.yandex.com/i/rXZd_pPM_wrJuw',
    'https://disk.yandex.com/i/Y7XnR45B_TDLQw',
    'https://disk.yandex.com/i/ekOURQQuC8ITsw',
    'https://disk.yandex.com/i/WKp0MQQK0ZsNRQ',
    'https://disk.yandex.com/i/tMMIrdczEXdt1w',
    'https://disk.yandex.com/i/CKgud8VMGF79bA',
    'https://disk.yandex.com/i/y5Pg2cHt9snTow',
    'https://disk.yandex.com/i/eBeKu5CkA-34DA',
    'https://disk.yandex.com/i/p0RrvM-1vwoCSA',
    'https://disk.yandex.com/i/VKhCQHFIfir-qw',
    'https://disk.yandex.com/i/3_zEV-DgkWJpJQ'
]

#@router.message()
async def autodelete(message: Message):
    msg = await message.answer('u gay')
    await asyncio.sleep(5) 
    await msg.delete()


@router.message(Command('help'))    
async def get_help(message: Message):
    await message.answer('Тебе не нужна помощь, мне нужна')

@router.message(F.text == 'Что скажешь?')
async def h_a_y(message: Message):
    await message.answer('Super!')

@router.message(F.photo)
async def _photo(message: Message):
    await message.answer(f'Photo ID: {message.photo[-1]}')

@router.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo ='https://disk.yandex.com/i/VKhCQHFIfir-qw')

@router.callback_query(F.data == 'catalogue')
async def catalogue(callback: CallbackQuery):
    await callback.answer('', show_alert = True)
    await callback.message.edit_text('Hiiiii', reply_markup = await kb.inline_cars())

@router.message(Command('reg'))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Имя?')

@router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer('Телефон?')

@router.message(Reg.number)
async def reg_three(message: Message, state: FSMContext):
    await state.update_data(number = message.text)
    data = await state.get_data()
    await message.answer(f'Спасибо! \n Имя:{data["name"]} \n Номер:{data["number"]}')
    await state.clear()
"""