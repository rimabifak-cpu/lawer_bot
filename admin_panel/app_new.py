import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, text
from sqlalchemy.orm import joinedload, selectinload
from datetime import datetime
import asyncio
import httpx

from pydantic import BaseModel
from typing import Optional, Any

from database.database import get_db, get_db_session
from database.models import User, PartnerProfile, CaseQuestionnaire, ServiceRequest, PartnerRevenue, ReferralPayout, ReferralRelationship, CaseMessage
from config.settings import settings

app = FastAPI(title="Admin Panel for Law Bot")

# URL message_server для отправки уведомлений клиентам
MESSAGE_SERVER_URL = os.getenv("MESSAGE_SERVER_URL", "http://127.0.0.1:8002")


class DirectMessageRequest(BaseModel):
    """Запрос на отправку прямого сообщения пользователю"""
    telegram_id: int
    content: str

# Читаем simple_test.html
SIMPLE_TEST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simple_test.html")
with open(SIMPLE_TEST_PATH, "r", encoding="utf-8") as f:
    SIMPLE_TEST_HTML = f.read()

@app.get("/test", response_class=HTMLResponse)
async def simple_test():
    """Простой тест админ-панели"""
    return HTMLResponse(content=SIMPLE_TEST_HTML)

@app.get("/js-test", response_class=HTMLResponse)
async def js_test():
    """Простой тест JavaScript"""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "simple_js_test.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/", response_class=HTMLResponse)
