from django.db import models
import os
from django.conf import settings

# Create your models here.

def product_image_upload_path(instance, filename):
    return f'{instance.product.reference}/images/{filename}'

class Product(models.Model):
    title = models.CharField(max_length=100)
    reference = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()
    price_dolar = models.DecimalField(max_digits=10, decimal_places=2)
    is_popular = models.BooleanField()
    is_new = models.BooleanField()
    discontinued = models.BooleanField()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_path)

    def save(self, *args, **kwargs):
        directory = os.path.join(settings.MEDIA_ROOT, f'{self.product.reference}/images/')
        if not os.path.exists(directory):
            os.makedirs(directory)
        super(ProductImage, self).save(*args, **kwargs)