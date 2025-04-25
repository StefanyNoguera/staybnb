from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Property
from .serializers import PropertySerializer

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)
