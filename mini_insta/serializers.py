from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'join_date', 'bio_text']

    def create(self, validated_data):
        profile = Profile.objects.create(user=User.objects.first(),**validated_data)
        profile.save()

        return profile