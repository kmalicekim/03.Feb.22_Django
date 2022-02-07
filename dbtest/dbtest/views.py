from django.shortcuts import render, redirect
from .models import MyBoard
from django.utils import timezone


def index(request):
    return render(request, 'index.html', {'list': MyBoard.objects.all()})
    # request를 받으면 'index.html'를 렌더링
    # MyBoard.objects --> model 객체 생성

def detail(request, id):
    return render(request, 'detail.html', {'dto': MyBoard.objects.get(id=id)})

def insert_form(request):
    return render(request, 'insert.html')

def insert_res(request):
    myname = request.POST['myname']
    mytitle = request.POST['mytitle']
    mycontent = request.POST['mycontent']

    result = MyBoard.objects.create(myname=myname, mytitle=mytitle, mycontent=mycontent, mydate=timezone.now())
    if result:
        return redirect('index')
    else:
        return redirect('insertform')

def update_form(request, id):
    return render(request, 'update.html', {'dto': MyBoard.objects.get(id=id)})

def update_res(request):
    id = request.POST['id']
    mytitle = request.POST['mytitle']
    mycontent = request.POST['mycontent']

    #get()과 filter()의 차이
    myboard = MyBoard.objects.filter(id=id)

    result_title = myboard.update(mytitle=mytitle)
    result_content = myboard.update(mycontent=mycontent)

    if result_title + result_content == 2:
        return redirect('/detail/'+id)    # detail 앞에 / 가 없으면 http://127.0.0.1:8000/updateres/detail/1 됨
                                          # / 가 있으면 http://127.0.0.1:8000/detail/1
    else:
        return redirect('/updateform/'+id)

def delete(request, id):
    result_delete = MyBoard.objects.filter(id=id).delete()

    if result_delete[0]:      #delete 하면 튜플형태로 반환됨 --> 찾아보기
        return redirect('index')
    else:
        return redirect('detail/'+id)