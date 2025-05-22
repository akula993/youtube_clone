import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_clone.settings')
django.setup()

from users.models import CustomUser
from videos.models import Video, Category
from comments.models import Comment
from django.core.files.uploadedfile import SimpleUploadedFile

# Создаем категории
categories = ['Музыка', 'Образование', 'Игры', 'Новости', 'Спорт', 'Технологии', 'Развлечения']

for cat_name in categories:
    Category.objects.get_or_create(name=cat_name)

# Создаем тестовых пользователей
test_users = [
    {'username': 'john_doe', 'email': 'john@example.com', 'password': 'testpass123'},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'testpass123'},
    {'username': 'tech_guru', 'email': 'tech@example.com', 'password': 'testpass123'},
]

for user_data in test_users:
    if not CustomUser.objects.filter(username=user_data['username']).exists():
        user = CustomUser.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        user.bio = f"Привет! Я {user_data['username']}. Добро пожаловать на мой канал!"
        user.save()

print("Тестовые данные созданы успешно!")
