from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Task, User

class TaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    desc = serializers.CharField()
    completion = serializers.BooleanField()
    pk = serializers.IntegerField()

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.completion = validated_data.get('completion', instance.completion)
        instance.save()
        return instance

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=6, write_only=True)
    token = serializers.CharField(max_length=25, read_only=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'token')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=30, write_only=True)

    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None:
            raise serializers.ValidationError('Username is required to log in')
        if password is None:
            raise serializers.ValidationError('Password is required to log in')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('User was not found')
        return {
            'username': user.username,
            'token': user.token
        }

