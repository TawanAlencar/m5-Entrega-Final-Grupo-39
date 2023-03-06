from .views import ListCreateUser, RetrieveUpdateDestroyUser
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("users/login/", TokenObtainPairView.as_view()),
    path("users/", ListCreateUser.as_view()),
    path(
        "users/<int:user_id>/",
        RetrieveUpdateDestroyUser.as_view(),
    ),
]
