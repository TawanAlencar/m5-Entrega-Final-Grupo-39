from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=40, null=True)
    followers = models.ManyToManyField(
        "users.User", through="books.Follow", related_name="followed_books"
    )
    is_avaliable = models.BooleanField(default=True)


class Follow(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="follow"
    )
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="follow"
    )
