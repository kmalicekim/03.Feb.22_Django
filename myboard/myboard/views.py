from django.shortcuts import render, redirect
from .models import MyBoard, MyMember
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password


def index(request):
    myboard = MyBoard.objects.all().order_by('-id')
    paginator = Paginator(myboard,5)          # 페이지당 5개식
    page_num = request.GET.get('page', '1')   # GET방식으로 호출된 url에서 page 값 가져옴.
                                              # page 값 없이 호출 시 디폴트로 1 설정

    # 페이지에 맞는 모델 가져오기
    page_obj = paginator.get_page(page_num)   # page_num에 해당하는 page_obj 라는 객체 생성

    # 관련 메서드
    print(type(page_obj))
    print(page_obj.count)
    print(page_obj.paginator.num_pages)
    print(page_obj.paginator.page_range)
    print(page_obj.has_next())
    print(page_obj.has_previous())
    try:
        print(page_obj.next_page_number())
        print(page_obj.previous_page_number())
    except:
        pass
    print(page_obj.start_index())
    print(page_obj.end_index())

    return render(request, 'index.html', {'list': page_obj})   # 'list' 에 page_obj 객체 전달
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

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        myname = request.POST['myname']
        mypassword = request.POST['mypassword']
        myemail = request.POST['myemail']

        mymember = MyMember(myname=myname, mypassword=make_password(mypassword), myemail=myemail)
        mymember.save()

        return redirect('/')

    return redirect('/')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        myname = request.POST['myname']
        mypassword = request.POST['mypassword']

        mymember = MyMember.objects.get(myname=myname)

        if check_password(mypassword, mymember.mypassword):
            request.session['myname'] = mymember.myname
            return redirect('/')
        else:
            return redirect('/login')

def logout(request):
    del request.session['myname']   # 클라이언트가 접속 종료하면 해당 session 지움 (DB 내용 지우는게 아님)
    return redirect('/')