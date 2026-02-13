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
    text = (
        "<b>Налоговое право и споры:</b>\n\n"
        "• Налоговый консалтинг и планирование\n"
        "• Защита в налоговых проверках (выездных и камеральных)\n"
        "• Обжалование решений и действий ИФНС\n"
        "• Взыскание излишне уплаченных налогов и пеней\n"
        "• Сопровождение процедуры банкротства в целях налоговой оптимизации\n"
        "• Защита по делам о налоговых преступлениях (ст. 198, 199 УК РФ)"
    )
    from bot.keyboards.keyboards import get_tax_law_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_tax_law_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_arbitration")
async def legal_category_arbitration_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Арбитражные споры и исполнительное производство'
    """
    text = (
        "<b>Арбитражные споры и исполнительное производство:</b>\n\n"
        "• Взыскание дебиторской задолженности в досудебном и судебном порядке\n"
        "• Защита интересов в спорах по договорам (поставки, подряда, оказания услуг)\n"
        "• Корпоративные споры (оспаривание решений собраний, выход из состава участников)\n"
        "• Банкротство (как кредитора, так и должника)\n"
        "• Оспаривание кадастровой стоимости\n"
        "• Исполнительное производство (контроль работы приставов, розыск имущества)"
    )
    from bot.keyboards.keyboards import get_arbitration_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_arbitration_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_corporate")
async def legal_category_corporate_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Сопровождение бизнеса (Corporate)'
    """
    text = (
        "<b>Сопровождение бизнеса (Corporate):</b>\n\n"
        "• Регистрация и ликвидация юридических лиц (ООО, АО, ИП)\n"
        "• Внесение изменений в ЕГРЮЛ\n"
        "• Корпоративное право (разработка уставов, договоров об управлении, эмиссия акций)\n"
        "• Протоколирование корпоративных мероприятий (собрания, заседания советов)\n"
        "• Юридический аутсорсинг (абонентское обслуживание)\n"
        "• Due Diligence (правовая проверка компаний перед сделками)"
    )
    from bot.keyboards.keyboards import get_corporate_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_corporate_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_labor")
async def legal_category_labor_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Трудовое право и кадровое делопроизводство'
    """
    text = (
        "<b>Трудовое право и кадровое делопроизводство:</b>\n\n"
        "• Подготовка и аудит трудовых договоров, ПВТР, положений\n"
        "• Защита интересов компании в трудовых спорах (восстановление на работе, взыскание ущерба)\n"
        "• Сопровождение проверок Государственной инспекции труда (ГИТ)\n"
        "• Увольнение и сокращение штата\n"
        "• Миграционное право (оформление патентов и разрешений для иностранных работников)"
    )
    from bot.keyboards.keyboards import get_labor_law_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_labor_law_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_contract")
async def legal_category_contract_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Договорное право и сделки'
    """
    text = (
        "<b>Договорное право и сделки:</b>\n\n"
        "• Разработка, экспертиза и правовой анализ договоров\n"
        "• Устранение правовых рисков в договорной работе\n"
        "• Легализация \"серых\" и \"черных\" схем\n"
        "• Сопровождение сделок с недвижимостью и активами"
    )
    from bot.keyboards.keyboards import get_contract_law_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_contract_law_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_ip")
async def legal_category_ip_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Интеллектуальная собственность и IT'
    """
    text = (
        "<b>Интеллектуальная собственность и IT:</b>\n\n"
        "• Регистрация товарных знаков, патентов, программ для ЭВМ\n"
        "• Защита авторских и смежных прав\n"
        "• Договоры в сфере IT (разработка ПО, лицензионные соглашения, SLA)\n"
        "• Правовое сопровождение digital-проектов"
    )
    from bot.keyboards.keyboards import get_ip_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_ip_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_administrative")
async def legal_category_administrative_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Административное право и защита при проверках'
    """
    text = (
        "<b>Административное право и защита при проверках:</b>\n\n"
        "• Сопровождение проверок МЧС, Роспотребнадзора, Роскомнадзора, Росприроднадзора\n"
        "• Обжалование протоколов и постановлений об административных правонарушениях\n"
        "• Защита в делах об административных приостановках деятельности"
    )
    from bot.keyboards.keyboards import get_admin_law_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_admin_law_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_real_estate")
async def legal_category_real_estate_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Недвижимость и строительство'
    """
    text = (
        "<b>Недвижимость и строительство:</b>\n\n"
        "• Юридический аудит объектов недвижимости\n"
        "• Сопровождение сделок купли-продажи, аренды коммерческой недвижимости\n"
        "• Правовое сопровождение строительных проектов (разрешительная документация, споры с подрядчиками)\n"
        "• Земельное право (перевод земель, разрешенное использование, споры)"
    )
    from bot.keyboards.keyboards import get_real_estate_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_real_estate_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_international")
async def legal_category_international_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Международное право и ВЭД'
    """
    text = (
        "<b>Международное право и ВЭД:</b>\n\n"
        "• Структурирование международных сделок\n"
        "• Создание и сопровождение зарубежных компаний\n"
        "• Правовое сопровождение внешнеэкономической деятельности (контракты, таможня, валютный контроль)"
    )
    from bot.keyboards.keyboards import get_international_law_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_international_law_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_antitrust")
async def legal_category_antitrust_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Антимонопольное право (ФАС)'
    """
    text = (
        "<b>Антимонопольное право (ФАС):</b>\n\n"
        "• Сопровождение сделок, требующих согласования с ФАС\n"
        "• Защита при проверках соблюдения закона о рекламе\n"
        "• Защита в делах о картелях и недобросовестной конкуренции"
    )
    from bot.keyboards.keyboards import get_antitrust_services_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_antitrust_services_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "legal_category_family_business")
async def legal_category_family_business_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик категории 'Семейный бизнес и наследственное планирование'
    """
    text = (
        "<b>Семейный бизнес и наследственное планирование:</b>\n\n"
        "• Структурирование активов для защиты при наследовании или разводе\n"
        "• Создание наследственных фондов\n"
        "• Раздел имущества супругов в отношении бизнеса"
    )
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
        "Выберите интересующую вас категорию услуг:"
    )
    await callback_query.message.edit_text(
        text,
        reply_markup=get_legal_services_keyboard()
    )
    await callback_query.answer()

def register_legal_services_handlers(dp):
    dp.include_router(router)