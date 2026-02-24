from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    registered_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationship to partner profile
    partner_profile = relationship("PartnerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    service_requests = relationship("ServiceRequest", back_populates="user", cascade="all, delete-orphan")
    case_questionnaires = relationship("CaseQuestionnaire", back_populates="user", cascade="all, delete-orphan")

class PartnerProfile(Base):
    __tablename__ = "partner_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    full_name = Column(String(255))
    company_name = Column(String(255))
    phone = Column(String(50))
    email = Column(String(255))
    specialization = Column(Text)
    experience = Column(Integer)  # years
    consent_to_share_data = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="partner_profile")

class ServiceRequest(Base):
    __tablename__ = "service_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(Text)
    status = Column(String(50), default="новый")  # 'новый', 'в работе', 'выполнен'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="service_requests")
    documents = relationship("RequestDocument", back_populates="request", cascade="all, delete-orphan")

class RequestDocument(Base):
    __tablename__ = "request_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("service_requests.id"))
    file_path = Column(String(500))
    file_type = Column(String(50))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    request = relationship("ServiceRequest", back_populates="documents")

class DocumentCategory(Base):
    __tablename__ = "document_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("document_categories.id"))
    title = Column(String(255))
    file_path = Column(String(500))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    category = relationship("DocumentCategory")

class FAQ(Base):
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    category = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class ReferralLink(Base):
    __tablename__ = "referral_links"
    
    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, ForeignKey("users.id"))  # Пользователь, который создал реферальную ссылку
    referral_code = Column(String(255), unique=True, index=True)  # Уникальный код реферала
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    partner = relationship("User")

class ReferralRelationship(Base):
    __tablename__ = "referral_relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))  # ID партнёра, который пригласил
    referred_id = Column(Integer, ForeignKey("users.id"))  # ID партнёра, который был приглашён
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    referrer = relationship("User", foreign_keys=[referrer_id])
    referred = relationship("User", foreign_keys=[referred_id])

class ReferralMonthlyStats(Base):
    __tablename__ = "referral_monthly_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))  # ID партнёра, который пригласил
    month = Column(Integer)  # Месяц (1-12)
    year = Column(Integer)  # Год
    total_revenue = Column(Integer)  # Общая выручка от рефералов в рублях
    commission_percent = Column(Float)  # Процент комиссии
    commission_amount = Column(Integer)  # Сумма комиссии в рублях
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    referrer = relationship("User")


class PartnerRevenue(Base):
    """Выручка партнёра от сделок с клиентами"""
    __tablename__ = "partner_revenues"
    
    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, ForeignKey("users.id"))  # ID партнёра
    amount = Column(Integer)  # Сумма сделки в рублях
    description = Column(Text)  # Описание сделки
    client_reference = Column(String(255))  # ID клиента или ссылка на сделку
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    partner = relationship("User")


class ReferralPayout(Base):
    """История выплат реферерам"""
    __tablename__ = "referral_payouts"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))  # ID партнёра-реферера
    amount = Column(Integer)  # Сумма выплаты в рублях
    month = Column(Integer)  # Месяц (1-12)
    year = Column(Integer)  # Год
    status = Column(String(50), default="pending")  # pending, paid, cancelled
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    referrer = relationship("User")


class CaseQuestionnaire(Base):
    """Анкета дела для отправки на оценку"""
    __tablename__ = "case_questionnaires"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Этап 1: Стороны конфликта
    parties_info = Column(Text)
    
    # Этап 2: Предмет спора
    dispute_subject = Column(Text)
    
    # Этап 3: Основания требований
    legal_basis = Column(Text)
    
    # Этап 4: Хронология событий
    chronology = Column(Text)
    
    # Этап 5: Имеющиеся доказательства
    evidence = Column(Text)
    
    # Этап 6: Процессуальная история
    procedural_history = Column(Text)
    
    # Этап 7: Цель клиента
    client_goal = Column(Text)
    
    # Метаданные
    status = Column(String(50), default="отправлено")  # отправлено, в работе, завершено
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="case_questionnaires")
    documents = relationship("CaseQuestionnaireDocument", back_populates="questionnaire", cascade="all, delete-orphan")


class CaseQuestionnaireDocument(Base):
    """Документы к анкете дела"""
    __tablename__ = "case_questionnaire_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    questionnaire_id = Column(Integer, ForeignKey("case_questionnaires.id"))
    section = Column(String(50))  # parties, dispute, legal_basis, chronology, evidence, procedural, goal
    file_path = Column(String(500))
    file_type = Column(String(50))
    original_name = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    questionnaire = relationship("CaseQuestionnaire", back_populates="documents")


class CaseMessage(Base):
    """Сообщения переписки по делу между админом и клиентом"""
    __tablename__ = "case_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    questionnaire_id = Column(Integer, ForeignKey("case_questionnaires.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    sender_type = Column(String(20))  # 'admin' или 'user'
    message_content = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    questionnaire = relationship("CaseQuestionnaire")
    sender = relationship("User")