"""
Logging Middleware для Telegram бота
Логирует все входящие сообщения и callback-запросы
"""
import logging
import time
from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """
    Middleware для логирования входящих сообщений и callback-запросов.
    Также измеряет время обработки запроса.
    """
    
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
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
        start_time = time.time()
        
        # Получаем информацию о пользователе
        user = event.from_user
        user_info = f"id={user.id}, username=@{user.username}" if user.username else f"id={user.id}"
        
        # Логируем в зависимости от типа события
        if isinstance(event, Message):
            event_type = "Message"
            event_info = f"text='{event.text[:50]}...'" if event.text and len(event.text) > 50 else f"text='{event.text}'" if event.text else "non-text"
        elif isinstance(event, CallbackQuery):
            event_type = "Callback"
            event_info = f"data='{event.data}'"
        else:
            event_type = "Unknown"
            event_info = str(type(event))
        
        logger.info(f"📥 {event_type} from {user_info}: {event_info}")
        
        try:
            # Выполняем обработчик
            result = await handler(event, data)
            
            # Логируем успешную обработку
            processing_time = time.time() - start_time
            logger.info(
                f"✅ {event_type} processed for {user_info} "
                f"in {processing_time:.3f}s"
            )
            
            return result
            
        except Exception as e:
            # Логируем ошибку
            processing_time = time.time() - start_time
            logger.error(
                f"❌ {event_type} failed for {user_info} "
                f"after {processing_time:.3f}s: {e}",
                exc_info=True
            )
            raise
