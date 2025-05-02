from django.urls import path
from .views import PropertyListCreateView, SignupView, ProfileView

urlpatterns = [
    path('properties/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='user-profile')
]
