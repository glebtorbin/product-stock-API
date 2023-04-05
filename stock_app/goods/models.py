from django.db import models


class Stock(models.Model):
    title = models.CharField(max_length=200)
    avail_sign = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=500)
    code = models.BigIntegerField(unique=True)
    quantity = models.IntegerField(default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    stocks = models.ManyToManyField(Stock, related_name='products')

    def __str__(self):
        return self.title


class Product_attr(models.Model):
    name = models.CharField(max_length=200)
    value = models.TextField(null=True)
    prod_id = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        blank=False, null=False
    )

    def __str__(self):
        return self.name


