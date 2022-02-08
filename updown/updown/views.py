from django.shortcuts import render, HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def index(request):
    return render(request, 'index.html')

def upload_process(request):
    upload_file = request.FILES['uploadfile']  # 전달된 파일을 받아줌
    # print(upload_file)
    # print(type(upload_file))

    uploaded = default_storage.save(upload_file.name, ContentFile(upload_file.read()))
    # default_storage() : settings 에서 설정했던 media 루트 찾음
    # print(uploaded)
    # print(type(uploaded))

    return render(request, 'download.html', {'filename': uploaded})

def download_process(request, filename):
    response = HttpResponse(default_storage.open(filename).read())
    response['Content-Disposition'] = f"attachment; filename={filename}"

    return response