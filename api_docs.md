# Документация по API телеграм бота

## Обзор

Этот документ описывает API для админ-панели телеграм бота юридической фирмы.

## Аутентификация

Все API-запросы к админ-панели не требуют аутентификации. В продакшене рекомендуется добавить аутентификацию.

## Заявки

### Получение списка заявок

```
GET /api/requests
```

#### Ответ

```json
[
  {
    "id": 1,
    "user_id": 123456,
    "description": "Описание проблемы...",
    "status": "новый",
    "created_at": "2023-10-20T10:30:00",
    "updated_at": "2023-10-20T10:30:00",
    "user": {
      "id": 123,
      "telegram_id": 123456,
      "username": "username",
      "first_name": "Имя",
      "last_name": "Фамилия"
    }
  }
]
```

### Обновление статуса заявки

```
PUT /api/requests/{request_id}
```

#### Тело запроса

```json
{
  "status": "в работе"
}
```

#### Ответ

```json
{
  "message": "Статус заявки обновлен"
}
```

## Партнеры

### Получение списка партнеров

```
GET /api/partners
```

#### Ответ

```json
[
  {
    "id": 1,
    "user_id": 123,
    "full_name": "Иванов Иван Иванович",
    "company_name": "ООО Ромашка",
    "phone": "+79991234567",
    "email": "ivanov@example.com",
    "specialization": "Налоговое право",
    "experience": 5,
    "consent_to_share_data": true,
    "created_at": "2023-10-20T10:30:00",
    "updated_at": "2023-10-20T10:30:00"
  }
]
```

## Рассылка

### Отправка рассылки

```
POST /api/broadcast
```

#### Тело запроса

```json
{
  "message": "Текст сообщения для рассылки"
}
```

#### Ответ

```json
{
  "message": "Рассылка успешно отправлена",
  "sent_count": 15
}
```

## Ошибки

В случае ошибки API возвращает JSON-объект с деталями:

```json
{
  "detail": "Описание ошибки"
}
```

### Возможные коды ошибок:

- `400 Bad Request` - Некорректный запрос
- `404 Not Found` - Ресурс не найден
- `500 Internal Server Error` - Внутренняя ошибка сервера

## Модели данных

### User

| Поле | Тип | Описание |
|------|-----|----------|
| id | integer | Уникальный ID пользователя |
| telegram_id | integer | Telegram ID пользователя |
| username | string | Username пользователя |
| first_name | string | Имя пользователя |
| last_name | string | Фамилия пользователя |
| registered_at | datetime | Дата регистрации |
| is_active | boolean | Статус активности |

### PartnerProfile

| Поле | Тип | Описание |
|------|-----|----------|
| id | integer | Уникальный ID профиля |
| user_id | integer | ID связанного пользователя |
| full_name | string | Полное имя |
| company_name | string | Название компании |
| phone | string | Телефон |
| email | string | Email |
| specialization | string | Специализация |
| experience | integer | Опыт в годах |
| consent_to_share_data | boolean | Согласие на передачу данных |
| created_at | datetime | Дата создания |
| updated_at | datetime | Дата последнего обновления |

### ServiceRequest

| Поле | Тип | Описание |
|------|-----|----------|
| id | integer | Уникальный ID заявки |
| user_id | integer | ID пользователя, создавшего заявку |
| description | string | Описание проблемы |
| status | string | Статус заявки (новый, в работе, выполнен) |
| created_at | datetime | Дата создания |
| updated_at | datetime | Дата последнего обновления |

### RequestDocument

| Поле | Тип | Описание |
|------|-----|----------|
| id | integer | Уникальный ID документа |
| request_id | integer | ID связанной заявки |
| file_path | string | Путь к файлу |
| file_type | string | Тип файла |
| uploaded_at | datetime | Дата загрузки |