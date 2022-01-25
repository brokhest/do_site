import os.path

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from .forms import FileForm
from .models import File
from django import http


# Create your views here.


def upload(request):
    if request.method == 'POST':
        file = request.FILES['document'] if 'document' in request.FILES else None
        if file:
            fss = FileSystemStorage()
            fss.save(file.name, file)
    return render(request, 'files/upload.html')


def file_download(request, pk):
    file = File.objects.get(pk=pk)
    if file != None:
        d_file = file.file
        response = http.HttpResponse(file.file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % d_file
        return response



def file_js(request):
    #files = serializers.py.serialize("json", File.objects.values_list('name'))
    files = File.objects.all()
    data = []
    for file in files:
        #os.path.getsize(file.file.path) один из варантов получения размера
        record = {"name":file.name, "size":file.file.size }
        data.append(record)

    return JsonResponse(data, safe=False)


def file_list(request):
    files = File.objects.all()

    return render(request, 'files/file_list.html', {'files': files})


def file_upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = FileForm()
    return render(request, 'files/upload.html', {'form': form})

def file_delete(request, pk):
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        file.delete()
    return redirect('list')

