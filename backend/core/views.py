from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, filters
from .models import Property, User, Booking
from .serializers import PropertySerializer, SignupSerializer, UserSerializer, BookingSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse



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

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)

class HostBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(property__host=self.request.user).order_by('-created_at')

class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, property_id):
        property = get_object_or_404(Property, id=property_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': property.title,
                    },
                    'unit_amount': int(property.price_per_night * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:3000/cancel',
            metadata={
                'user_id': request.user.id,
                'property_id': property.id,
            }
        )
        return Response({'checkout_url': session.url})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})
        user = User.objects.get(id=metadata['user_id'])
        property = Property.objects.get(id=metadata['property_id'])

        # Create booking with dummy dates (we'll refine later)
        Booking.objects.create(
            guest=user,
            property=property,
            check_in="2025-07-01",  # temporary
            check_out="2025-07-05"
        )

    return HttpResponse(status=200)
