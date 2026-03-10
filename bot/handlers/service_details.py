"""
Обработчики для детального описания юридических услуг
Каждая услуга содержит: описание, преимущества, этапы работы
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

# ============================================
# НАЛОГОВОЕ ПРАВО И СПОРЫ
# ============================================

@router.callback_query(F.data == "service_tax_consulting")
async def service_tax_consulting_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📊 Налоговый консалтинг и планирование</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Комплексный анализ вашей системы налогообложения, выявление точек оптимизации, "
        "разработка законных схем снижения налоговой нагрузки. Консультации по всем аспектам "
        "налогового права, подготовка заключений по сложным вопросам.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Экс-сотрудники ФНС в команде\n"
        "✓ Законная оптимизация без рисков\n"
        "✓ Экономия до 40% на налогах\n"
        "✓ Персональная стратегия под ваш бизнес\n"
        "✓ Сопровождение внедрения рекомендаций"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_tax_audits_defense")
async def service_tax_audits_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🛡️ Защита в налоговых проверках</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Полное сопровождение камеральных и выездных налоговых проверок. Подготовка к проверке, "
        "участие в мероприятиях контроля, анализ требований инспекции, подготовка возражений "
        "на акты проверок. Минимизация доначислений и штрафов.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Успешный опыт 200+ проверок\n"
        "✓ Снижение доначислений в 3-5 раз\n"
        "✓ Работаем на всех стадиях проверки\n"
        "✓ Круглосуточная поддержка клиента\n"
        "✓ Гарантия конфиденциальности"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_tax_disputes_appeal")
async def service_tax_disputes_appeal_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>⚖️ Обжалование решений и действий ИФНС</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Подготовка и подача жалоб на решения налоговых органов в вышестоящий орган и суд. "
        "Оспаривание актов проверок, требований об уплате налогов, решений о привлечении "
        "к ответственности. Представительство в судах всех инстанций.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ 85% выигранных дел\n"
        "✓ Опыт работы в арбитражных судах\n"
        "✓ Глубокое знание налоговой практики\n"
        "✓ Работа без предоплаты (по согласованию)\n"
        "✓ Прозрачная система оплаты"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_tax_refunds")
async def service_tax_refunds_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>💰 Взыскание излишне уплаченных налогов и пеней</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Помощь в возврате переплат по налогам, пеням и штрафам. Проводим сверку с ИФНС, "
        "подготавливаем заявления на возврат, оспариваем отказы. Взыскание через суд "
        "в случае бездействия налоговой инспекции.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Возвращаем миллионы рублей клиентам\n"
        "✓ Знаем все основания для отказа\n"
        "✓ Работаем по всей России\n"
        "✓ Ускоренный возврат за 30-45 дней\n"
        "✓ Оплата по факту возврата"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_tax_bankruptcy_optimization")
async def service_tax_bankruptcy_optimization_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🏢 Сопровождение банкротства в целях налоговой оптимизации</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Правовое сопровождение процедур банкротства с учётом налоговых аспектов. "
        "Защита от субсидиарной ответственности, оспаривание требований кредиторов, "
        "оптимизация налогов в рамках процедуры.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Защита личных активов собственника\n"
        "✓ Снижение налоговой нагрузки при ликвидации\n"
        "✓ Опыт 50+ успешных банкротств\n"
        "✓ Комплексный подход: юристы + налоговики\n"
        "✓ Конфиденциальность гарантирована"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_tax_crimes_defense")
async def service_tax_crimes_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🔒 Защита по делам о налоговых преступлениях</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Защита по ст. 198, 199 УК РФ на всех стадиях уголовного процесса. Участие "
        "в проверках, допросах, обысках. Подготовка позиции защиты, взаимодействие "
        "со следствием, представительство в суде.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Адвокаты с опытом работы в правоохранительных органах\n"
        "✓ 90% дел закрыто на досудебной стадии\n"
        "✓ Круглосуточный выезд при задержании\n"
        "✓ Полная защита бизнеса и собственников\n"
        "✓ Строгая конфиденциальность"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# ============================================
# АРБИТРАЖНЫЕ СПОРЫ
# ============================================

@router.callback_query(F.data == "service_debt_collection")
async def service_debt_collection_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>💵 Взыскание дебиторской задолженности</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Комплексное взыскание долгов в досудебном и судебном порядке. Претензионная работа, "
        "подача исков в арбитражный суд, получение исполнительных листов, сопровождение "
        "исполнительного производства, розыск имущества должника.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Взыскали более 500 млн рублей\n"
        "✓ Досудебное урегулирование в 60% случаев\n"
        "✓ Работаем по всей России\n"
        "✓ Оплата по факту взыскания (по согласованию)\n"
        "✓ Полное ведение дела «под ключ»"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_contract_disputes")
async def service_contract_disputes_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📄 Споры по договорам</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Защита интересов в спорах по договорам поставки, подряда, оказания услуг, аренды. "
        "Анализ договоров, подготовка правовой позиции, ведение дела в арбитражном суде, "
        "исполнение судебного решения.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Специализация на договорном праве\n"
        "✓ Выиграли 90% споров по договорам\n"
        "✓ Глубокий анализ перспектив дела\n"
        "✓ Честная оценка рисков\n"
        "✓ Прозрачное ценообразование"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_corporate_disputes")
async def service_corporate_disputes_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🏛️ Корпоративные споры</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Защита интересов участников и акционеров в корпоративных конфликтах. Оспаривание "
        "решений собраний, выход из состава участников, взыскание убытков с руководителей, "
        "разрешение споров о долях в уставном капитале.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт в сложных корпоративных конфликтах\n"
        "✓ Защита миноритарных акционеров\n"
        "✓ Работа с публичными компаниями\n"
        "✓ Конфиденциальность гарантирована\n"
        "✓ Индивидуальная стратегия защиты"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_bankruptcy")
async def service_bankruptcy_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>⚖️ Банкротство юридических лиц</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Сопровождение процедур банкротства на стороне должника или кредитора. Подготовка "
        "заявления о банкротстве, участие в собраниях кредиторов, защита от субсидиарной "
        "ответственности, оспаривание сделок должника.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Более 100 успешных процедур\n"
        "✓ Защита от субсидиарной ответственности\n"
        "✓ Работа с крупными долгами (от 100 млн ₽)\n"
        "✓ Команда: юристы + финансовые управляющие\n"
        "✓ Полное сопровождение «под ключ»"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_land_valuation_disputes")
async def service_land_valuation_disputes_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🏗️ Оспаривание кадастровой стоимости</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Снижение кадастровой стоимости недвижимости и земельных участков через комиссию "
        "по рассмотрению споров и суд. Подготовка отчёта об оценке, подача заявления, "
        "представительство в уполномоченных органах.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Снижение кадастровой стоимости до 70%\n"
        "✓ Экономия на налогах за 3-5 лет\n"
        "✓ Оплата по факту снижения\n"
        "✓ Работаем по всей России\n"
        "✓ Собственная сеть оценщиков"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_enforcement_proceedings")
async def service_enforcement_proceedings_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📋 Исполнительное производство</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Контроль работы судебных приставов-исполнителей, розыск имущества и счетов должника, "
        "обжалование действий и бездействия приставов, привлечение должника к ответственности, "
        "взыскание исполнительского сбора.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Знаем все методы работы приставов\n"
        "✓ Ускоряем исполнительное производство в 2-3 раза\n"
        "✓ Находим скрытое имущество\n"
        "✓ Работаем до фактического исполнения\n"
        "✓ Полное ведение дела"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# ============================================
# СОПРОВОЖДЕНИЕ БИЗНЕСА (CORPORATE)
# ============================================

@router.callback_query(F.data == "service_business_registration")
async def service_business_registration_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🏢 Регистрация и ликвидация юрлиц</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Полное сопровождение регистрации ООО, АО, ИП. Подготовка учредительных документов, "
        "выбор оптимальной организационно-правовой формы, взаимодействие с регистрирующим органом. "
        "Также сопровождаем процедуры ликвидации и реорганизации.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Регистрация за 3-5 рабочих дней\n"
        "✓ Гарантия прохождения госрегистрации\n"
        "✓ Подбор кодов ОКВЭД\n"
        "✓ Консультация по системе налогообложения\n"
        "✓ Сопровождение «под ключ»"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_changes_to_egrul")
async def service_changes_to_egrul_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📝 Внесение изменений в ЕГРЮЛ</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Подготовка и подача документов на изменение сведений в ЕГРЮЛ: смена юридического "
        "адреса, состава участников, размера уставного капитала, генерального директора, "
        "кодов ОКВЭД. Получение готовых документов.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Внесение изменений за 5-7 дней\n"
        "✓ Гарантия регистрации изменений\n"
        "✓ Подготовка всех документов\n"
        "✓ Подача без вашего участия\n"
        "✓ Получение готовых документов курьером"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_corporate_governance")
async def service_corporate_governance_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📊 Корпоративное право</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Разработка и актуализация корпоративных документов: уставов, положений, договоров "
        "об управлении. Сопровождение эмиссии акций, регистрация выпусков ценных бумаг в ЦБ РФ, "
        "подготовка отчётности.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт работы с ЦБ РФ\n"
        "✓ Разработка индивидуальных уставов\n"
        "✓ Защита от корпоративных захватов\n"
        "✓ Комплексное корпоративное сопровождение\n"
        "✓ Конфиденциальность гарантирована"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_corporate_events")
async def service_corporate_events_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📋 Протоколирование корпоративных мероприятий</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Подготовка и проведение общих собраний участников, заседаний советов директоров. "
        "Разработка повестки дня, подготовка проектов решений, ведение протоколов, "
        "уведомление участников, обеспечение кворума.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Соответствие всем требованиям закона\n"
        "✓ Защита от оспаривания решений\n"
        "✓ Опыт проведения сложных собраний\n"
        "✓ Полное документальное сопровождение\n"
        "✓ Присутствие на мероприятиях"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_legal_outsourcing")
async def service_legal_outsourcing_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>💼 Юридический аутсорсинг</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Абонентское юридическое обслуживание вашего бизнеса. Постоянное сопровождение "
        "деятельности, консультации по правовым вопросам, подготовка договоров, претензий, "
        "исков, представительство в судах и госорганах.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Экономия до 70% vs штатный юрист\n"
        "✓ Команда экспертов вместо одного специалиста\n"
        "✓ Фиксированная абонентская плата\n"
        "✓ Быстрое реагирование на запросы\n"
        "✓ Полная ответственность за результат"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_due_diligence")
async def service_due_diligence_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🔍 Due Diligence (правовая проверка компаний)</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Комплексная правовая проверка компании перед сделкой M&A, инвестициями, партнёрством. "
        "Анализ учредительных документов, договоров, судебных дел, активов, обязательств. "
        "Подготовка отчёта с выявленными рисками и рекомендациями.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Глубокий анализ всех аспектов бизнеса\n"
        "✓ Выявление скрытых рисков\n"
        "✓ Опыт проверки крупных сделок\n"
        "✓ Сжатые сроки (от 5 дней)\n"
        "✓ Практические рекомендации"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# ============================================
# ТРУДОВОЕ ПРАВО
# ============================================

@router.callback_query(F.data == "service_labor_agreements")
async def service_labor_agreements_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📑 Подготовка и аудит трудовых договоров</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Разработка и правовая экспертиза трудовых договоров, должностных инструкций, "
        "положений об оплате труда, ПВТР. Аудит кадровой документации, выявление нарушений, "
        "подготовка рекомендаций по приведению в соответствие с ТК РФ.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Защита от трудовых споров\n"
        "✓ Соответствие требованиям ГИТ\n"
        "✓ Учёт специфики вашего бизнеса\n"
        "✓ Быстрое внесение изменений\n"
        "✓ Консультации по применению документов"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_labor_disputes_defense")
async def service_labor_disputes_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>⚖️ Защита в трудовых спорах</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Представительство интересов работодателя в судах по трудовым спорам: восстановление "
        "на работе, взыскание заработной платы, оспаривание дисциплинарных взысканий, "
        "возмещение ущерба, причинённого работником.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ 80% выигранных дел в пользу работодателя\n"
        "✓ Защита от штрафов ГИТ\n"
        "✓ Опыт в сложных конфликтах\n"
        "✓ Досудебное урегулирование\n"
        "✓ Полное ведение дела"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_labor_inspection_accompaniment")
async def service_labor_inspection_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🛡️ Сопровождение проверок ГИТ</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Подготовка к плановым и внеплановым проверкам Государственной инспекции труда. "
        "Сопровождение в ходе проверки, подготовка возражений на предписания, обжалование "
        "постановлений о привлечении к ответственности.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Знаем критерии риска ГИТ\n"
        "✓ Снижение штрафов в 2-3 раза\n"
        "✓ Минимизация предписаний\n"
        "✓ Оперативная поддержка 24/7\n"
        "✓ Полное сопровождение проверки"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_employment_termination")
async def service_employment_termination_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📤 Увольнение и сокращение штата</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Правовое сопровождение процедур увольнения и сокращения численности персонала. "
        "Подготовка приказов, уведомлений, расчётов. Соблюдение процедур, минимизация "
        "рисков оспаривания увольнений.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Законное сокращение без восстановления\n"
        "✓ Экономия на выходных пособиях\n"
        "✓ Защита от массовых исков\n"
        "✓ Полное документальное сопровождение\n"
        "✓ Консультации по сложным случаям"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_migration_law")
async def service_migration_law_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🌍 Миграционное право</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Оформление разрешительных документов для иностранных работников: патенты, разрешения "
        "на работу, РВП, ВНЖ. Уведомление МВД о приёме и увольнении, сопровождение проверок, "
        "обжалование штрафов.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Знаем все требования миграционного законодательства\n"
        "✓ Быстрое оформление документов\n"
        "✓ Защита от штрафов до 1 млн ₽\n"
        "✓ Сопровождение «под ключ»\n"
        "✓ Работа с ВКС и обычными мигрантами"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# ============================================
# ДОГОВОРНОЕ ПРАВО
# ============================================

@router.callback_query(F.data == "service_contract_development")
async def service_contract_development_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📝 Разработка и экспертиза договоров</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Подготовка договоров «под ключ»: поставка, подряд, услуги, аренда, купля-продажа. "
        "Правовая экспертиза договоров контрагентов, выявление рисков, подготовка протоколов "
        "разногласий, согласование условий.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Индивидуальный подход к каждому договору\n"
        "✓ Защита ваших интересов в спорах\n"
        "✓ Быстрая подготовка (от 1 дня)\n"
        "✓ Глубокий анализ рисков\n"
        "✓ Практические рекомендации"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_risk_elimination")
async def service_risk_elimination_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🛡️ Устранение правовых рисков в договорной работе</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Анализ договорной практики компании, выявление правовых рисков, разработка мер "
        "по их устранению. Подготовка шаблонов договоров, регламентов, инструкций для "
        "сотрудников.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Комплексный аудит договорной работы\n"
        "✓ Выявление скрытых рисков\n"
        "✓ Практические рекомендации\n"
        "✓ Обучение сотрудников\n"
        "✓ Снижение судебных споров"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_gray_scheme_legalization")
async def service_gray_scheme_legalization_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>✅ Легализация «серых» схем</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Правовая оптимизация схем ведения бизнеса, легализация неформальных отношений. "
        "Разработка корректных правовых конструкций, внедрение документооборота, "
        "минимизация налоговых и правовых рисков.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Законная оптимизация без нарушений\n"
        "✓ Сохранение экономической эффективности\n"
        "✓ Конфиденциальность гарантирована\n"
        "✓ Поэтапное внедрение\n"
        "✓ Сопровождение на всех этапах"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_real_estate_transactions")
async def service_real_estate_transactions_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🏢 Сопровождение сделок с недвижимостью</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Полное юридическое сопровождение сделок купли-продажи, аренды, залога недвижимости "
        "и активов. Проверка юридической чистоты объектов, подготовка договоров, регистрация "
        "перехода прав, закрытие сделки.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Проверка всех рисков объекта\n"
        "✓ Сопровождение сделок от 10 млн ₽\n"
        "✓ Опыт работы с крупными портфелями\n"
        "✓ Полная ответственность за результат\n"
        "✓ Быстрое закрытие сделок"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# ============================================
# ИНТЕЛЛЕКТУАЛЬНАЯ СОБСТВЕННОСТЬ И IT
# ============================================

@router.callback_query(F.data == "service_tm_patent_registration")
async def service_tm_patent_registration_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>®️ Регистрация товарных знаков и патентов</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Регистрация товарных знаков, патентов на изобретения, полезные модели, "
        "программное обеспечение. Проверка обозначений, подача заявок в Роспатент, "
        "ведение дел до регистрации, продление сроков действия.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ 95% зарегистрированных товарных знаков\n"
        "✓ Патентные поверенные в штате\n"
        "✓ Международная регистрация\n"
        "✓ Защита от отказа в регистрации\n"
        "✓ Полное сопровождение процесса"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_ip_rights_protection")
async def service_ip_rights_protection_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>⚖️ Защита авторских и смежных прав</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Защита прав на произведения науки, литературы, искусства, программы для ЭВМ. "
        "Претензионная работа, взыскание компенсаций, блокировка контрафакта, "
        "представительство в Суде по интеллектуальным правам.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт взыскания компенсаций до 5 млн ₽\n"
        "✓ Блокировка сайтов с контрафактом\n"
        "✓ Работа с крупными платформами\n"
        "✓ Досудебное урегулирование\n"
        "✓ Полное ведение дела"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_it_contracts")
async def service_it_contracts_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>💻 Договоры в сфере IT</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Подготовка и экспертиза договоров в сфере информационных технологий: "
        "разработка ПО, лицензионные соглашения, SLA, аутсорсинг, облачные сервисы. "
        "Учёт специфики IT-бизнеса, защита интеллектуальных прав.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Глубокое понимание IT-бизнеса\n"
        "✓ Защита прав на код и алгоритмы\n"
        "✓ Опыт работы с зарубежными заказчиками\n"
        "✓ Соответствие GDPR и 152-ФЗ\n"
        "✓ Гибкие условия сотрудничества"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_digital_project_accompaniment")
async def service_digital_project_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🚀 Правовое сопровождение digital-проектов</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Комплексное правовое сопровождение digital-проектов: от идеи до запуска. "
        "Регистрация доменов, защита контента, договоры с подрядчиками и клиентами, "
        "соответствие требованиям законодательства о персональных данных.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт сопровождения стартапов\n"
        "✓ Понимание digital-бизнеса\n"
        "✓ Быстрое реагирование на изменения\n"
        "✓ Гибкое ценообразование\n"
        "✓ Полная правовая поддержка"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# ============================================
# АДМИНИСТРАТИВНОЕ ПРАВО
# ============================================

@router.callback_query(F.data == "service_authority_inspection_accompaniment")
async def service_authority_inspection_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🛡️ Сопровождение проверок контролирующих органов</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Подготовка и сопровождение проверок МЧС, Роспотребнадзора, Роскомнадзора, "
        "Росприроднадзора и других органов. Минимизация рисков, подготовка возражений, "
        "обжалование предписаний и постановлений.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Знаем критерии риска всех органов\n"
        "✓ Снижение штрафов в 2-5 раз\n"
        "✓ Оперативный выезд при проверке\n"
        "✓ Полное документальное сопровождение\n"
        "✓ Защита от приостановки деятельности"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_administrative_offenses_appeal")
async def service_administrative_offenses_appeal_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>⚖️ Обжалование протоколов об административных правонарушениях</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Подготовка жалоб на протоколы и постановления по делам об административных "
        "правонарушениях. Представительство в судах и госорганах, прекращение дел, "
        "снижение размеров штрафов.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ 70% дел прекращено или переквалифицировано\n"
        "✓ Опыт работы со всеми составами\n"
        "✓ Быстрое реагирование\n"
        "✓ Полное ведение дела\n"
        "✓ Прозрачное ценообразование"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_administrative_suspension_defense")
async def service_administrative_suspension_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🚫 Защита от приостановки деятельности</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Защита в делах об административных приостановках деятельности предприятия. "
        "Срочное обжалование постановлений, подготовка ходатайств о замене вида наказания, "
        "представительство в судах.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Срочное реагирование (24/7)\n"
        "✓ Опыт отмены приостановок\n"
        "✓ Замена на штраф в 80% случаев\n"
        "✓ Полное сопровождение процесса\n"
        "✓ Защита бизнеса от убытков"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# ============================================
# НЕДВИЖИМОСТЬ И СТРОИТЕЛЬСТВО
# ============================================

@router.callback_query(F.data == "service_real_estate_audit")
async def service_real_estate_audit_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🔍 Юридический аудит недвижимости</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Комплексная проверка юридической чистоты объектов недвижимости: земельные участки, "
        "здания, помещения. Анализ правоустанавливающих документов, обременений, прав третьих "
        "лиц, подготовка заключения о рисках.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Выявление всех скрытых рисков\n"
        "✓ Опыт аудита крупных портфелей\n"
        "✓ Быстрая подготовка заключения\n"
        "✓ Практические рекомендации\n"
        "✓ Полная ответственность за результат"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_commercial_real_estate_transactions")
async def service_commercial_real_estate_transactions_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🏢 Сделки с коммерческой недвижимостью</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Полное сопровождение сделок купли-продажи, аренды коммерческой недвижимости: "
        "офисы, склады, торговые центры. Проверка объектов, подготовка договоров, "
        "регистрация перехода прав, закрытие сделки.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Сопровождение сделок от 50 млн ₽\n"
        "✓ Опыт работы с портфелями недвижимости\n"
        "✓ Полная проверка объектов\n"
        "✓ Быстрое закрытие сделок\n"
        "✓ Защита интересов клиента"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_construction_accompaniment")
async def service_construction_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🏗️ Сопровождение строительных проектов</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Правовое сопровождение строительства: получение разрешительной документации, "
        "согласование проектной документации, сопровождение подрядных договоров, "
        "разрешение споров с подрядчиками и заказчиками.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт сопровождения крупных проектов\n"
        "✓ Знаем все требования градостроительства\n"
        "✓ Быстрое получение разрешений\n"
        "✓ Защита от претензий подрядчиков\n"
        "✓ Полное ведение проекта"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_land_law")
async def service_land_law_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🌱 Земельное право</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Оформление прав на земельные участки, перевод земель из одной категории в другую, "
        "установление разрешённого использования, межевание, постановка на кадастровый учёт. "
        "Защита в земельных спорах.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт работы с Росреестром\n"
        "✓ Быстрое оформление документов\n"
        "✓ Решение сложных земельных вопросов\n"
        "✓ Защита от изъятия участков\n"
        "✓ Полное сопровождение процесса"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# ============================================
# МЕЖДУНАРОДНОЕ ПРАВО И ВЭД
# ============================================

@router.callback_query(F.data == "service_international_structuring")
async def service_international_structuring_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🌐 Структурирование международных сделок</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Разработка правовых схем международной торговли и инвестиций. Оптимизация налоговой "
        "нагрузки, защита активов за рубежом, выбор юрисдикции, подготовка договорной "
        "документации, соблюдение валютного законодательства.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт работы с 20+ юрисдикциями\n"
        "✓ Законная налоговая оптимизация\n"
        "✓ Защита от блокировок счетов\n"
        "✓ Конфиденциальность гарантирована\n"
        "✓ Полное сопровождение сделки"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_foreign_company_accompaniment")
async def service_foreign_company_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🏢 Создание и сопровождение зарубежных компаний</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Регистрация иностранных юридических лиц в оптимальных юрисдикциях. Открытие счетов, "
        "получение лицензий, соблюдение требований местного законодательства, бухгалтерское "
        "сопровождение, подготовка отчётности.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Партнёры в 30+ странах\n"
        "✓ Быстрая регистрация (от 3 дней)\n"
        "✓ Открытие счетов в надёжных банках\n"
        "✓ Полное администрирование\n"
        "✓ Конфиденциальность бенефициаров"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_foreign_trade_accompaniment")
async def service_foreign_trade_accompaniment_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📦 Сопровождение внешнеэкономической деятельности</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Правовое сопровождение ВЭД: подготовка контрактов, соблюдение таможенных требований, "
        "валютный контроль, сертификация товаров, защита при проверках. Работа с экспортёрами "
        "и импортёрами.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт сопровождения ВЭД контрактов на $100+ млн\n"
        "✓ Знаем требования всех таможенных органов\n"
        "✓ Быстрое решение проблем на таможне\n"
        "✓ Защита от штрафов и блокировок\n"
        "✓ Полное ведение ВЭД"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# ============================================
# АНТИМОНОПОЛЬНОЕ ПРАВО (ФАС)
# ============================================

@router.callback_query(F.data == "service_transaction_approval_fas")
async def service_transaction_approval_fas_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📋 Согласование сделок с ФАС</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Подготовка документов для согласования сделок, требующих антимонопольного "
        "согласования. Подача ходатайств в ФАС, получение предварительного и окончательного "
        "согласия, обжалование отказов.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт согласования крупных сделок\n"
        "✓ Быстрое получение согласия\n"
        "✓ Защита от штрафов до 500 000 ₽\n"
        "✓ Полное ведение процесса\n"
        "✓ Конфиденциальность гарантирована"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_advertising_law_defense")
async def service_advertising_law_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📺 Защита при проверках рекламы</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Сопровождение проверок соблюдения закона о рекламе. Подготовка заключений "
        "о соответствии рекламы требованиям, защита от предписаний ФАС, обжалование "
        "постановлений о штрафах.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт защиты крупных рекламодателей\n"
        "✓ Снижение штрафов в 2-3 раза\n"
        "✓ Быстрое решение вопросов с ФАС\n"
        "✓ Полное сопровождение проверки\n"
        "✓ Превентивный аудит рекламы"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_anti_competition_defense")
async def service_anti_competition_defense_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>⚖️ Защита от недобросовестной конкуренции</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Защита в делах о картелях, сговорах, недобросовестной конкуренции. Подготовка "
        "возражений на обвинения, представительство в ФАС и судах, оспаривание решений, "
        "снижение штрафов.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт защиты в картельных делах\n"
        "✓ Снижение штрафов до 90%\n"
        "✓ Защита репутации бизнеса\n"
        "✓ Полное ведение дела\n"
        "✓ Конфиденциальность гарантирована"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

# ============================================
# СЕМЕЙНЫЙ БИЗНЕС И НАСЛЕДСТВЕННОЕ ПЛАНИРОВАНИЕ
# ============================================

@router.callback_query(F.data == "service_asset_structuring")
async def service_asset_structuring_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>🏦 Структурирование активов</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Разработка схем защиты активов при наследовании, разводе, банкротстве. Создание "
        "трастов, фондов, холдинговых структур. Брачные договоры, соглашения о разделе "
        "имущества, завещания.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Защита активов от кредиторов\n"
        "✓ Сохранение семейного бизнеса\n"
        "✓ Законная оптимизация налогов\n"
        "✓ Конфиденциальность гарантирована\n"
        "✓ Индивидуальный подход"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_trust_fund_creation")
async def service_trust_fund_creation_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>📜 Создание наследственных фондов</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Подготовка документов для создания наследственных фондов в РФ и за рубежом. "
        "Разработка условий управления активами, защита интересов бенефициаров, "
        "налоговое планирование, сопровождение деятельности фонда.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Опыт создания фондов в РФ и офшорах\n"
        "✓ Защита активов наследодателя\n"
        "✓ Контроль за исполнением воли\n"
        "✓ Налоговая оптимизация\n"
        "✓ Полное сопровождение фонда"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "service_business_division")
async def service_business_division_handler(callback_query: CallbackQuery) -> None:
    text = (
        "<b>💔 Раздел бизнеса при разводе</b>\n\n"
        "<b>Описание услуги:</b>\n"
        "Подготовка соглашений о разделе имущества супругов в отношении бизнеса. "
        "Оценка долей, разработка схем раздела, защита интересов в суде, сохранение "
        "бизнеса как действующего предприятия.\n\n"
        "<b>Наши преимущества:</b>\n"
        "✓ Сохранение контроля над бизнесом\n"
        "✓ Справедливая оценка долей\n"
        "✓ Минимизация потерь для бизнеса\n"
        "✓ Досудебное урегулирование\n"
        "✓ Полное ведение дела"
    )
    from bot.keyboards.keyboards import get_back_keyboard
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()


def register_service_detail_handlers(dp):
    """Регистрация обработчиков"""
    dp.include_router(router)
