from django.db import models

class DailySales(models.Model):
    date = models.DateField(unique=True)
    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    top_product = models.ForeignKey(
        "products.Product", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name_plural = "Daily Sales Analytics"
