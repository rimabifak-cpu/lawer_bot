import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

# Обработчики для услуг в категории "Налоговое право и споры"
@router.callback_query(F.data == "service_tax_consulting")
async def service_tax_consulting_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Налоговый консалтинг и планирование</b>\n\n"
        "Консультации по вопросам налогообложения, оптимизация налоговой нагрузки, "
        "подготовка заключений по налоговым рискам и планирование налоговых стратегий."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_tax_audits_defense")
async def service_tax_audits_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Защита в налоговых проверках (выездных и камеральных)</b>\n\n"
        "Представительство интересов в ходе камеральных и выездных проверок, "
        "подготовка возражений на акты проверок, защита от незаконных требований."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_tax_disputes_appeal")
async def service_tax_disputes_appeal_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Обжалование решений и действий ИФНС</b>\n\n"
        "Подготовка жалоб на решения налоговых органов, обжалование действий и "
        "бездействия налоговых органов в вышестоящий орган и суд."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_tax_refunds")
async def service_tax_refunds_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Взыскание излишне уплаченных налогов и пеней</b>\n\n"
        "Подготовка заявлений на возврат излишне уплаченных налогов, пеней и штрафов, "
        "ведение дел в налоговых органах и судах."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_tax_bankruptcy_optimization")
async def service_tax_bankruptcy_optimization_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Сопровождение процедуры банкротства в целях налоговой оптимизации</b>\n\n"
        "Правовое сопровождение процедур банкротства с учетом налоговых аспектов, "
        "оптимизация налоговой нагрузки в рамках процедур банкротства."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_tax_crimes_defense")
async def service_tax_crimes_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Защита по делам о налоговых преступлениях (ст. 198, 199 УК РФ)</b>\n\n"
        "Участие в делах о налоговых преступлениях, защита прав налогоплательщиков, "
        "досудебное урегулирование, участие в судебных процессах."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# Обработчики для услуг в категории "Арбитражные споры и исполнительное производство"
@router.callback_query(F.data == "service_debt_collection")
async def service_debt_collection_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Взыскание дебиторской задолженности в досудебном и судебном порядке</b>\n\n"
        "Подготовка претензий, ведение дел в арбитражных судах, исполнительное производство, "
        "работа с коллекторскими агентствами."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_contract_disputes")
async def service_contract_disputes_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Защита интересов в спорах по договорам (поставки, подряда, оказания услуг)</b>\n\n"
        "Подготовка исков по договорным спорам, защита интересов в судах, анализ договоров, "
        "разработка стратегии ведения дела."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_corporate_disputes")
async def service_corporate_disputes_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Корпоративные споры (оспаривание решений собраний, выход из состава участников)</b>\n\n"
        "Защита интересов участников и акционеров, оспаривание решений органов управления, "
        "осуществление выхода из состава участников обществ."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_bankruptcy")
async def service_bankruptcy_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Банкротство (как кредитора, так и должника)</b>\n\n"
        "Подготовка и подача заявления о банкротстве, участие в процедуре банкротства, "
        "защита интересов кредиторов и должников."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_land_valuation_disputes")
async def service_land_valuation_disputes_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Оспаривание кадастровой стоимости</b>\n\n"
        "Подготовка заявления в комиссию по рассмотрению споров, оспаривание результатов "
        "определения кадастровой стоимости в суде."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_enforcement_proceedings")
async def service_enforcement_proceedings_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Исполнительное производство (контроль работы приставов, розыск имущества)</b>\n\n"
        "Контроль за действиями судебных приставов-исполнителей, розыск имущества, "
        "обжалование действий и бездействия приставов."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# Обработчики для услуг в категории "Сопровождение бизнеса (Corporate)"
@router.callback_query(F.data == "service_business_registration")
async def service_business_registration_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Регистрация и ликвидация юридических лиц (ООО, АО, ИП)</b>\n\n"
        "Полное сопровождение регистрации и ликвидации организаций, подготовка документов, "
        "взаимодействие с регистрирующими органами."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_changes_to_egrul")
async def service_changes_to_egrul_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Внесение изменений в ЕГРЮЛ</b>\n\n"
        "Подготовка и подача документов на изменение юридических адресов, состава участников, "
        "размера уставного капитала и других сведений."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_corporate_governance")
async def service_corporate_governance_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Корпоративное право (разработка уставов, договоров об управлении, эмиссия акций)</b>\n\n"
        "Разработка корпоративных документов, договоров об управлении, сопровождение эмиссии ценных бумаг."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_corporate_events")
