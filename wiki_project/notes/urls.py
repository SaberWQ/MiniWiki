from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('note/new/', views.NoteCreateView.as_view(), name='note_create'),
    path('note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    path('note/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('my-notes/', views.MyNotesView.as_view(), name='my_notes'),
    path('category/<int:pk>/', views.CategoryNotesView.as_view(), name='category_notes'),
    path('register/', views.register, name='register'),
]