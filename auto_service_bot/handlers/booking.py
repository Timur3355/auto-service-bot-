from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID
from database import create_appointment
from keyboards.main import get_catalog_kb, get_date_kb

router = Router()

class Book(StatesGroup):
    pick_srv = State()
    pick_date = State()

@router.callback_query(F.data == "book_start")
async def start_book(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer("Запись. Выберите услугу:", reply_markup=get_catalog_kb())
    await state.set_state(Book.pick_srv)
    await cb.answer()

@router.callback_query(Book.pick_srv, F.data.startswith("srv_"))
async def pick_srv(cb: CallbackQuery, state: FSMContext):
    await state.update_data(sid=int(cb.data.split("_")[1]))
    await cb.message.answer("Выберите дату:", reply_markup=get_date_kb())
    await state.set_state(Book.pick_date)
    await cb.answer()

@router.callback_query(Book.pick_date, F.data.startswith("d_"))
async def pick_date(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    d_map = {"d_today": "Сегодня", "d_tomorrow": "Завтра"}
    date_str = d_map.get(cb.data, cb.data)
    
    await create_appointment(cb.from_user.id, data['sid'], date_str)
    
    try:
        if ADMIN_ID: 
            admin_msg = f"Запись: {cb.from_user.id} на {date_str}"
            await cb.bot.send_message(ADMIN_ID, admin_msg)
    except: 
        pass
        
    await cb.message.answer(f"✅ Записаны на {date_str}!")
    await state.clear()
    await cb.answer()