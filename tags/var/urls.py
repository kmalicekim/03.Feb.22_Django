from django.urls import path
from . import views

# {% url 'index' %} -> name = 'index' 인 것을 찾아라 (경로의 별칭)
urlpatterns = [
    path('', views.index, name='index'),
    path('var01/', views.variables01),
    path('var02/', views.variables02),
    path('forloop/', views.for_loop, name='for'),
    path('if01/', views.if01),
    path('if02/', views.if02),
    path('href/', views.href),
    path('request/', views.get_post),
]