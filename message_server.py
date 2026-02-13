"""
Сервер для отправки уведомлений клиентам через Telegram
Запускается на порту 8002

Использование:
    python message_server.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import httpx
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from config.settings import settings
from database.database import get_db
from database.models import User, CaseQuestionnaire, CaseMessage

# Создаём FastAPI приложение
app = FastAPI(
    title="Message Server",
    description="Сервер для отправки уведомлений клиентам",
    version="1.0.0"
)

# Разрешаем CORS для админ-панели
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы из admin_panel
ADMIN_PANEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "admin_panel")
app.mount("/static/admin_panel", StaticFiles(directory=ADMIN_PANEL_DIR), name="admin_panel")

# URL Telegram Bot API
TELEGRAM_API_URL = f"https://api.telegram.org/bot{settings.BOT_TOKEN}"


# ============ Pydantic Models ============

class SendMessageRequest(BaseModel):
    """Запрос на отправку сообщения"""
    telegram_id: int
    message: str
    parse_mode: str = "HTML"
    disable_web_page_preview: bool = True


class SendCaseReplyRequest(BaseModel):
    """Запрос на отправку ответа по делу"""
    case_id: int
    admin_message: str
    admin_id: int = 0


class BroadcastRequest(BaseModel):
    """Запрос на рассылку"""
    message: str
    user_ids: list[int] | None = None  # None = всем пользователям


# ============ Helper Functions ============

async def send_telegram_message(
    telegram_id: int,
    message: str,
    parse_mode: str = "HTML",
    disable_web_page_preview: bool = True
) -> dict:
    """Отправить сообщение через Telegram Bot API"""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    
    payload = {
        "chat_id": telegram_id,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": disable_web_page_preview
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload)
        
        if response.status_code != 200:
            error_info = response.json()
            raise Exception(f"Telegram API error: {error_info.get('description', 'Unknown error')}")
        
        return response.json()


async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int) -> User | None:
    """Получить пользователя по Telegram ID"""
    result = await db.execute(
        select(User).filter(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


async def get_case_by_id(db: AsyncSession, case_id: int) -> CaseQuestionnaire | None:
    """Получить дело по ID"""
    result = await db.execute(
        select(CaseQuestionnaire).filter(CaseQuestionnaire.id == case_id)
    )
    return result.scalar_one_or_none()


# ============ API Endpoints ============

@app.get("/health")
async def health_check():
    """Проверка работоспособности сервера"""
    return {
        "status": "healthy",
        "service": "message_server",
        "port": 8002,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/notify")
async def send_notification(request: SendMessageRequest, db: AsyncSession = Depends(get_db)):
    """
    Отправить уведомление клиенту
    
    Пример использования:
    ```json
    {
        "telegram_id": 123456789,
        "message": "Привет! У вас новое сообщение."
    }
    ```
    """
    try:
        result = await send_telegram_message(
            telegram_id=request.telegram_id,
            message=request.message,
            parse_mode=request.parse_mode,
            disable_web_page_preview=request.disable_web_page_preview
        )
        
        return {
            "success": True,
            "message": "Сообщение отправлено",
            "telegram_response": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/cases/{case_id}/reply")
async def send_case_reply(
    case_id: int,
    request: SendCaseReplyRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Отправить ответ по делу от администратора
    
    Пример использования:
    ```json
    {
        "admin_message": "Ваше дело рассмотрено. Ожидайте звонка.",
        "admin_id": 1
    }
    ```
    """
    # Получаем дело
    case = await get_case_by_id(db, case_id)
    
    if not case:
        raise HTTPException(status_code=404, detail=f"Дело #{case_id} не найдено")
    
    # Получаем пользователя
    user = await get_user_by_telegram_id(db, case.user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь дела не найден")
    
    # Создаём запись сообщения в базе данных
    new_message = CaseMessage(
        questionnaire_id=case_id,
        sender_id=request.admin_id,
        sender_type="admin",
        message_content=request.admin_message
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    
    # Формируем уведомление для клиента
    notification_text = (
        f"💬 <b>Новое сообщение по вашему делу #{case_id}</b>\n\n"
        f"📝 {request.admin_message}\n\n"
        f"📌 Ответьте на это сообщение в боте."
    )
    
    # Отправляем уведомление
    try:
        await send_telegram_message(
            telegram_id=user.telegram_id,
            message=notification_text
        )
        
        return {
            "success": True,
            "message": "Ответ отправлен клиенту",
            "case_id": case_id,
            "user_telegram_id": user.telegram_id
        }
    
    except Exception as e:
        # Логируем ошибку, но не возвращаем 500
        return {
            "success": False,
            "message": f"Ошибка отправки: {str(e)}",
            "case_id": case_id,
            "db_message_created": True  # Сообщение сохранено в БД
        }


@app.post("/api/broadcast")
async def send_broadcast(request: BroadcastRequest, db: AsyncSession = Depends(get_db)):
    """
    Рассылка сообщений пользователям
    
    Пример использования:
    ```json
    {
        "message": "Обновление системы!",
        "user_ids": [123, 456, 789]  // Опционально
    }
    ```
    """
    # Получаем список пользователей
    if request.user_ids:
        # Отправка конкретным пользователям
        result = await db.execute(
            select(User).filter(User.telegram_id.in_(request.user_ids))
        )
    else:
        # Отправка всем активным пользователям
        result = await db.execute(
            select(User).filter(User.is_active == True)
        )
    
    users = result.scalars().all()
    
    sent_count = 0
    failed_count = 0
    errors = []
    
    for user in users:
        try:
            await send_telegram_message(
                telegram_id=user.telegram_id,
                message=request.message
            )
            sent_count += 1
            
            # Небольшая задержка чтобы не превысить лимиты Telegram
            await asyncio.sleep(0.05)
        
        except Exception as e:
            failed_count += 1
            errors.append({
                "telegram_id": user.telegram_id,
                "error": str(e)
            })
    
    return {
        "success": True,
        "message": "Рассылка завершена",
        "total_users": len(users),
        "sent": sent_count,
        "failed": failed_count,
        "errors": errors[:10]  #最多返回前10个错误
    }


@app.get("/api/users/{telegram_id}")
async def get_user_info(telegram_id: int, db: AsyncSession = Depends(get_db)):
    """Получить информацию о пользователе по Telegram ID"""
    user = await get_user_by_telegram_id(db, telegram_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "registered_at": user.registered_at.isoformat() if user.registered_at else None
    }


# ============ Запуск сервера ============

if __name__ == "__main__":
    import uvicorn
    
    # Простой health endpoint без БД
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": "message_server",
            "port": 8002
        }
    
    print("=" * 50)
    print("🚀 Message Server запускается на порту 8002")
    print("=" * 50)
    print(f"📡 Telegram Bot API: {TELEGRAM_API_URL}")
    print("✅ Готов к работе!")
    print("=" * 50)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8002,
        log_level="info"
    )
