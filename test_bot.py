"""
Тестирование функционала телеграм бота
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.handlers.start import command_start_handler
from bot.handlers.profile import profile_update_handler, process_full_name, process_company_name, process_phone, process_email, process_specialization, process_experience
from bot.handlers.send_case import send_case_start_handler, process_document_upload, process_description, process_confirmation
from bot.database.models import User, PartnerProfile, ServiceRequest
from bot.config.settings import settings


@pytest.mark.asyncio
async def test_start_handler():
    """Тестирование команды /start"""
    # Создаем mock объекты
    mock_message = AsyncMock()
    mock_message.from_user.id = 123456
    mock_message.from_user.username = "test_user"
    mock_message.from_user.first_name = "Test"
    mock_message.from_user.last_name = "User"
    
    # Вызываем обработчик
    await command_start_handler(mock_message)
    
    # Проверяем, что метод answer был вызван
    mock_message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_profile_update_flow():
    """Тестирование процесса обновления профиля"""
    # Mock объекты
    mock_callback_query = AsyncMock()
    mock_callback_query.from_user.id = 123456
    mock_callback_query.message = AsyncMock()
    
    mock_state = AsyncMock(spec=FSMContext)
    
    # Тестируем начало процесса обновления профиля
    await profile_update_handler(mock_callback_query, mock_state)
    
    # Проверяем, что состояние установлено правильно
    mock_state.set_state.assert_called_once()
    

@pytest.mark.asyncio
async def test_send_case_flow():
    """Тестирование процесса отправки дела"""
    # Mock объекты
    mock_message = AsyncMock()
    mock_message.from_user.id = 123456
    mock_message.text = "Тестовое описание проблемы"
    
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.get_data.return_value = {
        'description': 'Тестовое описание проблемы',
        'documents': []
    }
    
    # Тестируем обработку описания
    await process_description(mock_message, mock_state)
    
    # Проверяем, что метод answer был вызван
    mock_message.answer.assert_called_once()


def test_config_values():
    """Тестирование значений конфигурации"""
    assert settings.BOT_TOKEN is not None
    assert isinstance(settings.MAX_FILE_SIZE, int)
    assert settings.MAX_FILE_SIZE > 0


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"])