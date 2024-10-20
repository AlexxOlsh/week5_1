from django.urls import path
from .views import *

urlpatterns = [
    path('api/notes/', NoteListAPI.as_view(), name='note_list'),
    path('api/notes/<int:pk>/', NoteDetailAPI.as_view(), name='apinote_detail'),
    path('notes/', NoteListView.as_view(), name='notes'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('api/admin/users/',  UserListAPI.as_view(), name='user_list'),
    path('api/admin/users/<int:pk>/',  UserDetailAPI.as_view(), name='user_detail'),
]