# Generated by Django 4.1.7 on 2023-03-08 01:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_follow",
            field=models.ManyToManyField(related_name="users", to="books.book"),
        ),
    ]
