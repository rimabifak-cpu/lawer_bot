const fetch = require('node-fetch');

async function test() {
    try {
        const response = await fetch('http://127.0.0.1:8001/api/dialogs');
        const data = await response.json();
        console.log('Диалоги:', data);
        
        if (data.length > 0) {
            const firstDialog = data[0];
            const messagesResponse = await fetch(`http://127.0.0.1:8001/api/dialogs/${firstDialog.telegram_id}/messages`);
            const messages = await messagesResponse.json();
            console.log('Сообщения:', messages);
        }
    } catch (e) {
        console.error('Ошибка:', e);
    }
}

test();
