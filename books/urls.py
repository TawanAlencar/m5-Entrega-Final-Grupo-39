from django.urls import path
from .views import ListCreateBook, FollowBook,UnfollowBook

urlpatterns = [
    path("books/", ListCreateBook.as_view()),
    path("books/<int:book_id>/follow/", FollowBook.as_view()),
    path("books/<int:book_id>/unfollow/", UnfollowBook.as_view())
]
