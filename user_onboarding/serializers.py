from rest_framework import serializers
from user_onboarding.models import User, Roles
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    user_type_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'user_type_name', 'f_name', 'l_name', 
            'username', 'profile_photo', 'address', 'city', 'pin'
        )

    def get_user_type_name(self, obj):
        return obj.user_type.name if obj.user_type else None

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'email', 'f_name', 'l_name', 'username', 'password', 
            'password2', 'user_type', 'profile_photo', 'address', 'city', 'pin'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']
class UserDetailSerializer(serializers.ModelSerializer):
    user_type_name = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'f_name', 'l_name', 'username', 'user_type_name',
            'profile_photo', 'address', 'city', 'pin', 'created_at', 'updated_at', 'is_active', 'is_admin'
        ]

    def get_user_type_name(self, obj):
        return obj.user_type.name if obj.user_type else None
    def get_profile_photo(self, obj):
        if obj.profile_photo:
            cloud_name = settings.CLOUDINARY['cloud_name']
            return f"https://res.cloudinary.com/{cloud_name}/{obj.profile_photo}"
        return None
    