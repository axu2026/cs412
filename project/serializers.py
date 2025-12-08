# project/serializers.py
# Aidan Xu (axu26@bu.edu) 11/23/25
# provides the serializers to allow for api transfer of models

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class CustomerSerializer(serializers.ModelSerializer):
    """create serializer for customer api"""
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        """tie serializer to the customer model"""
        model = Customer
        fields = [
                'username', 
                'password',
                'first_name',
                'last_name', 
                'date_of_birth', 
                'address',
                'phone_number',
                'email',]
        
    def create(self, validated_data):
        """to create a customer using the api"""

        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password)
        customer = Customer.objects.create(user=user, **validated_data)
        customer.save()

        return customer