# Django 에 기본적으로 회원가입을 위한 내장되어있는 form
from django.contrib.auth.forms import UserCreationForm

# Django 의 유저 관련 내장 모델
from django.contrib.auth.models import User   # User가 auth에서 만들어놓은 모델
from django import forms   # forms 는 화면에 보여주는 것


class MyMemberForm(UserCreationForm):
    """
    UserCreationForm 이 가진 기본적인 필드 : username, password1, password2
    password1 : 비밀번호 / password2 : 비밀번호 확인
    """
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User  # 데이터를 저장하기 위해 내장된 User모델을 지정함
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
