from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """Модель категории для организации заметок"""
    name = models.CharField('Название категории', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Note(models.Model):
    """Основная модель для заметок"""
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Автор',
        related_name='notes'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='notes'
    )
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_public = models.BooleanField('Публичная заметка', default=False)
    views_count = models.PositiveIntegerField('Количество просмотров', default=0)
    
    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('note_detail', kwargs={'pk': self.pk})
    
    def increment_views(self):
        """Увеличение счетчика просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Tag(models.Model):
    """Модель тегов для заметок"""
    name = models.CharField('Название тега', max_length=50, unique=True)
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class NoteTag(models.Model):
    """Связь между заметками и тегами"""
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='note_tags')
    
    class Meta:
        unique_together = ('note', 'tag')
        verbose_name = 'Тег заметки'
        verbose_name_plural = 'Теги заметок'


class Comment(models.Model):
    """Модель комментариев к заметкам"""
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Заметка'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
    
    def __str__(self):
        return f'Комментарий от {self.author.username} к "{self.note.title}"'