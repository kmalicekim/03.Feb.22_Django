from django.shortcuts import render, redirect
from .models import MyBoard, MyMember
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password


def index(request):
    myboard = MyBoard.objects.all().order_by('-id')  #'id'기준으로 정렬해줘 (default:ascending) / ('-id') : descending
    paginator = Paginator(myboard,5)          # 페이지당 5개씩
    page_num = request.GET.get('page', '1')   # GET방식으로 호출된 url에서 page 값 가져옴.
                                              # page 값 없이 호출 시 디폴트로 1 설정
    """
    get은 딕셔너리 자료형에서 key값으로 value를 찾을 때 사용.
    즉, request.GET 으로 받아온 값은 딕셔너리 자료형이라는 것.
    ex) http://127.0.0.1:8000/title=first&body=hello
        {'title':first, 'body':hello}
    여기서 page에 해당하는 value를 가져오면 page의 번호를 리턴 받을 수 있음
    """

    # 페이지에 맞는 모델 가져오기
    page_obj = paginator.get_page(page_num)   # page_num에 해당하는 page_obj 라는 객체 생성
    """get_page 메소드는 페이지 번호를 받아 해당 페이지를 리턴.
    그 후 이 페이지를 다시 render를 통해 넘겨주게 됨"""

    # 관련 메서드
    print(type(page_obj))   # <class 'django.core.paginator.Page'>
    print(page_obj.count)   # <bound method Sequence.count of <Page 9 of 21>> (내가 9페이지 눌렀음)
    print(page_obj.paginator.num_pages)   # 21  --- 총 페이지 수
    print(page_obj.paginator.page_range)  # range(1,22)   --- (1부터 시작하는)페이지 리스트 반환
    print(page_obj.has_next())            # True
    print(page_obj.has_previous())        # True
    try:
        print(page_obj.next_page_number())   # 10
        print(page_obj.previous_page_number())   # 8
    except:
        pass
    print(page_obj.start_index())    # 41
    print(page_obj.end_index())      # 45

    return render(request, 'index.html', {'list': page_obj})   # 'list' 에 page_obj 객체 전달

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

        mymember = MyMember(myname=myname, mypassword=make_password(mypassword), myemail=myemail)  # models.py 확인
        mymember.save()

        return redirect('/')

    return redirect('/')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        myname = request.POST['myname']
        mypassword = request.POST['mypassword']

        mymember = MyMember.objects.get(myname=myname) # DB에서 꺼내는 명령. POST로 받아온 myname으로 DB의 myname을 꺼내온다

        if check_password(mypassword, mymember.mypassword):   # check_password(a,b) : a,b가 일치하는지 확인, 반
            request.session['myname'] = mymember.myname  # 세션에 id값을 넣음. 로그인 상태를 유지하기 위함
            return redirect('/')
        else:
            return redirect('/login')

def logout(request):
    del request.session['myname']   # 클라이언트가 접속 종료하면 해당 session 지움 (DB 내용 지우는게 아님)
    return redirect('/')