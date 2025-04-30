from rest_framework import serializers
from .models import Blog, Profile
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken



class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog  # Specify the model here
        fields = '__all__'  # Include all fields from the Blog model

class SignupSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        fullname = validated_data.pop('fullname').strip().title()
        confirm_password = validated_data.pop('confirm_password')
        
        first_name, *last_name = fullname.split(' ', 1)
        last_name = last_name[0] if last_name else ''

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'id': instance.id,
                'username': instance.username,
                'email': instance.email,
                'fullname': f"{instance.first_name} {instance.last_name}".strip(),
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['about', 'image']

# NEW: Combined user + profile serializer for updates
class UserProfileSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(required=False)
    about = serializers.CharField(source='profile.about', required=False)
    image = serializers.ImageField(source='profile.image', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'fullname', 'about', 'image']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        fullname = validated_data.pop('fullname', '').strip()

        # Update user model fields
        if fullname:
            parts = fullname.split(' ', 1)
            instance.first_name = parts[0]
            instance.last_name = parts[1] if len(parts) > 1 else ''

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update profile model fields
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance

    def to_representation(self, instance):
        return {
            'username': instance.username,
            'email': instance.email,
            'fullname': f"{instance.first_name} {instance.last_name}".strip(),
            'about': instance.profile.about,
            'image': instance.profile.image.url if instance.profile.image else None,
        }