import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

# Обработчики для inline кнопок услуг
@router.callback_query(F.data == "service_tax_disputes")
async def service_tax_disputes_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик услуги 'Налоговые споры'
    """
    text = (
        "<b>Налоговые споры</b>\n\n"
        "Мы оказываем комплексную помощь в решении налоговых споров:\n"
        "• Представительство в налоговых органах\n"
        "• Защита интересов в судах различных инстанций\n"
        "• Анализ налоговых рисков\n"
        "• Подготовка возражений на акты проверок\n\n"
        "Если вас интересует данная услуга, вы можете отправить нам дело на оценку."
    )
    from bot.keyboards.keyboards import get_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_audits")
async def service_audits_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик услуги 'Проверки (ФНС, трудовая инспекция)'
    """
    text = (
        "<b>Проверки (ФНС, трудовая инспекция)</b>\n\n"
        "Правовое сопровождение во время проверок:\n"
        "• Подготовка к налоговым проверкам\n"
        "• Представительство в ходе камеральных и выездных проверок\n"
        "• Юридическая защита при проверках трудовой инспекции\n"
        "• Сопровождение в ходе проверок других контролирующих органов\n\n"
        "Наши специалисты помогут минимизировать риски и защитить ваши интересы."
    )
    from bot.keyboards.keyboards import get_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_registration")
async def service_registration_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик услуги 'Регистрация/ликвидация бизнеса'
    """
    text = (
        "<b>Арбитражные споры</b>\n\n"
        "Наши юристы — это не просто теоретики, а бывшие сотрудники ФНС и арбитражных судов. Они знают систему изнутри: как принимаются решения и на что смотрят проверяющие. Это позволяет не просто формально сопровождать дело, а прогнозировать и влиять на его исход, что напрямую экономит время и деньги ваших клиентов.\n\n"
        "Мы работаем по чёткому регламенту с полной финансовой прозрачностью. Вы и ваш клиент всегда знаете стоимость каждого этапа и видите статус работы в личном кабинете в режиме реального времени. Это исключает скрытые платежи и «сюрпризы» в конце месяца, строя долгосрочные отношения на доверии.\n\n"
        "В отличие от многих юридических фирм, мы даём финансовые гарантии результата на этапе оценки дела. Если после нашего анализа перспективы дела высоки, мы готовы зафиксировать это в соглашении. Для вас как для партнёра это сильнейший аргумент — вы предлагаете не просто услугу, а минимальные риски для бизнеса вашего клиента.\n\n"
        "Защита интересов в арбитражных судах:\n"
        "• Представительство в арбитражных судах\n"
        "• Подготовка исковых заявлений и жалоб\n"
        "• Защита в делах экономического характера\n"
        "• Взыскание дебиторской задолженности\n\n"
        "Комплексный подход к решению любых арбитражных споров."
    )
    from bot.keyboards.keyboards import get_legal_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_legal_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_arbitration")
async def service_arbitration_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик услуги 'Арбитражные споры'
    """
    text = (
        "<b>Арбитражные споры</b>\n\n"
        "Защита интересов в арбитражных судах:\n"
        "• Представительство в арбитражных судах\n"
        "• Подготовка исковых заявлений и жалоб\n"
        "• Защита в делах экономического характера\n"
        "• Взыскание дебиторской задолженности\n\n"
        "Комплексный подход к решению любых арбитражных споров."
    )
    from bot.keyboards.keyboards import get_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_services_keyboard())
    await callback_query.answer()

def register_services_handlers(dp):
    dp.include_router(router)