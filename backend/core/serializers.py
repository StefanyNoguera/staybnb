from rest_framework import serializers
from .models import User, Property, Booking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_host']

class PropertySerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)

    class Meta:
        model = Property
        fields = '__all__'

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_host']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # hashes the password
        user.save()
        return user

class BookingSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-in date must be before check-out date.")

        property = data['property']
        check_in = data['check_in']
        check_out = data['check_out']

        overlapping = Booking.objects.filter(
            property=property,
            check_in__lt=check_out,
            check_out__gt=check_in,
        )

        if overlapping.exists():
            raise serializers.ValidationError("This property is already booked for these dates.")

        return data
