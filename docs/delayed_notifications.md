# Отложенные уведомления (Delayed Notifications)

## Описание

Модуль автоматической отправки промо-сообщений **каждому новому пользователю** после первого нажатия `/start`:

1. **Через 1 час** — специальное предложение со скидкой 15%
2. **Через 24 часа** — результаты заработка партнёров

---

## Файлы

- `bot/utils/delayed_notification.py` — модуль отложенных уведомлений
- `bot/handlers/start.py` — обработчик команды /start (интегрировано)
- `run_bot.py` — точка запуска

---

## Как это работает

```
Пользователь нажимает /start
         ↓
Создается новый пользователь в БД
         ↓
Планируется задача №1 (через 1 час)
Планируется задача №2 (через 24 часа)
         ↓
[Ожидание 1 часа]
         ↓
Отправка промо-сообщения №1 (скидка 15%)
         ↓
[Ожидание ещё 23 часа]
         ↓
Отправка промо-сообщения №2 (результаты заработка)
```

---

## Уведомление №1 (через 1 час)

### Текст сообщения:

```
Уважаемый партнер, у нас для вас специальное предложение! 💼

Мы готовы предоставить постоянную скидку 15% для всех ваших клиентов на наши услуги.

Чтобы активировать ее навсегда, достаточно привести одного нового клиента, который совершит оплату в течение 14 дней.

После выполнения этого условия скидка закрепится за вашими клиентами на постоянной основе.
  
@legaldecision, поддержка 24/7
```

---

## Уведомление №2 (через 24 часа)

### Текст сообщения:

```
Вот это результаты! 🔥

Наш лучший партнер прошлого месяца заработал 142 580 рублей.

А знаете, что самое интересное? Даже средний доход среди всех партнеров составил 58 655 рублей.

Присоединяйтесь, возможности безграничны!
```

---

## Функции

### `schedule_promo_notification(bot, telegram_id, delay_hours=1)`
Запланировать отправку промо-сообщения №1 (скидка 15%).

**Аргументы:**
- `bot` — экземпляр бота
- `telegram_id` — Telegram ID пользователя
- `delay_hours` — задержка в часах (по умолчанию 1)

---

### `schedule_earnings_notification(bot, telegram_id, delay_hours=24)`
Запланировать отправку промо-сообщения №2 (результаты заработка).

**Аргументы:**
- `bot` — экземпляр бота
- `telegram_id` — Telegram ID пользователя
- `delay_hours` — задержка в часах (по умолчанию 24)

---

### `cancel_all_notifications(telegram_id)`
Отменить все уведомления для пользователя.

**Аргументы:**
- `telegram_id` — Telegram ID пользователя

---

### `get_pending_count()`
Получить количество пользователей с запланированными уведомлениями.

**Возвращает:** `int`

---

### `get_active_tasks_count()`
Получить количество активных задач.

**Возвращает:** `int`

---

## Интеграция

### В `bot/handlers/start.py`:

```python
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    async with get_db() as db:
        # Проверяем, существует ли пользователь
        result = await db.execute(select(User).filter(User.telegram_id == user_id))
        existing_user = result.scalar_one_or_none()
        
        is_new_user = existing_user is None
        
        # Создаем или получаем пользователя
        user = await get_or_create_user(db, user_id, username, first_name, last_name)
        
        # Если пользователь новый - планируем отправку уведомлений
        if is_new_user:
            from bot.utils.delayed_notification import (
                schedule_promo_notification,
                schedule_earnings_notification
            )
            from bot import main as bot_module
            
            # Планируем первое уведомление через 1 час
            await schedule_promo_notification(bot_module.bot, user_id, delay_hours=1)
            logger.info(f"📅 Промо-сообщение запланировано для нового пользователя {user_id}")
            
            # Планируем второе уведомление через 24 часа
            await schedule_earnings_notification(bot_module.bot, user_id, delay_hours=24)
            logger.info(f"📅 Уведомление о результатах запланировано для нового пользователя {user_id}")
```

---

## Логи

Модуль записывает логи:

```
2026-03-07 12:00:00 - bot.handlers.start - INFO - Команда /start от пользователя 123456789
2026-03-07 12:00:01 - bot.utils.delayed_notification - INFO - ⏰ Запланировано 'Промо-сообщение (скидка 15%)' для пользователя 123456789 через 1 ч.
2026-03-07 12:00:01 - bot.utils.delayed_notification - INFO - ⏰ Запланировано 'Результаты заработка партнёров' для пользователя 123456789 через 24 ч.
2026-03-07 12:00:01 - bot.handlers.start - INFO - 📅 Промо-сообщение запланировано для нового пользователя 123456789
2026-03-07 12:00:01 - bot.handlers.start - INFO - 📅 Уведомление о результатах запланировано для нового пользователя 123456789

[Через 1 час]

2026-03-07 13:00:01 - bot.utils.delayed_notification - INFO - 🚀 Отправка 'Промо-сообщение (скидка 15%)' пользователю 123456789 (прошло 1 ч.)
2026-03-07 13:00:02 - bot.utils.delayed_notification - INFO - ✅ Промо-сообщение (скидка 15%) отправлено пользователю 123456789

[Через 24 часа]

2026-03-07 12:00:01 - bot.utils.delayed_notification - INFO - 🚀 Отправка 'Результаты заработка партнёров' пользователю 123456789 (прошло 24 ч.)
2026-03-07 12:00:02 - bot.utils.delayed_notification - INFO - ✅ Результаты заработка партнёров отправлено пользователю 123456789
```

