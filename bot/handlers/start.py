"""
Обработчики команды /start и главного меню
Оптимизированная версия с улучшенной обработкой реферальных ссылок
"""
import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from database.database import get_db
from database.models import User, ReferralLink, ReferralRelationship, ServiceRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from bot.keyboards.keyboards import (
    get_main_menu_keyboard,
    get_legal_services_keyboard,
    get_partner_profile_keyboard,
    get_faq_categories_keyboard,
    get_back_keyboard
)

from bot.handlers.case_messages import get_user_cases, format_cases_list

# Настройка логирования
logger = logging.getLogger(__name__)

router = Router()

# Текст приветствия
WELCOME_TEXT = (
    "Партнёрство строится на взаимовыгодном сотрудничестве. Вы рекомендуете нашу юридическую помощь своим клиентам, а мы гарантируем вам вознаграждение за каждую успешную сделку.\n\n"
    "Основной принцип — прогрессивная комиссия: чем выше общая выручка от ваших клиентов за календарный месяц, тем больший процент от этой суммы вы получаете. Также есть реферальная система, чтобы вы получали пассивный доход\n\n"
    "Выберите интересующий вас раздел:"
)


# ============================================
# Вспомогательные функции
# ============================================

async def get_or_create_user(
    db: AsyncSession,
    user_id: int,
    username: str = None,
    first_name: str = None,
    last_name: str = None
) -> User:
    """
    Получает существующего пользователя или создает нового
    
    Args:
        db: Сессия базы данных
        user_id: Telegram ID пользователя
        username: Username в Telegram
        first_name: Имя
        last_name: Фамилия
    
    Returns:
        User: Объект пользователя
    """
    result = await db.execute(select(User).filter(User.telegram_id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            telegram_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Создан новый пользователь: {user_id}")
        
        # Отправляем уведомление в чат админов
        await send_new_user_notification(user)
    else:
        # Обновляем данные пользователя если изменились
        updated = False
        if username and user.username != username:
            user.username = username
            updated = True
        if first_name and user.first_name != first_name:
            user.first_name = first_name
            updated = True
        if last_name and user.last_name != last_name:
            user.last_name = last_name
            updated = True
        
        if updated:
            await db.commit()
            logger.debug(f"Обновлены данные пользователя: {user_id}")
    
    return user


async def send_new_user_notification(user: User):
    """
    Отправляет уведомление в чат админов о новом пользователе
    
    Args:
        user: Объект нового пользователя
    """
    try:
        from config.settings import settings
        from bot.main import bot
        
        admin_chat_id = settings.ADMIN_CHAT_ID
        if admin_chat_id:
            # Форматируем сообщение
            user_info = (
                f"👤 Новый пользователь:\n"
                f"ID: {user.telegram_id}\n"
                f"Имя: {user.first_name or 'Не указано'}\n"
                f"Фамилия: {user.last_name or 'Не указано'}\n"
                f"Username: @{user.username}" if user.username else "Username: Не указан"
            )
            
            await bot.send_message(
                chat_id=admin_chat_id,
                text=user_info
            )
            logger.info(f"Уведомление о новом пользователе {user.telegram_id} отправлено в чат админов")
        else:
            logger.warning("ADMIN_CHAT_ID не настроен, уведомление не отправлено")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления о новом пользователе {user.telegram_id}: {e}")


async def process_referral(
    db: AsyncSession,
    referral_code: str,
    new_user: User
) -> bool:
    """
    Обрабатывает реферальную ссылку
    
    Args:
        db: Сессия базы данных
        referral_code: Реферальный код
        new_user: Новый пользователь
    
    Returns:
        bool: True если реферальная связь успешно создана
    """
    if not referral_code:
        return False
    
    try:
        # Находим реферальную ссылку
        result = await db.execute(
            select(ReferralLink).filter(ReferralLink.referral_code == referral_code)
        )
        referral_link = result.scalar_one_or_none()
        
        if not referral_link:
            logger.warning(f"Реферальный код не найден: {referral_code}")
            return False
        
        # Проверяем, что пользователь не приглашает сам себя
        if referral_link.partner_id == new_user.id:
            logger.warning(f"Пользователь {new_user.id} пытается использовать свою реферальную ссылку")
            return False
        
        # Проверяем, что связь еще не существует
        existing = await db.execute(
            select(ReferralRelationship).filter(
                ReferralRelationship.referred_id == new_user.id
            )
        )
        if existing.scalar_one_or_none():
            logger.debug(f"Реферальная связь уже существует для пользователя {new_user.id}")
            return False
        
        # Создаем реферальную связь
        relationship = ReferralRelationship(
            referrer_id=referral_link.partner_id,
            referred_id=new_user.id
        )
        db.add(relationship)
        await db.commit()
        
        logger.info(
            f"Создана реферальная связь: реферер={referral_link.partner_id}, "
            f"реферал={new_user.id}"
        )
        return True
    
    except Exception as e:
        logger.error(f"Ошибка при обработке реферальной ссылки: {e}")
        await db.rollback()
        return False


# ============================================
# Обработчики команд
# ============================================

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    logger.info(f"Команда /start от пользователя {user_id}")
    
    async with get_db() as db:
        # Создаем или получаем пользователя
        user = await get_or_create_user(
            db, user_id, username, first_name, last_name
        )
        
        # Проверяем реферальный код
        command_parts = message.text.split(' ')
        if len(command_parts) > 1:
            referral_code = command_parts[1]
            await process_referral(db, referral_code, user)
    
    # Отправляем приветствие
    await message.answer(WELCOME_TEXT, reply_markup=get_main_menu_keyboard())


@router.message(F.text == "📋 Услуги")
async def services_handler(message: Message) -> None:
    """Обработчик раздела 'Услуги'"""
    text = (
        "<b>Наши услуги:</b>\n\n"
        "Мы предлагаем широкий спектр юридических услуг для вашего бизнеса. "
        "Выберите интересующую вас категорию услуг:"
    )
    await message.answer(text, reply_markup=get_legal_services_keyboard())


@router.message(F.text == "📚 История услуг")
async def history_handler(message: Message) -> None:
    """Обработчик раздела 'История услуг'"""
    user_id = message.from_user.id

    async with get_db() as db:
        # Находим пользователя
        result = await db.execute(select(User).filter(User.telegram_id == user_id))
        user = result.scalar_one_or_none()

        if user:
            # Получаем историю заявок пользователя
            result = await db.execute(
                select(ServiceRequest)
                .filter(ServiceRequest.user_id == user.id)
                .order_by(ServiceRequest.created_at.desc())
            )
            requests = result.scalars().all()

            if requests:
                history_text = "<b>Ваша история заявок:</b>\n\n"
                for req in requests:
                    created_at = req.created_at.strftime('%d.%m.%Y %H:%M') if req.created_at else 'не указана'
                    description = req.description[:50] if req.description else ''
                    if len(req.description or '') > 50:
                        description += '...'

                    history_text += (
                        f"• ID: {req.id}\n"
                        f"  Статус: {req.status}\n"
                        f"  Дата: {created_at}\n"
                        f"  Описание: {description}\n\n"
                    )
            else:
                history_text = "У вас пока нет заявок."
        else:
            history_history_text = "Ошибка: пользователь не найден в системе."

    await message.answer(history_text, reply_markup=get_back_keyboard())


@router.callback_query(F.data == "menu_history")
async def menu_history_callback_handler(callback_query: CallbackQuery) -> None:
    """Обработчик callback 'История услуг' из inline-меню"""
    user_id = callback_query.from_user.id

    async with get_db() as db:
        result = await db.execute(select(User).filter(User.telegram_id == user_id))
        user = result.scalar_one_or_none()

        if user:
            result = await db.execute(
                select(ServiceRequest)
                .filter(ServiceRequest.user_id == user.id)
                .order_by(ServiceRequest.created_at.desc())
            )
            requests = result.scalars().all()

            if requests:
                history_text = "<b>Ваша история заявок:</b>\n\n"
                for req in requests:
                    created_at = req.created_at.strftime('%d.%m.%Y %H:%M') if req.created_at else 'не указана'
                    description = req.description[:50] if req.description else ''
                    if len(req.description or '') > 50:
                        description += '...'

                    history_text += (
                        f"• ID: {req.id}\n"
                        f"  Статус: {req.status}\n"
                        f"  Дата: {created_at}\n"
                        f"  Описание: {description}\n\n"
                    )
            else:
                history_text = "У вас пока нет заявок."
        else:
            history_text = "Ошибка: пользователь не найден в системе."

    await callback_query.message.edit_text(history_text, reply_markup=get_partner_profile_keyboard())
    await callback_query.answer()


@router.callback_query(F.data == "menu_my_cases")
async def menu_my_cases_callback_handler(callback_query: CallbackQuery, state) -> None:
    """Обработчик callback 'Поддержка' из inline-меню"""
    from aiogram.fsm.context import FSMContext
    user_id = callback_query.from_user.id
    logger.info(f"Пользователь {user_id} открыл раздел поддержки из inline-меню")

    try:
        async with get_db() as db:
            cases = await get_user_cases(db, user_id)

            text = "<b>💬 Переписка с администратором</b>\n\n"
            text += format_cases_list(cases)
            text += (
                "💌 Вы можете написать сообщение администратору в любое время.\n\n"
                "<b>Просто напишите текст вашего сообщения ниже, и оно будет отправлено администратору.</b>"
            )

            await state.clear()

            await callback_query.message.answer(text, reply_markup=get_main_menu_keyboard())
            await callback_query.answer()

    except Exception as e:
        logger.exception(f"Ошибка в обработчике поддержки для пользователя {user_id}: {e}")
        await callback_query.message.answer("⚠️ Произошла ошибка. Попробуйте позже.")


@router.message(F.text == "👤 Партнёрский профиль")
async def profile_handler(message: Message) -> None:
    """Обработчик раздела 'Партнёрский профиль'"""
    text = "Управление вашим партнёрским профилем:"
    await message.answer(text, reply_markup=get_partner_profile_keyboard())


@router.message(F.text == "❓ FAQ")
async def faq_handler(message: Message) -> None:
    """Обработчик раздела 'FAQ'"""
    text = "<b>Выберите категорию вопросов:</b>"
    await message.answer(text, reply_markup=get_faq_categories_keyboard())


# ============================================
# Обработчики навигации
# ============================================

@router.callback_query(F.data == "back_to_main")
async def back_to_main_handler(callback_query: CallbackQuery) -> None:
    """Обработчик кнопки 'Назад'"""
    await callback_query.message.answer(
        "Выберите интересующий вас раздел:",
        reply_markup=get_main_menu_keyboard()
    )
    try:
        await callback_query.message.delete()
    except Exception:
        pass
    await callback_query.answer()


@router.callback_query(F.data == "back_to_legal_services")
async def back_to_legal_services_handler(callback_query: CallbackQuery) -> None:
    """Обработчик кнопки 'Назад к юридическим услугам'"""
    text = (
        "<b>Наши услуги:</b>\n\n"
        "Мы предлагаем широкий спектр юридических услуг для вашего бизнеса. "
        "Выберите интересующую вас категорию услуг:"
    )
    await callback_query.message.edit_text(
        text,
        reply_markup=get_legal_services_keyboard()
    )
    await callback_query.answer()


def register_start_handlers(dp):
    """Регистрация обработчиков"""
    dp.include_router(router)
