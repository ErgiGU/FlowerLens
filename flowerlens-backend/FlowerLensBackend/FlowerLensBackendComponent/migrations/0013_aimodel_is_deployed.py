# Generated by Django 4.2.7 on 2023-12-08 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FlowerLensBackendComponent', '0012_remove_metricstable_metrics_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodel',
            name='is_deployed',
            field=models.BooleanField(default=False),
        ),
    ]