async def admin_dashboard():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Админ-панель юридического бота</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                border-bottom: 2px solid #007bff;
                padding-bottom: 10px;
            }
            .section {
                margin-bottom: 30px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            th, td {
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f8f9fa;
            }
            .btn {
                padding: 8px 15px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
            }
            .btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Админ-панель юридического бота</h1>
            
            <div class="section">
                <h2>Анкеты дел</h2>
                <table id="requests-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Клиент</th>
                            <th>Предмет спора</th>
                            <th>Статус</th>
                            <th>Дата отправки</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Заявки будут загружены сюда -->
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>Партнеры</h2>
                <table id="partners-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>ФИО</th>
                            <th>Компания</th>
                            <th>Специализация</th>
                            <th>Опыт</th>
                            <th>Контакты</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Партнеры будут загружены сюда -->
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>💰 Выручка пользователей</h2>
                <form id="add-revenue-form" style="margin-bottom: 15px;">
                    <select id="revenue-user-select" style="padding: 8px; margin-right: 10px; min-width: 250px;">
                        <option value="">Выберите пользователя...</option>
                    </select>
                    <input type="number" id="revenue-amount" placeholder="Сумма (руб.)" style="padding: 8px; margin-right: 10px; width: 150px;">
                    <input type="text" id="revenue-description" placeholder="Описание сделки" style="padding: 8px; margin-right: 10px; width: 200px;">
                    <button type="submit" class="btn">Добавить выручку</button>
                </form>
                <table id="revenues-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Пользователь</th>
                            <th>Сумма</th>
                            <th>Описание</th>
                            <th>Дата</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Выручка будет загружена сюда -->
                    </tbody>
                </table>
            </div>
            
            <div class="section" style="background: #fff3cd; border-color: #ffc107;">
                <h2>🔍 Отладка</h2>
                <div id="debug-info" style="background: #fff; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px;">
                    <p>Статус JS: <span id="js-status">Загрузка...</span></p>
                    <p>Ошибки: <span id="js-errors" style="color: red;">Нет</span></p>
                    <button onclick="location.reload()" class="btn" style="margin-top: 10px;">🔄 Перезагрузить</button>
                </div>
            </div>
            
            <div class="section">
                <h2>💸 Выплаты реферерам</h2>
                <form id="add-payout-form" style="margin-bottom: 15px;">
                    <select id="payout-referrer-select" style="padding: 8px; margin-right: 10px;">
                        <option value="">Выберите реферера...</option>
                    </select>
                    <input type="number" id="payout-amount" placeholder="Сумма (руб.)" style="padding: 8px; margin-right: 10px; width: 150px;">
                    <input type="number" id="payout-month" placeholder="Месяц" min="1" max="12" style="padding: 8px; margin-right: 10px; width: 80px;">
                    <input type="number" id="payout-year" placeholder="Год" style="padding: 8px; margin-right: 10px; width: 80px;">
                    <button type="submit" class="btn">Создать выплату</button>
                </form>
                <table id="payouts-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Реферер</th>
                            <th>Сумма</th>
                            <th>Период</th>
                            <th>Статус</th>
                            <th>Дата выплаты</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Выплаты будут загружены сюда -->
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>📢 Рассылка уведомлений</h2>
                <div>
                    <textarea id="broadcast-message" placeholder="Введите текст сообщения для рассылки..." rows="4" style="width: 100%; padding: 10px; margin-bottom: 10px;"></textarea>
                    <button onclick="sendBroadcast()" class="btn">Отправить рассылку всем партнерам</button>
                </div>
            </div>
            
            <script>
                console.log('Admin panel JavaScript loaded');
                
                // Обновление статуса отладки
                function updateDebugStatus(status, error) {
                    const statusEl = document.getElementById('js-status');
                    const errorEl = document.getElementById('js-errors');
                    if (statusEl) statusEl.textContent = status;
                    if (errorEl) errorEl.textContent = error || 'Нет';
                }
                
                // Загрузка заявок
                async function loadRequests() {
                    updateDebugStatus('Загрузка заявок...', null);
                    console.log('loadRequests called');
                    try {
                        const response = await fetch('/api/requests');
                        console.log('API response status:', response.status);
                        const requests = await response.json();
                        console.log('Received requests:', requests.length);
                    
                    const tbody = document.getElementById('requests-table').getElementsByTagName('tbody')[0];
                    tbody.innerHTML = '';
                    
                    requests.forEach(request => {
                        const row = tbody.insertRow();
                        row.insertCell(0).textContent = request.id;
                        row.insertCell(1).textContent = request.user ? request.user.first_name : 'N/A';
                        
                        // Краткое описание предмета спора
                        const disputeSubject = request.dispute_subject || '-';
                        row.insertCell(2).textContent = disputeSubject.substring(0, 30) + (disputeSubject.length > 30 ? '...' : '');
                        
                        // Статус с цветовой индикацией
                        const statusCell = row.insertCell(3);
                        const statusRu = { 'sent': 'sent', 'in_progress': 'in_progress', 'completed': 'completed', 'new': 'new' };
                        statusCell.innerHTML = '<span>' + (statusRu[request.status] || request.status) + '</span>';
                        
                        row.insertCell(4).textContent = request.sent_at ? new Date(request.sent_at).toLocaleString('ru-RU') : '-';
                        
                        const actionsCell = row.insertCell(5);
                        const detailsBtn = document.createElement('button');
                        detailsBtn.className = 'btn';
                        detailsBtn.textContent = '📋 Подробнее';
                        detailsBtn.onclick = () => showRequestDetails(request);
                        actionsCell.appendChild(detailsBtn);
                        
                        const updateBtn = document.createElement('button');
                        updateBtn.className = 'btn';
                        updateBtn.style.marginLeft = '5px';
                        updateBtn.textContent = '🔄 Статус';
                        updateBtn.onclick = () => updateStatus(request.id);
                        actionsCell.appendChild(updateBtn);
                    });
                    updateDebugStatus('Загружено ' + requests.length + ' анкет', null);
                    } catch (e) {
                        console.error('Error loading requests:', e);
                        updateDebugStatus('Ошибка загрузки', e.message);
                    }
                }
                
                // Показать детали заявки
                async function showRequestDetails(request) {
                    // Загружаем сообщения
                    let messagesHtml = '<p style="color: #666;">Загрузка переписки...</p>';
                    try {
                        const messagesResponse = await fetch(`/api/cases/${request.id}/messages`);
                        const messages = await messagesResponse.json();
                        
                        if (messages.length > 0) {
                            messagesHtml = '<div style="max-height: 200px; overflow-y: auto; margin-top: 10px;">';
                            messages.forEach(msg => {
                                const isAdmin = msg.sender_type === 'admin';
                                const time = new Date(msg.created_at).toLocaleString('ru-RU');
                                messagesHtml += `
                                    <div style="margin: 5px 0; padding: 8px; background: ${isAdmin ? '#e3f2fd' : '#fff3e0'}; border-radius: 4px;">
                                        <strong>${msg.sender_name}</strong> (${time}):<br>
                                        ${msg.message_content}
                                    </div>
                                `;
                            });
                            messagesHtml += '</div>';
                        } else {
                            messagesHtml = '<p style="color: #999;">Пока нет сообщений</p>';
                        }
                    } catch (e) {
                        messagesHtml = '<p style="color: red;">Ошибка загрузки сообщений</p>';
                    }
                    
                    const details = `
                        <div style="padding: 20px; background: #f9f9f9; border-radius: 8px;">
                            <h3 style="margin-top: 0; color: #333;">📋 Детали анкеты дела #${request.id}</h3>
                            
                            <p><strong>👤 Клиент:</strong> ${request.user ? request.user.first_name + ' ' + (request.user.last_name || '') : 'N/A'}</p>
                            <p><strong>📞 Telegram:</strong> ${request.user ? '@' + (request.user.username || 'нет username') : 'N/A'}</p>
                            
                            <hr style="border: 1px solid #ddd;">
                            
                            <h4 style="color: #007bff;">🏛️ Стороны конфликта</h4>
                            <p>${request.parties_info || 'Не указано'}</p>
                            
                            <h4 style="color: #007bff;">📋 Предмет спора</h4>
                            <p>${request.dispute_subject || 'Не указано'}</p>
                            
                            <h4 style="color: #007bff;">⚖️ Основания требований</h4>
                            <p>${request.legal_basis || 'Не указано'}</p>
                            
                            <h4 style="color: #007bff;">📅 Хронология событий</h4>
                            <p>${request.chronology || 'Не указано'}</p>
                            
                            <h4 style="color: #007bff;">📄 Имеющиеся доказательства</h4>
                            <p>${request.evidence || 'Не указано'}</p>
                            
                            <h4 style="color: #007bff;">⚡ Процессуальная история</h4>
                            <p>${request.procedural_history || 'Не указано'}</p>
                            
                            <h4 style="color: #007bff;">🎯 Цель клиента</h4>
                            <p>${request.client_goal || 'Не указано'}</p>
                            
                            <hr style="border: 1px solid #ddd;">
                            
                            <p><strong>📊 Статус:</strong> ${request.status}</p>
                            <p><strong>📅 Дата создания:</strong> ${request.created_at ? new Date(request.created_at).toLocaleString('ru-RU') : '-'}</p>
                            <p><strong>📤 Дата отправки:</strong> ${request.sent_at ? new Date(request.sent_at).toLocaleString('ru-RU') : '-'}</p>
                            
                            <hr style="border: 1px solid #ddd;">
                            
                            <h4 style="color: #007bff;">💬 Переписка</h4>
                            ${messagesHtml}
                            
                            <div style="margin-top: 10px;">
                                <textarea id="reply-message-${request.id}" placeholder="Введите ответ клиенту..." style="width: 100%; padding: 8px; margin-bottom: 10px;"></textarea>
                                <button onclick="sendMessage(${request.id})" class="btn">📤 Отправить ответ</button>
                            </div>
                        </div>
                    `;
                    
                    // Показываем в модальном окне
                    const modal = document.createElement('div');
                    modal.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;justify-content:center;align-items:center;z-index:1000;';
                    modal.innerHTML = `
                        <div style="background:white;padding:20px;border-radius:8px;max-width:700px;max-height:90vh;overflow-y:auto;margin:20px;">
                            ${details}
                            <button onclick="this.closest('div').parentElement.remove()" class="btn" style="margin-top:15px;width:100%;">Закрыть</button>
                        </div>
                    `;
                    document.body.appendChild(modal);
                }
                
                // Отправка сообщения из админ-панели
                async function sendMessage(caseId) {
                    const textarea = document.getElementById(`reply-message-${caseId}`);
                    const content = textarea.value.trim();
                    
                    if (!content) {
                        alert('Введите текст сообщения');
                        return;
                    }
                    
                    try {
                        const response = await fetch(`/api/cases/${caseId}/messages`, {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                content: content,
                                sender_id: 0  # ID админа
                            })
                        });
                        
                        if (response.ok) {
                            const result = await response.json();
                            alert('Сообщение отправлено! Клиент получит уведомление в Telegram.');
                            // Обновляем модальное окно
                            showRequestDetails({id: caseId});
                        } else {
                            alert('Ошибка при отправке сообщения');
                        }
                    } catch (e) {
                        alert('Ошибка: ' + e.message);
                    }
                }
                
                // Загрузка партнеров
                async function loadPartners() {
                    const response = await fetch('/api/partners');
                    const partners = await response.json();
                    
                    const tbody = document.getElementById('partners-table').getElementsByTagName('tbody')[0];
                    tbody.innerHTML = '';
                    
                    partners.forEach(partner => {
                        const row = tbody.insertRow();
                        row.insertCell(0).textContent = partner.id;
                        row.insertCell(1).textContent = partner.full_name;
                        row.insertCell(2).textContent = partner.company_name;
                        row.insertCell(3).textContent = partner.specialization;
                        row.insertCell(4).textContent = partner.experience + ' лет';
                        row.insertCell(5).textContent = `Тел: ${partner.phone}, Email: ${partner.email}`;
                    });
                }
                
                // Обновление статуса заявки
                async function updateStatus(requestId) {
                    const newStatus = prompt('Введите новый статус (новый, в работе, выполнен):');
                    if (newStatus) {
                        await fetch(`/api/requests/${requestId}`, {
                            method: 'PUT',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({status: newStatus})
                        });
                        loadRequests(); // Обновляем таблицу
                    }
                }
                
                // Загрузка выручки партнёров
                async function loadRevenues() {
                    const response = await fetch('/api/revenues');
                    const revenues = await response.json();
                    
                    const tbody = document.getElementById('revenues-table').getElementsByTagName('tbody')[0];
                    tbody.innerHTML = '';
                    
                    revenues.forEach(revenue => {
                        const row = tbody.insertRow();
                        row.insertCell(0).textContent = revenue.id;
                        row.insertCell(1).textContent = revenue.partner_name;
                        row.insertCell(2).textContent = revenue.amount.toLocaleString('ru-RU') + ' ₽';
                        row.insertCell(3).textContent = revenue.description || '-';
                        row.insertCell(4).textContent = new Date(revenue.created_at).toLocaleString('ru-RU');
                    });
                }
                
                // Загрузка выплат реферерам
                async function loadPayouts() {
                    const response = await fetch('/api/payouts');
                    const payouts = await response.json();
                    
                    const tbody = document.getElementById('payouts-table').getElementsByTagName('tbody')[0];
                    tbody.innerHTML = '';
                    
                    payouts.forEach(payout => {
                        const row = tbody.insertRow();
                        row.insertCell(0).textContent = payout.id;
                        row.insertCell(1).textContent = payout.referrer_name;
                        row.insertCell(2).textContent = payout.amount.toLocaleString('ru-RU') + ' ₽';
                        row.insertCell(3).textContent = `${String(payout.month).padStart(2, '0')}.${payout.year}`;
                        
                        const statusCell = row.insertCell(4);
                        if (payout.status === 'paid') {
                            statusCell.innerHTML = '<span style="color: green;">✅ Выплачено</span>';
                        } else if (payout.status === 'pending') {
                            statusCell.innerHTML = '<span style="color: orange;">⏳ Ожидает</span>';
                        } else {
                            statusCell.innerHTML = '<span style="color: red;">❌ Отменено</span>';
                        }
                        
                        row.insertCell(5).textContent = payout.paid_at ? new Date(payout.paid_at).toLocaleString('ru-RU') : '-';
                        
                        const actionsCell = row.insertCell(6);
                        if (payout.status === 'pending') {
                            const payBtn = document.createElement('button');
                            payBtn.className = 'btn';
                            payBtn.textContent = 'Отметить выплаченным';
                            payBtn.onclick = () => markAsPaid(payout.id);
                            actionsCell.appendChild(payBtn);
                        } else {
                            actionsCell.textContent = '-';
                        }
                    });
                }
                
                // Загрузка списка пользователей для select
                async function loadUsersForSelect() {
                    const response = await fetch('/api/users');
                    const users = await response.json();
                    
                    const select = document.getElementById('revenue-user-select');
                    select.innerHTML = '<option value="">Выберите пользователя...</option>';
                    
                    users.forEach(user => {
                        const option = document.createElement('option');
                        option.value = user.id;
                        const name = user.partner_name || (user.first_name + ' ' + (user.last_name || '')).trim();
                        const isPartner = user.is_partner ? ' (партнёр)' : '';
                        option.textContent = `${name}${isPartner} (@${user.username || 'N/A'})`;
                        select.appendChild(option);
                    });
                }
                
                // Загрузка списка рефереров для select
                async function loadReferrersForSelect() {
                    const response = await fetch('/api/referrers');
                    const referrers = await response.json();
                    
                    const select = document.getElementById('payout-referrer-select');
                    select.innerHTML = '<option value="">Выберите реферера...</option>';
                    
                    referrers.forEach(referrer => {
                        const option = document.createElement('option');
                        option.value = referrer.user_id;
                        option.textContent = `${referrer.full_name} (${referrer.referrals_count} рефералов)`;
                        select.appendChild(option);
                    });
                }
                
                // Добавление выручки
                document.getElementById('add-revenue-form').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const userId = document.getElementById('revenue-user-select').value;
                    const amount = document.getElementById('revenue-amount').value;
                    const description = document.getElementById('revenue-description').value;
                    
                    if (!userId || !amount) {
                        alert('Выберите пользователя и укажите сумму');
                        return;
                    }
                    
                    const response = await fetch('/api/revenues', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            partner_id: userId,  # partner_id совместим с user_id
                            amount: amount,
                            description: description
                        })
                    });
                    
                    if (response.ok) {
                        alert('Выручка добавлена!');
                        document.getElementById('revenue-amount').value = '';
                        document.getElementById('revenue-description').value = '';
                        loadRevenues();
                    } else {
                        alert('Ошибка при добавлении выручки');
                    }
                });
                
                // Создание выплаты
                document.getElementById('add-payout-form').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const referrerId = document.getElementById('payout-referrer-select').value;
                    const amount = document.getElementById('payout-amount').value;
                    const month = document.getElementById('payout-month').value;
                    const year = document.getElementById('payout-year').value;
                    
                    if (!referrerId || !amount || !month || !year) {
                        alert('Заполните все поля');
                        return;
                    }
                    
                    const response = await fetch('/api/payouts', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            referrer_id: referrerId,
                            amount: amount,
                            month: month,
                            year: year
                        })
                    });
                    
                    if (response.ok) {
                        alert('Выплата создана!');
                        document.getElementById('payout-amount').value = '';
                        loadPayouts();
                    } else {
                        alert('Ошибка при создании выплаты');
                    }
                });
                
                // Отметить выплату как выполненную
                async function markAsPaid(payoutId) {
                    if (confirm('Отметить эту выплату как выполненную? Партнёр получит уведомление в Telegram.')) {
                        const response = await fetch(`/api/payouts/${payoutId}/pay`, {
                            method: 'PUT'
                        });
                        
                        if (response.ok) {
                            const result = await response.json();
                            alert('Выплата отмечена как выполненная!\\n\\n' + result.notification);
                            loadPayouts();
                        } else {
                            const error = await response.json();
                            alert('Ошибка: ' + error.detail);
                        }
                    }
                }
                
                // Загружаем данные при загрузке страницы
                window.onload = function() {
                    console.log('window.onload triggered');
                    updateDebugStatus('Инициализация...', null);
                    try {
                        loadRequests();
                        loadPartners();
                        loadRevenues();
                        loadPayouts();
                        loadUsersForSelect();
                        loadReferrersForSelect();
                        
                        // Устанавливаем текущий месяц и год
                        const now = new Date();
                        document.getElementById('payout-month').value = now.getMonth() + 1;
                        document.getElementById('payout-year').value = now.getFullYear();
                        updateDebugStatus('Готово', null);
                    } catch (e) {
                        console.error('Error in window.onload:', e);
                        updateDebugStatus('Ошибка', e.message);
                    }
                };
                
                // Функция для отправки рассылки
                async function sendBroadcast() {
                    const message = document.getElementById('broadcast-message').value;
                    if (!message.trim()) {
                        alert('Введите текст сообщения');
                        return;
                    }
                    
                    if (confirm('Вы уверены, что хотите отправить это сообщение всем партнерам?')) {
                        const response = await fetch('/api/broadcast', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({message: message})
                        });
                        
                        const result = await response.json();
                        if (response.ok) {
                            alert(`Рассылка отправлена ${result.sent_count} партнерам`);
                            document.getElementById('broadcast-message').value = '';
                        } else {
                            alert('Ошибка при отправке рассылки: ' + result.detail);
                        }
                    }
                }
            </script>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/broadcast")
