from rest_framework import serializers
from api import models


from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields ='__all__'


class MotherCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True, source='category')
    class Meta:
        model = models.MotherCategory
        fields = '__all__'



class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields ='__all__'

class CitySerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True, read_only=True, source='state')
    class Meta:
        model = models.City
        fields ='__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields ='__all__'



class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Variant
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    variants_details = VariantSerializer(many=True, read_only=True, source='variants')
    images_details = ProductImageSerializer(many=True, read_only=True, source='images')
    mother_category_details = MotherCategorySerializer(read_only=True, source='mother_category')
    category_details = CategorySerializer(read_only=True, source='category')
    class Meta:
        model = models.Product
        fields = '__all__'

        
class CartSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(read_only=True, source='product')
    variant_details = VariantSerializer(read_only=True, source='variant')
    class Meta:
        model = models.Cart
        fields = '__all__'



class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(read_only=True, source='product')
    variant_details = VariantSerializer(read_only=True, source='variant')
    class Meta:
        model = models.OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items_details = OrderItemSerializer(many=True, read_only=True, source='items')
    state_details = StateSerializer(read_only=True, source='state')
    class Meta:
        model = models.Order
        fields = '__all__'


