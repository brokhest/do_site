from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer, TaskSerializer
from .renderers import UserJSONRenderer
from .models import Task, User

# Create your views here.


class RegistrationAPIView(APIView):

    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class GetTask(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        login = request.data.get('user')['login']
        user = get_object_or_404(User.objects.all(), username=login)
        task = get_object_or_404(user.tasks.all(), pk=pk)
        record = {
            "title": task.title,
            "description": task.desc,
            "completion": task.completion,
            "pk": task.pk
        }
        return JsonResponse(record, safe=False)


class Tasks(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        login = request.data.get('user')['login']
        user = get_object_or_404(User.objects.all(), username=login)
        data = []
        for task in user.tasks.all():
            record = {
                "title": task.title,
                "description": task.desc,
                "completion": task.completion,
                "pk": task.pk
            }
            data.append(record)

        return JsonResponse(data, safe=False)

    def post(self, request):
        login = request.data.get('user')['login']
        data = request.data.get('task')
        user = get_object_or_404(User.objects.all(), username=login)
        # task ={
        #     "title": data['title'],
        #     "desc": data['desc'],
        #     "completion": data['completion'],
        #     "user": user.pk
        # }
        task = Task(title=data['title'], desc=data['desc'],
                    completion=data['completion'],
                    user=user)
        task.save()
        # serializer = TaskSerializer(user, data=task)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        return Response({"success": "yes"})
        # return Response({"success":"no"})

    def put(self, request, pk):
        user = get_object_or_404(User.objects.all(),
                                 username=request.data.get('user')['login'])
        task = get_object_or_404(user.tasks.all(), pk=pk)
        data = request.data.get('task')
        serializer = TaskSerializer(instance=task, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": "yes"})
        return Response({"success": "no"})

    def delete(self, request, pk):
        user = get_object_or_404(User.objects.all(),
                                 username=request.data.get('user')['login'])
        task = get_object_or_404(user.tasks.all(), pk=pk)
        task.delete()
        return Response({"success": "yes"})

        # saved_task = get_object_or_404(Task.objects.all(), pk=pk)

# class Task_list(APIView):
#     def get(self, request):
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response ({"Tasks":serializer.data})
#
#     def post(self, request):
#         task = request.data.get('task')
#         serializer = TaskSerializer(data=task)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#         return Response({"success":"yes"})
#
#     def put(self, request, pk):
#         saved_task = get_object_or_404(Task.objects.all(), pk=pk)
#         data = request.data.get('task')
#         serializer = TaskSerializer(instance=saved_task, data=data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             saved_task = serializer.save()
#         return Response({"success":"yes"})
#
#     def delete(self, request, pk):
#         task = get_object_or_404(Task.objects.all(), pk=pk)
#         task.delete()
#         return Response({"success":"yes"})