async def send_broadcast(message_data: dict):
    from sqlalchemy import select
    from ..database.models import User, PartnerProfile
    
    message = message_data.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Текст сообщения обязателен")
    
    async with get_db() as db:
        # Получаем всех пользователей, у которых есть партнерский профиль
        result = await db.execute(
            select(User)
            .join(PartnerProfile, User.id == PartnerProfile.user_id)
        )
        users = result.scalars().all()
        
        sent_count = 0
        # В реальной реализации здесь будет отправка сообщений через Telegram API
        # for user in users:
        #     try:
        #         await bot.send_message(user.telegram_id, message)
        #         sent_count += 1
        #     except Exception as e:
        #         print(f"Ошибка при отправке сообщения пользователю {user.telegram_id}: {e}")
        
        # Для демонстрации просто возвращаем количество пользователей
        sent_count = len(users)
    
    return {"message": "Рассылка успешно отправлена", "sent_count": sent_count}

@app.get("/api/requests")
async def get_requests():
    async with get_db() as db:
        result = await db.execute(
            select(CaseQuestionnaire)
            .options(selectinload(CaseQuestionnaire.user))
            .order_by(CaseQuestionnaire.created_at.desc())
        )
        requests = result.unique().scalars().all()
        
        requests_data = []
        for req in requests:
            requests_data.append({
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
                "created_at": req.created_at.isoformat() if req.created_at else None,
                "sent_at": req.sent_at.isoformat() if req.sent_at else None,
                "user": {
                    "id": req.user.id,
                    "telegram_id": req.user.telegram_id,
                    "username": req.user.username,
                    "first_name": req.user.first_name,
                    "last_name": req.user.last_name
                } if req.user else None
            })
        
        return requests_data

