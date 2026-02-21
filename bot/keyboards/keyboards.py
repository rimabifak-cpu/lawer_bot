"""
Модуль клавиатур для юридического бота
Оптимизированная версия с общими функциями для создания клавиатур
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from typing import List, Tuple, Optional


# ============================================
# Общие функции для создания клавиатур
# ============================================

def create_reply_keyboard(
    buttons: List[str],
    columns: int = 2,
    resize: bool = True
) -> ReplyKeyboardMarkup:
    """
    Создает Reply клавиатуру из списка кнопок
    
    Args:
        buttons: Список текстов для кнопок
        columns: Количество колонок
        resize: Автоматически изменять размер
    
    Returns:
        ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardBuilder()
    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    keyboard.adjust(columns)
    return keyboard.as_markup(resize_keyboard=resize)


def create_inline_keyboard(
    buttons: List[Tuple[str, str]],
    columns: int = 1
) -> InlineKeyboardMarkup:
    """
    Создает Inline клавиатуру из списка кнопок
    
    Args:
        buttons: Список кортежей (текст, callback_data)
        columns: Количество колонок
    
    Returns:
        InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardBuilder()
    for text, callback_data in buttons:
        keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    keyboard.adjust(columns)
    return keyboard.as_markup()


def create_service_keyboard(
    services: List[Tuple[str, str]],
    back_callback: str = "back_to_legal_services"
) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для категории услуг с кнопкой "Назад"
    
    Args:
        services: Список кортежей (название услуги, callback_data)
        back_callback: callback_data для кнопки "Назад"
    
    Returns:
        InlineKeyboardMarkup
    """
    buttons = services + [("🔙 Назад", back_callback)]
    return create_inline_keyboard(buttons, columns=1)


# ============================================
# Главное меню
# ============================================

MAIN_MENU_BUTTONS = [
    "📋 Услуги",
    "📚 История услуг",
    "👤 Партнёрский профиль",
    "💼 Отправить дело на оценку",
    "💬 Поддержка",
    "❓ FAQ"
]


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню (Reply - для обычных сообщений)"""
    return create_reply_keyboard(MAIN_MENU_BUTTONS, columns=2)


def get_main_menu_inline_keyboard() -> InlineKeyboardMarkup:
    """Inline-версия главного меню для использования с edit_text"""
    buttons = [
        ("📋 Услуги", "menu_services"),
        ("📚 История услуг", "menu_history"),
        ("👤 Партнёрский профиль", "menu_profile"),
        ("💼 Отправить дело на оценку", "menu_send_case"),
        ("💬 Поддержка", "menu_my_cases"),
        ("❓ FAQ", "menu_faq")
    ]
    return create_inline_keyboard(buttons, columns=2)


# ============================================
# Меню услуг
# ============================================

def get_services_keyboard() -> InlineKeyboardMarkup:
    """Меню услуг"""
    buttons = [
        ("Налоговые споры", "service_tax_disputes"),
        ("Проверки (ФНС, трудовая инспекция)", "service_audits"),
        ("Регистрация/ликвидация бизнеса", "service_registration"),
        ("Арбитражные споры", "service_arbitration"),
        ("🔙 Назад", "back_to_main")
    ]
    return create_inline_keyboard(buttons, columns=1)


# ============================================
# Меню профиля партнера
# ============================================

def get_partner_profile_keyboard() -> InlineKeyboardMarkup:
    """Меню профиля партнера"""
    buttons = [
        ("Заполнить/обновить мои данные", "profile_update"),
        ("Мой профиль", "profile_view"),
        ("Реферальная программа", "referral_program"),
        ("🔙 Назад", "back_to_main")
    ]
    return create_inline_keyboard(buttons, columns=1)


def get_referral_program_keyboard() -> InlineKeyboardMarkup:
    """Меню реферальной программы"""
    buttons = [
        ("📋 Скопировать реферальную ссылку", "copy_referral_link"),
        ("📊 История выплат", "payout_history"),
        ("🔙 Назад к профилю", "profile_view")
    ]
    return create_inline_keyboard(buttons, columns=1)


# ============================================
# Клавиатуры навигации
# ============================================

def get_back_keyboard() -> InlineKeyboardMarkup:
    """Кнопка назад"""
    return create_inline_keyboard([("🔙 Назад", "back_to_main")])


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для отмены"""
    return create_reply_keyboard(["❌ Отмена"], columns=1)


def get_skip_or_finish_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для пропуска или завершения"""
    return create_reply_keyboard(["Пропустить", "Завершить"], columns=2)


def get_finish_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для завершения"""
    return create_reply_keyboard(["Завершить"], columns=1)


def get_confirm_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для подтверждения"""
    return create_reply_keyboard(["Отправить", "Назад"], columns=2)


# ============================================
# FAQ клавиатуры
# ============================================

FAQ_CATEGORIES = [
    ("Начало работы и партнёрство", "faq_partnership"),
    ("Финансы и выплаты", "faq_finance"),
    ("Работа с клиентами и заявками", "faq_client_work"),
    ("Юридические услуги и экспертиза", "faq_legal_services"),
    ("Технические вопросы и безопасность", "faq_technical_security"),
]


def get_faq_categories_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категорий FAQ"""
    buttons = FAQ_CATEGORIES + [("🔙 Назад", "back_to_main")]
    return create_inline_keyboard(buttons, columns=1)


