from django.shortcuts import render, redirect
from .models import MyBoard
from django.utils import timezone


def index(request):
    return render(request, 'index.html', {'list': MyBoard.objects.all().order_by('-id')})
    #'id'기준으로 정렬해줘 (default:ascending) / ('-id') : descending

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

def detail(request, id):
    return render(request, 'detail.html', {'dto':MyBoard.objects.get(id=id)})   # 해당 id에 해당하는 row를 dto로 보냄

def update_form(request, id):
    return render(request, 'update.html', {'dto':MyBoard.objects.get(id=id)})

def update_res(request):
    id = request.POST['id']    # request.POST['id']로 받은 결과값 을 id 로 설정해라
    mytitle = request.POST['mytitle']
    mycontent = request.POST['mycontent']

    myboard = MyBoard.objects.filter(id=id)   # get은 값 1개만 (단일행) 불러옴. 값이 없을 때 DoesNotExist라는 메시지 띄움
                                              # filter는 괄호에 해당하는 모든 값 불러옴. 값이 없을 때 빈 쿼리셋을 불러옴

    result_title = myboard.update(mytitle=mytitle)
    result_content = myboard.update(mycontent=mycontent)
    # print(result_title, result_content)  # ---> 확인해보기

    if result_title + result_content == 2:    #제대로 두개가 얻어졌다면
        return redirect('/detail/'+id)     #detail에 다시 요청을 하려면 뒤에 id가 붙는 형태로 가야 함
                                           # path 에 detail/<int:id> / updateform/<int:id> 로
    else:
        return redirect('/updateform/'+id)

def delete(request, id):
    result_delete = MyBoard.objects.filter(id=id).delete()
    print(result_delete)   # (1, {'myboard.MyBoard': 1})
                           # --> 앞의 1은 delete 된 개수, {}안의 1도 같은 의미이나 {}안이 더 상세하게 말해주는 것

    if result_delete[0]:
        return redirect('index')
    else:
        return redirect('/detail/'+id)

"""
result_delete = MyBoard.objects.filter(id=id).delete() 는 아래와 같은 원리

def test():
    return 1

a = test()
print(a)  ---> 1나옴. 즉 result_delete는 우변의 return 값을 받는 것
"""