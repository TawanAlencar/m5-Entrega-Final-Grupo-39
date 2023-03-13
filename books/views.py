from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Book, Follow
from rest_framework.serializers import ValidationError
from .serializers import BookSerializer, FollowSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.permissions import IsColaboratorOrReadOnly
from .utils import email_send_handler
from django.db.models.signals import post_save
from django.dispatch import receiver



class ListCreateBook(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsColaboratorOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "book_id"


class RetriveUpdateDestroyBook(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsColaboratorOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "book_id"


class FollowBook(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_url_kwarg = "book_id"

    def perform_create(self, serializer):
        if Follow.objects.filter(book=self.kwargs.get("book_id"),user_id=self.request.user.id):
            raise ValidationError("book is already being followed")
        return serializer.save(
            book_id=self.kwargs.get("book_id"), user_id=self.request.user.id
        )


class UnfollowBook(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_url_kwarg = "book_id"
