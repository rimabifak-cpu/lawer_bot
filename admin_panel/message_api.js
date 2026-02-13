/**
 * JavaScript модуль для работы с Message Server (порт 8002)
 */

// URL Message Server
const MESSAGE_SERVER_URL = 'http://localhost:8002';

/**
 * Отправить сообщение по делу через message_server
 * @param {number} caseId - ID дела
 * @param {string} message - Текст сообщения
 * @param {number} adminId - ID администратора (0 для системных)
 * @returns {Promise<object>} - Результат отправки
 */
async function sendCaseReply(caseId, message, adminId = 0) {
    try {
        const response = await fetch(`${MESSAGE_SERVER_URL}/api/cases/${caseId}/reply`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                admin_message: message,
                admin_id: adminId
            })
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Unknown error');
        }
    } catch (error) {
        console.error('Ошибка отправки сообщения:', error);
        throw error;
    }
}

/**
 * Отправить уведомление клиенту
 * @param {number} telegramId - Telegram ID клиента
 * @param {string} message - Текст уведомления
 * @returns {Promise<object>} - Результат отправки
 */
async function sendNotification(telegramId, message) {
    try {
        const response = await fetch(`${MESSAGE_SERVER_URL}/api/notify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                telegram_id: telegramId,
                message: message
            })
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Unknown error');
        }
    } catch (error) {
        console.error('Ошибка отправки уведомления:', error);
        throw error;
    }
}

/**
 * Рассылка сообщений
 * @param {string} message - Текст сообщения
 * @param {number[]|null} userIds - Список ID пользователей (null = всем)
 * @returns {Promise<object>} - Результат рассылки
 */
async function sendBroadcast(message, userIds = null) {
    try {
        const body = { message: message };
        if (userIds) {
            body.user_ids = userIds;
        }

        const response = await fetch(`${MESSAGE_SERVER_URL}/api/broadcast`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Unknown error');
        }
    } catch (error) {
        console.error('Ошибка рассылки:', error);
        throw error;
    }
}

/**
 * Проверить работоспособность message_server
 * @returns {Promise<boolean>}
 */
async function checkMessageServerHealth() {
    try {
        const response = await fetch(`${MESSAGE_SERVER_URL}/health`);
        return response.ok;
    } catch (error) {
        console.error('Message Server недоступен:', error);
        return false;
    }
}
