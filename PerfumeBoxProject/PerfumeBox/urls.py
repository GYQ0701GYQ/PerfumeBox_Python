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
    path('perfume_compare', views.perfume_compare),
    path('judge_collect', views.judge_collect),
    path('handle_collect', views.handle_collect),
    path('handle_buy', views.handle_buy),
    path('show_shopping_cart', views.show_shopping_cart),
    path('show_collect', views.show_collect),
]
