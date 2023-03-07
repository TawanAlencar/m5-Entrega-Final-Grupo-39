from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from .serializers import CopySerializer, LendingSerializer
from .models import Copy, Lending
from users.permissions import IsColaboratorOrReadOnly

# Create your views here.


class Copyview(ListCreateAPIView):
    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def perform_create(self, serializer):
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

    lookup_url_kwarg = "copy_id"
