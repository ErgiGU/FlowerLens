# Generated by Django 4.2.7 on 2023-12-10 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FlowerLensBackendComponent', '0013_aimodel_is_deployed'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodel',
            name='latest_deployed',
            field=models.BooleanField(default=False),
        ),
    ]