def get_faq_questions_keyboard(category_key: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопками для каждого вопроса в указанной категории FAQ
    """
    from bot.handlers.faq import FAQ_CATEGORIES as FAQ_DATA
    
    keyboard = InlineKeyboardBuilder()
    
    if category_key in FAQ_DATA:
        category_data = FAQ_DATA[category_key]
        
        for i, qa in enumerate(category_data['questions']):
            callback_data = f"faq_{category_key}_q{i}"
            keyboard.add(
                InlineKeyboardButton(
                    text=qa['question'],
                    callback_data=callback_data
                )
            )
    
    keyboard.add(InlineKeyboardButton(
        text="🔙 Назад к категориям",
        callback_data="faq_main_menu"
    ))
    
    keyboard.adjust(1)
    return keyboard.as_markup()


# ============================================
# Клавиатуры для юридических услуг
# ============================================

LEGAL_SERVICES = [
    ("Налоговое право и споры", "legal_category_tax"),
    ("Арбитражные споры и исполнительное производство", "legal_category_arbitration"),
    ("Сопровождение бизнеса (Corporate)", "legal_category_corporate"),
    ("Трудовое право и кадровое делопроизводство", "legal_category_labor"),
    ("Договорное право и сделки", "legal_category_contract"),
    ("Интеллектуальная собственность и IT", "legal_category_ip"),
    ("Административное право и защита при проверках", "legal_category_administrative"),
    ("Недвижимость и строительство", "legal_category_real_estate"),
    ("Международное право и ВЭД", "legal_category_international"),
    ("Антимонопольное право (ФАС)", "legal_category_antitrust"),
    ("Семейный бизнес и наследственное планирование", "legal_category_family_business"),
]


def get_legal_services_keyboard() -> InlineKeyboardMarkup:
    """Меню юридических услуг"""
    buttons = LEGAL_SERVICES + [("🔙 Назад", "back_to_main")]
    return create_inline_keyboard(buttons, columns=1)


# Категории услуг
TAX_SERVICES = [
    ("Налоговый консалтинг и планирование", "service_tax_consulting"),
    ("Защита в налоговых проверках", "service_tax_audits_defense"),
    ("Обжалование решений ИФНС", "service_tax_disputes_appeal"),
    ("Взыскание излишне уплаченных налогов", "service_tax_refunds"),
    ("Сопровождение банкротства (налоги)", "service_tax_bankruptcy_optimization"),
    ("Защита по делам о налоговых преступлениях", "service_tax_crimes_defense"),
]

ARBITRATION_SERVICES = [
    ("Взыскание дебиторской задолженности", "service_debt_collection"),
    ("Споры по договорам", "service_contract_disputes"),
    ("Корпоративные споры", "service_corporate_disputes"),
    ("Банкротство", "service_bankruptcy"),
    ("Оспаривание кадастровой стоимости", "service_land_valuation_disputes"),
    ("Исполнительное производство", "service_enforcement_proceedings"),
]

CORPORATE_SERVICES = [
    ("Регистрация и ликвидация юрлиц", "service_business_registration"),
    ("Внесение изменений в ЕГРЮЛ", "service_changes_to_egrul"),
    ("Корпоративное право", "service_corporate_governance"),
    ("Протоколирование мероприятий", "service_corporate_events"),
    ("Юридический аутсорсинг", "service_legal_outsourcing"),
    ("Due Diligence", "service_due_diligence"),
]

LABOR_SERVICES = [
    ("Подготовка трудовых документов", "service_labor_agreements"),
    ("Защита в трудовых спорах", "service_labor_disputes_defense"),
    ("Сопровождение проверок ГИТ", "service_labor_inspections_accompaniment"),
    ("Увольнение и сокращение", "service_employment_termination"),
    ("Миграционное право", "service_migration_law"),
]

CONTRACT_SERVICES = [
    ("Разработка и экспертиза договоров", "service_contract_development"),
    ("Устранение правовых рисков", "service_risk_elimination"),
    ("Легализация серых схем", "service_gray_scheme_legalization"),
    ("Сопровождение сделок с недвижимостью", "service_real_estate_transactions"),
]

IP_SERVICES = [
    ("Регистрация товарных знаков и патентов", "service_tm_patent_registration"),
    ("Защита авторских прав", "service_ip_rights_protection"),
    ("Договоры в сфере IT", "service_it_contracts"),
    ("Сопровождение digital-проектов", "service_digital_project_accompaniment"),
]

ADMIN_SERVICES = [
    ("Сопровождение проверок контролирующих органов", "service_authority_inspection_accompaniment"),
    ("Обжалование административных правонарушений", "service_administrative_offenses_appeal"),
    ("Защита от приостановки деятельности", "service_administrative_suspension_defense"),
]

REAL_ESTATE_SERVICES = [
    ("Юридический аудит недвижимости", "service_real_estate_audit"),
    ("Сделки с коммерческой недвижимостью", "service_commercial_real_estate_transactions"),
    ("Сопровождение строительных проектов", "service_construction_accompaniment"),
    ("Земельное право", "service_land_law"),
]

INTERNATIONAL_SERVICES = [
    ("Структурирование международных сделок", "service_international_structuring"),
    ("Создание и сопровождение зарубежных компаний", "service_foreign_company_accompaniment"),
    ("Сопровождение ВЭД", "service_foreign_trade_accompaniment"),
]

ANTITRUST_SERVICES = [
    ("Сопровождение сделок с согласованием ФАС", "service_transaction_approval_fas"),
    ("Защита при проверках соблюдения закона о рекламе", "service_advertising_law_defense"),
    ("Защита от недобросовестной конкуренции", "service_anti_competition_defense"),
]

FAMILY_BUSINESS_SERVICES = [
    ("Структурирование активов", "service_asset_structuring"),
    ("Создание наследственных фондов", "service_trust_fund_creation"),
    ("Раздел имущества супругов", "service_business_division"),
]


def get_tax_law_services_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категории 'Налоговое право и споры'"""
    return create_service_keyboard(TAX_SERVICES)


def get_arbitration_services_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категории 'Арбитражные споры'"""
    return create_service_keyboard(ARBITRATION_SERVICES)


def get_corporate_services_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категории 'Сопровождение бизнеса'"""
    return create_service_keyboard(CORPORATE_SERVICES)


def get_labor_law_services_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категории 'Трудовое право'"""
    return create_service_keyboard(LABOR_SERVICES)


def get_contract_law_services_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категории 'Договорное право'"""
    return create_service_keyboard(CONTRACT_SERVICES)


def get_ip_services_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категории 'Интеллектуальная собственность'"""
    return create_service_keyboard(IP_SERVICES)


def get_admin_law_services_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категории 'Административное право'"""
    return create_service_keyboard(ADMIN_SERVICES)


def get_real_estate_services_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категории 'Недвижимость'"""
    return create_service_keyboard(REAL_ESTATE_SERVICES)


def get_international_law_services_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категории 'Международное право'"""
    return create_service_keyboard(INTERNATIONAL_SERVICES)


def get_antitrust_services_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категории 'Антимонопольное право'"""
    return create_service_keyboard(ANTITRUST_SERVICES)


def get_family_business_services_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для категории 'Семейный бизнес'"""
    return create_service_keyboard(FAMILY_BUSINESS_SERVICES)


# ============================================
# Клавиатуры для анкеты дела
# ============================================

def get_step_documents_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора: прикрепить документ или пропустить"""
    return create_reply_keyboard(["📎 Прикрепить документ", "➡️ Далее"], columns=2)


def get_document_upload_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура во время загрузки документов"""
    return create_reply_keyboard(["✅ Завершить загрузку", "⏭️ Пропустить"], columns=2)


def get_simple_documents_keyboard() -> ReplyKeyboardMarkup:
    """Простая клавиатура для загрузки документов без выбора раздела"""
    return create_reply_keyboard(["✅ Готово", "⏭️ Пропустить", "❌ Отмена"], columns=2)


def get_questionnaire_summary_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура на сводке анкеты"""
    buttons = [
        ("✏️ Редактировать раздел", "q_edit_section"),
        ("✅ Отправить на оценку", "q_submit")
    ]
    return create_inline_keyboard(buttons, columns=1)


def get_edit_section_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора раздела для редактирования"""
    buttons = [
        ("1️⃣ Стороны конфликта", "q_edit_parties"),
        ("2️⃣ Предмет спора", "q_edit_dispute"),
        ("3️⃣ Основания требований", "q_edit_legal_basis"),
        ("4️⃣ Хронология событий", "q_edit_chronology"),
        ("5️⃣ Доказательства", "q_edit_evidence"),
        ("6️⃣ Процессуальная история", "q_edit_procedural"),
        ("7️⃣ Цель клиента", "q_edit_goal"),
        ("🔙 Назад к сводке", "q_back_summary"),
    ]
    return create_inline_keyboard(buttons, columns=1)


def get_edit_section_actions_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура при редактировании раздела"""
    return create_reply_keyboard(["📝 Изменить текст", "📎 Изменить документы", "🔙 Отмена"], columns=1)


def get_cancel_questionnaire_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой отмены"""
    return create_reply_keyboard(["❌ Отмена"], columns=1)


def get_documents_section_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора раздела при загрузке документов"""
    buttons = [
        ("📄 Стороны конфликта", "doc_parties"),
        ("📄 Предмет спора", "doc_dispute"),
        ("📄 Основания требований", "doc_legal_basis"),
        ("📄 Хронология событий", "doc_chronology"),
        ("📄 Доказательства", "doc_evidence"),
        ("📄 Процессуальная история", "doc_procedural"),
        ("📄 Цель клиента", "doc_goal"),
        ("✅ Загрузить всё и перейти к сводке", "doc_done"),
        ("🔙 Назад к сводке", "doc_back"),
    ]
    return create_inline_keyboard(buttons, columns=1)
