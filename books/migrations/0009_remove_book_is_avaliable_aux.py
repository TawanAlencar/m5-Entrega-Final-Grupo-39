# Generated by Django 4.1.7 on 2023-03-13 15:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0008_rename_is_available_book_is_avaliable_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="is_avaliable_aux",
        ),
    ]
