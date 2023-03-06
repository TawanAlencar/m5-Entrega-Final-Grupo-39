# Generated by Django 4.1.7 on 2023-03-06 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Copy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_lending", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Lending",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_date", models.DateTimeField(auto_now_add=True)),
                ("return_date", models.DateTimeField(auto_now_add=True)),
                (
                    "copy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lending",
                        to="copies.copy",
                    ),
                ),
            ],
        ),
    ]
