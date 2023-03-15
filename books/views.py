from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Book, Follow
from copies.models import Copy
from users.models import User
from rest_framework.serializers import ValidationError
from .serializers import BookSerializer, FollowSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.permissions import IsColaboratorOrReadOnly
from .utils import email_send_handler
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings


class ListCreateBook(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsColaboratorOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "book_id"


class RetriveUpdateDestroyBook(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaboratorOrReadOnly]
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
        book = get_object_or_404(Book, id=self.kwargs.get("book_id"))
        copy_data = Copy.objects.filter(id=self.kwargs.get("book_id"))
        copy_is_leding = copy_data.last()
        user = get_object_or_404(User, id=self.kwargs.get("user_id"))
        email_user = user.email

        send_mail(
            "Você seguiu este livro",
            f"Nome do livro: {book.title} \nDescrição: {book.description}\nEmprestado:{copy_is_leding.is_lending}",
            settings.EMAIL_HOST_USER,
            [email_user],
            False,
        )

        if Follow.objects.filter(
            book=self.kwargs.get("book_id"), user_id=self.request.user.id
        ):
            raise ValidationError("book is already being followed")

        return serializer.save(
            book_id=self.kwargs.get("book_id"), user_id=self.request.user.id
        )


class UnfollowBook(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_url_kwarg = "follow_id"