async def service_corporate_events_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Протоколирование корпоративных мероприятий (собрания, заседания советов)</b>\n\n"
        "Подготовка протоколов общих собраний участников, заседаний советов директоров, "
        "обеспечение соответствия решений требованиям законодательства."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_legal_outsourcing")
async def service_legal_outsourcing_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Юридический аутсорсинг (абонентское обслуживание)</b>\n\n"
        "Постоянное юридическое сопровождение деятельности, подготовка документов, "
        "консультации по правовым вопросам."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_due_diligence")
async def service_due_diligence_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Due Diligence (правовая проверка компаний перед сделками)</b>\n\n"
        "Проверка юридической чистоты компании, анализ рисков, подготовка отчетов по правовому состоянию."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# Обработчики для услуг в категории "Трудовое право и кадровое делопроизводство"
@router.callback_query(F.data == "service_labor_agreements")
async def service_labor_agreements_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Подготовка и аудит трудовых договоров, ПВТР, положений</b>\n\n"
        "Разработка трудовых договоров, политик в области труда и их правового регулирования, "
        "аудит трудовой документации."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_labor_disputes_defense")
async def service_labor_disputes_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Защита интересов компании в трудовых спорах (восстановление на работе, взыскание ущерба)</b>\n\n"
        "Защита интересов работодателя в судах, обжалование решений ГИТ, защита от незаконных требований."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_labor_inspection_accompaniment")
async def service_labor_inspection_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Сопровождение проверок Государственной инспекции труда (ГИТ)</b>\n\n"
        "Подготовка к проверке, сопровождение в ходе проверки, подготовка возражений на акты проверки."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_employment_termination")
async def service_employment_termination_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Увольнение и сокращение штата</b>\n\n"
        "Подготовка документов для увольнения, сокращения штата, соблюдение процедур, "
        "защита интересов в случае споров."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_migration_law")
async def service_migration_law_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Миграционное право (оформление патентов и разрешений для иностранных работников)</b>\n\n"
        "Оформление разрешительных документов для иностранных граждан, сопровождение миграционных процедур."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# Обработчики для услуг в категории "Договорное право и сделки"
@router.callback_query(F.data == "service_contract_development")
async def service_contract_development_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Разработка, экспертиза и правовой анализ договоров</b>\n\n"
        "Подготовка договоров различной направленности, правовая экспертиза, "
        "анализ рисков и рекомендации по снижению правовых рисков."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_risk_elimination")
async def service_risk_elimination_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Устранение правовых рисков в договорной работе</b>\n\n"
        "Анализ договорной практики, выявление и устранение правовых рисков, "
        "разработка рекомендаций по оптимизации договорной работы."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_gray_scheme_legalization")
async def service_gray_scheme_legalization_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Легализация \"серых\" и \"черных\" схем</b>\n\n"
        "Правовая оптимизация схем ведения бизнеса, легализация неформальных отношений, "
        "разработка корректных правовых конструкций."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_real_estate_transactions")
async def service_real_estate_transactions_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Сопровождение сделок с недвижимостью и активами</b>\n\n"
        "Подготовка и сопровождение сделок купли-продажи, аренды, залога недвижимости, "
        "анализ юридической чистоты объектов."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# Обработчики для услуг в категории "Интеллектуальная собственность и IT"
@router.callback_query(F.data == "service_tm_patent_registration")
async def service_tm_patent_registration_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Регистрация товарных знаков, патентов, программ для ЭВМ</b>\n\n"
        "Регистрация объектов интеллектуальной собственности, сопровождение процедур, "
        "защита прав на результаты интеллектуальной деятельности."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_ip_rights_protection")
async def service_ip_rights_protection_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Защита авторских и смежных прав</b>\n\n"
        "Защита прав на произведения науки, литературы и искусства, обжалование решений, "
        "представительство в делах об интеллектуальных спорах."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_it_contracts")
async def service_it_contracts_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Договоры в сфере IT (разработка ПО, лицензионные соглашения, SLA)</b>\n\n"
        "Подготовка и экспертиза договоров в сфере информационных технологий, "
        "защита интересов в IT-проектах."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_digital_project_accompaniment")
async def service_digital_project_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Правовое сопровождение digital-проектов</b>\n\n"
        "Правовое сопровождение разработки и продвижения цифровых продуктов, "
        "защита интересов в онлайн-проектах."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# Обработчики для услуг в категории "Административное право и защита при проверках"
