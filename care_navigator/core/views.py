from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User, Provider, Appointment
from .serializers import UserSerializer, ProviderSerializer, AppointmentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


# View for getting and updating user details
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data['username'],
                password=request.data['password'],
                email=request.data.get('email', ''),
                role=request.data.get('role', 'patient'),
                phone_number=request.data.get('phone_number', ''),
            )
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return Response({"message": "Logout successful!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# View for retrieving and searching providers
class ProviderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        specialty = request.query_params.get('specialty', None)
        location = request.query_params.get('location', None)
        providers = Provider.objects.all()

        if specialty:
            providers = providers.filter(specialty__icontains=specialty)
        if location:
            providers = providers.filter(location__icontains=location)

        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# View for managing appointments
class AppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get appointments for the authenticated user
        if request.user.role == 'patient':
            appointments = Appointment.objects.filter(patient=request.user)
        else:
            provider = Provider.objects.get(user=request.user)
            appointments = Appointment.objects.filter(provider=provider)

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role != 'patient':
            return Response({"error": "Only patients can book appointments."}, status=status.HTTP_403_FORBIDDEN)

        provider_id = request.data.get('provider_id')
        date = request.data.get('date')

        try:
            provider = Provider.objects.get(id=provider_id)
        except Provider.DoesNotExist:
            return Response({"error": "Provider not found."}, status=status.HTTP_404_NOT_FOUND)

        appointment = Appointment.objects.create(patient=request.user, provider=provider, date=date)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
