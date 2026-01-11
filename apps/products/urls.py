from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.products.views import ProductViewSet, CategoryViewSet, WishlistViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories",CategoryViewSet, basename="category")
router.register(r"wishlist", WishlistViewSet, basename="wishlist")

urlpatterns = [
    path("", include(router.urls)),
]
