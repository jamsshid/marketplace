from rest_framework import serializers
from apps.products.models import Category, Product, ProductImage, Wishlist

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id','name','slug','parent','children']

    def get_children(self, obj):
        serializer = CategorySerializer(obj.children.all(), many=True)
        return serializer.data

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','image','is_feature']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
        required=False,
    )
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Product
        fields = [
           "id", "seller", "category", "category_name",
            "name", "slug", "description", "price",
            "stock", "images", 'uploaded_images', "created_at",
        ]
        read_only_fields = ["slug", "seller"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        validated_data["seller"] = self.context["request"].user
        product = super().create(validated_data)
        for image_data in uploaded_images:
            ProductImage.objects.create(product=product, image=image_data)

        return product


class WishlistSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "product", "product_details", "added_at"]
