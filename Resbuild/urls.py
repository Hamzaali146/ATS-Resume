from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('signin',views.signin,name = 'signin'),
    path('analyzer',views.analyzer,name = 'analyzer'),
    path('generate',views.getText,name = 'getText'),
    path('builder',views.builder,name = 'builder')
]