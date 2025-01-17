# Generated by Django 4.2.7 on 2023-11-30 10:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('FlowerLensBackendComponent', '0003_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_id', models.CharField(max_length=100, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('version', models.CharField(max_length=100, null=True)),
                ('file_path', models.FileField(null=True, upload_to='model_files/')),
            ],
        ),
        migrations.CreateModel(
            name='MetricsTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metrics_id', models.CharField(max_length=100)),
                ('accuracy', models.FloatField()),
                ('precision', models.FloatField()),
                ('recall', models.FloatField()),
                ('f1_score', models.FloatField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('model_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlowerLensBackendComponent.aimodel')),
            ],
        ),
        migrations.CreateModel(
            name='MatrixImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(max_length=100)),
                ('image_path', models.ImageField(upload_to='matrix_images/')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('model_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlowerLensBackendComponent.aimodel')),
            ],
        ),
    ]
