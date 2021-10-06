from django.db import models


# Create your models here.
class Seller(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username


class Products(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    unit_price = models.IntegerField()
    seller_id = models.CharField(max_length=100)
    quantity = models.IntegerField()
    product_description = models.TextField()
    product_image = models.ImageField(null=True, blank=True, upload_to='products/')

    def __str__(self):
        return self.product_name
