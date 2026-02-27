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

# Настройки для уведомлений о профиле
MAX_ATTEMPTS = 3  # Максимум 3 попытки
FIRST_ATTEMPT_HOURS = 24  # Первая попытка через 24 часа
REPEAT_INTERVAL_DAYS = 3  # Повтор каждые 3 дня

# Настройки для реферальных уведомлений
REFERRAL_TEXT = (
    "💸 За прошлый месяц средний доход партнёров, развивающих реферальную сеть, "
    "составил {amount:,} ₽ пассивного дохода.\n\n"
    "Приглашайте друзей и получайте бонусы без лишних усилий!"
)
ACTIVE_USER_DAYS = 14  # Пользователи активные за последние 14 дней


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


async def send_referral_notification(user: User, bot) -> bool:
    """Отправить уведомление о реферальной программе"""
    import random

    try:
        # Генерируем уникальную сумму
        amount = random.randint(25000, 100000)
        text = REFERRAL_TEXT.format(amount=amount)

        await bot.send_message(
            chat_id=user.telegram_id,
            text=text,
            parse_mode="HTML"
        )

        # Записываем в лог
        async with get_db() as db:
            log = NotificationLog(
                user_id=user.id,
                notification_type="referral_invite",
                attempt_number=1,
                is_delivered=True
            )
            db.add(log)
            await db.commit()

        logger.info(f"Отправлено реферальное уведомление пользователю {user.telegram_id}")
        return True

    except Exception as e:
        logger.error(f"Ошибка отправки реферального уведомления пользователю {user.telegram_id}: {e}")
        return False


async def check_and_send_referral_notifications(bot):
    """Проверить активных пользователей и отправить реферальные уведомления"""
    try:
        async with get_db() as db:
            # Находим активных пользователей без рефералов
            from sqlalchemy import and_
            from datetime import timedelta

            fourteen_days_ago = datetime.utcnow() - timedelta(days=ACTIVE_USER_DAYS)

            # Получаем всех пользователей у которых нет рефералов
            result = await db.execute(
                select(User)
                .outerjoin(ReferralRelationship, User.id == ReferralRelationship.referrer_id)
                .where(ReferralRelationship.id.is_(None))
                .where(User.registered_at <= fourteen_days_ago)
            )
            users_without_referrals = result.scalars().all()

            logger.info(f"Найдено {len(users_without_referrals)} активных пользователей без рефералов")

            for user in users_without_referrals:
                # Проверяем было ли уже отправлено реферальное уведомление
                result = await db.execute(
                    select(NotificationLog.id)
                    .where(NotificationLog.user_id == user.id)
                    .where(NotificationLog.notification_type == "referral_invite")
                )
                already_sent = result.scalar_one_or_none()

                # Если уже отправляли - пропускаем
                if already_sent:
                    continue

                # Отправляем уведомление
                await send_referral_notification(user, bot)

    except Exception as e:
        logger.error(f"Ошибка в check_and_send_referral_notifications: {e}")


async def main(notification_type: str = "all"):
    """Точка входа

    Args:
        notification_type: 'all', 'profile', или 'referral'
    """
    from aiogram import Bot
    from aiogram.client.session.aiohttp import AiohttpSession

    if not settings.BOT_TOKEN:
        logger.error("BOT_TOKEN не настроен")
        return

    session = AiohttpSession()
    bot = Bot(token=settings.BOT_TOKEN, session=session)

    try:
        logger.info("Запуск проверки уведомлений...")

        if notification_type in ("all", "profile"):
            await check_and_send_notifications(bot)
            logger.info("Проверка уведомлений профиля завершена")

        if notification_type in ("all", "referral"):
            await check_and_send_referral_notifications(bot)
            logger.info("Проверка реферальных уведомлений завершена")

        logger.info("Все проверки завершены")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
