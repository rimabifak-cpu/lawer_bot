import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

router = Router()

# Определяем категории FAQ
FAQ_CATEGORIES = {
    "faq_partnership": {
        "name": "Начало работы и партнёрство",
        "questions": [
            {
                "question": "Как стать вашим партнёром?",
                "answer": "Заполните анкету в разделе «Партнёрский профиль». Мы свяжемся для согласования деталей."
            },
            {
                "question": "Нужно ли заключать договор?",
                "answer": "Да, мы оформляем договор об оказании услуг (агентский или партнёрский)."
            },
            {
                "question": "Это сотрудничество эксклюзивное?",
                "answer": "Нет, вы можете работать с другими юристами параллельно."
            },
            {
                "question": "Есть ли вступительный взнос или плата за доступ?",
                "answer": "Нет, доступ к боту и базе материалов для партнёров бесплатный."
            },
            {
                "question": "Как быстро активируется мой профиль после регистрации?",
                "answer": "Профиль активен сразу. Для начала работы нужно заполнить контактные данные."
            }
        ]
    },
    "faq_finance": {
        "name": "Финансы и выплаты",
        "questions": [
            {
                "question": "Как рассчитывается мое вознаграждение?",
                "answer": "Процент от итоговой суммы оплаты клиентом. Ставка растёт с увеличением общего объёма ваших сделок за месяц."
            },
            {
                "question": "Как и когда я получу свои деньги?",
                "answer": "Выплаты происходят 10 числа следующего месяца на вашу карту или расчётный счёт."
            },
            {
                "question": "Могу ли я установить свою наценку для клиента?",
                "answer": "Да, вы самостоятельно определяете итоговую цену для клиента. Ваша наценка остаётся вам полностью."
            },
            {
                "question": "Вы предоставляете документы для моей отчётности?",
                "answer": "Да, мы высылаем вам все закрывающие документы (акты, счета) для бухгалтерии."
            },
            {
                "question": "Что происходит, если клиент не платит?",
                "answer": "Наше вознаграждение начисляется только после 100% оплаты услуг клиентом."
            }
        ]
    },
    "faq_client_work": {
        "name": "Работа с клиентами и заявками",
        "questions": [
            {
                "question": "Как быстро вы даёте ответ по заявке?",
                "answer": "Предварительный анализ и ответ о возможности взятия дела — в течение 1 рабочего дня."
            },
            {
                "question": "Кто ведёт общение с моим клиентом?",
                "answer": "По вашему желанию. Вы можете быть единственным контактом, либо мы подключаемся напрямую."
            },
            {
                "question": "Могу ли я отслеживать статус дела моего клиента?",
                "answer": "Да, в разделе «История услуг» отображается этап работы по каждому делу."
            },
            {
                "question": "Что делать, если я не уверен, подходит ли дело вам?",
                "answer": "Отправьте заявку на оценку в любом случае. Наши юристы определят перспективы и предложат решение."
            },
            {
                "question": "Вы берётесь за срочные/экстренные случаи (например, внеплановая проверка)?",
                "answer": "Да, для срочных вопросов в боте есть кнопка «Срочная помощь». Реакция — в течение 2 часов."
            }
        ]
    },
    "faq_legal_services": {
        "name": "Юридические услуги и экспертиза",
        "questions": [
            {
                "question": "По каким именно направлениям вы работаете?",
                "answer": "Полный спектр для бизнеса: налоги, споры, проверки, договоры, корпоративное право. Актуальный список в разделе «Услуги»."
            },
            {
                "question": "Кто именно будет вести дело моего клиента?",
                "answer": "Дело ведёт профильный юрист или команда (например, по налоговым спорам — экс-сотрудник ФНС)."
            },
            {
                "question": "Даёте ли вы гарантию выигрыша в суде?",
                "answer": "Мы не даём гарантий, так как это запрещено правилами адвокатской деятельности. Мы берёмся только за дела с высокой экспертной оценкой перспектив."
            },
            {
                "question": "Предоставляете ли вы шаблоны документов для самостоятельного использования?",
                "answer": "Да, в разделе «Материалы» есть база актуальных шаблонов и инструкций для партнёров."
            },
            {
                "question": "Можете ли вы сопровождать клиента при проверках лично?",
                "answer": "Да, возможен выезд нашего юриста к клиенту для участия в мероприятиях проверяющих органов."
            }
        ]
    },
    "faq_technical_security": {
        "name": "Технические вопросы и безопасность",
        "questions": [
            {
                "question": "Конфиденциальны ли данные моего клиента в заявке?",
                "answer": "Абсолютно. Все данные шифруются и используются строго в рамках работы по делу. Мы соблюдаем 152-ФЗ."
            },
            {
                "question": "Мой клиент не хочет никуда загружать документы. Есть другой способ?",
                "answer": "Да, вы можете переслать файлы нам напрямую в зашифрованном виде, мы дадим инструкции."
            },
            {
                "question": "Что, если я потеряю доступ к Telegram?",
                "answer": "Свяжитесь с нашим менеджером по контакту из раздела «Поддержка» для восстановления доступа к истории."
            },
            {
                "question": "Как часто обновляются материалы в базе знаний?",
                "answer": "База обновляется еженедельно с учётом последних изменений законодательства и судебной практики."
            },
            {
                "question": "Можно ли интегрировать бота с моим CRM?",
                "answer": "Интеграция возможна для корпоративных партнёров по индивидуальному согласованию."
            }
        ]
    }
}

