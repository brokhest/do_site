from rest_framework import serializers
from .models import User, Task
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username= serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None:
            raise serializers.ValidationError(
                'An username is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user was not found.'
            )
        return {
            'id': user.pk,
            'username': user.username,
            'token': user.token
        }


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='User', queryset=User.objects.all())
    class Meta:
        model = Task
        fields = ('title', 'desc', 'completion', 'user')

    def create(self, user, **validated_data):
        #username = validated_data.get().username
        #task = Task(title=validated_data.get('title'), desc=validated_data.get('desc'), completion= validated_data.get('completion'), user=user)
        #return task

        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.desc = validated_data.get('desc')
        instance.completion = validated_data.get('completion')
        instance.save()
        return instance
