from .serializers import BookSerializer
from django.shortcuts import get_object_or_404
from .models import Book
from django.core.mail import send_mail
from django.conf import settings


def get_emails(book_id):
    book = get_object_or_404(Book, id=book_id)
    serializer = BookSerializer(book)
    email_list = []
    for follower in serializer.data["followers"]:
        email = follower["email"]
        if not email in email_list:
            email_list.append(email)

    return email_list


def email_send_handler(sender, instance, **kwargs):
    emails = get_emails(instance.copy.book.id)
    if instance.copy.book.is_avaliable == True:
        email_sending(
            emails,
            f"Atualização sobre {instance.copy.book.title}",
            f"Uma cópia do livro {instance.copy.book.title}, que você está seguindo foi emprestada, mas ainda há outras disponíveis, corra para não perder a chance de lê-lo!",
        )
    if instance.copy.book.is_avaliable == False:
        email_sending(
            emails,
            f"Atualização sobre {instance.copy.book.title}",
            f"A última cópia do livro {instance.copy.book.title}, que você está seguindo foi emprestada, data de retorno prevista é {instance.return_date}.",
        )

def email_send_handler_delete(sender, instance, **kwargs):
    emails = get_emails(instance.copy.book.id)
    email_sending(
        emails,
            f"Atualização sobre {instance.copy.book.title}",
            f"Uma cópia do livro {instance.copy.book.title}, que você está seguindo foi devolvida e ele está disponível novamente!"
    )



def email_sending(email_list, title, body):
    send_mail(
        title,
        body,
        settings.EMAIL_HOST_USER,
        email_list,
        fail_silently=False,
    )
