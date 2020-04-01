from django.conf.urls import url, include
from . import views
from django.urls import path
urlpatterns = [
    path('search_perfume', views.search_perfume),
    path('show_perfume', views.show_perfume)
]
