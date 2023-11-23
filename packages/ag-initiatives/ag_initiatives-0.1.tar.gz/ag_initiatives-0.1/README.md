# Система "Активный Гражданин" Backend

## Инструкция по разворачиванию проекта локально
Команды выполняем с корня проекта.

---
 - Копируем проект с гитлаба
```bash
# Если установлены ключи SSH
git clone ssh://git@git.cifra-k.ru:1022/voting-system/voting-core-backend.git
# Если ключей SSH нет (скорее всего потребуется ввод логина и пароля от гитлаба)
git clone http://git.cifra-k.ru/voting-system/voting-core-backend.git
```

---
 - Меняем ветку на `master_build`
```bash
git checkout master_build
```

---
- Запуск происходит через [docker-compose](https://docs.docker.com/) командой
```bash
docker-compose up -d
```

---
- Далее необходимо запустить миграцию командой
```bash
docker-compose exec server python manage.py migrate
```

---
- Теперь создаем супер-пользователя
```bash
docker-compose exec server python manage.py createsuperuser
```

---
- [Можно пользоваться (ссылка на административный интерфейс)](http://127.0.0.1:8000/admin/)

