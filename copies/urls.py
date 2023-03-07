from django.urls import path
from .views import Copyview

urlpatterns = [
    path("books/<int:book_id>/copy/", Copyview.as_view()),
]
