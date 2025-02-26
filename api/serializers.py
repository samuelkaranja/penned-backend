from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog  # Specify the model here
        fields = '__all__'  # Include all fields from the Blog model
