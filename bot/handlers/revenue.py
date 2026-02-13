"""
Обработчики для добавления выручки любым пользователем
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.database import get_db
from database.models import User, PartnerRevenue
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from bot.states.states import RevenueStates
from bot.keyboards.keyboards import get_main_menu_keyboard, get_cancel_keyboard

router = Router()


@router.callback_query(F.data == "menu_add_revenue")
async def menu_add_revenue_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Обработчик кнопки добавления выручки из inline-меню"""
    await callback_query.message.answer(
        "💰 <b>Добавление выручки</b>\n\n"
        "Введите сумму выручки в рублях (только число):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(RevenueStates.waiting_for_amount)
    await callback_query.answer()


@router.message(F.text == "💰 Добавить выручку")
async def add_revenue_start_handler(message: Message, state: FSMContext) -> None:
    """
    Обработчик начала добавления выручки
    """
    await state.clear()
    
    await message.answer(
        "💰 <b>Добавление выручки</b>\n\n"
        "Введите сумму выручки в рублях (только число):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(RevenueStates.waiting_for_amount)


@router.message(RevenueStates.waiting_for_amount)
async def process_revenue_amount(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода суммы выручки
    """
    try:
        amount = int(message.text.replace(' ', '').replace(',', '.'))
        if amount <= 0:
            await message.answer("Сумма должна быть положительным числом. Попробуйте ещё раз:")
            return
        
        await state.update_data(amount=amount)
        
        await message.answer(
            f"💰 Сумма: <b>{amount:,} ₽</b>\n\n"
            "Введите описание сделки (откуда пришла выручка):",
            reply_markup=get_cancel_keyboard()
        )
        await state.set_state(RevenueStates.waiting_for_description)
        
    except ValueError:
        await message.answer(
            "Пожалуйста, введите число без пробелов и символов.\n"
            "Например: 50000"
        )


@router.message(RevenueStates.waiting_for_description)
async def process_revenue_description(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода описания и сохранение выручки
    """
    description = message.text.strip()
    data = await state.get_data()
    amount = data.get('amount')
    
    if not description:
        description = "Добавлено через бота"
    
    user_id = None
    
    async with get_db() as db:
        # Находим пользователя
        result = await db.execute(
            select(User).filter(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            user_id = user.id
            
            # Создаём запись о выручке
            new_revenue = PartnerRevenue(
                partner_id=user_id,  # partner_id совместим с user_id
                amount=amount,
                description=description
            )
            db.add(new_revenue)
            await db.commit()
            
            success_text = (
                f"✅ <b>Выручка успешно добавлена!</b>\n\n"
                f"💰 Сумма: <b>{amount:,} ₽</b>\n"
                f"📝 Описание: {description}\n\n"
                f"Спасибо за использование нашего сервиса!"
            )
        else:
            success_text = (
                "⚠️ Ошибка: пользователь не найден в системе.\n"
                "Пожалуйста, перезапустите бота командой /start"
            )
    
    await message.answer(
        success_text,
        reply_markup=get_main_menu_keyboard()
    )
    await state.clear()


@router.message(F.text == "❌ Отмена", RevenueStates())
async def cancel_revenue(message: Message, state: FSMContext) -> None:
    """
    Отмена добавления выручки
    """
    await state.clear()
    await message.answer(
        "❌ Добавление выручки отменено.",
        reply_markup=get_main_menu_keyboard()
    )


def register_revenue_handlers(dp):
    """Регистрация обработчиков"""
    dp.include_router(router)
