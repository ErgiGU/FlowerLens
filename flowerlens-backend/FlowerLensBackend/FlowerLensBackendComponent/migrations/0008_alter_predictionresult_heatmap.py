# Generated by Django 4.2.7 on 2023-12-02 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FlowerLensBackendComponent', '0007_alter_predictionresult_confidence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictionresult',
            name='heatmap',
            field=models.TextField(),
        ),
    ]
