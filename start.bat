@echo off

echo Запускаем админ панель и телеграм бот...

REM Запускаем админ панель в новом окне
start "Admin Panel" cmd /k "cd /d C:\Users\HONOR\Documents\law_bot && python admin_panel/app.py"

REM Ожидаем, пока админ панель запустится
timeout /t 2 /nobreak >nul

REM Запускаем телеграм бот в новом окне
start "Telegram Bot" cmd /k "cd /d C:\Users\HONOR\Documents\law_bot && python run_bot.py"

echo Админ панель и телеграм бот запущены!
echo Админ панель доступна по адресу: http://127.0.0.1:8001
pause
