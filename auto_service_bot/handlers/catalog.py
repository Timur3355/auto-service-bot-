from aiogram import Router, F
from aiogram.types import CallbackQuery
from data.services import SERVICES_BY_ID
from keyboards.main import get_catalog_kb

router = Router()

@router.callback_query(F.data == "catalog")
async def show_cat(cb: CallbackQuery):
    await cb.message.edit_text("Выберите услугу:", reply_markup=get_catalog_kb())
    await cb.answer()

@router.callback_query(F.data.startswith("srv_"))
async def show_srv(cb: CallbackQuery):
    sid = int(cb.data.split("_")[1])
    s = SERVICES_BY_ID.get(sid)
    if s:
        # Формируем текст по частям, чтобы не было ошибок с кавычками
        msg = f"{s['name']}\n"
        msg += f"Цена работы: {s['price']}р"
        await cb.message.edit_text(msg)
    await cb.answer()

@router.callback_query(F.data == "cancel")
async def cancel(cb: CallbackQuery, state):
    from aiogram.fsm.context import FSMContext
    await state.clear()
    from keyboards.main import get_main_menu
    await cb.message.edit_text("Отменено.", reply_markup=get_main_menu())
    await cb.answer()