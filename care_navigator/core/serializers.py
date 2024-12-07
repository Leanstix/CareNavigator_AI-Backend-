from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Provider, Appointment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number']


class ProviderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Provider
        fields = ['id', 'user', 'specialty', 'location', 'rating']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    provider = serializers.StringRelatedField()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'provider', 'date', 'status']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token