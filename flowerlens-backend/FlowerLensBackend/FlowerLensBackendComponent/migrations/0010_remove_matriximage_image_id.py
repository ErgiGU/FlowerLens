# Generated by Django 4.2.7 on 2023-12-03 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FlowerLensBackendComponent', '0009_remove_aimodel_description_remove_aimodel_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matriximage',
            name='image_id',
        ),
    ]