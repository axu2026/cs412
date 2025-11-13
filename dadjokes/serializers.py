# dadjokes/serializers.py
# aidan xu (axu26@bu.edu) 11/13/25
# the serializers defined for the dadjokes application

from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    """serializer for the joke model"""

    class Meta:
        """ties to the joke model and its fields to be serialized"""
        model = Joke
        fields = ['joke', 'contributor', 'timestamp']

    def create(self, validated_data):
        """creates and saves a new joke instance from validated data"""
        joke = Joke.objects.create(**validated_data)
        joke.save()

        return joke
    

class PictureSerializer(serializers.ModelSerializer):
    """serializer for the picture model"""

    class Meta:
        """ties to the picture model and its fields to be serialized"""
        model = Picture
        fields = ['image_url', 'contributor', 'timestamp']