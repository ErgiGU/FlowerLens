# Generated by Django 4.2.7 on 2023-12-08 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FlowerLensBackendComponent', '0010_remove_matriximage_image_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictionresult',
            name='heatmap',
            field=models.ImageField(upload_to='heatmap_images/'),
        ),
    ]
