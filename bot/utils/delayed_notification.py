"""
Модуль отложенных уведомлений для бота
Отправляет промо-сообщения новым пользователям:
- Через 1 час: специальное предложение со скидкой 15%
- Через 24 часа: результаты заработка партнёров
"""
import asyncio
import logging
from typing import Dict, Optional

from config.settings import settings

logger = logging.getLogger(__name__)

# Текст уведомления №1 (через 1 час)
PROMO_MESSAGE = (
    "Уважаемый партнер, у нас для вас специальное предложение! 💼\n\n"
    "Мы готовы предоставить <b>постоянную скидку 15%</b> для всех ваших клиентов на наши услуги.\n\n"
    "Чтобы активировать ее навсегда, достаточно привести одного нового клиента, который совершит оплату в течение 14 дней.\n\n"
    "После выполнения этого условия скидка закрепится за вашими клиентами на постоянной основе.\n\n"
    "  \n\n"
    "@legaldecision, поддержка 24/7"
)

# Текст уведомления №2 (через 24 часа)
EARNINGS_MESSAGE = (
    "Вот это результаты! 🔥\n\n"
    "Наш лучший партнер прошлого месяца заработал <b>142 580 рублей</b>.\n\n"
    "А знаете, что самое интересное? Даже средний доход среди всех партнеров составил <b>58 655 рублей</b>.\n\n"
    "Присоединяйтесь, возможности безграничны!"
)

# Словарь для отслеживания задач уведомлений по пользователям
# {telegram_id: {"promo_task": Optional[Task], "earnings_task": Optional[Task]}}
pending_notifications: Dict[int, dict] = {}


async def send_message_to_user(bot, telegram_id: int, message: str, notification_type: str) -> bool:
    """
    Отправить сообщение конкретному пользователю

    Args:
        bot: Экземпляр бота
        telegram_id: Telegram ID пользователя
        message: Текст сообщения
        notification_type: Тип уведомления (для лога)

    Returns:
        bool: True если успешно отправлено
    """
    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=message,
            parse_mode="HTML"
        )
        logger.info(f"✅ {notification_type} отправлено пользователю {telegram_id}")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка отправки {notification_type} пользователю {telegram_id}: {e}")
        return False


async def _delayed_send(bot, telegram_id: int, delay_seconds: int, message: str, notification_type: str, task_key: str):
    """
    Внутренняя функция для отправки с задержкой

    Args:
        bot: Экземпляр бота
        telegram_id: Telegram ID пользователя
        delay_seconds: Задержка в секундах
        message: Текст сообщения
        notification_type: Тип уведомления (для лога)
        task_key: Ключ задачи в словаре
    """
    try:
        # Ждем указанное время
        await asyncio.sleep(delay_seconds)

        hours = delay_seconds // 3600
        logger.info(f"🚀 Отправка '{notification_type}' пользователю {telegram_id} (прошло {hours} ч.)")

        # Отправляем сообщение
        await send_message_to_user(bot, telegram_id, message, notification_type)

    except asyncio.CancelledError:
        # Задача была отменена
        logger.info(f"Уведомление '{notification_type}' для пользователя {telegram_id} отменено")
        return
    except Exception as e:
        logger.error(f"Ошибка при отложенной отправке '{notification_type}' пользователю {telegram_id}: {e}")
    finally:
        # Удаляем задачу из словаря после выполнения
        if telegram_id in pending_notifications:
            pending_notifications[telegram_id][task_key] = None
            # Если обе задачи завершены, удаляем запись
            if not any(pending_notifications[telegram_id].values()):
                pending_notifications.pop(telegram_id, None)


def schedule_notification(bot, telegram_id: int, message: str, delay_hours: int, notification_type: str, task_key: str):
    """
    Запланировать отправку уведомления пользователю через указанное время

    Args:
        bot: Экземпляр бота
        telegram_id: Telegram ID пользователя
        message: Текст сообщения
        delay_hours: Задержка в часах
        notification_type: Тип уведомления (для лога)
        task_key: Ключ задачи в словаре
    """
    delay_seconds = delay_hours * 60 * 60

    logger.info(f"⏰ Запланировано '{notification_type}' для пользователя {telegram_id} через {delay_hours} ч.")

    # Создаем задачу с задержкой
    task = asyncio.create_task(
        _delayed_send(bot, telegram_id, delay_seconds, message, notification_type, task_key),
        name=f"{task_key}_{telegram_id}"
    )

    # Инициализируем запись для пользователя если нет
    if telegram_id not in pending_notifications:
        pending_notifications[telegram_id] = {"promo_task": None, "earnings_task": None}

    pending_notifications[telegram_id][task_key] = task


async def schedule_promo_notification(bot, telegram_id: int, delay_hours: int = 1):
    """
    Запланировать отправку промо-сообщения (уведомление №1)

    Args:
        bot: Экземпляр бота
        telegram_id: Telegram ID пользователя
        delay_hours: Задержка в часах (по умолчанию 1)
    """
    # Проверяем, нет уже ли запланированной задачи
    if telegram_id in pending_notifications and pending_notifications[telegram_id].get("promo_task"):
        logger.debug(f"Промо-уведомление уже запланировано для пользователя {telegram_id}")
        return

    schedule_notification(
        bot=bot,
        telegram_id=telegram_id,
        message=PROMO_MESSAGE,
        delay_hours=delay_hours,
        notification_type="Промо-сообщение (скидка 15%)",
        task_key="promo_task"
    )


async def schedule_earnings_notification(bot, telegram_id: int, delay_hours: int = 24):
    """
    Запланировать отправку уведомления о результатах заработка (уведомление №2)

    Args:
        bot: Экземпляр бота
        telegram_id: Telegram ID пользователя
        delay_hours: Задержка в часах (по умолчанию 24)
    """
    # Проверяем, нет уже ли запланированной задачи
    if telegram_id in pending_notifications and pending_notifications[telegram_id].get("earnings_task"):
        logger.debug(f"Уведомление о результатах уже запланировано для пользователя {telegram_id}")
        return

    schedule_notification(
        bot=bot,
        telegram_id=telegram_id,
        message=EARNINGS_MESSAGE,
        delay_hours=delay_hours,
        notification_type="Результаты заработка партнёров",
        task_key="earnings_task"
    )


def cancel_notification(telegram_id: int, task_key: str):
    """
    Отменить запланированное уведомление для пользователя

    Args:
        telegram_id: Telegram ID пользователя
        task_key: Ключ задачи ("promo_task" или "earnings_task")
    """
    if telegram_id in pending_notifications:
        task = pending_notifications[telegram_id].get(task_key)
        if task:
            task.cancel()
            pending_notifications[telegram_id][task_key] = None
            logger.info(f"Уведомление {task_key} для пользователя {telegram_id} отменено")


def cancel_all_notifications(telegram_id: int):
    """
    Отменить все уведомления для пользователя

    Args:
        telegram_id: Telegram ID пользователя
    """
    if telegram_id in pending_notifications:
        for task_key, task in pending_notifications[telegram_id].items():
            if task:
                task.cancel()
        pending_notifications.pop(telegram_id, None)
        logger.info(f"Все уведомления для пользователя {telegram_id} отменены")


def get_pending_count() -> int:
    """
    Получить количество пользователей с запланированными уведомлениями

    Returns:
        int: Количество пользователей
    """
    return len(pending_notifications)


def get_active_tasks_count() -> int:
    """
    Получить количество активных задач

    Returns:
        int: Количество активных задач
    """
    count = 0
    for user_tasks in pending_notifications.values():
        count += sum(1 for task in user_tasks.values() if task is not None)
    return count
