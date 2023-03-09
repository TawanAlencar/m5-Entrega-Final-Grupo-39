from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from .serializers import CopySerializer, LendingSerializer
from .models import Copy, Lending
from users.permissions import IsColaboratorOrReadOnly
from django.shortcuts import get_object_or_404
from books.models import Book
from rest_framework.views import Response

# Create your views here.


class Copyview(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaboratorOrReadOnly]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.kwargs.get("book_id"))
        return serializer.save(book_id=self.kwargs.get("book_id"))


class LendingView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaboratorOrReadOnly]

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    def perform_create(self, serializer):
        return serializer.save(
            copy_id=self.kwargs.get("copy_id"), user_id=self.request.user.id
        )
    

class DestroyLendingView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaboratorOrReadOnly]

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    lookup_url_kwarg = "lending_id"

    def delete(self, request, *args, **kwargs):
        lending = get_object_or_404(Lending, id=self.kwargs.get("lending_id"))
        copy = get_object_or_404(Copy, id=lending.copy.id)
        copy.is_lending = False
        copy.save()
        lending.delete()
        return Response(status=204)
    
    
