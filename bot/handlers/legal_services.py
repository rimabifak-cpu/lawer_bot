import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

# Обработчики для основных категорий юридических услуг
@router.callback_query(F.data == "legal_category_tax")
async def legal_category_tax_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Налоговое право и споры'
    """
    text = "<b>Налоговое право и споры</b>"
    from bot.keyboards.keyboards import get_tax_law_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_tax_law_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_arbitration")
async def legal_category_arbitration_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Арбитражные споры и исполнительное производство'
    """
    text = "<b>Арбитражные споры и исполнительное производство</b>"
    from bot.keyboards.keyboards import get_arbitration_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_arbitration_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_corporate")
async def legal_category_corporate_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Сопровождение бизнеса (Corporate)'
    """
    text = "<b>Сопровождение бизнеса (Corporate)</b>"
    from bot.keyboards.keyboards import get_corporate_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_corporate_services_keyboard())
    await callback_query.answer()


@router.callback_query(F.data == "legal_category_labor")
async def legal_category_labor_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Трудовое право и кадровое делопроизводство'
    """
    text = "<b>Трудовое право и кадровое делопроизводство</b>"
    from bot.keyboards.keyboards import get_labor_law_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_labor_law_services_keyboard())
    await callback_query.answer()


@router.callback_query(F.data == "legal_category_contract")
async def legal_category_contract_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Договорное право и сделки'
    """
    text = "<b>Договорное право и сделки</b>"
    from bot.keyboards.keyboards import get_contract_law_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_contract_law_services_keyboard())
    await callback_query.answer()


@router.callback_query(F.data == "legal_category_ip")
async def legal_category_ip_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Интеллектуальная собственность и IT'
    """
    text = "<b>Интеллектуальная собственность и IT</b>"
    from bot.keyboards.keyboards import get_ip_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_ip_services_keyboard())
    await callback_query.answer()


@router.callback_query(F.data == "legal_category_administrative")
async def legal_category_administrative_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Административное право и защита при проверках'
    """
    text = "<b>Административное право и защита при проверках</b>"
    from bot.keyboards.keyboards import get_admin_law_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_admin_law_services_keyboard())
    await callback_query.answer()


@router.callback_query(F.data == "legal_category_real_estate")
async def legal_category_real_estate_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Недвижимость и строительство'
    """
    text = "<b>Недвижимость и строительство</b>"
    from bot.keyboards.keyboards import get_real_estate_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_real_estate_services_keyboard())
    await callback_query.answer()


@router.callback_query(F.data == "legal_category_international")
async def legal_category_international_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Международное право и ВЭД'
    """
    text = "<b>Международное право и ВЭД</b>"
    from bot.keyboards.keyboards import get_international_law_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_international_law_services_keyboard())
    await callback_query.answer()


@router.callback_query(F.data == "legal_category_antitrust")
async def legal_category_antitrust_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Антимонопольное право (ФАС)'
    """
    text = "<b>Антимонопольное право (ФАС)</b>"
    from bot.keyboards.keyboards import get_antitrust_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_antitrust_services_keyboard())
    await callback_query.answer()


@router.callback_query(F.data == "legal_category_family_business")
async def legal_category_family_business_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Семейный бизнес и наследственное планирование'
    """
    text = "<b>Семейный бизнес и наследственное планирование</b>"
    from bot.keyboards.keyboards import get_family_business_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_family_business_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "back_to_legal_services")
async def back_to_legal_services_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик кнопки 'Назад к юридическим услугам'
    """
    from bot.keyboards.keyboards import get_legal_services_keyboard
    text = (
        "<b>Наши услуги:</b>\n\n"
        "Мы предлагаем широкий спектр юридических услуг для вашего бизнеса. "
        "Выберите интересующую вас категорию услуг:\n\n"
        "  \n\n"
        "@legaldecision, поддержка 24/7"
    )
    await callback_query.message.edit_text(
        text,
        reply_markup=get_legal_services_keyboard()
    )
    await callback_query.answer()

def register_legal_services_handlers(dp):
    dp.include_router(router)