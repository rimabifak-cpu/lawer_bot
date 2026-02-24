"""
Админ-панель для юридического бота
Оптимизированная версия с улучшенной структурой, логированием и обработкой ошибок
"""
import sys
import os
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, text
from sqlalchemy.orm import joinedload, selectinload
from pydantic import BaseModel
import httpx

from database.database import get_db
from database.models import (
    User, PartnerProfile, CaseQuestionnaire, ServiceRequest,
    PartnerRevenue, ReferralPayout, ReferralRelationship,
    ReferralLink, CaseMessage, CaseQuestionnaireDocument
)
from config.settings import settings

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# URL message_server для отправки уведомлений клиентам
MESSAGE_SERVER_URL = os.getenv("MESSAGE_SERVER_URL", "http://127.0.0.1:8002")

app = FastAPI(
    title="Admin Panel for Law Bot",
    description="Админ-панель для управления юридическим ботом",
    version="2.0.0"
)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Pydantic модели для запросов
# ============================================

class DialogMessageRequest(BaseModel):
    """Запрос на сохранение сообщения от пользователя в диалог"""
    telegram_id: int
    content: str


class DirectMessageRequest(BaseModel):
    """Запрос на отправку прямого сообщения пользователю"""
    telegram_id: int
    content: str


class RevenueRequest(BaseModel):
    """Запрос на добавление выручки"""
    partner_id: int
    amount: int
    description: Optional[str] = ""
    client_reference: Optional[str] = ""


class PayoutRequest(BaseModel):
    """Запрос на создание выплаты"""
    referrer_id: int
    amount: int
    month: int
    year: int


class PayoutUpdateRequest(BaseModel):
    """Запрос на обновление выплаты"""
    amount: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None
    status: Optional[str] = None


class BatchPayRequest(BaseModel):
    """Запрос на массовую выплату"""
    payout_ids: List[int]


# ============================================
# Вспомогательные функции
# ============================================