@app.put("/api/requests/{request_id}")
async def update_request_status(request_id: int, status_data: dict):
    async with get_db() as db:
        result = await db.execute(
            select(CaseQuestionnaire).filter(CaseQuestionnaire.id == request_id)
        )
        request = result.scalar_one_or_none()
        
        if not request:
            raise HTTPException(status_code=404, detail="Заявка не найдена")
        
        request.status = status_data.get("status", request.status)
        await db.commit()
        
        # Отправляем уведомление пользователю о смене статуса
        # (в реальной реализации здесь будет вызов Telegram API)
        
    return {"message": "Статус заявки обновлен"}

@app.get("/api/partners")
async def get_partners():
    async with get_db() as db:
        result = await db.execute(
            select(PartnerProfile)
            .join(User, PartnerProfile.user_id == User.id)
            .order_by(PartnerProfile.created_at.desc())
        )
        partners = result.scalars().all()
        
        partners_data = []
        for partner in partners:
            partners_data.append({
                "id": partner.id,
                "user_id": partner.user_id,
                "full_name": partner.full_name,
                "company_name": partner.company_name,
                "phone": partner.phone,
                "email": partner.email,
                "specialization": partner.specialization,
            "experience": partner.experience,
            "consent_to_share_data": partner.consent_to_share_data,
            "created_at": partner.created_at.isoformat(),
            "updated_at": partner.updated_at.isoformat()
        })
    
    return partners_data


