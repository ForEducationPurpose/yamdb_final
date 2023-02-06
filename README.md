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

Проект доступен по адресу  51.250.110.142 или learnproject.ddns.net и поделен на 3 контейнера, контейнер приложения web,
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
## 3. Техническая информация

Стек технологий: Python 3, Django, Django Rest, Docker, PostgreSQL, Nginx.

---
## 4. Об авторах 
Лобанов Максим

Никитина Вероника 

Абрамов Александр
