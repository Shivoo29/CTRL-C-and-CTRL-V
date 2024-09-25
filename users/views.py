from django.shortcuts import render
from .models import User , Report, UserLocation
from .serialisers import UserRegistrationSerializer , UserLoginSerializer , UserDetailSerializer, ReportSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import status
from .utils import calculate_distance


# Create your views here.
# manually generate token 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self, request, format =None):
        serializer = UserRegistrationSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token= get_tokens_for_user(user)
            return Response({'token': token},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    # renderer_classes= [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                tokens = get_tokens_for_user(user)
                response_data = {
                    'refresh': tokens['refresh'],
                    'access': tokens['access'],
                    'msg': 'login success'
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AllUserDetail(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    

class UserProfileDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    # For fetching details of the logged in user
    def get(self, request):
        user = request.user
        serializer_data = UserDetailSerializer(user).data
        return Response(serializer_data, status=status.HTTP_200_OK)
    


class ReportCreateView(CreateAPIView):
    # permission_classes= [IsAuthenticated]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class UpdateLocationView(APIView):
    def post(self, request):
        user = request.user  # assuming the user is authenticated
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        if latitude and longitude:
            # Update the user's location
            user_location, created = UserLocation.objects.get_or_create(user=user)
            user_location.latitude = latitude
            user_location.longitude = longitude
            user_location.save()

            # Find nearby users (within 10 km radius)
            nearby_users = []
            user_lat = float(latitude)
            user_lon = float(longitude)

            all_users = UserLocation.objects.exclude(user=user)  # Exclude the current user
            for location in all_users:
                distance = calculate_distance(user_lat, user_lon, location.latitude, location.longitude)
                if distance <= 10:  # 10 km radius
                    nearby_users.append({
                        'username': location.user.username,
                        'latitude': location.latitude,
                        'longitude': location.longitude
                    })

            return Response({
                'message': 'Location updated',
                'nearby_users': nearby_users
            }, status=200)
        return Response({'error': 'Latitude and longitude required'}, status=400)