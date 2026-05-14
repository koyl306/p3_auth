# Flask Auth Blog API

REST API для блог-платформи з JWT автентифікацією, RBAC, refresh token системою та SQLite базою даних.

---

# Функціонал

## Authentication

- Register
- Login
- JWT Access Token
- JWT Refresh Token
- Logout
- Refresh token invalidation

---

## RBAC

Ролі:

- admin
- author
- reader

---

## User Profile

Користувач може:

- оновлювати bio
- оновлювати avatar_url
- змінювати пароль

---

## Security

- bcrypt password hashing
- JWT auth
- password validation
- rate limiting (5 login attempts / 15 min)

---

# Технології

- Python
- Flask
- SQLite
- SQLAlchemy
- JWT
- bcrypt
- Flask-Limiter

---

# Встановлення

## 1. Створити venv

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 2. Встановити залежності

```bash
pip install -r requirements.txt
```

---

## 3. Створити .env

```env
ACCESS_SECRET=access_secret_key
REFRESH_SECRET=refresh_secret_key
```

---

## 4. Запуск

```bash
python app.py
```

---

# База даних

SQLite файл:

```txt
database.db
```

Автоматично створюються таблиці:

* user
* refresh_token

---

# API Endpoints

| Method | Endpoint              | Description            |
| ------ | --------------------- | ---------------------- |
| POST   | /auth/register        | Реєстрація             |
| POST   | /auth/login           | Логін                  |
| POST   | /auth/refresh         | Оновлення access token |
| POST   | /auth/logout          | Logout                 |
| PUT    | /auth/profile         | Оновлення профілю      |
| POST   | /auth/change-password | Зміна пароля           |
| GET    | /admin/users          | Список користувачів    |

---

# Password Rules

Пароль повинен містити:

* мінімум 8 символів
* 1 велику літеру
* 1 малу літеру
* 1 цифру

---

# Authorization Header

```txt
Authorization: Bearer ACCESS_TOKEN
```

---

# CURL Examples

## Register

```bash
curl -X POST http://127.0.0.1:5000/auth/register \
-H "Content-Type: application/json" \
-d "{
    \"username\":\"admin\",
    \"email\":\"admin@gmail.com\",
    \"password\":\"Password123\",
    \"role\":\"admin\"
}"
```

---

## Login

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
-H "Content-Type: application/json" \
-d "{
    \"email\":\"admin@gmail.com\",
    \"password\":\"Password123\"
}"
```

---

## Refresh Token

```bash
curl -X POST http://127.0.0.1:5000/auth/refresh \
-H "Content-Type: application/json" \
-d "{
    \"refresh_token\":\"YOUR_REFRESH_TOKEN\"
}"
```

---

## Logout

```bash
curl -X POST http://127.0.0.1:5000/auth/logout \
-H "Content-Type: application/json" \
-d "{
    \"refresh_token\":\"YOUR_REFRESH_TOKEN\"
}"
```

---

## Update Profile

```bash
curl -X PUT http://127.0.0.1:5000/auth/profile \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ACCESS_TOKEN" \
-d "{
    \"bio\":\"Python developer\",
    \"avatar_url\":\"https://example.com/avatar.jpg\"
}"
```

---

## Change Password

```bash
curl -X POST http://127.0.0.1:5000/auth/change-password \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ACCESS_TOKEN" \
-d "{
    \"old_password\":\"Password123\",
    \"new_password\":\"NewPassword123\"
}"
```

---

## Admin Get Users

```bash
curl -X GET http://127.0.0.1:5000/admin/users \
-H "Authorization: Bearer ACCESS_TOKEN"
```

---

# Postman / Insomnia

Для тестування можна імпортувати curl-запити у:

* Postman
* Insomnia

---

# Авторизація

## Access Token

* живе 15 хвилин

## Refresh Token

* живе 7 днів
* зберігається у БД

---

# Rate Limiting

Login endpoint:

```txt
5 requests / 15 minutes
```

---

# RBAC

## admin

Може:

* переглядати всіх користувачів

## author

Може:

* працювати зі своїм профілем

## reader

Може:

* працювати зі своїм профілем
