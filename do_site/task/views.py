from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Task
from .serializers import TaskSerializer, RegistrationSerializer, LoginSerializer
from .renders import UserJSONRenderer

# Create your views here.

class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = (UserJSONRenderer)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user',{})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
         status=status.HTTP_201_CREATED,)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = (UserJSONRenderer)
    serializer_class = LoginSerializer
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


def get_tasks(request):
    if request.method == "GET":
        return JsonResponse(serializers.serialize(Task.objects.all(), safe=False))


class Task_list(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response ({"Tasks":serializer.data})

    def post(self, request):
        task = request.data.get('task')
        serializer = TaskSerializer(data=task)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success":"yes"})

    def put(self, request, pk):
        saved_task = get_object_or_404(Task.objects.all(), pk=pk)
        data = request.data.get('task')
        serializer = TaskSerializer(instance=saved_task, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_task = serializer.save()
        return Response({"success":"yes"})

    def delete(self, request, pk):
        task = get_object_or_404(Task.objects.all(), pk=pk)
        task.delete()
        return Response({"success":"yes"})

