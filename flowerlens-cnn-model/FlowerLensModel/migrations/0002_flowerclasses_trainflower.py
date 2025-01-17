# Generated by Django 5.0 on 2023-12-09 13:13

import FlowerLensModel.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("FlowerLensModel", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FlowerClasses",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="TrainFlower",
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
                (
                    "image",
                    models.ImageField(
                        upload_to=FlowerLensModel.models.flower_image_directory_path
                    ),
                ),
                (
                    "flower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="FlowerLensModel.flowerclasses",
                    ),
                ),
            ],
        ),
    ]
