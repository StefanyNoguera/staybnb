from django.urls import path
from .views import PropertyListCreateView, SignupView, ProfileView, BookingListCreateView, HostBookingListView, CreateCheckoutSessionView, stripe_webhook

urlpatterns = [
    path('properties/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('host/bookings/', HostBookingListView.as_view(), name='host-bookings'),
    path('create-checkout-session/<int:property_id>/', CreateCheckoutSessionView.as_view(), name='create-checkout'),
    path('webhook/stripe/', stripe_webhook, name='stripe-webhook'),
]