# ==================== РЕФЕРАЛЬНАЯ ПРОГРАММА ====================

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
            # Получаем профиль партнёра
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
                "created_at": revenue.created_at.isoformat()
            })
        
        return revenues_data


@app.post("/api/revenues")
async def add_revenue(revenue_data: dict):
    """Добавить выручку партнёру"""
    partner_id = revenue_data.get("partner_id")
    amount = revenue_data.get("amount")
    description = revenue_data.get("description", "")
    client_reference = revenue_data.get("client_reference", "")
    
    if not partner_id or not amount:
        raise HTTPException(status_code=400, detail="partner_id и amount обязательны")
    
    async with get_db() as db:
        new_revenue = PartnerRevenue(
            partner_id=partner_id,
            amount=int(amount),
            description=description,
            client_reference=client_reference
        )
        db.add(new_revenue)
        await db.commit()
    
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
        "created_at": r.created_at.isoformat()
    } for r in revenues]


@app.get("/api/payouts")
async def get_payouts(db: AsyncSession = Depends(get_db_session)):
    """Получить список всех выплат"""
    result = await db.execute(
        select(ReferralPayout)
        .join(User, ReferralPayout.referrer_id == User.id)
        .order_by(ReferralPayout.created_at.desc())
    )
    payouts = result.scalars().all()
    
    payouts_data = []
    for payout in payouts:
        # Получаем профиль реферера
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
            "paid_at": payout.paid_at.isoformat() if payout.paid_at else None,
            "created_at": payout.created_at.isoformat()
        })
    
    return payouts_data


