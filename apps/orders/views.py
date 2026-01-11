from rest_framework import viewsets, status, permissions
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.orders.models import Cart, CartItem, OrderItem, Order
from apps.orders.serializers import CartSerializer, CartItemSerializer, OrderSerializer
from apps.products.models import Product


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if product.stock < quantity:
            return Response(
                {"detail": f"Only {product.stock} items available in stock."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            if product.stock < (item.quantity + quantity):
                return Response(
                    {"detail": "Total quantity exceeds available stock."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            item.quantity += quantity
        else:
            item.quantity = quantity

        item.save()
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["delete"])
    def clear_cart(self, request):
        cart = request.user.cart
        cart.items.all().delete()
        return Response(
            {"message": "Savat bo'shatildi"}, status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        try:
            order = cart.make_order(
                shipping_address=request.data.get('shipping_address'),
                contact_number=request.data.get('contact_number')
            )
            return Response({"message": "Order placed!", "id": order.id}, status=201)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            "items__product"
        )