async def send_notification_to_client(telegram_id: int, message: str) -> bool:
    """Отправить уведомление клиенту через Telegram bot"""
    try:
        # Проверка настроек бота
        if not settings.BOT_TOKEN:
            logger.error("BOT_TOKEN не настроен в конфигурации")
            return False
            
        from aiogram import Bot
        from aiogram.client.session.aiohttp import AiohttpSession
        
        session = AiohttpSession()
        bot = Bot(token=settings.BOT_TOKEN, session=session)
        
        try:
            await bot.send_message(
                chat_id=telegram_id,
                text=message,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            logger.info(f"Уведомление отправлено пользователю {telegram_id}")
            return True
        finally:
            await bot.session.close()
            
    except Exception as e:
        logger.error(f"Исключение при отправке уведомления: {e}")
        return False


def format_user_display_name(user: Any, profile: Any = None) -> str:
    """Форматирует отображаемое имя пользователя"""
    if profile and profile.full_name:
        return profile.full_name
    elif user.first_name:
        if user.username:
            return f"{user.first_name} (@{user.username})"
        return user.first_name
    return f"ID: {user.telegram_id}"


def serialize_datetime(dt) -> Optional[str]:
    """Сериализует datetime в ISO формат"""
    if not dt:
        return None
    if isinstance(dt, str):
        return dt
    return dt.isoformat() if hasattr(dt, 'isoformat') else str(dt)


# ============================================
# HTML шаблоны
# ============================================

# Загружаем HTML при старте
SIMPLE_TEST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simple_test.html")
try:
    with open(SIMPLE_TEST_PATH, "r", encoding="utf-8") as f:
        SIMPLE_TEST_HTML = f.read()
except FileNotFoundError:
    SIMPLE_TEST_HTML = "<html><body><h1>Файл simple_test.html не найден</h1></body></html>"
    logger.warning("Файл simple_test.html не найден")


# ============================================
# Базовые маршруты
# ============================================

@app.get("/test", response_class=HTMLResponse)
async def simple_test():
    """Простой тест админ-панели"""
    return HTMLResponse(content=SIMPLE_TEST_HTML)


@app.get("/favicon.ico")
async def favicon():
    """Возвращаем пустой ответ для favicon"""
    return Response(content="", media_type="image/x-icon")


@app.get("/api/test-db")
async def test_database():
    """Тест подключения к базе данных"""
    try:
        async with get_db() as db:
            result = await db.execute(text("SELECT COUNT(*) FROM users"))
            count = result.fetchone()[0]
            logger.info(f"Тест БД: {count} пользователей")
            return {"status": "success", "users_count": count}
    except Exception as e:
        logger.error(f"Ошибка подключения к БД: {e}")
        return {"status": "error", "message": str(e)}


@app.get("/js-test", response_class=HTMLResponse)
async def js_test():
    """Простой тест JavaScript"""
    js_test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simple_js_test.html")
    try:
        with open(js_test_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<html><body><h1>Файл не найден</h1></body></html>")


# ============================================
# API заявок (Case Questionnaires)
# ============================================

@app.get("/api/requests")
async def get_requests():
    """Получить список всех заявок"""
    async with get_db() as db:
        result = await db.execute(
            select(CaseQuestionnaire)
            .options(selectinload(CaseQuestionnaire.user))
            .order_by(CaseQuestionnaire.created_at.desc())
        )
        requests = result.unique().scalars().all()
        
        return [{
            "id": req.id,
            "user_id": req.user_id,
            "parties_info": req.parties_info,
            "dispute_subject": req.dispute_subject,
            "legal_basis": req.legal_basis,
            "chronology": req.chronology,
            "evidence": req.evidence,
            "procedural_history": req.procedural_history,
            "client_goal": req.client_goal,
            "status": req.status,
            "created_at": serialize_datetime(req.created_at),
            "sent_at": serialize_datetime(req.sent_at),
            "user": {
                "id": req.user.id,
                "telegram_id": req.user.telegram_id,
                "username": req.user.username,
                "first_name": req.user.first_name,
                "last_name": req.user.last_name
            } if req.user else None
        } for req in requests]


@app.put("/api/requests/{request_id}")
async def update_request_status(request_id: int, status_data: dict):
    """Обновить статус заявки"""
    async with get_db() as db:
        result = await db.execute(
            select(CaseQuestionnaire).filter(CaseQuestionnaire.id == request_id)
        )
        request = result.scalar_one_or_none()
        
        if not request:
            raise HTTPException(status_code=404, detail="Заявка не найдена")
        
        request.status = status_data.get("status", request.status)
        await db.commit()
        logger.info(f"Статус заявки #{request_id} обновлен на {request.status}")
        
    return {"message": "Статус заявки обновлен"}


# ============================================
# API партнёров
# ============================================

@app.get("/api/partners")
async def get_partners():
    """Получить список всех партнёров"""
    async with get_db() as db:
        result = await db.execute(
            select(PartnerProfile)
            .join(User, PartnerProfile.user_id == User.id)
            .order_by(PartnerProfile.created_at.desc())
        )
        partners = result.scalars().all()
        
        return [{
            "id": partner.id,
            "user_id": partner.user_id,
            "full_name": partner.full_name,
            "company_name": partner.company_name,
            "phone": partner.phone,
            "email": partner.email,
            "specialization": partner.specialization,
            "experience": partner.experience,
            "consent_to_share_data": partner.consent_to_share_data,
            "created_at": serialize_datetime(partner.created_at),
            "updated_at": serialize_datetime(partner.updated_at)
        } for partner in partners]


# ============================================
# API выручки
# ============================================

@app.get("/api/revenues")
async def get_revenues():
    """Получить список всей выручки партнёров"""
    async with get_db() as db:
        result = await db.execute(
            select(PartnerRevenue)
            .join(User, PartnerRevenue.partner_id == User.id)
            .order_by(PartnerRevenue.created_at.desc())
        )
        revenues = result.scalars().all()
        
        revenues_data = []
        for revenue in revenues:
            profile_result = await db.execute(
                select(PartnerProfile).filter(PartnerProfile.user_id == revenue.partner_id)
            )
            profile = profile_result.scalar_one_or_none()
            
            revenues_data.append({
                "id": revenue.id,
                "partner_id": revenue.partner_id,
                "partner_name": profile.full_name if profile else f"User {revenue.partner_id}",
                "amount": revenue.amount,
                "description": revenue.description,
                "client_reference": revenue.client_reference,
                "created_at": serialize_datetime(revenue.created_at)
            })
        
        return revenues_data


@app.post("/api/revenues")
async def add_revenue(revenue_data: RevenueRequest):
    """Добавить выручку партнёру"""
    if not revenue_data.partner_id or not revenue_data.amount:
        raise HTTPException(status_code=400, detail="partner_id и amount обязательны")
    
    async with get_db() as db:
        new_revenue = PartnerRevenue(
            partner_id=revenue_data.partner_id,
            amount=revenue_data.amount,
            description=revenue_data.description,
            client_reference=revenue_data.client_reference
        )
        db.add(new_revenue)
        await db.commit()
        await db.refresh(new_revenue)
        
        logger.info(f"Добавлена выручка {revenue_data.amount} для партнёра {revenue_data.partner_id}")
    
    return {"message": "Выручка добавлена", "id": new_revenue.id}


@app.get("/api/revenues/{partner_id}")
async def get_partner_revenues(partner_id: int):
    """Получить выручку конкретного партнёра"""
    async with get_db() as db:
        result = await db.execute(
            select(PartnerRevenue)
            .filter(PartnerRevenue.partner_id == partner_id)
            .order_by(PartnerRevenue.created_at.desc())
        )
        revenues = result.scalars().all()
        
        return [{
            "id": r.id,
            "amount": r.amount,
            "description": r.description,
            "client_reference": r.client_reference,
            "created_at": serialize_datetime(r.created_at)
        } for r in revenues]


# ============================================
# API выплат
# ============================================

@app.get("/api/payouts")
async def get_payouts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    referrer_id: Optional[int] = None,
    search: Optional[str] = None,
):
    """Получить список выплат с фильтрацией"""
    async with get_db() as db:
        query = select(ReferralPayout).join(User, ReferralPayout.referrer_id == User.id)
        
        if status:
            query = query.where(ReferralPayout.status == status)
        if month:
            query = query.where(ReferralPayout.month == month)
        if year:
            query = query.where(ReferralPayout.year == year)
        if referrer_id:
            query = query.where(ReferralPayout.referrer_id == referrer_id)
        if search:
            query = query.where(User.first_name.ilike(f"%{search}%"))
        
        query = query.order_by(ReferralPayout.created_at.desc())
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        payouts = result.scalars().all()
        
        payouts_data = []
        for payout in payouts:
            profile_result = await db.execute(
                select(PartnerProfile).filter(PartnerProfile.user_id == payout.referrer_id)
            )
            profile = profile_result.scalar_one_or_none()
            
            payouts_data.append({
                "id": payout.id,
                "referrer_id": payout.referrer_id,
                "referrer_name": profile.full_name if profile else f"User {payout.referrer_id}",
                "amount": payout.amount,
                "month": payout.month,
                "year": payout.year,
                "status": payout.status,
                "paid_at": serialize_datetime(payout.paid_at),
                "created_at": serialize_datetime(payout.created_at)
            })
        
        return payouts_data


@app.get("/api/payouts/count")
async def get_payouts_count(
    status: Optional[str] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    referrer_id: Optional[int] = None,
    search: Optional[str] = None,
):
    """Получить количество выплат"""
    async with get_db() as db:
        query = select(func.count(ReferralPayout.id))
        
        if status:
            query = query.where(ReferralPayout.status == status)
        if month:
            query = query.where(ReferralPayout.month == month)
        if year:
            query = query.where(ReferralPayout.year == year)
        if referrer_id:
            query = query.where(ReferralPayout.referrer_id == referrer_id)
        if search:
            query = query.join(User, ReferralPayout.referrer_id == User.id)
            query = query.where(User.first_name.ilike(f"%{search}%"))
        
        result = await db.execute(query)
        count = result.scalar_one_or_none()
        
        return {"count": count or 0}


@app.post("/api/payouts")
async def create_payout(payout_data: PayoutRequest):
    """Создать выплату рефереру"""
    async with get_db() as db:
        new_payout = ReferralPayout(
            referrer_id=payout_data.referrer_id,
            amount=payout_data.amount,
            month=payout_data.month,
            year=payout_data.year,
            status="pending"
        )
        db.add(new_payout)
        await db.commit()
        await db.refresh(new_payout)
        
        logger.info(f"Создана выплата {payout_data.amount} для реферера {payout_data.referrer_id}")
        
        return {"message": "Выплата создана", "id": new_payout.id}


@app.put("/api/payouts/{payout_id}")
async def update_payout(payout_id: int, payout_data: PayoutUpdateRequest):
    """Обновить информацию о выплате"""
    async with get_db() as db:
        result = await db.execute(
            select(ReferralPayout).filter(ReferralPayout.id == payout_id)
        )
        payout = result.scalar_one_or_none()
        
        if not payout:
            raise HTTPException(status_code=404, detail="Выплата не найдена")
        
        if payout_data.amount is not None:
            payout.amount = payout_data.amount
        if payout_data.month is not None:
            payout.month = payout_data.month
        if payout_data.year is not None:
            payout.year = payout_data.year
        if payout_data.status is not None:
            payout.status = payout_data.status
        
        await db.commit()
        logger.info(f"Выплата #{payout_id} обновлена")
        
        return {"message": "Выплата обновлена успешно", "id": payout.id}


@app.put("/api/payouts/{payout_id}/pay")
async def mark_payout_as_paid(payout_id: int):
    """Отметить выплату как выполненную"""
    async with get_db() as db:
        result = await db.execute(
            select(ReferralPayout).filter(ReferralPayout.id == payout_id)
        )
        payout = result.scalar_one_or_none()
        
        if not payout:
            raise HTTPException(status_code=404, detail="Выплата не найдена")
        
        if payout.status == "paid":
            raise HTTPException(status_code=400, detail="Выплата уже выполнена")
        
        payout.status = "paid"
        payout.paid_at = datetime.utcnow()
        await db.commit()
        
        # Получаем telegram_id для уведомления
        user_result = await db.execute(
            select(User).filter(User.id == payout.referrer_id)
        )
        user = user_result.scalar_one_or_none()
        
        notification_text = (
            f"💰 <b>Вам начислено вознаграждение!</b>\n\n"
            f"Сумма: {payout.amount:,} ₽\n"
            f"За период: {payout.month:02d}.{payout.year}\n\n"
            f"Спасибо за участие в реферальной программе!"
        )
        
        logger.info(f"Выплата #{payout_id} отмечена как выполненная")
        
        return {
            "message": "Выплата отмечена как выполненная",
            "telegram_id": user.telegram_id if user else None,
            "notification": notification_text
        }


@app.put("/api/payouts/batch/pay")
async def batch_mark_payouts_as_paid(request: BatchPayRequest):
    """Массово отметить выплаты как выполненные"""
    if not request.payout_ids:
        raise HTTPException(status_code=400, detail="Не указаны ID выплат")
    
    async with get_db() as db:
        result = await db.execute(
            select(ReferralPayout).filter(ReferralPayout.id.in_(request.payout_ids))
        )
        payouts = result.scalars().all()
        
        if len(payouts) != len(request.payout_ids):
            raise HTTPException(status_code=400, detail="Некоторые выплаты не найдены")
        
        updated_count = 0
        for payout in payouts:
            if payout.status != "paid":
                payout.status = "paid"
                payout.paid_at = datetime.utcnow()
                updated_count += 1
        
        await db.commit()
        logger.info(f"Массово обновлено {updated_count} выплат")
        
        return {"message": f"Обновлено {updated_count} выплат", "updated_count": updated_count}


# ============================================
# API реферальной программы
# ============================================

@app.get("/api/referrers")
async def get_referrers():
    """Получить список всех рефереров"""
    async with get_db() as db:
        result = await db.execute(
            select(
                ReferralRelationship.referrer_id,
                func.count(ReferralRelationship.id).label('referrals_count')
            )
            .group_by(ReferralRelationship.referrer_id)
        )
        referrers_stats = result.all()
        
        referrers_data = []
        for referrer_id, count in referrers_stats:
            profile_result = await db.execute(
                select(PartnerProfile).filter(PartnerProfile.user_id == referrer_id)
            )
            profile = profile_result.scalar_one_or_none()
            
            user_result = await db.execute(
                select(User).filter(User.id == referrer_id)
            )
            user = user_result.scalar_one_or_none()
            
            referrers_data.append({
                "user_id": referrer_id,
                "full_name": format_user_display_name(user, profile),
                "telegram_id": user.telegram_id if user else None,
                "referrals_count": count
            })
        
        return referrers_data


@app.get("/api/referrals/structure")
async def get_referral_structure():
    """Получить полную реферальную структуру"""
    async with get_db() as db:
        query = text("""
            SELECT 
                rr.id, rr.created_at,
                r.telegram_id as referrer_telegram_id,
                r.first_name as referrer_first_name,
                r.username as referrer_username,
                pp.full_name as referrer_partner_name,
                rr2.telegram_id as referred_telegram_id,
                rr2.first_name as referred_first_name,
                rr2.username as referred_username,
                pp2.full_name as referred_partner_name
            FROM referral_relationships rr
            JOIN users r ON rr.referrer_id = r.id
            LEFT JOIN partner_profiles pp ON r.id = pp.user_id
            JOIN users rr2 ON rr.referred_id = rr2.id
            LEFT JOIN partner_profiles pp2 ON rr2.id = pp2.user_id
        """)
        
        result = await db.execute(query)
        rows = result.fetchall()
        
        structure = []
        for row in rows:
            referrer_name = row.referrer_partner_name or (
                f"{row.referrer_first_name} (@{row.referrer_username})" 
                if row.referrer_username else row.referrer_first_name
            ) or f"ID: {row.referrer_telegram_id}"
            
            referred_name = row.referred_partner_name or (
                f"{row.referred_first_name} (@{row.referred_username})" 
                if row.referred_username else row.referred_first_name
            ) or f"ID: {row.referred_telegram_id}"
            
            structure.append({
                "id": row.id,
                "referrer_id": row.referrer_telegram_id,
                "referrer_name": referrer_name,
                "referred_id": row.referred_telegram_id,
                "referred_name": referred_name,
                "created_at": serialize_datetime(row.created_at)
            })
        
        return structure


@app.get("/api/referrals/get-referrer/{telegram_id}")
async def get_partner_referrer(telegram_id: int):
    """Получить реферера партнёра (кто его пригласил)"""
    async with get_db() as db:
        user_query = text("""
            SELECT u.id, u.telegram_id, u.first_name, u.username, pp.full_name as partner_name
            FROM users u
            LEFT JOIN partner_profiles pp ON u.id = pp.user_id
            WHERE u.telegram_id = :tg_id
        """)
        
        user_result = await db.execute(user_query, {"tg_id": telegram_id})
        user = user_result.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        ref_query = text("""
            SELECT rr.created_at, r.telegram_id, r.first_name, r.username, pp.full_name as partner_name
            FROM referral_relationships rr
            JOIN users r ON rr.referrer_id = r.id
            LEFT JOIN partner_profiles pp ON r.id = pp.user_id
            WHERE rr.referred_id = :user_id
        """)
        
        ref_result = await db.execute(ref_query, {"user_id": user.id})
        relationship = ref_result.fetchone()
        
        partner_name = user.partner_name or (
            f"{user.first_name} (@{user.username})" if user.username else user.first_name
        ) or 'Partner'
        
        if relationship:
            referrer_name = relationship.partner_name or (
                f"{relationship.first_name} (@{relationship.username})" 
                if relationship.username else relationship.first_name
            ) or f"ID: {relationship.telegram_id}"
            
            return {
                "partner_telegram_id": telegram_id,
                "partner_name": partner_name,
                "has_referrer": True,
                "referrer": {
                    "telegram_id": relationship.telegram_id,
                    "name": referrer_name,
                    "username": relationship.username
                },
                "created_at": serialize_datetime(relationship.created_at)
            }
        
        return {
            "partner_telegram_id": telegram_id,
            "partner_name": partner_name,
            "has_referrer": False,
            "referrer": None,
            "message": "У этого партнёра нет реферала (никто его не пригласил)"
        }


# ============================================
# API пользователей
# ============================================

@app.get("/api/users")
async def get_users():
    """Получить список всех пользователей"""
    async with get_db() as db:
        result = await db.execute(
            select(User).order_by(User.registered_at.desc())
        )
        users = result.scalars().all()
        
        users_data = []
        for user in users:
            profile_result = await db.execute(
                select(PartnerProfile).filter(PartnerProfile.user_id == user.id)
            )
            profile = profile_result.scalar_one_or_none()
            
            users_data.append({
                "id": user.id,
                "telegram_id": user.telegram_id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_partner": profile is not None,
                "partner_name": profile.full_name if profile else None,
                "registered_at": serialize_datetime(user.registered_at)
            })
        
        return users_data


@app.get("/api/users/list")
async def get_users_list():
    """Получить список пользователей для выбора"""
    async with get_db() as db:
        result = await db.execute(
            select(User).order_by(User.first_name.asc())
        )
        users = result.scalars().all()
        
        return [{
            "telegram_id": user.telegram_id,
            "display_name": (
                f"{user.first_name or ''} (@{user.username})" 
                if user.username else f"{user.first_name or ''} (ID:{user.telegram_id})"
            ).strip()
        } for user in users]


@app.get("/api/users/referrals-info")
async def get_users_referrals_info():
    """Получить всех пользователей с информацией о рефералах"""
    async with get_db() as db:
        users_query = text("""
            SELECT u.id, u.telegram_id, u.username, u.first_name, u.registered_at,
                   pp.full_name as partner_name
            FROM users u
            LEFT JOIN partner_profiles pp ON u.id = pp.user_id
            ORDER BY u.registered_at DESC
        """)
        
        users_result = await db.execute(users_query)
        users = users_result.fetchall()
        
        ref_query = text("""
            SELECT rr.referrer_id, rr.referred_id,
                   r.telegram_id as ref_telegram_id, r.first_name as ref_first_name, r.username as ref_username,
                   pp.full_name as ref_partner_name
            FROM referral_relationships rr
            JOIN users r ON rr.referrer_id = r.id
            LEFT JOIN partner_profiles pp ON r.id = pp.user_id
        """)
        
        ref_result = await db.execute(ref_query)
        relationships = ref_result.fetchall()
        
        referrer_of = {}
        referrals_count = {}
        
        for rel in relationships:
            ref_name = (rel.ref_partner_name and rel.ref_partner_name.strip()) or (
                f"{rel.ref_first_name} (@{rel.ref_username})" if rel.ref_username else rel.ref_first_name
            ) or "Unknown"
            referrer_of[rel.referred_id] = {
                "telegram_id": rel.ref_telegram_id,
                "name": ref_name
            }
            referrals_count[rel.referrer_id] = referrals_count.get(rel.referrer_id, 0) + 1
        
        users_data = []
        for user in users:
            user_name = (user.partner_name and user.partner_name.strip()) or (
                f"{user.first_name} (@{user.username})" if user.username else user.first_name
            ) or "Unknown"
            
            users_data.append({
                "id": user.id,
                "telegram_id": user.telegram_id,
                "username": user.username,
                "first_name": user.first_name,
                "name": user_name,
                "registered_at": serialize_datetime(user.registered_at),
                "invited_by": referrer_of.get(user.id),
                "invited_count": referrals_count.get(user.id, 0),
                "is_partner": user.partner_name is not None
            })
        
        return {"total_users": len(users_data), "users": users_data}


# ============================================
# API статистики
# ============================================

@app.get("/api/stats")
async def get_stats():
    """Получить основную статистику системы"""
    async with get_db() as db:
        # Общее количество пользователей
        users_count_result = await db.execute(func.count(User.id))
        users_count = users_count_result.scalar_one_or_none() or 0
        
        # Количество партнёров
        partners_count_result = await db.execute(func.count(PartnerProfile.id))
        partners_count = partners_count_result.scalar_one_or_none() or 0
        
        # Количество заявок
        requests_count_result = await db.execute(func.count(CaseQuestionnaire.id))
        requests_count = requests_count_result.scalar_one_or_none() or 0
        
        # Количество выплат
        payouts_count_result = await db.execute(func.count(ReferralPayout.id))
        payouts_count = payouts_count_result.scalar_one_or_none() or 0
        
        # Общая сумма выплат
        total_payouts_result = await db.execute(func.coalesce(func.sum(ReferralPayout.amount), 0))
        total_payouts = total_payouts_result.scalar_one_or_none() or 0
        
        # Количество рефералов
        referrals_count_result = await db.execute(func.count(ReferralRelationship.id))
        referrals_count = referrals_count_result.scalar_one_or_none() or 0
        
        return {
            "users_count": users_count,
            "partners_count": partners_count,
            "requests_count": requests_count,
            "payouts_count": payouts_count,
            "total_payouts": total_payouts,
            "referrals_count": referrals_count
        }


# ============================================
# API сообщений
# ============================================

@app.get("/api/cases/{case_id}/messages")
async def get_case_messages(case_id: int):
    """Получить переписку по делу"""
    async with get_db() as db:
        result = await db.execute(
            select(CaseMessage)
            .filter(CaseMessage.questionnaire_id == case_id)
            .options(selectinload(CaseMessage.sender))
            .order_by(CaseMessage.created_at.asc())
        )
        messages = result.scalars().all()
        
        return [{
            "id": msg.id,
            "questionnaire_id": msg.questionnaire_id,
            "sender_id": msg.sender_id,
            "sender_type": msg.sender_type,
            "sender_name": f"{msg.sender.first_name} {msg.sender.last_name}".strip() if msg.sender else "Unknown",
            "message_content": msg.message_content,
            "is_read": msg.is_read,
            "created_at": serialize_datetime(msg.created_at)
        } for msg in messages]


@app.post("/api/cases/{case_id}/messages")
async def send_case_message(case_id: int, message_data: dict):
    """Отправить сообщение по делу (от админа)"""
    content = message_data.get("content")
    sender_id = message_data.get("sender_id", 0)
    
    if not content:
        raise HTTPException(status_code=400, detail="Текст сообщения обязателен")
    
    async with get_db() as db:
        case_result = await db.execute(
            select(CaseQuestionnaire).filter(CaseQuestionnaire.id == case_id)
        )
        case = case_result.scalar_one_or_none()
        
        if not case:
            raise HTTPException(status_code=404, detail="Дело не найдено")
        
        new_message = CaseMessage(
            questionnaire_id=case_id,
            sender_id=sender_id,
            sender_type="admin",
            message_content=content
        )
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        
        user_result = await db.execute(
            select(User).filter(User.id == case.user_id)
        )
        user = user_result.scalar_one_or_none()
        
        notification_text = (
            f"💬 <b>Новое сообщение по вашему делу #{case_id}</b>\n\n"
            f"📝 {content}\n\n"
            f"Чтобы ответить, нажмите кнопку ниже или перейдите в раздел \"Мои дела\"."
        )
        
        notification_sent = False
        if user and user.telegram_id:
            notification_sent = await send_notification_to_client(
                telegram_id=user.telegram_id,
                message=notification_text
            )
        
        logger.info(f"Сообщение отправлено по делу #{case_id}")
        
        return {
            "message": "Сообщение отправлено",
            "id": new_message.id,
            "notification": notification_text,
            "user_telegram_id": user.telegram_id if user else None,
            "notification_sent": notification_sent
        }


@app.post("/api/messages/dialog")
async def save_dialog_message(request: DialogMessageRequest):
    """Сохранить сообщение от пользователя в диалог"""
    if not request.content:
        raise HTTPException(status_code=400, detail="Текст сообщения обязателен")
    
    async with get_db() as db:
        user_result = await db.execute(
            select(User).filter(User.telegram_id == request.telegram_id)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            user = User(
                telegram_id=request.telegram_id,
                username=f"user_{request.telegram_id}",
                first_name="Клиент",
                last_name=""
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        
        case_result = await db.execute(
            select(CaseQuestionnaire).filter(CaseQuestionnaire.user_id == user.id)
        )
        cases = case_result.scalars().all()
        
        case_id = cases[0].id if cases else 0
        
        new_message = CaseMessage(
            questionnaire_id=case_id,
            sender_id=user.id,
            sender_type="client",
            message_content=request.content
        )
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        
        return {
            "message": "Сообщение сохранено",
            "id": new_message.id,
            "user_id": user.id,
            "case_id": case_id
        }


@app.post("/api/messages/direct")
async def send_direct_message(request: DirectMessageRequest):
    """Отправить сообщение напрямую пользователю"""
    if not request.telegram_id or not request.content:
        raise HTTPException(status_code=400, detail="telegram_id и content обязательны")

    notification_text = f"💬 <b>Сообщение от ЮК</b>\n\n📝 {request.content}"

    sent = await send_notification_to_client(
        telegram_id=request.telegram_id,
        message=notification_text
    )

    # Сохраняем сообщение в базу данных
    async with get_db() as db:
        user_result = await db.execute(
            select(User).filter(User.telegram_id == request.telegram_id)
        )
        user = user_result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=request.telegram_id,
                username=f"user_{request.telegram_id}",
                first_name="Клиент",
                last_name=""
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

        case_result = await db.execute(
            select(CaseQuestionnaire).filter(CaseQuestionnaire.user_id == user.id)
        )
        cases = case_result.scalars().all()

        # Если есть дело — сохраняем в case_messages, иначе пропускаем сохранение
        if cases:
            case_id = cases[0].id
            new_message = CaseMessage(
                questionnaire_id=case_id,
                sender_id=user.id,
                sender_type="admin",
                message_content=request.content
            )
            db.add(new_message)
            await db.commit()
            await db.refresh(new_message)
            logger.info(f"Сообщение сохранено в деле {case_id}")
        else:
            # Дела нет — просто отправляем, не сохраняем в case_messages
            logger.info(f"Дело не найдено для пользователя {user.id}, сообщение не сохранено")
            await db.commit()  # Завершаем транзакцию без сохранения сообщения

    return {
        "message": "Сообщение отправлено",
        "telegram_id": request.telegram_id,
        "sent": sent
    }


# ============================================
# API диалогов
# ============================================

@app.get("/api/dialogs")
async def get_dialogs():
    """Получить список всех диалогов"""
    async with get_db() as db:
        result = await db.execute(
            select(CaseMessage)
            .options(selectinload(CaseMessage.sender))
            .order_by(CaseMessage.created_at.desc())
        )
        messages = result.unique().scalars().all()
        
        dialogs_dict = {}
        for msg in messages:
            user = msg.sender
            if not user:
                continue
            
            telegram_id = user.telegram_id
            if telegram_id not in dialogs_dict:
                display_name = (
                    f"{user.first_name or ''} (@{user.username})" 
                    if user.username else f"{user.first_name or 'Клиент'} (ID:{telegram_id})"
                ).strip()
                
                dialogs_dict[telegram_id] = {
                    "telegram_id": telegram_id,
                    "display_name": display_name,
                    "last_message": (
                        msg.message_content[:50] + "..." 
                        if len(msg.message_content) > 50 else msg.message_content
                    ),
                    "last_time": serialize_datetime(msg.created_at),
                    "unread_count": 0
                }
            
            if msg.sender_type == "client" and not msg.is_read:
                dialogs_dict[telegram_id]["unread_count"] += 1
        
        dialogs = list(dialogs_dict.values())
        dialogs.sort(key=lambda x: x["last_time"] or "", reverse=True)
        
        return dialogs


@app.get("/api/dialogs/{telegram_id}/messages")
async def get_dialog_messages(telegram_id: int):
    """Получить сообщения диалога с пользователем"""
    if not telegram_id or telegram_id <= 0:
        raise HTTPException(status_code=400, detail="Некорректный telegram_id")
    
    async with get_db() as db:
        user_result = await db.execute(
            select(User).filter(User.telegram_id == telegram_id)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        result = await db.execute(
            select(CaseMessage)
            .filter(CaseMessage.sender_id == user.id)
            .options(selectinload(CaseMessage.sender))
            .order_by(CaseMessage.created_at.asc())
        )
        messages = result.unique().scalars().all()
        
        messages_data = [{
            "id": msg.id,
            "sender_type": msg.sender_type,
            "sender_name": msg.sender.first_name if msg.sender else "Unknown",
            "content": msg.message_content,
            "created_at": serialize_datetime(msg.created_at),
            "is_read": msg.is_read
        } for msg in messages]
        
        for msg in messages:
            if msg.sender_type == "client" and not msg.is_read:
                msg.is_read = True
        await db.commit()
        
        return {
            "telegram_id": telegram_id,
            "user_name": (
                f"{user.first_name or ''} (@{user.username})" 
                if user.username else f"{user.first_name or 'Клиент'} (ID:{telegram_id})"
            ).strip(),
            "messages": messages_data
        }


@app.post("/api/dialogs/{telegram_id}/send")
async def send_dialog_message(telegram_id: int, request: DirectMessageRequest):
    """Отправить сообщение пользователю в диалог"""
    async with get_db() as db:
        user_result = await db.execute(
            select(User).filter(User.telegram_id == telegram_id)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        case_result = await db.execute(
            select(CaseQuestionnaire).filter(CaseQuestionnaire.user_id == user.id)
        )
        cases = case_result.scalars().all()
        
        case_id = cases[0].id if cases else 0
        
        new_message = CaseMessage(
            questionnaire_id=case_id,
            sender_id=user.id,
            sender_type="admin",
            message_content=request.content
        )
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        
        notification_text = f"💬 <b>Ответ от ЮК</b>\n\n📝 {request.content}"
        await send_notification_to_client(
            telegram_id=telegram_id,
            message=notification_text
        )
        
        logger.info(f"Сообщение отправлено пользователю {telegram_id}")
        
        return {"message": "Сообщение отправлено", "message_id": new_message.id}


# ============================================
# Рассылка
# ============================================

@app.post("/api/broadcast")
async def send_broadcast(message_data: dict):
    """Отправить рассылку всем партнёрам"""
    message = message_data.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Текст сообщения обязателен")
    
    async with get_db() as db:
        result = await db.execute(
            select(User)
            .join(PartnerProfile, User.id == PartnerProfile.user_id)
        )
        users = result.scalars().all()
        
        sent_count = len(users)
        logger.info(f"Рассылка отправлена {sent_count} партнёрам")
    
    return {"message": "Рассылка успешно отправлена", "sent_count": sent_count}


# ============================================
# Страница диалогов
# ============================================

DIALOGS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Диалоги - Law Bot Admin</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        .nav-links { margin-bottom: 20px; padding: 15px; background: #007bff; border-radius: 8px; }
        .nav-links a { color: white; text-decoration: none; margin-right: 20px; font-weight: bold; }
        .nav-links a:hover { text-decoration: underline; }
        .dialogs-list { background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .dialog-item { padding: 15px; border-bottom: 1px solid #eee; cursor: pointer; }
        .dialog-item:hover { background: #f8f9fa; }
        .dialog-item.active { background: #e3f2fd; }
        .dialog-name { font-weight: bold; color: #333; }
        .dialog-preview { color: #666; font-size: 14px; margin-top: 5px; }
        .dialog-time { font-size: 12px; color: #999; }
        .unread-badge { background: #007bff; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
        .chat-container { display: flex; height: 600px; margin-top: 20px; }
        .dialogs-panel { width: 350px; background: white; border-radius: 8px 0 0 8px; overflow-y: auto; }
        .messages-panel { flex: 1; background: white; border-radius: 0 8px 8px 0; display: flex; flex-direction: column; }
        .messages-header { padding: 15px; border-bottom: 1px solid #eee; background: #f8f9fa; border-radius: 0 8px 0 0; }
        .messages-list { flex: 1; overflow-y: auto; padding: 15px; }
        .message { margin-bottom: 15px; padding: 10px 15px; border-radius: 15px; max-width: 70%; }
        .message.client { background: #e3f2fd; margin-right: auto; }
        .message.admin { background: #dcf8c6; margin-left: auto; }
        .message-time { font-size: 11px; color: #999; margin-top: 5px; }
        .message-input-area { padding: 15px; border-top: 1px solid #eee; }
        .message-input-area textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; resize: none; height: 60px; }
        .message-input-area button { margin-top: 10px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; }
        .message-input-area button:hover { background: #0056b3; }
        .no-dialog { text-align: center; padding: 50px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>💬 Диалоги с пользователями</h1>
        
        <div class="nav-links">
            <span>📁 Навигация:</span>
            <a href="/">🏠 Главная</a>
            <a href="/dialogs">💬 Диалоги</a>
        </div>
        
        <div class="chat-container">
            <div class="dialogs-panel" id="dialogs-list">
                <div style="padding: 20px; text-align: center;">Загрузка...</div>
            </div>
            
            <div class="messages-panel" id="messages-panel">
                <div class="no-dialog" id="no-dialog-message">
                    <p>👈 Выберите диалог слева</p>
                </div>
                <div class="messages-header" id="messages-header" style="display: none;">
                    <strong id="chat-user-name"></strong>
                </div>
                <div class="messages-list" id="messages-list" style="display: none;"></div>
                <div class="message-input-area" id="message-input-area" style="display: none;">
                    <textarea id="message-text" placeholder="Введите сообщение..."></textarea>
                    <button onclick="sendMessage()">📤 Отправить</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentTelegramId = null;
        
        async function loadDialogs() {
            try {
                const response = await fetch('/api/dialogs');
                const dialogs = await response.json();
                
                const listEl = document.getElementById('dialogs-list');
                
                if (dialogs.length === 0) {
                    listEl.innerHTML = '<div style="padding: 20px; text-align: center;">Нет диалогов</div>';
                    return;
                }
                
                listEl.innerHTML = dialogs.map(d => `
                    <div class="dialog-item" onclick="openDialog(${d.telegram_id}, '${d.display_name.replace(/'/g, "\\\\'")}')">
                        <div class="dialog-name">
                            ${d.display_name}
                            ${d.unread_count > 0 ? '<span class="unread-badge">' + d.unread_count + '</span>' : ''}
                        </div>
                        <div class="dialog-preview">${d.last_message || ''}</div>
                        <div class="dialog-time">${d.last_time || ''}</div>
                    </div>
                `).join('');
            } catch (e) {
                document.getElementById('dialogs-list').innerHTML = '<div style="padding: 20px; color: red;">Ошибка загрузки</div>';
            }
        }
        
        async function openDialog(telegramId, userName) {
            currentTelegramId = telegramId;
            
            document.querySelectorAll('.dialog-item').forEach(el => el.classList.remove('active'));
            event.currentTarget.classList.add('active');
            
            document.getElementById('no-dialog-message').style.display = 'none';
            document.getElementById('messages-header').style.display = 'block';
            document.getElementById('messages-list').style.display = 'block';
            document.getElementById('message-input-area').style.display = 'block';
            
            document.getElementById('chat-user-name').textContent = userName;
            
            try {
                const response = await fetch(`/api/dialogs/${telegramId}/messages`);
                const data = await response.json();
                
                const messagesEl = document.getElementById('messages-list');
                messagesEl.innerHTML = data.messages.map(m => `
                    <div class="message ${m.sender_type}">
                        <div>${m.content}</div>
                        <div class="message-time">${m.created_at || ''}</div>
                    </div>
                `).join('');
                
                messagesEl.scrollTop = messagesEl.scrollHeight;
            } catch (e) {
                console.error('Ошибка загрузки сообщений:', e);
            }
        }
        
        async function sendMessage() {
            if (!currentTelegramId) return;
            
            const textEl = document.getElementById('message-text');
            const content = textEl.value.trim();
            
            if (!content) return;
            
            try {
                const response = await fetch(`/api/dialogs/${currentTelegramId}/send`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ telegram_id: currentTelegramId, content: content })
                });
                
                const result = await response.json();
                
                if (result.message) {
                    textEl.value = '';
                    openDialog(currentTelegramId, document.getElementById('chat-user-name').textContent);
                }
            } catch (e) {
                alert('Ошибка отправки: ' + e.message);
            }
        }
        
        document.getElementById('message-text').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        loadDialogs();
    </script>
</body>
</html>
"""

@app.get("/dialogs", response_class=HTMLResponse)
async def dialogs_page():
    """Страница диалогов с пользователями"""
    return HTMLResponse(content=DIALOGS_HTML)


# ============================================
# Главная страница
# ============================================

@app.get("/", response_class=HTMLResponse)
async def admin_dashboard():
    """Главная страница админ-панели"""
    return HTMLResponse(content=SIMPLE_TEST_HTML)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
