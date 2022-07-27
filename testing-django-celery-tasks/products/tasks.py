from celery import shared_task

@shared_task(name="calculate_total_purchased_value")
def calculate_total_purchased_value(id_product):
    from products.models import Product, Purchase

    product = Product.objects.filter(pk=id_product).first()
    purchases = Purchase.objects.filter(product=product).all()

    value = 0
    for purchase in purchases:
        value += purchase.purchase_final_value

    product.total_purchased_value = value
    product.save()
