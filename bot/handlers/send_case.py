"""
Обработчики для отправки дела на оценку (пошаговая анкета из 7 этапов + документы в конце)
Оптимизированная версия с устранением дублирования кода
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import logging
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, FSInputFile, ContentType
from aiogram.fsm.context import FSMContext

from database.database import get_db
from database.models import User, CaseQuestionnaire, CaseQuestionnaireDocument
from config.settings import settings
from bot.utils.helpers import validate_file_type, validate_file_size, save_file
from bot.keyboards.keyboards import (
    get_cancel_questionnaire_keyboard,
    get_main_menu_keyboard,
    get_main_menu_inline_keyboard,
    get_questionnaire_summary_keyboard,
    get_edit_section_keyboard,
    get_documents_section_keyboard,
    get_step_documents_keyboard,
    get_simple_documents_keyboard,
    get_back_keyboard
)
from bot.states.states import CaseQuestionnaireStates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

# Настройка логирования
logger = logging.getLogger(__name__)

router = Router()

# ID чата для отправки анкет
PARTNERS_CHAT_ID = -1003899118823

# Тексты вопросов для каждого этапа
STEP_QUESTIONS = {
    1: {
        "title": "Стороны конфликта",
        "question": (
            "📋 <b>Этап 1 из 7: Стороны конфликта</b>\n\n"
            "Введите стороны конфликта:\n"
            "• Кто истец?\n"
            "• Кто ответчик?\n"
            "• Третьи лица?\n"
            "• Где среди них наш клиент?"
        ),
        "section": "parties",
        "field": "parties_info"
    },
    2: {
        "title": "Предмет спора",
        "question": (
            "📋 <b>Этап 2 из 7: Предмет спора</b>\n\n"
            "Введите предмет спора:\n"
            "• В чём суть требований?\n"
            "• Деньги, право или расторжение?\n"
            "• Какая сумма или предмет спора?"
        ),
        "section": "dispute",
        "field": "dispute_subject"
    },
    3: {
        "title": "Основания требований",
        "question": (
            "📋 <b>Этап 3 из 7: Основания требований</b>\n\n"
            "Введите основания требований:\n"
            "• Какие законы ссылаются стороны?\n"
            "• Какие договоры указаны?\n"
            "• Какие факты приводятся?"
        ),
        "section": "legal_basis",
        "field": "legal_basis"
    },
    4: {
        "title": "Хронология событий",
        "question": (
            "📋 <b>Этап 4 из 7: Хронология событий</b>\n\n"
            "Введите хронологию событий (кратко, по датам):\n"
            "• Что произошло?\n"
            "• Когда это было?\n"
            "• Кто это сделал?"
        ),
        "section": "chronology",
        "field": "chronology"
    },
    5: {
        "title": "Имеющиеся доказательства",
        "question": (
            "📋 <b>Этап 5 из 7: Имеющиеся доказательства</b>\n\n"
            "Введите имеющиеся доказательства:\n"
            "• Какие документы есть?\n"
            "• Есть ли переписка?\n"
            "• Кто свидетели?"
        ),
        "section": "evidence",
        "field": "evidence"
    },
    6: {
        "title": "Процессуальная история",
        "question": (
            "📋 <b>Этап 6 из 7: Процессуальная история</b>\n\n"
            "Введите процессуальную историю:\n"
            "• Были ли уже иски?\n"
            "• Были ли жалобы?\n"
            "• Какие решения уже были?"
        ),
        "section": "procedural",
        "field": "procedural_history"
    },
    7: {
        "title": "Цель клиента",
        "question": (
            "📋 <b>Этап 7 из 7: Цель клиента</b>\n\n"
            "Введите цель клиента:\n"
            "• Чего он хочет добиться в итоге?\n"
            "• Какой результат ожидает?"
        ),
        "section": "goal",
        "field": "client_goal"
    }
}

# Маппинг состояний для этапов
STATE_MAP = {
    1: CaseQuestionnaireStates.waiting_for_parties,
    2: CaseQuestionnaireStates.waiting_for_dispute_subject,
    3: CaseQuestionnaireStates.waiting_for_legal_basis,
    4: CaseQuestionnaireStates.waiting_for_chronology,
    5: CaseQuestionnaireStates.waiting_for_evidence,
    6: CaseQuestionnaireStates.waiting_for_procedural_history,
    7: CaseQuestionnaireStates.waiting_for_client_goal,
}

# Названия разделов для отображения
SECTION_NAMES = {
    "parties": "Стороны конфликта",
    "dispute": "Предмет спора",
    "legal_basis": "Основания требований",
    "chronology": "Хронология событий",
    "evidence": "Доказательства",
    "procedural": "Процессуальная история",
    "goal": "Цель клиента"
}

MAX_DOCUMENTS_PER_SECTION = 5


# ============================================
# Основные обработчики
# ============================================

@router.message(F.text == "💼 Отправить дело на оценку")
async def send_case_start_handler(message: Message, state: FSMContext) -> None:
    """
    Обработчик начала отправки дела на оценку
    """
    logger.info(f"Пользователь {message.from_user.id} начал заполнение анкеты")
    
    # Очищаем предыдущее состояние
    await state.clear()
    
    # Инициализируем данные анкеты
    initial_data = {
        "step": 1,
        "parties_info": "",
        "dispute_subject": "",
        "legal_basis": "",
        "chronology": "",
        "evidence": "",
        "procedural_history": "",
        "client_goal": "",
        "documents_list": []
    }
    await state.update_data(initial_data)

    # Отправляем сообщение о вознаграждении
    await message.answer(
        "После оценки задания мы сообщим точную сумму вашего вознаграждения.\n"
        "Если вы сможете продать результат дороже этой суммы — разница полностью остаётся вам.\n\n"
        "  \n\n"
        "@legaldecision, поддержка 24/7"
    )

    # Показываем первый вопрос
    await show_step_question(message, state, 1)


async def show_step_question(message: Message, state: FSMContext, step: int) -> None:
    """Показывает вопрос для указанного этапа"""
    if step not in STEP_QUESTIONS:
        logger.error(f"Неверный шаг анкеты: {step}")
        return
    
    step_data = STEP_QUESTIONS[step]
    
    await message.answer(
        step_data["question"],
        reply_markup=get_cancel_questionnaire_keyboard()
    )
    
    await state.set_state(STATE_MAP[step])
    await state.update_data(current_step=step)
    logger.debug(f"Показан шаг {step} анкеты")


# ============================================
# Общий обработчик ввода текста для всех этапов
# ============================================

def create_step_handler(step: int):
    """Фабрика для создания обработчиков этапов"""
    async def handler(message: Message, state: FSMContext) -> None:
        step_data = STEP_QUESTIONS[step]
        field_name = step_data["field"]
        
        await state.update_data({field_name: message.text})
        logger.info(f"Шаг {step} заполнен: {field_name}")
        
        if step < 7:
            await show_step_question(message, state, step + 1)
        else:
            await show_documents_upload(message, state)
    
    return handler


# Регистрируем обработчики для каждого этапа
for step in range(1, 8):
    handler = create_step_handler(step)
    # Используем декоратор для регистрации
    router.message(STATE_MAP[step])(handler)


# ============================================
# Загрузка документов после всех этапов
# ============================================

async def show_documents_upload(message: Message, state: FSMContext) -> None:
    """Показывает упрощённый интерфейс загрузки документов"""
    data = await state.get_data()
    documents = data.get("documents_list", [])
    total_docs = len(documents)
    
    text = (
        "📎 <b>Загрузка документов</b>\n\n"
        "Прикрепите документы, относящиеся к вашему делу.\n"
        "Вы можете отправить несколько файлов подряд.\n\n"
    )
    
    if total_docs > 0:
        text += f"📊 <b>Загружено документов: {total_docs}</b>\n\n"
        for i, doc in enumerate(documents, 1):
            text += f"{i}. {doc['original_name']}\n"
        text += "\n"
    
    text += "Отправьте документы или нажмите 'Готово' для перехода к сводке."
    
    await message.answer(
        text,
        reply_markup=get_simple_documents_keyboard()
    )
    await state.set_state(CaseQuestionnaireStates.waiting_for_simple_documents)


# Обработчик кнопки "Готово" в состоянии ожидания документов
@router.message(F.text == "✅ Готово", CaseQuestionnaireStates.waiting_for_simple_documents)
async def documents_ready_handler(message: Message, state: FSMContext) -> None:
    """Пользователь нажал Готово - переходим к сводке"""
    await show_summary(message, state)


# Обработчик кнопки "Пропустить" в состоянии ожидания документов
@router.message(F.text == "⏭️ Пропустить", CaseQuestionnaireStates.waiting_for_simple_documents)
async def skip_documents_handler(message: Message, state: FSMContext) -> None:
    """Пользователь пропустил загрузку документов"""
    await show_summary(message, state)


# Обработчик отмены в состоянии ожидания документов
@router.message(F.text == "❌ Отмена", CaseQuestionnaireStates.waiting_for_simple_documents)
async def cancel_documents_handler(message: Message, state: FSMContext) -> None:
    """Отмена загрузки документов"""
    await state.clear()
    await message.answer(
        "❌ Заполнение анкеты отменено.",
        reply_markup=get_main_menu_keyboard()
    )
    logger.info("Анкета отменена на этапе загрузки документов")


# ============================================
# Обработка загрузки файлов (общая функция)
# ============================================

async def process_file_upload(message: Message, state: FSMContext, file_obj, file_name: str, file_size: int) -> bool:
    """
    Общая функция для обработки загрузки файлов (документы и фото)
    
    Returns:
        bool: True если файл успешно загружен, False иначе
    """
    # Валидация
    if not validate_file_type(file_name):
        await message.answer(
            f"❌ Файл '{file_name}' имеет недопустимый тип.\n"
            f"Допустимые типы: PDF, JPG, JPEG, PNG, DOC, DOCX",
            reply_markup=get_simple_documents_keyboard()
        )
        return False
        
    if not validate_file_size(file_size):
        await message.answer(
            f"❌ Файл '{file_name}' слишком большой.\n"
            f"Максимальный размер: {settings.MAX_FILE_SIZE / 1024 / 1024:.1f} МБ",
            reply_markup=get_simple_documents_keyboard()
        )
        return False
    
    # Скачиваем файл
    try:
        file_info = await message.bot.get_file(file_obj.file_id)
        file_data = await message.bot.download_file(file_info.file_path)
    except Exception as e:
        logger.error(f"Ошибка при скачивании файла: {e}")
        await message.answer(
            f"❌ Не удалось скачать файл '{file_name}'. Попробуйте снова.",
            reply_markup=get_simple_documents_keyboard()
        )
        return False
    
    # Генерируем путь для сохранения
    uploads_dir = settings.UPLOAD_FOLDER
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{timestamp}_{file_name}"
    file_path = os.path.join(uploads_dir, unique_filename)
    
    # Сохраняем файл
    if await save_file(file_path, file_data.read()):
        data = await state.get_data()
        documents_list = data.get("documents_list", [])
        
        documents_list.append({
            "file_path": file_path,
            "file_type": os.path.splitext(file_name)[1],
            "original_name": file_name
        })
        
        await state.update_data(documents_list=documents_list)
        logger.info(f"Файл '{file_name}' успешно загружен")
        return True
    else:
        logger.error(f"Не удалось сохранить файл '{file_name}'")
        await message.answer(
            f"❌ Не удалось сохранить файл '{file_name}'. Попробуйте снова.",
            reply_markup=get_simple_documents_keyboard()
        )
        return False


@router.message(CaseQuestionnaireStates.waiting_for_simple_documents, F.document)
async def simple_upload_document_handler(message: Message, state: FSMContext) -> None:
    """Обработка загрузки документа"""
    file = message.document
    success = await process_file_upload(
        message, state, file, file.file_name, file.file_size or 0
    )
    
    if success:
        data = await state.get_data()
        doc_count = len(data.get("documents_list", []))
        await message.answer(
            f"✅ Файл '{file.file_name}' загружен.\n"
            f"Загружено документов: {doc_count}\n\n"
            "Отправьте ещё документы или нажмите 'Готово'.",
            reply_markup=get_simple_documents_keyboard()
        )


@router.message(CaseQuestionnaireStates.waiting_for_simple_documents, F.photo)
async def simple_upload_photo_handler(message: Message, state: FSMContext) -> None:
    """Обработка загрузки фото"""
    photo = message.photo[-1]  # Самое большое фото
    file_name = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    
    success = await process_file_upload(
        message, state, photo, file_name, photo.file_size or 0
    )
    
    if success:
        data = await state.get_data()
        doc_count = len(data.get("documents_list", []))
        await message.answer(
            f"✅ Фото загружено.\n"
            f"Загружено документов: {doc_count}\n\n"
            "Отправьте ещё документы или нажмите 'Готово'.",
            reply_markup=get_simple_documents_keyboard()
        )


# ============================================
# Отмена анкеты
# ============================================

@router.message(F.text == "❌ Отмена", CaseQuestionnaireStates())
async def cancel_questionnaire(message: Message, state: FSMContext) -> None:
    """Отмена заполнения анкеты"""
    await state.clear()
    await message.answer(
        "❌ Заполнение анкеты отменено.",
        reply_markup=get_main_menu_keyboard()
    )
    logger.info("Анкета отменена")


# ============================================
# Сводка анкеты
# ============================================

async def show_summary(message: Message, state: FSMContext) -> None:
    """Показывает сводку всей анкеты"""
    data = await state.get_data()
    summary_text = format_summary_text(data)
    
    await message.answer(
        summary_text,
        reply_markup=get_questionnaire_summary_keyboard()
    )
    await state.set_state(CaseQuestionnaireStates.viewing_summary)


def format_summary_text(data: dict) -> str:
    """Форматирует текст сводки"""
    sections = [
        ("1️⃣ <b>СТОРОНЫ КОНФЛИКТА:</b>", "parties_info"),
        ("2️⃣ <b>ПРЕДМЕТ СПОРА:</b>", "dispute_subject"),
        ("3️⃣ <b>ОСНОВАНИЯ ТРЕБОВАНИЙ:</b>", "legal_basis"),
        ("4️⃣ <b>ХРОНОЛОГИЯ СОБЫТИЙ:</b>", "chronology"),
        ("5️⃣ <b>ДОКАЗАТЕЛЬСТВА:</b>", "evidence"),
        ("6️⃣ <b>ПРОЦЕССУАЛЬНАЯ ИСТОРИЯ:</b>", "procedural_history"),
        ("7️⃣ <b>ЦЕЛЬ КЛИЕНТА:</b>", "client_goal"),
    ]
    
    text = "📋 <b>СВОДКА АНКЕТЫ ДЕЛА</b>\n\n" + "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for title, field in sections:
        text += f"{title}\n{data.get(field, 'Не заполнено')}\n\n" + "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    documents_list = data.get("documents_list", [])
    total_docs = len(documents_list)
    text += f"📎 <b>Всего документов: {total_docs}</b>\n\nВыберите действие:"
    
    return text


# ============================================
# Редактирование разделов
# ============================================

@router.callback_query(F.data == "q_edit_section")
async def edit_section_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Показывает меню выбора раздела для редактирования"""
    await callback_query.message.edit_text(
        "Выберите раздел для редактирования:",
        reply_markup=get_edit_section_keyboard()
    )
    await callback_query.answer()


