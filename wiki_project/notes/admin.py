from django.contrib import admin
from .models import Note, Category, Tag, NoteTag, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'notes_count')
    search_fields = ('name', 'description')
    list_per_page = 20
    
    def notes_count(self, obj):
        return obj.notes.count()
    notes_count.short_description = 'Количество заметок'


class NoteTagInline(admin.TabularInline):
    model = NoteTag
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'created_at')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_public', 'created_at', 'views_count')
    list_filter = ('is_public', 'category', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at', 'views_count')
    list_per_page = 20
    date_hierarchy = 'created_at'
    inlines = [NoteTagInline, CommentInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'author')
        }),
        ('Категоризация', {
            'fields': ('category', 'is_public')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at', 'views_count'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Если создается новый объект
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'notes_count')
    search_fields = ('name',)
    
    def notes_count(self, obj):
        return obj.note_tags.count()
    notes_count.short_description = 'Количество заметок'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('note', 'author', 'text_preview', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username', 'note__title')
    readonly_fields = ('created_at',)
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст'