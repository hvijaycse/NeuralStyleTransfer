from django import forms
from . import models


class ImageForm(forms.ModelForm):

    class Meta:
        model = models.Image
        fields = ['content_image', 'style_image']