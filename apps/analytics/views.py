from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum, Count, F
from apps.orders.models import Order, OrderItem
from apps.products.models import Product


class AdminAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_revenue = (
            Order.objects.filter(status="delivered").aggregate(
                revenue=Sum("total_price")
            )["revenue"]
            or 0
        )

        status_stats = Order.objects.values("status").annotate(count=Count("id"))
        top_products = (
            OrderItem.objects.values("product__name")
            .annotate(
                total_sold=Sum("quantity"), total_earned=Sum(F("price") * F("quantity"))
            )
            .order_by("-total_sold")[:5]
        )
        low_stock_products = Product.objects.filter(stock__lt=5).values("name", "stock")

        return Response(
            {
                "overview": {
                    "total_revenue": total_revenue,
                    "total_orders": Order.objects.count(),
                    "currency": "USD",
                },
                "sales_by_status": status_stats,
                "top_selling_products": top_products,
                "inventory_alerts": low_stock_products,
            }
        )
