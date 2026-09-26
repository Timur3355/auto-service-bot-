from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from data.services import SERVICES_BY_ID
from parser import get_part_price
from keyboards.main import get_catalog_kb

router = Router()

class Calc(StatesGroup):
    wait_car = State()

@router.callback_query(F.data == "calc_start")
async def start_calc(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer("Выберите услугу для расчета:", reply_markup=get_catalog_kb())
    await state.set_state(Calc.wait_car)
    await cb.answer()

@router.callback_query(Calc.wait_car, F.data.startswith("srv_"))
async def pick_srv(cb: CallbackQuery, state: FSMContext):
    sid = int(cb.data.split("_")[1])
    s = SERVICES_BY_ID.get(sid)
    if s:
        await state.update_data(srv=s)
        await cb.message.answer(f"Выбрано: {s['name']}. Напишите марку авто:")
    await cb.answer()

@router.message(Calc.wait_car)
async def get_car(msg: Message, state: FSMContext):
    data = await state.get_data()
    s = data.get('srv')
    if not s: 
        return
    
    p = await get_part_price()
    total = s['price'] + p['price']
    
    # Собираем сообщение по частям
    result = f"✅ Расчет для {msg.text}:\n"
    result += f"Работа: {s['price']}р\n"
    result += f"Запчасть: {p['price']}р\n"
    result += f"<b>Итого: {total}р</b>"
    
    await msg.answer(result, parse_mode="HTML")
    await state.clear()