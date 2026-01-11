from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.orders.views import CartViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"history", OrderViewSet, basename="order-history")
urlpatterns = [
    path("", include(router.urls)),
]
