from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from database import get_or_create_user
from keyboards.main import get_main_menu
router = Router()

@router.message(CommandStart())
async def start_cmd(message: Message):
    await get_or_create_user(message.from_user.id, message.from_user.first_name)
    await message.answer("Привет! Я бот автосервиса.", reply_markup=get_main_menu())
