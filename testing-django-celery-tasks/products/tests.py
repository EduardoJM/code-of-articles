from django.test import TestCase
from unittest.mock import patch
from products.models import Product, Purchase
from products.tasks import calculate_total_purchased_value

class TaskTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="First Product", price=60)

    @patch("products.tasks.calculate_total_purchased_value.apply_async")
    def test_save_purchase_call_task(self, apply_async_mock):
        item = Purchase()
        item.product = self.product
        item.purchase_final_value = 50
        item.save()

        apply_async_mock.assert_called_once_with(args=[self.product.pk], countdown=2)

    @patch("products.tasks.calculate_total_purchased_value.apply_async")
    def test_background_task(self, apply_async_mock):
        purchase1 = Purchase()
        purchase1.product = self.product
        purchase1.purchase_final_value = 50
        purchase1.save()
        
        purchase2 = Purchase()
        purchase2.product = self.product
        purchase2.purchase_final_value = 40
        purchase2.save()

        calculate_total_purchased_value(self.product.pk)

        product = Product.objects.get(id=self.product.pk)

        self.assertEqual(product.total_purchased_value, 90)
