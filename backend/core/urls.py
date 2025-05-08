from django.urls import path
from .views import PropertyListCreateView, SignupView, ProfileView, BookingListCreateView

urlpatterns = [
    path('properties/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
]
