const { exec } = require('child_process');

exec('start http://127.0.0.1:8001/dialogs', (err, stdout, stderr) => {
    if (err) {
        console.error('Ошибка открытия страницы:', err);
        return;
    }
    console.log('Страница диалогов открыта в браузере');
});
