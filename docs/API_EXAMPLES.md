# 📚 Примеры использования API TgWork

---

## 1️⃣ Регистрация и Профиль

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_id": 123456789,
    "first_name": "Иван",
    "last_name": "Петров",
    "telegram_username": "ivan_petrov",
    "avatar_url": "https://example.com/avatar.jpg",
    "bio": "Фронтенд разработчик",
    "skills": "React, TypeScript, Vue.js"
  }'
```

**Response:**
```json
{
  "id": 1,
  "telegram_id": 123456789,
  "first_name": "Иван",
  "last_name": "Петров",
  "avatar_url": "https://example.com/avatar.jpg",
  "rating": 0.0,
  "total_reviews": 0,
  "balance": 0.0,
  "total_earned": 0.0,
  "total_spent": 0.0,
  "completed_orders": 0,
  "created_at": "2025-12-31T12:00:00",
  "is_active": true,
  "is_banned": false
}
```

### Получить профиль

```bash
curl "http://localhost:8000/api/v1/users/1"
```

### Обновить профиль

```bash
curl -X PUT "http://localhost:8000/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Опытный фронтенд разработчик",
    "skills": "React, TypeScript, Vue.js, Tailwind CSS"
  }'
```

---

## 2️⃣ Создание и Поиск Услуг

### Создать услугу

```bash
curl -X POST "http://localhost:8000/api/v1/services/" \
  -H "Content-Type: application/json" \
  -d '{
    "seller_id": 1,
    "title": "Создам красивый и функциональный веб-сайт на React",
    "description": "Создам для вас современный сайт используя React, TypeScript и Tailwind CSS. Включает адаптивный дизайн, оптимизацию для SEO и чистый код.",
    "category": "Программирование",
    "tags": "React, Frontend, Web Development, UI/UX",
    "price": 15000.0,
    "execution_days": 7,
    "revision_count": 3,
    "preview_url": "https://example.com/preview.jpg"
  }'
```

### Получить услугу

```bash
curl "http://localhost:8000/api/v1/services/1"
```

### Список услуг по категории

```bash
curl "http://localhost:8000/api/v1/services/?category=Программирование&skip=0&limit=20"
```

### Поиск услуг

```bash
curl "http://localhost:8000/api/v1/services/search/?q=React%20веб"
```

### Услуги конкретного продавца

```bash
curl "http://localhost:8000/api/v1/services/seller/1/?skip=0&limit=50"
```

---

## 3️⃣ Заказы и Оплата

### Создать заказ (купить услугу)

```bash
curl -X POST "http://localhost:8000/api/v1/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "buyer_id": 2,
    "service_id": 1,
    "buyer_comment": "Нужен сайт для моего стартапа. Макет есть в Figma."
  }'
```

**Response:**
```json
{
  "id": 1,
  "buyer_id": 2,
  "seller_id": 1,
  "service_id": 1,
  "price": 15000.0,
  "platform_fee_percent": 10.0,
  "seller_gets": 13500.0,
  "status": "waiting_payment",
  "is_paid": false,
  "payment_date": null,
  "deadline": "2026-01-07T12:00:00",
  "revisions_used": 0,
  "revisions_allowed": 3,
  "created_at": "2025-12-31T12:30:00",
  "completed_at": null,
  "updated_at": "2025-12-31T12:30:00"
}
```

### Оплатить заказ

```bash
curl -X POST "http://localhost:8000/api/v1/orders/1/pay" \
  -H "Content-Type: application/json" \
  -d '{
    "buyer_id": 2
  }'
```

### Получить заказ

```bash
curl "http://localhost:8000/api/v1/orders/1"
```

### Получить мои заказы (как покупатель)

```bash
curl "http://localhost:8000/api/v1/orders/buyer/2/?skip=0&limit=20"
```

### Получить мои заказы (как продавец)

```bash
curl "http://localhost:8000/api/v1/orders/seller/1/?skip=0&limit=20"
```

### Обновить статус заказа (продавец отправил результат)

```bash
curl -X PUT "http://localhost:8000/api/v1/orders/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "under_review",
    "seller_result": "Готовая версия сайта на GitHub: https://github.com/example/my-site"
  }'
```

### Завершить заказ (покупатель принял работу)

```bash
curl -X PUT "http://localhost:8000/api/v1/orders/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

---

## 4️⃣ Чат в Заказе

### Отправить сообщение

```bash
curl -X POST "http://localhost:8000/api/v1/orders/1/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "author_id": 2,
    "text": "Получил результат, выглядит отлично! Но попроси ещё немного изменить цвет кнопок.",
    "attachments": "[\"https://example.com/feedback.png\"]"
  }'
```

### Получить историю сообщений

```bash
curl "http://localhost:8000/api/v1/orders/1/messages/?skip=0&limit=50&user_id=2"
```

### Отредактировать сообщение

```bash
curl -X PUT "http://localhost:8000/api/v1/orders/1/messages/1" \
  -H "Content-Type: application/json" \
  -d '{
    "author_id": 2,
    "text": "Получил результат, выглядит отлично! Но попроси ещё немного изменить цвета."
  }'
```

---

## 5️⃣ Отзывы и Рейтинг

### Оставить отзыв

```bash
curl -X POST "http://localhost:8000/api/v1/orders/1/review/" \
  -H "Content-Type: application/json" \
  -d '{
    "reviewer_id": 2,
    "rating": 5,
    "text": "Отличная работа! Всё сделано быстро и качественно. Буду сотрудничать снова."
  }'
```

### Получить отзыв на заказ

```bash
curl "http://localhost:8000/api/v1/orders/1/review/"
```

### Получить все отзывы продавца

```bash
curl "http://localhost:8000/api/v1/orders/user/1/reviews/?skip=0&limit=50"
```

### Топ-рейтинговые продавцы

```bash
curl "http://localhost:8000/api/v1/orders/top-rated/?limit=10"
```

### Отзывы с конкретной оценкой

```bash
curl "http://localhost:8000/api/v1/orders/by-rating/?rating=5"
```

---

## 🔄 Полный Цикл Заказа

```
1. Регистрация
   POST /api/v1/users/register

2. Создание услуги (продавец)
   POST /api/v1/services/

3. Поиск услуги (покупатель)
   GET /api/v1/services/search/?q=...

4. Создание заказа (покупатель)
   POST /api/v1/orders/

5. Оплата заказа (покупатель)
   POST /api/v1/orders/{id}/pay

6. Общение в чате
   POST /api/v1/orders/{id}/messages/
   GET /api/v1/orders/{id}/messages/

7. Отправка результата (продавец)
   PUT /api/v1/orders/{id}
   status: under_review

8. Завершение заказа (покупатель)
   PUT /api/v1/orders/{id}
   status: completed

9. Оставление отзыва (покупатель)
   POST /api/v1/orders/{id}/review/

10. Продавец получает деньги и его рейтинг обновляется
```

---

## 🧪 Тестирование

Используйте Swagger UI для интерактивного тестирования:
```
http://localhost:8000/docs
```

Или используйте Postman/Insomnia с этими примерами.

---

## 📝 Замечания

- Все денежные суммы в рублях
- Даты в формате ISO 8601
- Все ID должны быть целыми числами
- Пользователь может быть одновременно покупателем и продавцом
- Баланс в БД хранится для быстрого доступа (в реальном приложении нужна более продвинутая система)
