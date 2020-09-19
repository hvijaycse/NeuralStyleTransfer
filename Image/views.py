
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.conf import settings
from . import forms
from . import models
import os
from . import NST


BASE_DIR = settings.BASE_DIR
Genrator = NST.Generate_Image()
# Create your views here.


def image_view(request):

    if request.method == 'POST':
        form = forms.ImageForm(request.POST, request.FILES)

        if form.is_valid():
            New_image = form.save()
            return HttpResponseRedirect(reverse('Image:images', args=(New_image.pk,)))
    else:
        form = forms.ImageForm
    return render(request, 'Image/image_form.html', {'form': form})


def view_images(request, ide):
    if request.method == 'GET':
        Images = models.Image.objects.get(pk=ide)
        Gen_img = Genrator.Generate_image(Images)
        Gen_img_object = models.GeneratedImage()
        Gen_img_object.generated_image = Gen_img
        Gen_img_object.save()
        cxt = {'image_path': Gen_img_object.generated_image.url}
        return render(
            request, 'Image/display_image.html', context=cxt
        )