---

## Изменение задержки

Для изменения задержки используйте параметр `delay_hours`:

```python
# Отправка первого уведомления через 2 часа вместо 1
await schedule_promo_notification(bot, user_id, delay_hours=2)

# Отправка второго уведомления через 48 часов вместо 24
await schedule_earnings_notification(bot, user_id, delay_hours=48)
```

---

## Отключение уведомлений

### Отключить второе уведомление для конкретного пользователя:

```python
from bot.utils.delayed_notification import cancel_notification

cancel_notification(user_id, "earnings_task")
```

### Отключить все уведомления для пользователя:

```python
from bot.utils.delayed_notification import cancel_all_notifications

cancel_all_notifications(user_id)
```

### Полностью отключить в коде:

Закомментируйте код в `bot/handlers/start.py`:

```python
# Если пользователь новый - планируем отправку уведомлений
# if is_new_user:
#     from bot.utils.delayed_notification import (
#         schedule_promo_notification,
#         schedule_earnings_notification
#     )
#     from bot import main as bot_module
#     
#     await schedule_promo_notification(bot_module.bot, user_id, delay_hours=1)
#     logger.info(f"📅 Промо-сообщение запланировано для нового пользователя {user_id}")
#     
#     await schedule_earnings_notification(bot_module.bot, user_id, delay_hours=24)
#     logger.info(f"📅 Уведомление о результатах запланировано для нового пользователя {user_id}")
```

---

## Особенности

- ✅ **Два уведомления** — через 1 час и через 24 часа
- ✅ **Индивидуальный таймер** — для каждого пользователя
- ✅ **Защита от дублирования** — уведомления не отправляются повторно
- ✅ **Отмена задач** — можно отменить любое уведомление
- ✅ **Обработка ошибок** — ошибки логируются, не ломают бота
- ✅ **Логирование** — полный контроль за процессом
- ✅ **Фоновый режим** — работает во время polling бота
- ✅ **Автоматическая очистка** — завершённые задачи удаляются из памяти

---

## Лимиты Telegram Bot API

- **30 сообщений в секунду** — соблюдается при массовой отправке
- **Блокировка пользователем** — ошибка логируется

---

## Отслеживание задач

### Проверить количество пользователей с задачами:

```python
from bot.utils.delayed_notification import get_pending_count

count = get_pending_count()
print(f"Пользователей с задачами: {count}")
```

### Проверить количество активных задач:

```python
from bot.utils.delayed_notification import get_active_tasks_count

count = get_active_tasks_count()
print(f"Активных задач: {count}")
```

---

## Тестирование

### Быстрое тестирование (без ожидания 24 часа):

Временно измените задержку в `bot/handlers/start.py`:

```python
# Первое уведомление через 1 минуту
await schedule_promo_notification(bot_module.bot, user_id, delay_hours=1/60)

# Второе уведомление через 2 минуты
await schedule_earnings_notification(bot_module.bot, user_id, delay_hours=2/60)
```

### Ручная отправка:

```python
from bot.utils.delayed_notification import send_message_to_user, EARNINGS_MESSAGE

# Отправить второе уведомление конкретному пользователю
await send_message_to_user(bot, telegram_id=123456789, message=EARNINGS_MESSAGE, notification_type="Тест")
```

---

## Сравнение версий

| Версия | Уведомление №1 | Уведомление №2 |
|--------|----------------|----------------|
| **v1.0** (старая) | Через 1 час всем пользователям после запуска бота | ❌ Нет |
| **v2.0** | Через 1 час каждому новому пользователю после `/start` | ❌ Нет |
| **v3.0** (новая) | Через 1 час каждому новому пользователю после `/start` | ✅ Через 24 часа |

---

## Структура данных

```python
pending_notifications: Dict[int, dict] = {
    123456789: {
        "promo_task": asyncio.Task,      # Задача №1 (1 час)
        "earnings_task": asyncio.Task     # Задача №2 (24 часа)
    },
    987654321: {
        "promo_task": None,               #已完成
        "earnings_task": asyncio.Task     # Активна
    }
}
```

---

**Создано:** 7 марта 2026 г.  
**Обновлено:** 7 марта 2026 г.  
**Версия:** 3.0.0  
**Статус:** ✅ Готово к использованию