@router.callback_query(F.data == "q_back_summary")
async def back_to_summary_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Возврат к сводке"""
    data = await state.get_data()
    summary_text = format_summary_text(data)
    
    await callback_query.message.edit_text(
        summary_text,
        reply_markup=get_questionnaire_summary_keyboard()
    )
    await state.set_state(CaseQuestionnaireStates.viewing_summary)
    await callback_query.answer()


# Создаём обработчики редактирования через фабрику
def create_edit_handler(step: int):
    """Фабрика для создания обработчиков редактирования разделов"""
    async def handler(callback_query: CallbackQuery, state: FSMContext) -> None:
        await edit_section(callback_query, state, step)
    return handler


# Регистрируем обработчики редактирования
edit_callbacks = [
    ("q_edit_parties", 1),
    ("q_edit_dispute", 2),
    ("q_edit_legal_basis", 3),
    ("q_edit_chronology", 4),
    ("q_edit_evidence", 5),
    ("q_edit_procedural", 6),
    ("q_edit_goal", 7),
]

for callback_data, step in edit_callbacks:
    handler = create_edit_handler(step)
    router.callback_query(F.data == callback_data)(handler)


async def edit_section(callback_query: CallbackQuery, state: FSMContext, step: int) -> None:
    """Общая функция для редактирования раздела"""
    step_data = STEP_QUESTIONS[step]
    data = await state.get_data()
    
    field_name = step_data["field"]
    current_value = data.get(field_name, "")
    doc_count = len(data.get("documents_list", []))
    
    text = (
        f"✏️ <b>Редактирование: {step_data['title']}</b>\n\n"
        f"<b>Текущее значение:</b>\n"
        f"{current_value or 'Не заполнено'}\n\n"
        f"<b>Загружено документов:</b> {doc_count}\n\n"
        "Введите новое значение или нажмите 'Отмена':"
    )
    
    await callback_query.message.edit_text(
        text,
        reply_markup=get_cancel_questionnaire_keyboard()
    )
    
    await state.set_state(STATE_MAP[step])
    await state.update_data(editing_step=step)
    await callback_query.answer()


# ============================================
# Отправка анкеты
# ============================================

@router.callback_query(F.data == "q_submit")
async def submit_questionnaire_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Отправка анкеты на оценку"""
    data = await state.get_data()
    user_id = callback_query.from_user.id
    
    logger.info(f"Отправка анкеты пользователем {user_id}")
    
    async with get_db() as db:
        result = await db.execute(select(User).filter(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            await callback_query.message.edit_text("❌ Ошибка: пользователь не найден.")
            await callback_query.answer()
            logger.error(f"Пользователь {user_id} не найден в базе")
            return
        
        # Создаём запись анкеты в БД
        questionnaire = CaseQuestionnaire(
            user_id=user.id,
            parties_info=data.get("parties_info", ""),
            dispute_subject=data.get("dispute_subject", ""),
            legal_basis=data.get("legal_basis", ""),
            chronology=data.get("chronology", ""),
            evidence=data.get("evidence", ""),
            procedural_history=data.get("procedural_history", ""),
            client_goal=data.get("client_goal", ""),
            status="sent",
            sent_at=datetime.utcnow()
        )
        db.add(questionnaire)
        await db.flush()
        
        # Сохраняем документы
        documents_list = data.get("documents_list", [])
        for doc in documents_list:
            case_doc = CaseQuestionnaireDocument(
                questionnaire_id=questionnaire.id,
                section="general",
                file_path=doc["file_path"],
                file_type=doc["file_type"],
                original_name=doc["original_name"]
            )
            db.add(case_doc)
        
        await db.commit()
        logger.info(f"Анкета #{questionnaire.id} сохранена в базе")
        
        # Отправляем карточку в чат партнёров
        await send_card_to_chat(callback_query.message, state, questionnaire.id, data, user)
    
    # Подтверждение пользователю
    success_text = (
        "✅ <b>Анкета успешно отправлена на оценку!</b>\n\n"
        "Наши юристы рассмотрят ваше дело и свяжутся с вами в ближайшее время."
    )
    
    await callback_query.message.answer(
        success_text,
        reply_markup=get_back_keyboard()
    )
    
    try:
        await callback_query.message.delete()
    except Exception:
        pass
    
    await callback_query.answer()
    await state.clear()


async def send_card_to_chat(message: types.Message, state: FSMContext, questionnaire_id: int, data: dict, user: User) -> None:
    """Отправляет карточку анкеты в чат партнёров"""
    card_text = format_card_text(questionnaire_id, data, user)
    
    try:
        await message.bot.send_message(PARTNERS_CHAT_ID, card_text, parse_mode="HTML")
        logger.info(f"Карточка анкеты #{questionnaire_id} отправлена в чат")
    except Exception as e:
        logger.error(f"Ошибка при отправке карточки в чат: {e}")
    
    # Отправляем документы
    documents_list = data.get("documents_list", [])
    for doc in documents_list:
        try:
            if os.path.exists(doc["file_path"]):
                file = FSInputFile(doc["file_path"])
                await message.bot.send_document(
                    PARTNERS_CHAT_ID,
                    document=file,
                    caption=f"📎 {doc['original_name']}"
                )
        except Exception as e:
            logger.error(f"Ошибка при отправке документа {doc['original_name']}: {e}")


def format_card_text(questionnaire_id: int, data: dict, user: User) -> str:
    """Форматирует текст карточки для отправки в чат"""
    username = f"@{user.username}" if user.username else "нет"
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    
    text = (
        f"📋 <b>АНКЕТА ДЕЛА #{questionnaire_id}</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>Отправитель:</b> {full_name}\n"
        f"🔗 <b>Ссылка:</b> {username}\n"
        f"📱 <b>Telegram ID:</b> {user.telegram_id}\n"
        f"📅 <b>Дата:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    
    sections = [
        ("1️⃣ <b>СТОРОНЫ КОНФЛИКТА:</b>", "parties_info"),
        ("2️⃣ <b>ПРЕДМЕТ СПОРА:</b>", "dispute_subject"),
        ("3️⃣ <b>ОСНОВАНИЯ ТРЕБОВАНИЙ:</b>", "legal_basis"),
        ("4️⃣ <b>ХРОНОЛОГИЯ СОБЫТИЙ:</b>", "chronology"),
        ("5️⃣ <b>ДОКАЗАТЕЛЬСТВА:</b>", "evidence"),
        ("6️⃣ <b>ПРОЦЕССУАЛЬНАЯ ИСТОРИЯ:</b>", "procedural_history"),
        ("7️⃣ <b>ЦЕЛЬ КЛИЕНТА:</b>", "client_goal"),
    ]
    
    for title, field in sections:
        text += f"{title}\n{data.get(field, 'Не заполнено')}\n\n" + "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    documents_list = data.get("documents_list", [])
    total_docs = len(documents_list)
    text += f"📎 <b>Всего документов: {total_docs}</b>"
    
    return text


def register_send_case_handlers(dp):
    """Регистрация обработчиков"""
    dp.include_router(router)
