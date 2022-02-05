from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'name': 'alice'})
    # templates/index.html 이라고 안 써도 settings.py 에 이미 세팅 완료되어 경로 안써도 templates 폴더 밑의 index.html 이라고 생각