@router.callback_query(F.data == "service_authority_inspection_accompaniment")
async def service_authority_inspection_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Сопровождение проверок МЧС, Роспотребнадзора, Роскомнадзора, Росприроднадзора</b>\n\n"
        "Подготовка к проверкам, сопровождение в ходе проверок, подготовка возражений на акты проверок."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_administrative_offenses_appeal")
async def service_administrative_offenses_appeal_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Обжалование протоколов и постановлений об административных правонарушениях</b>\n\n"
        "Подготовка жалоб на постановления по делам об административных правонарушениях, "
        "защита интересов в судах."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_administrative_suspension_defense")
async def service_administrative_suspension_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Защита в делах об административных приостановках деятельности</b>\n\n"
        "Защита от приостановки деятельности, оспаривание решений, представительство в судах."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# Обработчики для услуг в категории "Недвижимость и строительство"
@router.callback_query(F.data == "service_real_estate_audit")
async def service_real_estate_audit_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Юридический аудит объектов недвижимости</b>\n\n"
        "Проверка юридической чистоты объектов недвижимости, анализ рисков, "
        "подготовка заключений о правовом состоянии объектов."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_commercial_real_estate_transactions")
async def service_commercial_real_estate_transactions_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Сопровождение сделок купли-продажи, аренды коммерческой недвижимости</b>\n\n"
        "Подготовка и сопровождение сделок с коммерческой недвижимостью, "
        "анализ правового состояния объектов."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_construction_accompaniment")
async def service_construction_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Правовое сопровождение строительных проектов (разрешительная документация, споры с подрядчиками)</b>\n\n"
        "Подготовка разрешительной документации, сопровождение строительства, "
        "защита интересов в спорах с подрядчиками."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_land_law")
async def service_land_law_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Земельное право (перевод земель, разрешенное использование, споры)</b>\n\n"
        "Оформление прав на земельные участки, перевод земель, установление разрешенного использования, "
        "защита интересов в земельных спорах."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# Обработчики для услуг в категории "Международное право и ВЭД"
@router.callback_query(F.data == "service_international_structuring")
async def service_international_structuring_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Структурирование международных сделок</b>\n\n"
        "Разработка правовых схем международной торговли, оптимизация налоговой нагрузки, "
        "защита активов за рубежом."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_foreign_company_accompaniment")
async def service_foreign_company_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Создание и сопровождение зарубежных компаний</b>\n\n"
        "Регистрация и сопровождение иностранных юридических лиц, "
        "обеспечение соответствия требованиям местного законодательства."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_foreign_trade_accompaniment")
async def service_foreign_trade_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Правовое сопровождение внешнеэкономической деятельности (контракты, таможня, валютный контроль)</b>\n\n"
        "Подготовка ВЭД контрактов, сопровождение таможенных процедур, "
        "соблюдение требований валютного законодательства."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# Обработчики для услуг в категории "Антимонопольное право (ФАС)"
@router.callback_query(F.data == "service_transaction_approval_fas")
async def service_transaction_approval_fas_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Сопровождение сделок, требующих согласования с ФАС</b>\n\n"
        "Подготовка документов для согласования сделок с антимонопольным органом, "
        "представительство в ФАС."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_advertising_law_defense")
async def service_advertising_law_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Защита при проверках соблюдения закона о рекламе</b>\n\n"
        "Сопровождение проверок рекламы, защита от незаконных требований, "
        "обжалование решений антимонопольного органа."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_anti_competition_defense")
async def service_anti_competition_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Защита в делах о картелях и недобросовестной конкуренции</b>\n\n"
        "Защита интересов в антимонопольных делах, оспаривание решений, "
        "представительство в судах."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# Обработчики для услуг в категории "Семейный бизнес и наследственное планирование"
@router.callback_query(F.data == "service_asset_structuring")
async def service_asset_structuring_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Структурирование активов для защиты при наследовании или разводе</b>\n\n"
        "Разработка схем защиты активов, подготовка брачных контрактов, "
        "структурирование семейного бизнеса."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_trust_fund_creation")
async def service_trust_fund_creation_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Создание наследственных фондов</b>\n\n"
        "Подготовка документов для создания наследственных фондов, "
        "сопровождение процедур, защита интересов бенефициаров."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_business_division")
async def service_business_division_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>Раздел имущества супругов в отношении бизнеса</b>\n\n"
        "Подготовка соглашений о разделе имущества, защита интересов в судебных спорах, "
        "учет специфики бизнеса при разделе."
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

def register_service_detail_handlers(dp):
    dp.include_router(router)