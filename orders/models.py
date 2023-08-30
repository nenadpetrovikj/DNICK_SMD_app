from decimal import Decimal
from django.conf import settings
from django.db import models

from store.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')

    # The data below may seem like a duplicate since the order will be tied to a user from the user table that may have this data already
    # A billing address is an address associated with your credit or debit card account. In my system it is assumed that
    # the billing address and the delivery are the same. So I store this "duplicate" data, because I may have an account, but decide to pay
    # with my father's debit card, and I would need to enter my father's debit card data (his name, his address, etc.)
    # The system can be further developed where the billing and delivery addresses are not the same

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30)

    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    post_code = models.CharField(max_length=12)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=8, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.created)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)