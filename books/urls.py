from django.urls import path
from .views import ListCreateBook

urlpatterns = [
    path("books/", ListCreateBook.as_view()),
]
