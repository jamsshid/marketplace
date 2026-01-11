from celery import shared_task
from django.utils import timezone
from apps.orders.models import Order
from apps.analytics.models import DailySales
from django.db.models import Sum, Count


@shared_task
def generate_daily_report():
    today = timezone.now().date()
    stats = Order.objects.filter(created_at__date=today).aggregate(
        count=Count("id"), revenue=Sum("total_price")
    )

    DailySales.objects.update_or_create(
        date=today,
        defaults={
            "total_orders": stats["count"] or 0,
            "total_revenue": stats["revenue"] or 0,
        },
    )
    return f"Report for {today} generated."
