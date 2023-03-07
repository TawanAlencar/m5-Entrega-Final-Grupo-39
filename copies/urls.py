from django.urls import path
from .views import Copyview, LendingView, DestroyLendingView

urlpatterns = [
    path("books/<int:book_id>/copy/", Copyview.as_view()),
    path("lending/<int:copy_id>/", LendingView.as_view()),
    path("lending/<int:copy_id>/delete/", DestroyLendingView.as_view()),
]
