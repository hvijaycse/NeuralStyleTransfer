from os import path
import functools
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from io import BytesIO
from django.core.files import File
from PIL import Image
# import matplotlib.pylab as plt
# from django.conf import settings
# BASE_DIR = settings.BASE_DIR


class Generate_Image():
    def __init__(self,):
        self.hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
        self.hub_module = hub.load(self.hub_handle)

    def crop_center(self, image):
        """Returns a cropped square image."""
        shape = image.shape
        new_shape = min(shape[1], shape[2])
        offset_y = max(shape[1] - shape[2], 0) // 2
        offset_x = max(shape[2] - shape[1], 0) // 2
        image = tf.image.crop_to_bounding_box(
            image, offset_y, offset_x, new_shape, new_shape)
        return image

    @functools.lru_cache(maxsize=None)
    def load_image(self, image_path, image_size=(256, 256), preserve_aspect_ratio=True):
        """Loads and preprocesses images."""
        # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
        img = Image.open(image_path)
        img = np.array(img).astype(np.float32)[np.newaxis, ...]
        if img.max() > 1.0:
            img = img / 255.
        if len(img.shape) == 3:
            img = tf.stack([img, img, img], axis=-1)
        img = self.crop_center(img)
        img = tf.image.resize(
            img, image_size, preserve_aspect_ratio=preserve_aspect_ratio)
        return img

    def Generate_image(self, images):
        output_image_size = 1024
        # The content image size can be arbitrary.
        content_img_size = (output_image_size, output_image_size)
        # recommended image size for the style image (though, other sizes work as
        # well but will lead to different results)
        output_image_size_dim = 256
        # Recommended to keep it at 256.
        style_img_size = (output_image_size_dim, output_image_size_dim)
        content_image = self.load_image(images.content_image.path,
                                        content_img_size, preserve_aspect_ratio=True)
        style_image = self.load_image(images.style_image.path, style_img_size,
                                      preserve_aspect_ratio=False)
        style_image = tf.nn.avg_pool(
            style_image, ksize=[3, 3], strides=[1, 1], padding='SAME')
        outputs = self.hub_module(tf.constant(
            content_image), tf.constant(style_image))
        stylized_image = outputs[0]
        gen_image = Image.fromarray(np.array(tf.image.convert_image_dtype(stylized_image[0],
                                                                          dtype=tf.uint8)))
        # save_dir = path.join(
        #     BASE_DIR, 'media/images/generated/' + str(ide) + '.jpg')
        # gen_image.save(save_dir)
        # return
        thumb_io = BytesIO()
        gen_image.save(thumb_io, 'JPEG', quality=100)
        return File(thumb_io, name=str(images.pk) + '.jpg')
