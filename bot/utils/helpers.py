"""
Вспомогательные функции для юридического бота
Оптимизированная версия с улучшенной обработкой файлов и логированием
"""
import os
import sys
import logging
import aiofiles
from pathlib import Path
from typing import Optional, Union

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import settings

# Настройка логирования
logger = logging.getLogger(__name__)


# ============================================
# Валидация файлов
# ============================================

def validate_file_type(file_name: str) -> bool:
    """
    Проверяет, разрешен ли тип файла для загрузки
    
    Args:
        file_name: Имя файла с расширением
    
    Returns:
        bool: True если тип файла разрешен
    """
    if not file_name:
        return False
    
    _, ext = os.path.splitext(file_name.lower())
    return ext.lstrip('.') in settings.ALLOWED_EXTENSIONS


def validate_file_size(file_size: int) -> bool:
    """
    Проверяет, не превышает ли размер файла ограничение
    
    Args:
        file_size: Размер файла в байтах
    
    Returns:
        bool: True если размер файла в пределах допустимого
    """
    return file_size <= settings.MAX_FILE_SIZE


def get_file_extension(file_name: str) -> str:
    """
    Получает расширение файла без точки
    
    Args:
        file_name: Имя файла
    
    Returns:
        str: Расширение файла в нижнем регистре
    """
    _, ext = os.path.splitext(file_name.lower())
    return ext.lstrip('.')


# ============================================
# Сохранение файлов
# ============================================

async def save_file(file_path: str, data: bytes) -> bool:
    """
    Асинхронно сохраняет файл на диск
    
    Args:
        file_path: Полный путь для сохранения файла
        data: Данные файла в байтах
    
    Returns:
        bool: True если файл успешно сохранен
    """
    try:
        # Создаем директорию, если она не существует
        directory = os.path.dirname(file_path)
        if directory:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Асинхронная запись файла
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(data)
        
        logger.info(f"Файл успешно сохранен: {file_path}")
        return True
    
    except PermissionError as e:
        logger.error(f"Ошибка доступа при сохранении файла {file_path}: {e}")
        return False
    except OSError as e:
        logger.error(f"Ошибка ОС при сохранении файла {file_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"Неожиданная ошибка при сохранении файла {file_path}: {e}")
        return False


async def delete_file(file_path: str) -> bool:
    """
    Асинхронно удаляет файл с диска
    
    Args:
        file_path: Путь к файлу для удаления
    
    Returns:
        bool: True если файл успешно удален
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Файл успешно удален: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при удалении файла {file_path}: {e}")
        return False


def ensure_directory_exists(directory: str) -> bool:
    """
    Создает директорию, если она не существует
    
    Args:
        directory: Путь к директории
    
    Returns:
        bool: True если директория существует или создана
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Ошибка при создании директории {directory}: {e}")
        return False


# ============================================
# Форматирование данных
# ============================================

def format_user_info(user) -> str:
    """
    Форматирует информацию о пользователе для отображения
    
    Args:
        user: Объект пользователя
    
    Returns:
        str: Отформатированная строка с информацией
    """
    info_parts = [
        f"ФИО: {user.full_name}",
        f"Компания: {user.company_name}",
        f"Телефон: {user.phone}",
        f"Email: {user.email}",
        f"Специализация: {user.specialization}",
        f"Опыт: {user.experience} лет",
        f"Согласие на передачу данных: {'Да' if user.consent_to_share_data else 'Нет'}"
    ]
    return '\n'.join(info_parts)


def format_request_info(request) -> str:
    """
    Форматирует информацию о заявке для отображения
    
    Args:
        request: Объект заявки
    
    Returns:
        str: Отформатированная строка с информацией
    """
    created_at_str = request.created_at.strftime('%d.%m.%Y %H:%M') if request.created_at else 'не указана'
    
    info_parts = [
        f"ID заявки: {request.id}",
        f"Статус: {request.status}",
        f"Дата создания: {created_at_str}",
        f"Описание: {request.description}"
    ]
    return '\n'.join(info_parts)


def format_currency(amount: Union[int, float], currency: str = "руб.") -> str:
    """
    Форматирует сумму в валюту
    
    Args:
        amount: Сумма
        currency: Валюта
    
    Returns:
        str: Отформатированная строка
    """
    return f"{amount:,.0f} {currency}".replace(",", " ")


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Обрезает текст до указанной длины
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина
        suffix: Суффикс для обрезанного текста
    
    Returns:
        str: Обрезанный текст
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


# ============================================
# Валидация данных
# ============================================

def validate_phone(phone: str) -> bool:
    """
    Проверяет формат номера телефона
    
    Args:
        phone: Номер телефона
    
    Returns:
        bool: True если формат корректный
    """
    if not phone:
        return False
    
    # Удаляем все нецифровые символы
    digits = ''.join(filter(str.isdigit, phone))
    
    # Проверяем длину (10 или 11 цифр для российских номеров)
    return len(digits) in (10, 11)


def validate_email(email: str) -> bool:
    """
    Проверяет формат email
    
    Args:
        email: Email адрес
    
    Returns:
        bool: True если формат корректный
    """
    if not email:
        return False
    
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Очищает пользовательский ввод от потенциально опасных символов
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина
    
    Returns:
        str: Очищенный текст
    """
    if not text:
        return ""
    
    # Обрезаем до максимальной длины
    text = text[:max_length]
    
    # Удаляем потенциально опасные HTML теги (кроме разрешенных)
    # Для Telegram разрешены: <b>, <i>, <u>, <s>, <code>, <pre>, <a>
    import re
    # Удаляем все теги кроме разрешенных
    text = re.sub(r'<(?!/?[biuscodeprea]|a\s)[^>]*>', '', text)
    
    return text.strip()


# ============================================
# Генерация уникальных имен
# ============================================

def generate_unique_filename(original_name: str, prefix: str = "") -> str:
    """
    Генерирует уникальное имя файла с timestamp
    
    Args:
        original_name: Оригинальное имя файла
        prefix: Префикс для имени файла
    
    Returns:
        str: Уникальное имя файла
    """
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    _, ext = os.path.splitext(original_name)
    
    if prefix:
        return f"{prefix}_{timestamp}{ext}"
    return f"{timestamp}{ext}"
