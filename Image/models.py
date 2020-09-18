from django.db import models

# Create your models here.


class Image(models.Model):
    # file_name = models.CharField( max_length=50)
    content_image = models.ImageField(upload_to='images/content')
    style_image = models.ImageField(upload_to='images/style')