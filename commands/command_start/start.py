import asyncio
import time
from datetime import datetime
from .states import Wait, TimeUser

from aiogram import Router, F, types
from aiogram.types import Message 
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext

router = Router(name=__name__)

place = [0,0,0,0]

usr = 0
num_place = 0


@router.message(TimeUser.timeForWait, Command('start'))
async def start_checking_place(message: Message, state: FSMContext):
    kb = [[
        types.KeyboardButton(text="Отказаться от места"),
    ]]

    builder = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите место")

    for x in range(len(place)):
        msg = ""
        if place[x] != 0:
            msg += f"🔴 {x+1} место\n"
        else:
            msg += f"🟢 {x+1} место\n"

        await message.answer(msg)
    
    await message.answer(f"Ваше занятое место номер {num_place}", reply_markup=builder)

@router.message(TimeUser.timeForWait, F.text == "Отказаться от места")
async def start_canceled_place(message: Message, state: FSMContext):
    await state.clear()

    place[num_place-1] = 0
    await message.answer("Спасибо за время на парковке", reply_markup=types.ReplyKeyboardRemove())


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(Wait.number)

    kb = [[
        types.KeyboardButton(text="1"),
        types.KeyboardButton(text="2"),
        types.KeyboardButton(text="3"),
        types.KeyboardButton(text="4"),
    ]]

    builder = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите место")

    global usr
    usr = message.from_user.username

    for x in range(len(place)):
        msg = ""
        if place[x] != 0:
            msg += f"🔴 {x+1} место\n"
        else:
            msg += f"🟢 {x+1} место\n"

        await message.answer(msg, reply_markup=builder)

    

@router.message(Wait.number, (F.text == '1') | (F.text == '2') | (F.text == '3') | (F.text == '4'))  
async def search_place(message: Message, state: FSMContext):

    await state.clear()

    print(message.text)
    global num_place

    if message.text == "1":
        num_place = 1
    elif message.text == "2":
        num_place = 2
    elif message.text == "3":
        num_place = 3
    elif message.text == "4":
        num_place = 4
    
    if place[num_place-1] != 0:
        await message.answer("Место занято. Приходите ещё.", reply_markup=types.ReplyKeyboardRemove())

    else:

        kb = [[
            types.KeyboardButton(text="30 минут"),
            types.KeyboardButton(text="1 час"),
            types.KeyboardButton(text="2 часа"),
        ]]
        builder = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите время во-сколько вас упомянуть?")

        place[num_place-1] = usr

        await state.set_state(TimeUser.timeForWait)
        await message.reply("Выберите время во-сколько вас упомянуть?", reply_markup=builder) 


@router.message(Wait.number)
async def search_place_invalid(message: Message):
    await message.answer("Напиши-ка ещё раз число...")


@router.message(TimeUser.timeForWait, (F.text == "30 минут") | (F.text == "1 час") | (F.text == "2 часа"))
async def inf_timer_with_break(message: Message, state: FSMContext):

    await message.answer("Окей", reply_markup=types.ReplyKeyboardRemove())

    if message.text == "30 минут":
        time_ = 30
            
    elif message.text == "1 час":
        time_ = 60
        
    elif message.text == "2 часа":
        time_ = 120

    await asyncio.sleep(time_)

    if place[num_place-1] != 0:

        kb = [[
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет"),
        ]]

        builder = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Продливать ли время?")
        await message.answer("Продливать ли время?", reply_markup=builder)

        start_time = time.time()

        if time.time() - start_time > 10.0:
            state.clear()
            await message.answer("Ваше место освобождено")
        



@router.message(TimeUser.timeForWait, F.text.startswith("Да"))
async def yes(message: Message):

    if message.text == "Да":
        kb = [[
            types.KeyboardButton(text="30 минут"),
            types.KeyboardButton(text="1 час"),
            types.KeyboardButton(text="2 часа"),
        ]]
        builder = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите время во-сколько вас упомянуть?")
        await message.reply("Выберите время во-сколько вас упомянуть?", reply_markup=builder) 


@router.message(TimeUser.timeForWait, F.text.startswith("Нет"))
async def no(message: Message, state: FSMContext):
    
    global num_place
    
    place[num_place-1] = 0
    await state.clear()

    await message.answer("Спасибо за время на парковке", reply_markup= types.ReplyKeyboardRemove())


