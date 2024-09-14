# Inside an app's management/commands directory, create a file named bulk_upload.py

from django.core.management.base import BaseCommand
from pathlib import Path
from FlowerLensBackendComponent.models import FlowerImage, Flower
from django.core.files import File

class Command(BaseCommand):
    help = 'Bulk uploads photos and assigns them to flower classes'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to the directory containing flower class folders')

    def handle(self, *args, **kwargs):
        root_path = Path(kwargs['path'])
        for flower_class_dir in root_path.iterdir():
            if flower_class_dir.is_dir():
                flower_class_name = flower_class_dir.name
                flower_class, created = Flower.objects.get_or_create(name=flower_class_name)

                for image_path in flower_class_dir.glob('*.jpg'):
                    with open(image_path, 'rb') as image_file:
                        flower_image = FlowerImage(flower=flower_class)  # Create a FlowerImage instance
                        flower_image.image.save(image_path.name, File(image_file), save=True)
                        self.stdout.write(self.style.SUCCESS(f'Uploaded {image_path.name}'))
