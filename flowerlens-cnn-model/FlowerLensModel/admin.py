from django.contrib import admin
from .models import FlowerClasses, TrainFlower, Images

# models registered for the DB
admin.site.register(FlowerClasses)
admin.site.register(TrainFlower)
admin.site.register(Images)