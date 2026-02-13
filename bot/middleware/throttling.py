"""
Throttling Middleware для Telegram бота
Защита от спама и частых запросов
"""
import logging
import time
from typing import Callable, Awaitable, Any
from collections import defaultdict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramAPIException

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware для защиты от спама.
    Ограничивает количество запросов от пользователя в единицу времени.
    """
    
    def __init__(
        self,
        rate_limit: float = 0.5,
        burst_limit: int = 5,
        burst_window: float = 10.0
    ):
        """
        Инициализация middleware
        
        Args:
            rate_limit: Минимальный интервал между запросами в секундах
            burst_limit: Максимальное количество запросов в окне burst_window
            burst_window: Временное окно для burst-ограничения в секундах
        """
        self.rate_limit = rate_limit
        self.burst_limit = burst_limit
        self.burst_window = burst_window
        
        # Хранилище времён последних запросов
        self._last_request: dict[int, float] = defaultdict(float)
        # Хранилище истории запросов для burst-ограничения
        self._request_history: dict[int, list[float]] = defaultdict(list)
        
        logger.info(
            f"ThrottlingMiddleware initialized: rate_limit={rate_limit}s, "
            f"burst_limit={burst_limit} per {burst_window}s"
        )
    
    def _cleanup_old_requests(self, user_id: int, current_time: float) -> None:
        """
        Удалить старые запросы из истории
        
        Args:
            user_id: ID пользователя
            current_time: Текущее время
        """
        cutoff_time = current_time - self.burst_window
        self._request_history[user_id] = [
            t for t in self._request_history[user_id] if t > cutoff_time
        ]
    
    def _is_rate_limited(self, user_id: int, current_time: float) -> tuple[bool, str]:
        """
        Проверить, ограничен ли пользователь
        
        Args:
            user_id: ID пользователя
            current_time: Текущее время
            
        Returns:
            tuple[bool, str]: (ограничен ли, причина)
        """
        # Проверяем rate limit
        last_request = self._last_request[user_id]
        if current_time - last_request < self.rate_limit:
            wait_time = self.rate_limit - (current_time - last_request)
            return True, f"rate_limit (wait {wait_time:.1f}s)"
        
        # Очищаем старые запросы
        self._cleanup_old_requests(user_id, current_time)
        
        # Проверяем burst limit
        if len(self._request_history[user_id]) >= self.burst_limit:
            return True, "burst_limit"
        
        return False, ""
    
    async def _send_throttle_warning(
        self, 
        event: Message | CallbackQuery, 
        reason: str
    ) -> None:
        """
        Отправить предупреждение о throttling
        
        Args:
            event: Событие
            reason: Причина ограничения
        """
        try:
            if isinstance(event, Message):
                await event.answer(
                    "⚠️ Пожалуйста, не отправляйте сообщения так часто. "
                    "Попробуйте через несколько секунд."
                )
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "⚠️ Слишком много запросов. Подождите немного.",
                    show_alert=True
                )
        except TelegramAPIException as e:
            logger.warning(f"Не удалось отправить предупреждение о throttling: {e}")
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any]
    ) -> Any:
        """
        Обработчик middleware
        
        Args:
            handler: Следующий обработчик в цепочке
            event: Событие (Message или CallbackQuery)
            data: Данные контекста
            
        Returns:
            Результат обработки
        """
        user = event.from_user
        if not user:
            return await handler(event, data)
        
        user_id = user.id
        current_time = time.time()
        
        # Проверяем ограничения
        is_limited, reason = self._is_rate_limited(user_id, current_time)
        
        if is_limited:
            logger.warning(
                f"🚫 Throttled user {user_id} (@{user.username}): {reason}"
            )
            await self._send_throttle_warning(event, reason)
            return None
        
        # Обновляем время последнего запроса
        self._last_request[user_id] = current_time
        self._request_history[user_id].append(current_time)
        
        # Выполняем обработчик
        return await handler(event, data)


class AdminBypassThrottlingMiddleware(ThrottlingMiddleware):
    """
    Throttling middleware с обходом для администраторов
    """
    
    def __init__(
        self,
        admin_ids: set[int] | None = None,
        rate_limit: float = 0.5,
        burst_limit: int = 5,
        burst_window: float = 10.0
    ):
        """
        Инициализация middleware
        
        Args:
            admin_ids: Множество ID администраторов
            rate_limit: Минимальный интервал между запросами в секундах
            burst_limit: Максимальное количество запросов в окне burst_window
            burst_window: Временное окно для burst-ограничения в секундах
        """
        super().__init__(rate_limit, burst_limit, burst_window)
        self.admin_ids = admin_ids or set()
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any]
    ) -> Any:
        """
        Обработчик middleware с проверкой на администратора
        """
        user = event.from_user
        if not user:
            return await handler(event, data)
        
        # Пропускаем администраторов
        if user.id in self.admin_ids:
            return await handler(event, data)
        
        return await super().__call__(handler, event, data)
