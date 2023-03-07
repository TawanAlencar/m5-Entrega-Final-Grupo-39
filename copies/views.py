from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView
from .serializers import CopySerializer
from .models import Copy
# Create your views here.

class Copyview(ListCreateAPIView):
    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def perform_create(self, serializer):
        return serializer.save(book_id=self.kwargs.get("book_id"))