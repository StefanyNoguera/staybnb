from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .models import Property, User
from .serializers import PropertySerializer, UserSerializer
from django.contrib.auth import get_user_model

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['city', 'country']

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

class SignupView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
