from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()

class friendname (StatesGroup):
    adress = State()
    sendtext = State()




@router.message(CommandStart())
async def cmd_start(message: Message):
    username = message.from_user.username
    await message.answer(f"Твой ник: @{username}")
    await message.answer('Привет!', reply_markup = kb.main)
    await message.reply('Этот бот принимает анонимные сообщения и пересылает их вам, сохраняя конфиденциальность отправителя. Вы можете отвечать на сообщения — бот доставит ваш ответ, не раскрывая ваших данных. Просто напишите боту, и он станет вашим секретным посредником!')
    await rq.set_user(message.from_user.id, username)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи')




@router.message(F.text == 'Выбрать функцию')
async def cmd_message(message: Message):
    await message.answer('Выберите функцию', reply_markup = kb.send)

@router.callback_query(F.data == 'input')
async def input(callback : CallbackQuery, state: FSMContext):
    await callback.answer("Вы выбрали отправку анонимных сообщений", show_alert = True)
    await state.set_state(friendname.adress)
    await callback.message.answer('Напишите ник пользователя, которому вы хотите отправить сообщение.')

@router.message(friendname.adress)
async def name_nick(message: Message, state =  FSMContext):
    username = message.text 
    
    receiver_id = await rq.get_id_by_username(username)
    
    if not receiver_id:
        await message.answer("Пользователь не найден в базе данных")
        await state.clear()
        return
    
    await state.update_data(
        adress=username,
        receiver_id=receiver_id  
    )
    

    await message.answer(f"Юзернейм {username} сохранён!")  

    await state.set_state(friendname.sendtext)
    await message.answer('Напишите сообщение, которое вы хотите отправить.')


@router.message(friendname.sendtext)
async def text_message(message: Message, state =  FSMContext):
    text = message.text 
    
    await state.update_data(sendtext = text)
    data = await state.get_data()
    saved_text = data['sendtext']

    await rq.set_message(
        text= saved_text,
        user1 = message.from_user.id,
        user2=data['receiver_id']
    )
    


    await message.answer(f"Сообщение {saved_text} сохранено!")  

    data = await state.get_data()

    await state.clear()




@router.callback_query(F.data == 'read')
async def input(callback : CallbackQuery):
    await callback.answer("Здесь будут показаны соощения для вас", show_alert = True)
    user_id = callback.from_user.id
    message = await rq.get_first_message(user_id)
    
    if not message:
        await callback.message.answer(f"У вас нет сообщений")
        return

    await callback.message.answer(f"{message.text}")

    await rq.delete_message(message.id)

    await callback.message.answer("Показать ещё сообщения?", reply_markup = kb.another)

@router.message(F.text == 'Показать ещё сообщения?')
async def cmd_message(message: Message):
    await message.answer('Выберите функцию', reply_markup = kb.send)



@router.callback_query(F.data == 'newmessanges')
async def input(callback : CallbackQuery):
    await callback.answer("Вы смотрите новые сообщения", show_alert = True)

    user_id = callback.from_user.id
    message = await rq.get_first_message(user_id)
    
    if not message:
        await callback.message.answer(f"У вас нет сообщений")
        return

    await callback.message.answer(f"{message.text}")

    await rq.delete_message(message.id)

    await callback.message.answer("Показать ещё сообщения?", reply_markup = kb.another)
    

@router.callback_query(F.data == 'sleep')
async def input(callback : CallbackQuery):
    await callback.answer("Если вы захоите увидеть новые сообщения, нажмите на кпопку: Показать ещё сообщния", show_alert = True)

