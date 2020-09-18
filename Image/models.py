from django.db import models
from . import NST
# Create your models here.

Genrator = NST.Generate_Image()


class Image(models.Model):
    # file_name = models.CharField( max_length=50)
    content_image = models.ImageField(upload_to='images/content')
    style_image = models.ImageField(upload_to='images/style')

class GeneratedImage(models.Model):
    generated_image = models.ImageField(upload_to='images/generated')
