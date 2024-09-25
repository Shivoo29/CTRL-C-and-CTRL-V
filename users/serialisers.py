from rest_framework import serializers
from .models import User, UserManager, Report

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'phn']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        email = attrs.get('email')
        name = attrs.get('name')
        password = attrs.get('password')
        phn = attrs.get('phn')

        # Check that all fields are provided
        if not email:
            raise serializers.ValidationError({"email": "This field is required."})
        if not name:
            raise serializers.ValidationError({"name": "This field is required."})
        if not password:
            raise serializers.ValidationError({"password": "This field is required."})
        if not phn:
            raise serializers.ValidationError({"phn": "This field is required."})

        return attrs
    
    
class UserLoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phn', 'is_active', 'is_admin']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class LocationSerializer(serializers.Serializer):
    latitude = serializers.CharField(max_length=50)
    longitude = serializers.CharField(max_length=50)