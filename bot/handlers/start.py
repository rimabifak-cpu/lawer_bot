"""
Обработчики команды /start и главного меню
Оптимизированная версия с улучшенной обработкой реферальных ссылок
"""
import sys
import os
import logging
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
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
    get_back_keyboard,
    get_how_to_earn_keyboard
)

from bot.handlers.case_messages import get_user_cases, format_cases_list

# Настройка логирования
logger = logging.getLogger(__name__)

router = Router()

# Текст приветствия
WELCOME_TEXT = (
    "Партнёрство строится на взаимовыгодном сотрудничестве. Вы рекомендуете нашу юридическую помощь своим клиентам, а мы гарантируем вам вознаграждение за каждую успешную сделку и спокойствие за личное и надёжное сопровождение каждого вашего клиента.\n\n"
    "Основной принцип — прогрессивная комиссия: чем выше общая выручка от ваших клиентов за месяц, тем больший процент от этой суммы вы получаете. Также есть реферальная система, чтобы вы получали пассивный доход.\n\n"
    "Вся коммуникация происходит здесь, а вопросы вы можете направить в поддержку @legaldecision\n\n"
    "  \n\n"
    "@legaldecision, поддержка 24/7\n\n"
    "Выберите интересующий вас раздел:"
)

# Текст о процентах дохода
REVENUE_PERCENT_TEXT = (
    "💰 Ваш доход с ежемесячной выручки:\n\n"
    "0 - 100,000 р = 7%\n"
    "100,001 - 250,000 р = 7.5%\n"
    "250,001 - 500,000 р = 8%\n"
    "500,001 - 750,000 р = 8.5%\n"
    "750,001 - 1,000,000 р = 9%\n"
    "1,000,001 - 1,250,000 р = 9.5%\n"
    "1,250,001 - 1,500,000 р = 10%\n"
    "1,500,001 - 1,750,000 р = 11%\n"
    "1,750,001 - 2,000,000 р = 12%\n"
    "2,000,001 р < = 13%\n\n"
    "@legaldecision, поддержка 24/7"
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
    Планирует отправку промо-сообщения через 1 час для новых пользователей
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    logger.info(f"Команда /start от пользователя {user_id}")

    async with get_db() as db:
        # Проверяем, существует ли пользователь
        result = await db.execute(select(User).filter(User.telegram_id == user_id))
        existing_user = result.scalar_one_or_none()
        
        is_new_user = existing_user is None
        
        # Создаем или получаем пользователя
        user = await get_or_create_user(
            db, user_id, username, first_name, last_name
        )

        # Проверяем реферальный код
        command_parts = message.text.split(' ')
        if len(command_parts) > 1:
            referral_code = command_parts[1]
            await process_referral(db, referral_code, user)
        
        # Если пользователь новый - планируем отправку уведомлений
        if is_new_user:
            from bot.utils.delayed_notification import (
                schedule_promo_notification,
                schedule_earnings_notification
            )
            from bot import main as bot_module
            
            # Планируем первое уведомление через 1 час
            await schedule_promo_notification(bot_module.bot, user_id, delay_hours=1)
            logger.info(f"📅 Промо-сообщение запланировано для нового пользователя {user_id}")
            
            # Планируем второе уведомление через 24 часа
            await schedule_earnings_notification(bot_module.bot, user_id, delay_hours=24)
            logger.info(f"📅 Уведомление о результатах запланировано для нового пользователя {user_id}")

    # Отправляем изображение (если файл существует)
    try:
        image_path = "/app/uploads/start_image.jpg"
        if os.path.exists(image_path):
            image = FSInputFile(image_path)
            await message.answer_photo(photo=image)
            await asyncio.sleep(0.3)
        else:
            logger.warning(f"Файл изображения не найден: {image_path}")
    except Exception as e:
        logger.error(f"Ошибка отправки изображения: {e}")

    # Отправляем приветствие
    try:
        logger.info(f"Отправка приветствия пользователю {user_id}")
        await message.answer(WELCOME_TEXT, reply_markup=get_main_menu_keyboard(), parse_mode=None)
        logger.info(f"Приветствие отправлено пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки приветствия: {e}")

    await asyncio.sleep(0.5)

    # Отправляем информацию о процентах дохода (третье сообщение)
    try:
        logger.info(f"Отправка процентов дохода пользователю {user_id}")
        await message.answer(REVENUE_PERCENT_TEXT, parse_mode=None)
        logger.info(f"Проценты дохода отправлены пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки процентов дохода: {e}")

    await asyncio.sleep(0.5)

    # Отправляем кнопку с инструкцией после приветствия
    try:
        logger.info(f"Отправка кнопки инструкции пользователю {user_id}")
        await message.answer(
            "💡 Хотите узнать, как заработать с нами?\n\n"
            "Нажмите кнопку ниже, чтобы получить пошаговую инструкцию:",
            reply_markup=get_how_to_earn_keyboard()
        )
        logger.info(f"Кнопка инструкции отправлена пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки кнопки инструкции: {e}")
    
    logger.info(f"✅ Все сообщения отправлены пользователю {user_id}")


@router.message(F.text == "📋 Услуги")
async def services_handler(message: Message) -> None:
    """Обработчик раздела 'Услуги'"""
    text = (
        "<b>Наши услуги:</b>\n\n"
        "Мы предлагаем широкий спектр юридических услуг для вашего бизнеса. "
        "Выберите интересующую вас категорию услуг:\n\n"
        "  \n\n"
        "@legaldecision, поддержка 24/7"
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
    text = "<b>Выберите категорию вопросов:</b>\n\n  \n\n@legaldecision, поддержка 24/7"
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
        "Выберите интересующую вас категорию услуг:\n\n"
        "  \n\n"
        "@legaldecision, поддержка 24/7"
    )
    await callback_query.message.edit_text(
        text,
        reply_markup=get_legal_services_keyboard()
    )
    await callback_query.answer()


def register_start_handlers(dp):
    """Регистрация обработчиков"""
    dp.include_router(router)

@router.callback_query(F.data == "get_referral_link")
async def get_referral_link_callback_handler(callback_query: CallbackQuery) -> None:
    """Обработчик кнопки 'Получить реферальную ссылку' из уведомления"""
    from sqlalchemy import select

    user_id = callback_query.from_user.id

    async with get_db() as db:
        result = await db.execute(select(User).filter(User.telegram_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            await callback_query.answer("Пользователь не найден", show_alert=True)
            return

        result = await db.execute(
            select(ReferralLink).filter(ReferralLink.partner_id == user.id)
        )
        referral_link = result.scalar_one_or_none()

        if not referral_link:
            import random
            import string
            referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            referral_link = ReferralLink(partner_id=user.id, referral_code=referral_code)
            db.add(referral_link)
            await db.commit()

        bot_username = (await callback_query.bot.get_me()).username
        link = f"https://t.me/{bot_username}?start={referral_link.referral_code}"

        text = f"<b>🔗 Ваша реферальная ссылка</b>\n\nОтправьте друзьям:\n<code>{link}</code>\n\nЗа каждого приглашённого вы будете получать процент!"

        await callback_query.message.answer(text, parse_mode="HTML")
        await callback_query.answer()

@router.callback_query(F.data == "onboarding_instruction")
async def onboarding_instruction_handler(callback_query: CallbackQuery) -> None:
    """Обработчик кнопки 'Показать инструкцию' из onboarding уведомления"""
    text = (
        "<b>🔥 Инструкция для повышенного процента</b>\n\n"
        "Чтобы получить повышенный процент на все сделки:\n\n"
        "1️⃣ Заполните профиль партнёра\n"
        "2️⃣ Отправьте нам первую заявку на оценку дела\n"
        "3️⃣ Получите вознаграждение по повышенной ставке\n\n"
        "<b>Важно:</b> Успейте провести первую сделку до конца месяца!"
    )

    from bot.keyboards.keyboards import get_partner_profile_keyboard

    await callback_query.message.answer(text, reply_markup=get_partner_profile_keyboard(), parse_mode="HTML")
    await callback_query.answer()

