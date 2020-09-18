
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from . import forms
from . import models
from . import NST
import os
from pathlib import PureWindowsPath as PWP

BASE_DIR = PWP(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Create your views here.
Generator = NST.Generate_Image()


def image_view(request):

    if request.method == 'POST':
        form = forms.ImageForm(request.POST, request.FILES)

        if form.is_valid():
            New_image = form.save()
            return HttpResponseRedirect(reverse('Image:success', args=(New_image.pk,)))
    else:
        form = forms.ImageForm
    return render(request, 'Image/image_form.html', {'form': form})


def success(request, ide):
    Image = models.Image.objects.get(pk=ide)
    # print(BASE_DIR)
    # print(PWP(Image.content_image.url[1:]))
    content_image_url = os.path.join(BASE_DIR, PWP(Image.content_image.url[1:]))
    style_image_url = os.path.join(BASE_DIR, PWP(Image.style_image.url[1:]))
    # print(content_image_url)
    Generator.Generate_image(content_image_url, style_image_url, ide)
    return HttpResponseRedirect( (reverse('Image:images', args=(ide,))))


def view_images(request, ide):
    if request.method == 'GET':
        # Images = models.Image.objects.all()
        gen_path = '/media/images/generated/' + str(ide) + '.jpg'
        cxt = {'gen_path': gen_path}
        return render(
            request, 'Image/display_image.html', cxt
        )
