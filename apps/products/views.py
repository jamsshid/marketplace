from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.products.models import Product, Category
from apps.products.serializers import ProductSerializer, CategorySerializer
from apps.common.permissions import IsSeller, IsOwnerOrReadOnly
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.products.models import Wishlist, Product
from apps.products.serializers import WishlistSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).prefetch_related('images').order_by('-id')
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "price"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.IsAuthenticated(), IsSeller()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_queryset(self):
        return super().get_queryset()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(
        parent__isnull=True
    )
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class WishlistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        # Faqat joriy foydalanuvchining wishlistini qaytaradi
        return Wishlist.objects.filter(user=self.request.user).select_related("product")

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"detail": "product_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )

        wish_item = Wishlist.objects.filter(user=request.user, product=product)

        if wish_item.exists():
            wish_item.delete()
            return Response(
                {"message": "Product removed from wishlist."}, status=status.HTTP_200_OK
            )
        else:
            Wishlist.objects.create(user=request.user, product=product)
            return Response(
                {"message": "Product added to wishlist."},
                status=status.HTTP_201_CREATED,
            )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
