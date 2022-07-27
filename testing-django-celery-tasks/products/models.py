from decimal import Decimal
from django.db import models
from products.tasks import calculate_total_purchased_value

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    total_purchased_value = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class Purchase(models.Model):
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_final_value = models.DecimalField(max_digits=15, decimal_places=2)

    def save(self, *args, **kwargs):
        super(Purchase, self).save(*args, **kwargs)

        calculate_total_purchased_value.apply_async(args=[self.product.pk], countdown=2)

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
