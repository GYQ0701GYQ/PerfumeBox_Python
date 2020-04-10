from django.conf.urls import url, include
from . import views
from django.urls import path
urlpatterns = [
    path('search_perfume', views.search_perfume),
    path('search_one_perfume', views.search_one_perfume),
    path('show_top100', views.show_top100),
    path('search_one_letter', views.search_one_letter),
    path('user_login', views.user_login),
    path('user_register', views.user_register),
]
