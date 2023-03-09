from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Book, Follow
from .serializers import BookSerializer, FollowSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ListCreateBook(ListCreateAPIView):
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
        return serializer.save(
            book_id=self.kwargs.get("book_id"), user_id=self.request.user.id
        )
    
class  UnfollowBook(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_url_kwarg = "book_id"