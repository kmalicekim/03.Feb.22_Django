from django.shortcuts import render
from .models import MyBoard


def index(request):
    return render(request, 'index.html', {'list': MyBoard.objects.all()})  #request를 받으면 'index.html'를 렌더링해줘라
