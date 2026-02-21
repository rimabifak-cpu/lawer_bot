import requests from 'requests';

async function main() {
    console.log("Проверка API...");

    try {
        // Проверка страницы диалогов
        const dialogsPage = await requests.get('http://127.0.0.1:8001/dialogs', { timeout: 5000 });
        console.log(`\nСтраница /dialogs: статус ${dialogsPage.status}`);
        console.log(`Контент: ${dialogsPage.text.slice(0, 200)}...`);
    } catch (e) {
        console.log(`\nОшибка страницы /dialogs: ${e}`);
    }

    try {
        // Проверка API диалогов
        const dialogsApi = await requests.get('http://127.0.0.1:8001/api/dialogs', { timeout: 5000 });
        console.log(`\nAPI /api/dialogs: статус ${dialogsApi.status}`);
        console.log(`Ответ: ${dialogsApi.text}`);
    } catch (e) {
        console.log(`\nОшибка API /api/dialogs: ${e}`);
    }

    try {
        // Проверка отправки сообщения
        const sendMessage = await requests.post('http://127.0.0.1:8001/api/dialogs/5093303797/send', {
            json: { telegram_id: 5093303797, content: 'Тест отправки сообщения' },
            timeout: 5000
        });
        console.log(`\nAPI /api/dialogs/5093303797/send: статус ${sendMessage.status}`);
        console.log(`Ответ: ${sendMessage.text}`);
    } catch (e) {
        console.log(`\nОшибка API /api/dialogs/5093303797/send: ${e}`);
    }
}

main();
