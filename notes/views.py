from rest_framework import generics, permissions
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Note
from .serializers import NoteSerializer, UserSerializer
from django.contrib.auth import get_user_model
from .forms import NoteForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import DetailView, ListView


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UserListAPI(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class NoteListAPI(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteListView(ListView):
    model = Note
    template_name = 'notes_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'message': 'Deleted'}, status=200)