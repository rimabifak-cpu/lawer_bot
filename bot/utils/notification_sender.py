"""
Скрипт отправки уведомлений пользователям
"""
import asyncio
import logging
from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from database.database import get_db
from database.models import User, PartnerProfile, NotificationLog
from config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Текст уведомления
PROFILE_INCOMPLETE_TEXT = (
    "🔥 У нас за эту неделю появилось 2 новых запроса, которые мы уже передали партнёрам.\n\n"
    "Чтобы не упустить свой шанс, пожалуйста, заполните профиль полностью. "
    "Так клиенты смогут найти именно вас.\n\n"
    "[Кнопка: ✏️ Заполнить профиль]"
)

# Настройки
MAX_ATTEMPTS = 3  # Максимум 3 попытки
FIRST_ATTEMPT_HOURS = 24  # Первая попытка через 24 часа
REPEAT_INTERVAL_DAYS = 3  # Повтор каждые 3 дня


async def send_profile_incomplete_notification(user: User, attempt: int, bot) -> bool:
    """Отправить уведомление о незаполненном профиле"""
    try:
        await bot.send_message(
            chat_id=user.telegram_id,
            text=PROFILE_INCOMPLETE_TEXT.replace("[Кнопка: ✏️ Заполнить профиль]", ""),
            parse_mode="HTML"
        )

        # Записываем в лог
        async with get_db() as db:
            log = NotificationLog(
                user_id=user.id,
                notification_type="profile_incomplete",
                attempt_number=attempt,
                is_delivered=True
            )
            db.add(log)
            await db.commit()

        logger.info(f"Отправлено уведомление пользователю {user.telegram_id} (попытка {attempt})")
        return True

    except Exception as e:
        logger.error(f"Ошибка отправки уведомления пользователю {user.telegram_id}: {e}")
        return False


async def check_and_send_notifications(bot):
    """Проверить пользователей и отправить уведомления"""
    try:
        async with get_db() as db:
            # Находим пользователей без заполненного профиля
            result = await db.execute(
                select(User)
                .outerjoin(PartnerProfile, User.id == PartnerProfile.user_id)
                .where(PartnerProfile.id.is_(None))
                .where(User.registered_at <= datetime.utcnow() - timedelta(hours=FIRST_ATTEMPT_HOURS))
            )
            users_without_profile = result.scalars().all()

            logger.info(f"Найдено {len(users_without_profile)} пользователей без профиля")

            for user in users_without_profile:
                # Проверяем сколько уведомлений уже отправлено
                result = await db.execute(
                    select(func.count(NotificationLog.id))
                    .where(NotificationLog.user_id == user.id)
                    .where(NotificationLog.notification_type == "profile_incomplete")
                )
                sent_count = result.scalar() or 0

                # Если уже отправили 3 раза - пропускаем
                if sent_count >= MAX_ATTEMPTS:
                    continue

                # Проверяем когда было последнее уведомление
                if sent_count > 0:
                    result = await db.execute(
                        select(func.max(NotificationLog.sent_at))
                        .where(NotificationLog.user_id == user.id)
                        .where(NotificationLog.notification_type == "profile_incomplete")
                    )
                    last_sent = result.scalar()

                    # Если прошло меньше 3 дней - пропускаем
                    if last_sent and (datetime.utcnow() - last_sent) < timedelta(days=REPEAT_INTERVAL_DAYS):
                        continue

                # Отправляем уведомление
                attempt = sent_count + 1
                await send_profile_incomplete_notification(user, attempt, bot)

    except Exception as e:
        logger.error(f"Ошибка в check_and_send_notifications: {e}")


async def main():
    """Точка входа"""
    from aiogram import Bot
    from aiogram.client.session.aiohttp import AiohttpSession

    if not settings.BOT_TOKEN:
        logger.error("BOT_TOKEN не настроен")
        return

    session = AiohttpSession()
    bot = Bot(token=settings.BOT_TOKEN, session=session)

    try:
        logger.info("Запуск проверки уведомлений...")
        await check_and_send_notifications(bot)
        logger.info("Проверка завершена")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
