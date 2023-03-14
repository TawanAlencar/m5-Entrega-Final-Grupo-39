from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.serializers import ValidationError
from .serializers import CopySerializer, LendingSerializer
from .models import Copy, Lending
from users.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.permissions import IsColaboratorOrReadOnly
from django.shortcuts import get_object_or_404
from books.models import Book
from rest_framework.views import Response, Request
from django.db.models.signals import post_save, post_delete
from books.utils import email_send_handler, email_send_handler_delete
import datetime


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
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_blocked == True:
            raise ValidationError("This user is blocked")
        for lending in Lending.objects.filter(user_id=user.id):
            if lending.return_date < datetime.date.today():
                user.is_blocked = True
                user.save()
                raise ValidationError("User blocked")
        if Lending.objects.filter(user_id=user.id) is False:
            user.is_blocked = False
            user.save()

        return serializer.save(
            copy_id=self.kwargs.get("copy_id"), user_id=self.request.user.id
        )


class ListLendingStudants(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaboratorOrReadOnly]
    lookup_url_kwarg = "studants_id"

    def get(self, request: Request, studants_id: int) -> Response:
        lending = Lending.objects.filter(user=studants_id)
        serializer = LendingSerializer(lending, many=True)

        return Response(serializer.data, 200)


class DestroyLendingView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaboratorOrReadOnly]

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    lookup_url_kwarg = "lending_id"

    def delete(self, request, *args, **kwargs):
        lending_obj = get_object_or_404(Lending, id=self.kwargs.get("lending_id"))
        copy = get_object_or_404(Copy, id=lending_obj.copy.id)
        copy.is_lending = False
        copy.save()
        user = get_object_or_404(User, id=lending_obj.user.id)
        if lending_obj.return_date < datetime.date.today():
            user.is_blocked = True
            user.save()
            lending_obj.is_active = False
            lending_obj.save()
            raise ValidationError("User blocked")
        if Lending.objects.filter(user_id=user.id) is False:
            user.is_blocked = False
            user.save()
        lending_obj.is_active = False
        lending_obj.save()
        return Response(status=204)


post_save.connect(email_send_handler, sender=Lending)
post_delete.connect(email_send_handler_delete, sender=Lending)
