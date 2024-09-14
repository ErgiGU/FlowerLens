# serializers.py

from rest_framework import serializers
from .models import AIModel, MetricsTable, MatrixImage, FlowerImage, TrainFlower, FlowerClasses, Images

# file with serializers for the database models
class AIModelSerializer(serializers.ModelSerializer):
    """Serializer for AIModel model"""
    class Meta:
        model = AIModel
        fields = ['model_id', 'timestamp', 'version']

class MetricsTableSerializer(serializers.ModelSerializer):
    """Serializer for MetricsTable model"""
    class Meta:
        model = MetricsTable
        fields = ['model_id', 'accuracy', 'precision', 'recall', 'f1_score', 'timestamp']

class MatrixImageSerializer(serializers.ModelSerializer):
    """Serializer for MatrixImage model"""
    class Meta:
        model = MatrixImage
        fields = ['model_id', 'image_path', 'timestamp']
        
class FlowerImageSerializer(serializers.ModelSerializer):
    """Serializer for MatrixImage model"""
    class Meta:
        model = FlowerImage
        fields = ['flower', 'imag']

class FlowerClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowerClasses
        fields = ('id', 'name')

class TrainFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainFlower
        fields = ('flower', 'image')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('image_id','flower', 'image')