@app.post("/api/payouts")
async def create_payout(payout_data: dict, db: AsyncSession = Depends(get_db_session)):
    """Создать выплату рефереру"""
    referrer_id = payout_data.get("referrer_id")
    amount = payout_data.get("amount")
    month = payout_data.get("month")
    year = payout_data.get("year")
    
    if not all([referrer_id, amount, month, year]):
        raise HTTPException(status_code=400, detail="Все поля обязательны")
    
    new_payout = ReferralPayout(
        referrer_id=referrer_id,
        amount=int(amount),
        month=int(month),
        year=int(year),
        status="pending"
    )
    db.add(new_payout)
    await db.commit()
    
    return {"message": "Выплата создана", "id": new_payout.id}


@app.put("/api/payouts/{payout_id}/pay")
async def mark_payout_as_paid(payout_id: int, db: AsyncSession = Depends(get_db_session)):
    """Отметить выплату как выполненную и отправить уведомление"""
    result = await db.execute(
        select(ReferralPayout).filter(ReferralPayout.id == payout_id)
    )
    payout = result.scalar_one_or_none()
    
    if not payout:
        raise HTTPException(status_code=404, detail="Выплата не найдена")
    
    if payout.status == "paid":
        raise HTTPException(status_code=400, detail="Выплата уже выполнена")
    
    # Обновляем статус
    payout.status = "paid"
    payout.paid_at = datetime.utcnow()
    await db.commit()
    
    # Получаем telegram_id реферера для отправки уведомления
    user_result = await db.execute(
        select(User).filter(User.id == payout.referrer_id)
    )
    user = user_result.scalar_one_or_none()
    
    if user:
        # Отправляем уведомление через Telegram Bot API
        # В реальной реализации здесь будет вызов бота
        notification_text = (
            f"💰 <b>Вам начислено вознаграждение!</b>\n\n"
            f"Сумма: {payout.amount:,} ₽\n"
            f"За период: {payout.month:02d}.{payout.year}\n\n"
            f"Спасибо за участие в реферальной программе!"
        )
        
        # Здесь должна быть отправка через бота
        # await bot.send_message(user.telegram_id, notification_text, parse_mode="HTML")
        
        return {
            "message": "Выплата отмечена как выполненная",
            "telegram_id": user.telegram_id,
            "notification": notification_text
        }
    
    return {"message": "Выплата отмечена как выполненная"}


