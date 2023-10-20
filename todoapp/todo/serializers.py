from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UsersListSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'fullname', 'email']

    def get_fullname(self, obj):
        return f'{obj.first_name} {obj.last_name}'



class TodoListSerializer(serializers.ModelSerializer):
    user = UsersListSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = TodoLists
        fields = ['id', 'user', 'title', 'description', 'scheduled_at', 'status', 'created_at', 'updated_at']

    
    def get_status(self, obj):
        return obj.get_status_display()
    

class TodoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoLists
        fields = "__all__"


class UserAuthModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

