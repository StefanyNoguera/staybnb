from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .models import Property, User
from .serializers import PropertySerializer, SignupSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['city', 'country']

    def perform_create(self, serializer):
        if not self.request.user.is_host:
            raise PermissionDenied("Only hosts can create properties")
        serializer.save(host=self.request.user)

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]
