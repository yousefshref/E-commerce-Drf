from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from . import serializers
from . import models


@api_view(['POST'])
def signup(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = serializers.UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})



@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = serializers.UserSerializer(request.user)
    return Response(serializer.data)



@api_view(['GET', 'POST'])
def mother_category_list(request):
    if request.method == 'GET':
        query = models.MotherCategory.objects.all()
        serializer = serializers.MotherCategorySerializer(query, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.MotherCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def mother_category_detail(request, pk):
    try:
        query = models.MotherCategory.objects.get(pk=pk)
    except models.MotherCategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.MotherCategorySerializer(query)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.MotherCategorySerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        query.delete()
        return Response({'deleted': True})









@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        query = models.Category.objects.all()

        if request.GET.get('mother_category'):
            query = models.Category.objects.filter(mother_category__id=request.GET.get('mother_category'))

        serializer = serializers.CategorySerializer(query, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)




@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    try:
        query = models.Category.objects.get(pk=pk)
    except models.Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.CategorySerializer(query)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.CategorySerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        query.delete()
        return Response({'deleted': True})




@api_view(['GET', 'POST'])
def country_list(request):
    if request.method == 'GET':
        query = models.Country.objects.all()
        serializer = serializers.CountrySerializer(query, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.CountrySerializer(data=request.data)
        if serializer.is_valid():
            country = serializer.save()
            # cities
            cities = request.data.get('cities')
            for city in cities:
                models.City.objects.create(name=city['name'], country=country).save()
                # states
                created_city = models.City.objects.get(name=city['name'], country=country)
                states = city['states']
                for state in states:
                    models.State.objects.create(name=state['name'], shipping_fee=state['shipping_fee'], city=created_city)
            return Response(serializer.data)
        return Response(serializer.errors)




@api_view(['GET', 'PUT', 'DELETE'])
def country_detail(request, pk):
    try:
        query = models.Country.objects.get(pk=pk)
    except models.Country.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.CountrySerializer(query)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.CountrySerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            country = serializer.save()
            # cities
            cities = request.data.get('cities')
            for city in cities:
                # check if the city with id --> update it and check also the states if id exist update it
                if city.get('id'): #update
                    models.City.objects.filter(id=city['id']).update(name=city['name'])
                    # states
                    states = city['states']
                    get_city = models.City.objects.get(id=city['id'])
                    for state in states:
                        if state.get('id'): #update
                            models.State.objects.filter(id=state['id']).update(name=state['name'], shipping_fee=state['shipping_fee'])
                        else:
                            models.State.objects.create(name=state['name'], shipping_fee=state['shipping_fee'], city=get_city)
                else:
                    models.City.objects.create(name=city['name'], country=country).save()
                    created_city = models.City.objects.get(name=city['name'], country=country)
                    states = city['states']
                    for state in states:
                        models.State.objects.create(name=state['name'], shipping_fee=state['shipping_fee'], city=created_city)
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        query.delete()
        return Response({'deleted': True})




@api_view(['GET', 'POST'])
def city_list(request):
    if request.method == 'GET':
        query = models.City.objects.all()
        if request.GET.get('country'):
            query = models.City.objects.filter(country__id=request.GET.get('country'))
        serializer = serializers.CitySerializer(query, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)




@api_view(['GET', 'PUT', 'DELETE'])
def city_detail(request, pk):
    try:
        query = models.City.objects.get(pk=pk)
    except models.City.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.CitySerializer(query)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.CitySerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        query.delete()
        return Response({'deleted': True})




@api_view(['GET', 'POST'])
def state_list(request):
    if request.method == 'GET':
        query = models.State.objects.all()
        if request.GET.get('city'):
            query = models.State.objects.filter(city__id=request.GET.get('city'))
        serializer = serializers.StateSerializer(query, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.StateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)




@api_view(['GET', 'PUT', 'DELETE'])
def state_detail(request, pk):
    try:
        query = models.State.objects.get(pk=pk)
    except models.State.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.StateSerializer(query)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.StateSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        query.delete()
        return Response({'deleted': True})



from rest_framework.pagination import PageNumberPagination

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        query = models.Product.objects.all()

        search = request.GET.get('search')
        if search:
            query = query.filter(name__contains=search)
        
        if request.GET.get('category'):
            query = query.filter(category__id=request.GET.get('category'))
        
        if request.GET.get('mother_category'):
            query = query.filter(mother_category__id=request.GET.get('mother_category'))
        
        result_page = paginator.paginate_queryset(query, request)
        serializer = serializers.ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            # variants
            variants = request.data.get('variants')
            if variants:
                for variant in variants:
                    models.Variant.objects.create(product=product, **variant)
            # images
            images = request.data.get('images')
            if images:
                for image in images:
                    models.ProductImage.objects.create(product=product, **image)
            return Response(serializer.data)
        return Response(serializer.errors)




@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        query = models.Product.objects.get(pk=pk)
    except models.Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.ProductSerializer(query)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.ProductSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # images
            all_images = models.ProductImage.objects.filter(product=query)
            for image in all_images:
                image.delete()
            images = request.data.get('images')
            if images:
                for img in images:
                    models.ProductImage.objects.create(product=query, **img)

            # variants
            variants = request.data.get('variants')
            if variants:
                for variant in variants:
                    models.Variant.objects.create(product=query, **variant)
            updatedVariants = request.data.get('updatedVariants')
            if updatedVariants:
                for updatedVariant in updatedVariants:
                    variant = models.Variant.objects.get(pk=updatedVariant['id'])
                    variant.name = updatedVariant['name']
                    variant.description = updatedVariant['description']
                    variant.buy_price = updatedVariant['buy_price']
                    variant.sell_price = updatedVariant['sell_price']
                    variant.stock = updatedVariant['stock']
                    variant.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

    elif request.method == 'DELETE':
        query.delete()
        return Response({'deleted': True})
    



@api_view(['GET', 'POST'])
def variant_list(request):
    if request.method == 'GET':
        query = models.Variant.objects.all()

        if request.GET.get('product'):
            query = models.Variant.objects.filter(product__id=request.GET.get('product'))

        serializer = serializers.VariantSerializer(query, many=True)
        return Response(serializer.data)
    

    elif request.method == 'POST':
        serializer = serializers.VariantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    



@api_view(['GET', 'PUT', 'DELETE'])
def variant_detail(request, pk):
    try:
        query = models.Variant.objects.get(pk=pk)
    except models.Variant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.VariantSerializer(query)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.VariantSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        query.delete()
        return Response({'deleted': True})




@api_view(['GET', 'POST'])
def product_image_list(request):
    if request.method == 'GET':
        query = models.ProductImage.objects.all()
        if request.GET.get('product'):
            query = models.ProductImage.objects.filter(product__id=request.GET.get('product'))
        serializer = serializers.ProductImageSerializer(query, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    


@api_view(['GET', 'PUT', 'DELETE'])
def product_image_detail(request, pk):
    try:
        query = models.ProductImage.objects.get(pk=pk)
    except models.ProductImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.ProductImageSerializer(query)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.ProductImageSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        query.delete()
        return Response({'deleted': True})





@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_detail(request, pk):
    try:
        query = models.Cart.objects.get(pk=pk)
    except models.Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.CartSerializer(query)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.CartSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        query.delete()
        return Response({'deleted': True})

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_list(request):
    if request.method == 'GET':
        query = models.Cart.objects.all()
        if request.GET.get('user'):
            query = models.Cart.objects.filter(user__id=request.GET.get('user'))
        serializer = serializers.CartSerializer(query, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = serializers.CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)




from datetime import datetime


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def orders_list(request):
    if request.method == 'GET':
        query = models.Order.objects.all()

        if not request.user.is_superuser:
            query = models.Order.objects.filter(user__id=request.user.id)

        status = request.GET.get('status')
        if status:
            query = query.filter(status=status)
        
        date_from = request.GET.get('date_from')

        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(created_at__date__gte=date_from)

        date_to = request.GET.get('date_to')
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(created_at__date__lte=date_to)

        serializer = serializers.OrderSerializer(query, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data=request.data.copy()
        data['user'] = request.user.id
        serializer = serializers.OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            
            # items
            items = data.get('order_items')
            # check if there's an order is out of stock
            out_of_stock_items = []
            for item in items:
                variant = models.Variant.objects.get(pk=item['variant'])
                if variant.stock < item['quantity']:
                    out_of_stock_items.append(variant.name)
            if out_of_stock_items:
                order_just_created = models.Order.objects.get(pk=order.id)
                order_just_created.delete()
                return Response({'error': f'يرجي اختيار عدد اقل من المنتج {", ".join(out_of_stock_items)}'})
            else:
                for item in items:
                    variant = models.Variant.objects.get(pk=item['variant'])
                    item['order'] = order.id
                    item['price'] = item['quantity'] * variant.sell_price
                    item_ser = serializers.OrderItemSerializer(data=item)
                    if item_ser.is_valid():
                        item_ser.save()
                        variant.stock -= item['quantity']
                        variant.save()
                return Response(serializer.data)
            # items
 
        return Response(serializer.errors)


@api_view(['DELETE'])
def delete_user_cart(request):
    cart = models.Cart.objects.filter(user__id=request.user.id)
    for i in cart:
        i.delete()
    return Response({'deleted': True})






