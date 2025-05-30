# YouTube Clone - Django

🎬 Полнофункциональный клон YouTube, созданный на Django

## 🚀 Возможности
- 📺 Загрузка и просмотр видео
- 👥 Система пользователей и каналов
- 💬 Комментарии с ответами
- 📋 Плейлисты с управлением
- 🔔 Система уведомлений
- 🔍 Поиск и рекомендации
- 📱 Адаптивный дизайн
- ⭐ Лайки и подписки

## 🛠 Технологии
- **Backend:** Django 4.2.7, SQLite
- **Frontend:** Bootstrap 5, jQuery
- **UI:** Crispy Forms, Font Awesome
- **Медиа:** Pillow для изображений

## ⚡ Быстрый старт
```bash
# Клонировать репозиторий
git clone https://github.com/akula993/youtube_clone.git
cd youtube_clone

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Выполнить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver
