from aiogram.fsm.state import State, StatesGroup

class ProfileStates(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_company_name = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_specialization = State()
    waiting_for_experience = State()


class SendCaseStates(StatesGroup):
    waiting_for_documents = State()
    waiting_for_description = State()
    waiting_for_company_info = State()  # Новое состояние
    waiting_for_confirmation = State()


class CaseQuestionnaireStates(StatesGroup):
    """Состояния для пошаговой анкеты дела"""
    
    # Этапы 1-7: Только вопросы без документов
    waiting_for_parties = State()
    waiting_for_dispute_subject = State()
    waiting_for_legal_basis = State()
    waiting_for_chronology = State()
    waiting_for_evidence = State()
    waiting_for_procedural_history = State()
    waiting_for_client_goal = State()
    
    # Загрузка документов после всех этапов (упрощённая)
    waiting_for_documents_upload = State()
    waiting_for_simple_documents = State()  # Новое состояние для приёма документов без выбора раздела
    
    # Сводка и подтверждение
    viewing_summary = State()
    editing_section = State()


class RevenueStates(StatesGroup):
    """Состояния для добавления выручки"""
    waiting_for_amount = State()
    waiting_for_description = State()