@router.message(F.text == "❓ FAQ")
async def faq_main_handler(message: Message) -> None:
    """
    Обработчик FAQ из главного меню - показывает категории
    """
    text = "<b>Выберите категорию вопросов:</b>\n\n  \n\n@legaldecision, поддержка 24/7"

    from bot.keyboards.keyboards import get_faq_categories_keyboard
    await message.answer(text, reply_markup=get_faq_categories_keyboard())

@router.callback_query(F.data.startswith("faq_"))
async def faq_category_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик выбора категории FAQ
    """
    category_key = callback_query.data
    
    # Проверяем, является ли это выбором конкретного вопроса
    if "_q" in category_key:
        # Это выбор конкретного вопроса, обрабатываем отдельно
        await faq_question_handler(callback_query)
        return
    
    # Если это просто выбор категории, показываем кнопки с вопросами
    if category_key == "faq_main_menu":
        # Возвращаемся к списку категорий
        text = "<b>Выберите категорию вопросов:</b>\n\n  \n\n@legaldecision, поддержка 24/7"
        from bot.keyboards.keyboards import get_faq_categories_keyboard
        await callback_query.message.edit_text(text, reply_markup=get_faq_categories_keyboard())
        await callback_query.answer()
        return
    
    # Определяем правильный ключ категории и показываем вопросы в виде кнопок
    if category_key in FAQ_CATEGORIES:
        category_data = FAQ_CATEGORIES[category_key]
        text = f"<b>{category_data['name']}:</b>\n\nВыберите интересующий вас вопрос:"
        
        from bot.keyboards.keyboards import get_faq_questions_keyboard
        await callback_query.message.edit_text(text, reply_markup=get_faq_questions_keyboard(category_key))
    else:
        text = "Категория не найдена."
        from bot.keyboards.keyboards import get_back_keyboard
        await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    
    await callback_query.answer()


async def faq_question_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик выбора конкретного вопроса в категории FAQ
    """
    # callback_data в формате 'faq_faq_partnership_q0' или 'faq_faq_client_work_q4'
    data = callback_query.data
    
    # Проверяем что это формат вопроса (заканчивается на _qN)
    if data.startswith("faq_") and "_q" in data:
        # Извлекаем номер вопроса из конца строки
        try:
            # Находим позицию _q
            q_pos = data.rfind("_q")
            category_part = data[4:q_pos]  # Убираем "faq_" в начале
            question_index = int(data[q_pos + 2:])  # Берём всё после "_q"
            
            # Теперь category_part содержит "faq_partnership" или "faq_client_work"
            if category_part.startswith("faq_"):
                category_key = category_part
            else:
                category_key = f"faq_{category_part}"
        except (ValueError, IndexError):
            text = "Неверный формат запроса."
            from bot.keyboards.keyboards import get_back_keyboard
            await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
            await callback_query.answer()
            return
        
        if category_key in FAQ_CATEGORIES:
            category_data = FAQ_CATEGORIES[category_key]
            
            if 0 <= question_index < len(category_data['questions']):
                qa = category_data['questions'][question_index]
                text = f"<b>{qa['question']}</b>\n\n{qa['answer']}"
                
                # Клавиатура с возможностью вернуться к списку вопросов
                from bot.keyboards.keyboards import InlineKeyboardBuilder, InlineKeyboardButton
                keyboard = InlineKeyboardBuilder()
                keyboard.add(
                    InlineKeyboardButton(
                        text="🔙 Назад к вопросам",
                        callback_data=f"faq_{category_key.replace('faq_', '')}"
                    ),
                    InlineKeyboardButton(
                        text="🏠 Главное меню",
                        callback_data="back_to_main"
                    )
                )
                keyboard.adjust(1)
                
                await callback_query.message.edit_text(text, reply_markup=keyboard.as_markup())
            else:
                text = "Вопрос не найден."
                from bot.keyboards.keyboards import get_back_keyboard
                await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
        else:
            text = "Категория не найдена."
            from bot.keyboards.keyboards import get_back_keyboard
            await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    else:
        text = "Неверный формат запроса."
        from bot.keyboards.keyboards import get_back_keyboard
        await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    
    await callback_query.answer()

def register_faq_handlers(dp):
    dp.include_router(router)