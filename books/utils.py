from .serializers import BookSerializer
from django.shortcuts import get_object_or_404
from .models import Book
from django.core.mail import send_mail
from django.conf import settings


def get_emails(book_id):
    book = get_object_or_404(Book, id=book_id)
    teste = BookSerializer(book)
    email_list = []
    for follower in teste.data["followers"]:
        email = follower["email"]
        if not email in email_list:
            email_list.append(email)

    return email_list


def email_send_handler(sender, instance, **kwargs):
    emails = get_emails(instance.id)

    email_sending(emails, "teste", "teste_teste_teste")


def email_sending(email_list, title, body):
    send_mail(
        title,
        body,
        settings.EMAIL_HOST_USER,
        email_list,
        fail_silently=False,
    )
