from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('test/', views.test),    #test/ 앞에 hello01이 생략된 것 (hello01/test/)
    path('my/', views.my),
]