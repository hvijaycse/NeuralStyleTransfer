from django.urls import path
from . import views

app_name = 'Image'
urlpatterns = [
    path('', views.image_view, name = 'image_upload'),
    path('success/<int:ide>', views.success, name = 'success'),
    path('views/<int:ide>', views.view_images, name = 'images'),
]