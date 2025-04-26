from rest_framework import serializers
from .models import Blog
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
