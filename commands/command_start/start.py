import asyncio
from .states import Wait, TimeUser
from .keyboards import Keyboards
from .answers import Answers

from aiogram import Router, F, types
from aiogram.types import Message 
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router(name=__name__)

place = [0,0,0,0]
y = [19, 22, 61, 43]




@router.message(TimeUser.timeForWait, Command('start'))
async def start_checking_place(message: Message, state: FSMContext):
    builder = types.ReplyKeyboardMarkup(keyboard=Keyboards.KeyboardCancel(), resize_keyboard=True, input_field_placeholder="Выберите место")
    msg = Answers.AnswerRection(place, y)
    await message.answer(msg)
    for x in range(len(place)):
        if place[x] == message.from_user.username:
            num = x
            break 
    await message.answer(f"Ваше место под номером {y[num]} место", reply_markup=builder)

@router.message(TimeUser.timeForWait, F.text == "Показать все места на данный момент")
async def start_checking_place(message: Message, state: FSMContext):
    builder = types.ReplyKeyboardMarkup(keyboard=Keyboards.KeyboardCancel(), resize_keyboard=True, input_field_placeholder="Выберите место")
    msg = Answers.AnswerRection(place, y)
    await message.answer(msg)
    for x in range(len(place)):
        if place[x] == message.from_user.username:
            num = x
            break 
    await message.answer(f"Ваше место под номером {y[num]} место", reply_markup=builder)


@router.message(TimeUser.timeForWait, F.text == "Завершить парковку")
async def start_canceled_place(message: Message, state: FSMContext):
    await state.clear()
    for x in range(len(place)):
        if place[x] == message.from_user.username:
            place[x] = 0
            builder = types.ReplyKeyboardMarkup(keyboard=Keyboards.KeyboardUploadTable(), resize_keyboard=True)
            await message.answer("Спасибо за вашу работу в офисе", reply_markup=builder)
            break


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):  
    msg = Answers.AnswerRection(place, y)
    await message.answer(msg, reply_markup=Keyboards.Keyboard1Per4().as_markup(resize_keyboard=True, input_field_placeholder="Выберите место"))
    await state.set_state(Wait.number)


@router.message(F.text == "Показать все места на данный момент")
async def start(message: Message, state: FSMContext):  
    msg = Answers.AnswerRection(place, y)
    await message.answer(msg, reply_markup=Keyboards.Keyboard1Per4().as_markup(resize_keyboard=True, input_field_placeholder="Выберите место"))
    await state.set_state(Wait.number)

    

@router.message(Wait.number, (F.text == '19') | (F.text == '22') | (F.text == '61') | (F.text == '43'))  
async def search_place(message: Message, state: FSMContext):
    await state.clear()
    if message.text == "19":
        num_place = 1
    elif message.text == "22":
        num_place = 2
    elif message.text == "61":
        num_place = 3
    elif message.text == "43":
        num_place = 4  
    if place[num_place-1] != 0:
        await message.answer("Место занято. Выберете другое место", reply_markup=types.ReplyKeyboardRemove())
    else:
        builder = types.ReplyKeyboardMarkup(keyboard=Keyboards.KeyboardTime(), resize_keyboard=True, input_field_placeholder="Сколько планируете находиться на парковке?")
        place[num_place-1] = message.from_user.username
        await state.set_state(TimeUser.timeForWait)
        await message.reply("Сколько планируете находиться на парковке?", reply_markup=builder) 


@router.message(Wait.number)
async def search_place_invalid(message: Message):
    await message.answer("Напиши-ка ещё раз число...")


@router.message(TimeUser.timeForWait, (F.text == "30 минут") | (F.text == "1 час") | (F.text == "2 часа"))
async def inf_timer_with_break(message: Message, state: FSMContext):

    builder = types.ReplyKeyboardMarkup(keyboard=Keyboards.KeyboardCancel(), resize_keyboard=True)
    await message.answer("Окей", reply_markup=builder)

    if message.text == "30 минут":
        time_ = 30 
    elif message.text == "1 час":
        time_ = 60 
    elif message.text == "2 часа":
        time_ = 120
    
    for x in range(len(place)):
        if place[x] == message.from_user.username:
            usr = True
            break
        else:
            usr = False
    
    if usr == False:
        builder = types.ReplyKeyboardMarkup(keyboard=Keyboards.KeyboardUploadTable(), resize_keyboard=True)
        await message.answer("Что-то пошло не так", reply_markup=builder)

    else:
        await asyncio.sleep(time_)

        for x in range(len(place)):
            if place[x] == message.from_user.username:  
                builder = types.ReplyKeyboardMarkup(keyboard=Keyboards.KeyboardYesOrNo(), resize_keyboard=True, input_field_placeholder="Вы уехали с места парковки?")
                await message.answer("Вы уехали с места парковки?", reply_markup=builder)
                await state.set_state(TimeUser.timeToAnswer)
                await asyncio.sleep(30)

                if await state.get_state() == "TimeUser:timeToAnswer":
                    await state.clear()
                    for x in range(len(place)):
                        if place[x] == message.from_user.username:
                            place[x] = 0
                    builder = types.ReplyKeyboardMarkup(keyboard=Keyboards.KeyboardUploadTable(), resize_keyboard=True)
                    await message.answer("Место вашей парковки свободно для всех пользователей.", reply_markup=builder)
                break


@router.message(TimeUser.timeToAnswer, (F.text == "Нет"))
async def no(message: Message, state: FSMContext):
    await state.set_state(TimeUser.timeForWait)
    builder = types.ReplyKeyboardMarkup(keyboard=Keyboards.KeyboardTime(), resize_keyboard=True, input_field_placeholder="Сколько еще планируете находиться на парковке?")
    await message.reply("Сколько еще планируете находиться на парковке?", reply_markup=builder) 


@router.message(TimeUser.timeToAnswer, (F.text == "Да"))
async def yes(message: Message, state: FSMContext):
    for x in range(len(place)):
        if place[x] == message.from_user.username:
            await state.clear()
            place[x] = 0
            builder = types.ReplyKeyboardMarkup(keyboard=Keyboards.KeyboardUploadTable(), resize_keyboard=True)
            await message.answer("Спасибо за вашу работу в офисе", reply_markup=builder)
            break


