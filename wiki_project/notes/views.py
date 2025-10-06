from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.contrib import messages
from .models import Note, Category, Tag, NoteTag, Comment
from .forms import NoteForm, CommentForm, UserRegisterForm, SearchForm


class HomeView(ListView):
    """Главная страница со списком заметок"""
    model = Note
    template_name = 'notes/home.html'
    context_object_name = 'notes'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Note.objects.select_related('author', 'category').annotate(
            comments_count=Count('comments')
        )
        
        # Если пользователь авторизован, показываем его заметки + публичные
        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(author=self.request.user) | Q(is_public=True)
            )
        else:
            # Неавторизованным показываем только публичные
            queryset = queryset.filter(is_public=True)
        
        # Поиск
        search_query = self.request.GET.get('query')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        # Фильтр по категории
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        context['categories'] = Category.objects.annotate(
            notes_count=Count('notes')
        )
        return context


class NoteDetailView(DetailView):
    """Детальная страница заметки"""
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Авторизованный пользователь видит свои и публичные заметки
        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(author=self.request.user) | Q(is_public=True)
            )
        # Неавторизованные видят только публичные
        return queryset.filter(is_public=True)
    
    def get_object(self):
        obj = super().get_object()
        # Увеличиваем счетчик просмотров
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        context['tags'] = self.object.note_tags.select_related('tag')
        return context


class NoteCreateView(LoginRequiredMixin, CreateView):
    """Создание новой заметки"""
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        # Обработка тегов
        tags_string = form.cleaned_data.get('tags', '')
        if tags_string:
            tag_names = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                NoteTag.objects.create(note=self.object, tag=tag)
        
        messages.success(self.request, 'Заметка успешно создана!')
        return response


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование заметки"""
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    
    def test_func(self):
        note = self.get_object()
        return self.request.user == note.author
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Обновление тегов
        self.object.note_tags.all().delete()
        tags_string = form.cleaned_data.get('tags', '')
        if tags_string:
            tag_names = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                NoteTag.objects.create(note=self.object, tag=tag)
        
        messages.success(self.request, 'Заметка успешно обновлена!')
        return response


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление заметки"""
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        note = self.get_object()
        return self.request.user == note.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Заметка успешно удалена!')
        return super().delete(request, *args, **kwargs)


@login_required
def add_comment(request, pk):
    """Добавление комментария к заметке"""
    note = get_object_or_404(Note, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.note = note
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
        else:
            messages.error(request, 'Ошибка при добавлении комментария')
    
    return redirect('note_detail', pk=pk)


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})


class MyNotesView(LoginRequiredMixin, ListView):
    """Список заметок текущего пользователя"""
    model = Note
    template_name = 'notes/my_notes.html'
    context_object_name = 'notes'
    paginate_by = 10
    
    def get_queryset(self):
        return Note.objects.filter(author=self.request.user).select_related('category')


class CategoryNotesView(ListView):
    """Список заметок по категории"""
    model = Note
    template_name = 'notes/category_notes.html'
    context_object_name = 'notes'
    paginate_by = 10
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        queryset = Note.objects.filter(category=self.category)
        
        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(author=self.request.user) | Q(is_public=True)
            )
        else:
            queryset = queryset.filter(is_public=True)
        
        return queryset.select_related('author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context