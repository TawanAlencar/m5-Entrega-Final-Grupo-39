# Generated by Django 4.1.7 on 2023-03-13 12:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0003_book_followers"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="is_available",
            field=models.BooleanField(default=True),
        ),
    ]
