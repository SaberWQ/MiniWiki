from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notes.models import Category, Note, Tag, NoteTag, Comment


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начало заполнения базы данных...')

        # Создание тестовых пользователей
        users = []
        for i in range(1, 4):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={
                    'email': f'user{i}@example.com',
                    'first_name': f'Пользователь{i}',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Создан пользователь: {user.username}')
            users.append(user)

        # Создание категорий
        categories_data = [
            {'name': 'Программирование', 'description': 'Заметки о программировании и технологиях'},
            {'name': 'Личное', 'description': 'Личные заметки и мысли'},
            {'name': 'Работа', 'description': 'Рабочие заметки и проекты'},
            {'name': 'Обучение', 'description': 'Материалы для изучения'},
            {'name': 'Идеи', 'description': 'Идеи и планы'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Создана категория: {category.name}')
            categories.append(category)

        # Создание тегов
        tags_names = ['python', 'django', 'web', 'backend', 'frontend', 'база-данных', 
                      'api', 'tutorial', 'заметка', 'важно']
        tags = []
        for tag_name in tags_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'Создан тег: {tag.name}')
            tags.append(tag)

        # Создание заметок
        notes_data = [
            {
                'title': 'Введение в Django',
                'content': '''Django - это высокоуровневый Python веб-фреймворк, который позволяет быстро создавать безопасные и масштабируемые веб-приложения.

Основные компоненты Django:
- Models (Модели) - для работы с базой данных
- Views (Представления) - для обработки запросов
- Templates (Шаблоны) - для отображения данных
- URLconf - для маршрутизации URL

Django следует принципу DRY (Don't Repeat Yourself) и использует архитектуру MTV (Model-Template-View).''',
                'category': categories[0],
                'is_public': True,
                'tags': [tags[0], tags[1], tags[7]]
            },
            {
                'title': 'Работа с моделями Django ORM',
                'content': '''Django ORM (Object-Relational Mapping) предоставляет мощный интерфейс для работы с базой данных.

Пример создания модели:

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

Основные операции:
- Article.objects.all() - получить все записи
- Article.objects.filter(title__contains='Django') - фильтрация
- Article.objects.get(id=1) - получить одну запись
- article.save() - сохранить изменения
- article.delete() - удалить запись''',
                'category': categories[0],
                'is_public': True,
                'tags': [tags[0], tags[1], tags[5]]
            },
            {
                'title': 'Список дел на неделю',
                'content': '''План задач на эту неделю:

1. Завершить проект мини-wiki
2. Изучить Docker для деплоя приложений
3. Прочитать документацию по Django REST Framework
4. Написать тесты для основных функций
5. Обновить резюме

Важные встречи:
- Понедельник 10:00 - встреча с командой
- Среда 14:00 - код-ревью
- Пятница 16:00 - демо проекта''',
                'category': categories[2],
                'is_public': False,
                'tags': [tags[9]]
            },
            {
                'title': 'Идея: Приложение для трекинга привычек',
                'content': '''Концепция приложения для отслеживания ежедневных привычек.

Основной функционал:
- Создание и управление привычками
- Ежедневные напоминания
- Статистика и визуализация прогресса
- Мотивационные цитаты
- Система достижений

Технологии:
- Backend: Django + Django REST Framework
- Frontend: React или Vue.js
- Mobile: React Native
- База данных: PostgreSQL

Монетизация:
- Бесплатная версия с ограничениями
- Premium подписка для расширенных функций''',
                'category': categories[4],
                'is_public': True,
                'tags': [tags[0], tags[6]]
            },
            {
                'title': 'Конспект: Асинхронное программирование в Python',
                'content': '''Асинхронное программирование позволяет эффективно обрабатывать множество задач одновременно.

Ключевые концепции:
- async/await - синтаксис для асинхронных функций
- Корутины - функции, которые могут приостанавливать выполнение
- Event Loop - цикл обработки событий
- asyncio - библиотека для асинхронного программирования

Пример:

import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "Данные получены"

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())

Преимущества:
- Эффективное использование ресурсов
- Лучшая производительность при I/O операциях
- Масштабируемость приложений''',
                'category': categories[3],
                'is_public': True,
                'tags': [tags[0], tags[7]]
            },
        ]

        for i, note_data in enumerate(notes_data):
            note, created = Note.objects.get_or_create(
                title=note_data['title'],
                defaults={
                    'content': note_data['content'],
                    'author': users[i % len(users)],
                    'category': note_data['category'],
                    'is_public': note_data['is_public'],
                }
            )
            if created:
                # Добавление тегов
                for tag in note_data['tags']:
                    NoteTag.objects.create(note=note, tag=tag)
                
                self.stdout.write(f'Создана заметка: {note.title}')
                
                # Добавление комментариев к некоторым заметкам
                if i % 2 == 0:
                    Comment.objects.create(
                        note=note,
                        author=users[(i + 1) % len(users)],
                        text='Отличная заметка! Очень полезная информация.'
                    )

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))