from django.db import models
from django.utils import timezone


# here we define the database models for the data we store
# these are shared with the backend component

def flower_image_directory_path(instance, filename):
    """Method for passing the directory path to the image storage folder"""
    return f'flowers/{instance.flower.name}/{filename}'

class Images(models.Model):
    """Model for each individual image of a flower. flower is a field that creates a many-to-one relationship to the Flower model """
    image_id = models.CharField(max_length=100)
    flower = models.CharField(max_length= 20)
    image = models.ImageField(upload_to= 'Images/')
    def __str__(self):
        return str(self.flower)

class Photo(models.Model):
    """Class for dynamically adding photons uploaded by uswers to the database"""
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    # Directory where images will be stored
    image = models.ImageField(upload_to='user_uploads/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.title or "Unnamed Photo")

class AIModel(models.Model):
    """Class for dynamically adding AI models to the database"""
    model_id = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    version = models.CharField(max_length=100, null=True)
    is_deployed = models.BooleanField(default=False)

    def __str__(self):
        return f"Model ID: {self.model_id}"

class MetricsTable(models.Model):
    """Class for dynamically adding metrics associated with AI models"""
    model_id = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Metrics for Model ID: {self.model_id.model_id}"

class MatrixImage(models.Model):
    """Class for dynamically adding matrix images associated with AI models"""
    model_id = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='matrix_images/')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Matrix Image for Model ID: {self.model_id.model_id}"


class PredictionResult(models.Model):
    """Class for storing the results of a prediction"""
    prediction = models.CharField(max_length=255)
    confidence = models.CharField(max_length=255)
    heatmap = models.ImageField(upload_to='heatmap_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction: {self.prediction}, Confidence: {self.confidence}"

#
# The following models are currently unused 
#

class FlowerClasses(models.Model):
    """Flower class to be used for storing images of flowers"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class TrainFlower(models.Model):
    """Model for each individual image of a flower. flower is a field that creates a many-to-one relationship to the Flower model """
    # If Flower object is deleted, then corresponding FlowerImage should also be deleted.
    flower = models.ForeignKey(FlowerClasses, on_delete=models.CASCADE)
    # Use the flower_image_directory function to determine the upload path of the image.
    image = models.ImageField(upload_to=flower_image_directory_path)

    def __str__(self):
        # If we have an image of a rose, the string representation will be "Image of Rose"
        return f"Image of {self.flower.name}"

class Flower(models.Model):
    """Flower class to be used for storing images of flowers"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class FlowerImage(models.Model):
    """Model for each individual image of a flower. flower is a field that creates a many-to-one relationship to the Flower model """
    # If Flower object is deleted, then corresponding FlowerImage should also be deleted.
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    # Use the flower_image_directory function to determine the upload path of the image.
    image = models.ImageField(upload_to=flower_image_directory_path)

    def __str__(self):
        # If we have an image of a rose, the string representation will be "Image of Rose"
        return f"Image of {self.flower.name}"
