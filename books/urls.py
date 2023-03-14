from django.urls import path
from .views import ListCreateBook, FollowBook, UnfollowBook, RetriveUpdateDestroyBook

urlpatterns = [
    path("books/", ListCreateBook.as_view()),
    path("books/<int:book_id>/follow/", FollowBook.as_view()),
    path("books/<int:book_id>/", RetriveUpdateDestroyBook.as_view()),
    path("books/<int:follow_id>/unfollow/", UnfollowBook.as_view()),
]