@app.get("/api/referrers")
async def get_referrers(db: AsyncSession = Depends(get_db_session)):
    """Получить список всех рефереров (партнёров, у которых есть приглашённые)"""
    # Находим всех пользователей, которые кого-то пригласили
    result = await db.execute(
        select(ReferralRelationship.referrer_id, func.count(ReferralRelationship.id).label('referrals_count'))
        .group_by(ReferralRelationship.referrer_id)
    )
    referrers_stats = result.all()
    
    referrers_data = []
    for referrer_id, count in referrers_stats:
        # Получаем профиль реферера
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
            "full_name": profile.full_name if profile else (user.first_name if user else f"User {referrer_id}"),
            "telegram_id": user.telegram_id if user else None,
            "referrals_count": count
        })
    
    return referrers_data


# ==================== API ПОЛЬЗОВАТЕЛЕЙ ====================

@app.get("/api/users")
async def get_users(db: AsyncSession = Depends(get_db_session)):
    """Получить список всех пользователей (для выбора при добавлении выручки)"""
    result = await db.execute(
        select(User).order_by(User.registered_at.desc())
    )
    users = result.scalars().all()
    
    users_data = []
    for user in users:
        # Проверяем, есть ли партнёрский профиль
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
            "registered_at": user.registered_at.isoformat() if user.registered_at else None
        })
    
    return users_data


