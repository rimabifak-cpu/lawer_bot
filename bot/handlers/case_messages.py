"""
Обработчики для переписки с администратором
Оптимизированная версия с логированием и обработкой ошибок
"""
import sys
import os
import logging
from typing import Optional, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import httpx
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database.database import get_db
from database.models import User, CaseQuestionnaire
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from bot.keyboards.keyboards import get_main_menu_keyboard

# Настройка логирования
logger = logging.getLogger(__name__)

router = Router()

# URL админ-панели для сохранения сообщений пользователей
ADMIN_PANEL_URL = os.getenv("ADMIN_PANEL_URL", "http://127.0.0.1:8001")

# Константы
MENU_COMMANDS = frozenset([
    "📋 Услуги",
    "📚 История услуг",
    "👤 Партнёрский профиль",
    "💼 Отправить дело на оценку",
    "💬 Поддержка",
    "❓ FAQ",
    "📖 Инструкция, как заработать"
])

HTTP_TIMEOUT = 30.0


async def send_message_to_admin(telegram_id: int, message_text: str) -> bool:
    """
    Отправить сообщение пользователя администратору (сохранить в общую переписку)
    
    Args:
        telegram_id: Telegram ID пользователя
        message_text: Текст сообщения
        
    Returns:
        bool: True если сообщение успешно отправлено, иначе False
    """
    if not message_text or not message_text.strip():
        logger.warning(f"Попытка отправить пустое сообщение от пользователя {telegram_id}")
        return False
    
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            response = await client.post(
                f"{ADMIN_PANEL_URL}/api/messages/dialog",
                json={
                    "telegram_id": telegram_id,
                    "content": message_text.strip()
                }
            )
            
            if response.status_code == 200:
                logger.info(f"Сообщение от пользователя {telegram_id} успешно сохранено")
                return True
            else:
                logger.error(
                    f"Ошибка сохранения сообщения от {telegram_id}: "
                    f"status={response.status_code}, response={response.text}"
                )
                return False
                
    except httpx.TimeoutException:
        logger.error(f"Таймаут при отправке сообщения от пользователя {telegram_id}")
        return False
    except httpx.ConnectError:
        logger.error(f"Не удалось подключиться к админ-панели: {ADMIN_PANEL_URL}")
        return False
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при отправке сообщения от {telegram_id}: {e}")
        return False


async def get_user_cases(db: AsyncSession, user_id: int) -> List[CaseQuestionnaire]:
    """
    Получить список дел пользователя
    
    Args:
        db: Сессия базы данных
        user_id: ID пользователя
        
    Returns:
        List[CaseQuestionnaire]: Список дел пользователя
    """
    try:
        result = await db.execute(
            select(CaseQuestionnaire)
            .filter(CaseQuestionnaire.user_id == user_id)
            .order_by(CaseQuestionnaire.created_at.desc())
        )
        return result.scalars().all()
    except Exception as e:
        logger.exception(f"Ошибка при получении дел пользователя {user_id}: {e}")
        return []


def format_case_status(status: str) -> str:
    """
    Форматировать статус дела для отображения
    
    Args:
        status: Статус дела
        
    Returns:
        str: Отформатированный статус
    """
    status_map = {
        "new": "📋 Новый",
        "in_progress": "📝 В работе",
        "completed": "✅ Завершён",
        "rejected": "❌ Отклонён"
    }
    return status_map.get(status, f"❓ {status}")


def format_cases_list(cases: List[CaseQuestionnaire]) -> str:
    """
    Форматировать список дел для отображения
    
    Args:
        cases: Список дел
        
    Returns:
        str: Отформатированный текст
    """
    if not cases:
        return ""
    
    text = "<b>📋 Ваши дела:</b>\n"
    for case in cases:
        status = format_case_status(case.status)
        created_at = case.created_at.strftime("%d.%m.%Y") if case.created_at else "неизвестно"
        text += f"- {status} <b>Дело #{case.id}</b> - {created_at}\n"
    return text + "\n"


@router.message(F.text == "💬 Поддержка")
async def support_handler(message: Message, state: FSMContext) -> None:
    """
    Обработчик раздела '💬 Поддержка / Переписка с админом'
    """
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} открыл раздел поддержки")
    
    try:
        async with get_db() as db:
            cases = await get_user_cases(db, user_id)
            
            # Формируем приветственное сообщение
            text = "<b>💬 Переписка с администратором</b>\n\n"
            text += format_cases_list(cases)
            text += (
                "💌 Вы можете написать сообщение администратору в любое время.\n\n"
                "<b>Просто напишите текст вашего сообщения ниже, и оно будет отправлено администратору.</b>"
            )
            
            # Очищаем состояние, если было
            await state.clear()
            
            await message.answer(text, reply_markup=get_main_menu_keyboard())
            
    except Exception as e:
        logger.exception(f"Ошибка в обработчике поддержки для пользователя {user_id}: {e}")
        await message.answer(
            "⚠️ Произошла ошибка. Попробуйте позже.",
            reply_markup=get_main_menu_keyboard()
        )


@router.message(F.text)
async def handle_user_message(message: Message, state: FSMContext) -> None:
    """
    Обработчик любых текстовых сообщений от пользователя.
    Сообщение сохраняется и отправляется администратору.
    """
    user_id = message.from_user.id
    message_text = message.text
    
    # Пропускаем команды меню
    if message_text in MENU_COMMANDS:
        return
    
    # Проверяем длину сообщения
    if len(message_text) > 4000:
        await message.answer(
            "⚠️ Сообщение слишком длинное. Пожалуйста, сократите его до 4000 символов.",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    logger.info(f"Получено сообщение от пользователя {user_id}: {message_text[:50]}...")
    
    # Отправляем сообщение администратору
    success = await send_message_to_admin(
        telegram_id=user_id,
        message_text=message_text
    )
    
    if success:
        await message.answer(
            "✅ Ваше сообщение отправлено администратору.\n\n"
            "💬 Вы можете продолжить переписку или вернуться в главное меню.",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await message.answer(
            "⚠️ Не удалось отправить сообщение. Попробуйте позже или обратитесь к нам другим способом.",
            reply_markup=get_main_menu_keyboard()
        )


def register_case_messages_handlers(dp):
    """Регистрация обработчиков переписки"""
    dp.include_router(router)
    logger.info("Обработчики переписки зарегистрированы")
