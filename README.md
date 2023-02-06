![Workflow](https://github.com/ForEducationPurpose/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)
# API для базы данных YaMDb

---
## 1. Описание

Проект предназначен для взаимодействия с API социальной сети YaMDb.
YaMDb собирает отзывы пользователей на различные произведения.

API предоставляет возможность взаимодействовать с базой данных по следующим направлениям:
  - авторизироваться
  - создавать свои отзывы и управлять ими (корректировать\удалять)
  - просматривать и комментировать отзывы других пользователей
  - просматривать комментарии к своему и другим отзывам
  - просматривать произведения, категории и жанры произведений

работающий проект доступен по адресу  51.250.110.142  и поделен на 3 контейнера, контейнер приложения web,
контейнер базы db, работающий на порту 5432, контейнер с сервером nginx, использующийся как прокси и передающий с 80 порта на 80 порт приложения.
Данные работы контейнеров сохраняются на тома values.



---
## 2. Команды для запуска

Перед запуском необходимо склонировать проект:
```bash
HTTPS: git clone https://github.com/ForEducationPurpose/yamdb_final.git
SSH: git@github.com:ForEducationPurpose/yamdb_final.git
```
Убедитесь, что на компьюетере установлен [Docker](https://docs.docker.com/desktop/install/linux-install/ "ссылка на гайд для Linux" ) и [Docker-compose](https://docs.docker.com/compose/install/ "на docker-compose")

Перед запуском сделайте файл .env и поместите его в папку infra, шаблон заполнения посмотрите в [.env.template](https://github.com/ForEducationPurpose/yamdb_final/blob/master/infra/.env.template "шаблон")

После клонирования проекта откройте терминал и перейдите в папку, где лежит файл docker-compose.yaml

<h2>Запустите контейнеры:</h2>
<h3> 1. Разверните контейнеры с помощью docker-compose </h3>
```docker-compose up -d
```
<h3> 2. Выполните миграции </h3>
```docker-compose exec web python manage.py migrate
```
<h3> 3. Создайте суперпользователя </h3>
```docker-compose exec web python manage.py createsuperuser
```
<h3> 4. Сделайте доступной раздачу статики </h3>
```docker-compose exec web python manage.py collecstatic --no-input
```

---
## 3. Структура проекта

Список эндпоинтов:
```
/api/v1/auth/signup/
/api/v1/auth/token/
/api/v1/categories/
/api/v1/categories/{slug}/
/api/v1/genres/
/api/v1/genres/{slug}/
/api/v1//titles/
/api/v1/titles/{titles_id}/
/api/v1/{title_id}/reviews/
/api/v1/titles/{title_id}/reviews/{review_id}/
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
/api/v1/users/
/api/v1/users/{username}/
/api/v1/users/me/
```
---
## 4. Примеры запросов
Все пути начинаются с ваш_хост/api/v1/...
Регистрация нового пользователя
Уровень доступа: без токена
POST auth/signup
```
{
  "email": "string",
  "username": "string"
}
```
Получение JWT-токена
Уровень доступа: без токена
POST auth/token
```
{
  "username": "string",
  "confirmation_code": "string"
}
```
Получение списка всех категорий
Уровень доступа: без токена
GET /categories/ 
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
Добавление новой категории
Уровень доступа: админ
POST /categories/
```
{
  "name": "string",
  "slug": "string"
}
```
Получение списка всех произведений
Уровень доступа: без токена
GET /titles/ 
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
Добавление произведения
Права доступа: Администратор.
POST /titles/
Пример запроса
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
---
## 5. Техническая информация

Стек технологий: Python 3, Django, Django Rest, Docker, PostgreSQL, Nginx.

---
## 6. Об авторах 
Лобанов Максим

Никитина Вероника 

Абрамов Александр
