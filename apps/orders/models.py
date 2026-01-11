from django.db import models
from django.conf import settings
from apps.products.models import Product
from django.db import transaction
from apps.orders.tasks import send_order_confirmation_email
from django.db.models import CheckConstraint, Q

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def make_order(self, shipping_address, contact_number):
        cart_items = self.items.all()
        if not cart_items.exists():
            raise ValueError("Cart is empty")

        with transaction.atomic():
            total_sum = sum(item.product.price * item.quantity for item in cart_items)
            from .models import (
                Order,
                OrderItem,
            )  

            order = Order.objects.create(
                user=self.user,
                total_price=total_sum,
                shipping_address=shipping_address,
                contact_number=contact_number,
            )

            for item in cart_items:
                if item.product.stock < item.quantity:
                    raise ValueError(f"Not enough stock for {item.product.name}")

                item.product.stock -= item.quantity
                item.product.save()

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                )
            send_order_confirmation_email.delay(order.id, self.user.email)
            cart_items.delete()
            return order

    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders"
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    shipping_address = models.TextField()
    contact_number = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    class Meta:
        constraints = [
            CheckConstraint(condition=Q(price__gte=0), name="price_cannot_be_negative")
        ]
        indexes = [
            models.Index(fields=["order", "product"]),
        ]

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Unknown Product'}"