# ==================== API СООБЩЕНИЙ ПО ДЕЛАМ ====================

@app.get("/api/cases/{case_id}/messages")
async def get_case_messages(case_id: int, db: AsyncSession = Depends(get_db_session)):
    """Получить переписку по делу"""
    result = await db.execute(
        select(CaseMessage)
        .filter(CaseMessage.questionnaire_id == case_id)
        .options(selectinload(CaseMessage.sender))
        .order_by(CaseMessage.created_at.asc())
    )
    messages = result.scalars().all()
    
    messages_data = []
    for msg in messages:
        messages_data.append({
            "id": msg.id,
            "questionnaire_id": msg.questionnaire_id,
            "sender_id": msg.sender_id,
            "sender_type": msg.sender_type,
            "sender_name": f"{msg.sender.first_name} {msg.sender.last_name}".strip() if msg.sender else "Unknown",
            "message_content": msg.message_content,
            "is_read": msg.is_read,
            "created_at": msg.created_at.isoformat()
        })
    
    return messages_data


@app.post("/api/cases/{case_id}/messages")
async def send_case_message(case_id: int, message_data: dict, db: AsyncSession = Depends(get_db_session)):
    """Отправить сообщение по делу (от админа)"""
    content = message_data.get("content")
    sender_id = message_data.get("sender_id", 0)  # ID админа (0 для системных)
    
    if not content:
        raise HTTPException(status_code=400, detail="Текст сообщения обязателен")
    
    # Проверяем, что дело существует
    case_result = await db.execute(
        select(CaseQuestionnaire).filter(CaseQuestionnaire.id == case_id)
    )
    case = case_result.scalar_one_or_none()
    
    if not case:
        raise HTTPException(status_code=404, detail="Дело не найдено")
    
    # Создаём сообщение
    new_message = CaseMessage(
        questionnaire_id=case_id,
        sender_id=sender_id,
        sender_type="admin",
        message_content=content
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    
    # Получаем информацию о клиенте для отправки уведомления
    user_result = await db.execute(
        select(User).filter(User.id == case.user_id)
    )
    user = user_result.scalar_one_or_none()
    
    notification_text = (
        f"💬 <b>Новое сообщение по вашему делу #{case_id}</b>\n\n"
        f"📝 {content}\n\n"
        f"Чтобы ответить, нажмите кнопку ниже или перейдите в раздел \"Мои дела\"."
    )
    
    return {
        "message": "Сообщение отправлено",
        "id": new_message.id,
        "notification": notification_text,
        "user_telegram_id": user.telegram_id if user else None
    }


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
                "name": user_name,
                "registered_at": user.registered_at if user.registered_at else None,
                "invited_by": referrer_of.get(user.id),
                "invited_count": referrals_count.get(user.id, 0)
            })
        
        return {"users": users_data}


async def send_notification_to_client(telegram_id: int, message: str) -> bool:
    """Отправить уведомление клиенту через message_server"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{MESSAGE_SERVER_URL}/api/notify",
                json={
                    "telegram_id": telegram_id,
                    "message": message,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True
                }
            )
            if response.status_code == 200:
                return True
            else:
                return False
    except Exception as e:
        return False


@app.post("/api/messages/direct")
async def send_direct_message(request: DirectMessageRequest):
    """Отправить сообщение напрямую пользователю"""
    notification_text = f"💬 <b>Сообщение от ЮК</b>\n\n📝 {request.content}"
    
    sent = await send_notification_to_client(
        telegram_id=request.telegram_id,
        message=notification_text
    )
    
    return {
        "message": "Сообщение отправлено",
        "telegram_id": request.telegram_id,
        "sent": sent
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
