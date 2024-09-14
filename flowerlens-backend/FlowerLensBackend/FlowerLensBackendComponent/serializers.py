# serializers.py

from rest_framework import serializers
from .models import AIModel, MetricsTable, MatrixImage

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