from django.http import JsonResponse, HttpResponse
import mimetypes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import File
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .serializers import UploadSerializer
# Create your views here.


class FileDownloadView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, name):
        files = File.objects.filter(name=name)
        if len(files) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        file = File.objects.get(name=name)
        path = open(file.file.path, 'r')
        mime_type = mimetypes.guess_type(file.file.path)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % file.name

        return response


class FileView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        file = request.data.get('file')
        files = File.objects.all()
        if len(files.filter(name=file.name)) != 0:
            return Response(status=status.HTTP_409_CONFLICT)
        file_serializer = UploadSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, filename, format=None):
    #     if 'file' not in request.data:
    #         raise ParseError('empty content')
    #     f = request.FILES('file')
    #     name = request.data['name']
    #     file = File(name=name, file=f)
    #     file.save()
    #     return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, name):
        file = get_object_or_404(File.objects.all(), name=name)
        file.delete()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        data = []
        for file in File.objects.all():
            record = {
                'name': file.name,
                'size': file.file.size}
            data.append(record)
        return JsonResponse(data, safe=False)
