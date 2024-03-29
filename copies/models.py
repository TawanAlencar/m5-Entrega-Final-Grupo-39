from django.db import models


# Create your models here.
class Copy(models.Model):
    is_lending = models.BooleanField(default=False)
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="copies"
    )


class Lending(models.Model):
    is_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="lending"
    )
    copy = models.ForeignKey(
        "copies.Copy", on_delete=models.CASCADE, related_name="lending"
    )
