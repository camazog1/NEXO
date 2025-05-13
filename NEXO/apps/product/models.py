from django.db import models

def product_image_upload_path(instance, filename):
    return f'{instance.product.reference}/images/{filename}'

EXCHANGE_RATE = 1/4205.32
class Product(models.Model):
    title = models.CharField(max_length=255)
    reference = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio en COP
    price_dolar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Precio en USD
    is_popular = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    discontinued = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.price and not self.price_dolar:
            self.price_dolar = self.price * EXCHANGE_RATE
        super().save(*args, **kwargs)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_path)
