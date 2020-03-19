from django.conf.urls import url, include
from . import views
from django.urls import path
urlpatterns = [
    path('add_book', views.add_book),
    path('show_books', views.show_books),
]
