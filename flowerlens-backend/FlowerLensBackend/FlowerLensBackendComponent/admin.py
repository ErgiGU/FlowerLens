from django.contrib import admin
from .models import Flower, FlowerImage, Photo, AIModel, MetricsTable, MatrixImage, PredictionResult

admin.site.register(Flower)
admin.site.register(FlowerImage)
admin.site.register(Photo)
admin.site.register(AIModel)
admin.site.register(MetricsTable)
admin.site.register(MatrixImage)
admin.site.register(PredictionResult)

