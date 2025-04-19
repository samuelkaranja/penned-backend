from rest_framework import serializers
from .models import Blog
from django.contrib.auth.models import User


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog  # Specify the model here
        fields = '__all__'  # Include all fields from the Blog model

class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(max_length=255)  # Add fullname field

    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Create a user with the fullname field included
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.first_name = validated_data['fullname']  # Store fullname in the first_name field
        user.save()
        return user
