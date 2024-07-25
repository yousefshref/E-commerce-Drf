from django.contrib import admin
from django.urls import path

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/sign-up/', views.signup),
    path('api/login/', views.login),

    path('api/user/', views.get_user),

    path('api/mother-category/', views.mother_category_list),
    path('api/mother-category/<int:pk>/', views.mother_category_detail),

    path('api/category/', views.category_list),
    path('api/category/<int:pk>/', views.category_detail),

    path('api/countries/', views.country_list),
    path('api/country/<int:pk>/', views.country_detail),

    path('api/states/', views.state_list),
    path('api/state/<int:pk>/', views.state_detail),

    path('api/cities/', views.city_list),
    path('api/city/<int:pk>/', views.city_detail),

    path('api/product/', views.product_list),
    path('api/product/<int:pk>/', views.product_detail),

    path('api/variant/', views.variant_list),
    path('api/variant/<int:pk>/', views.variant_detail),

    path('api/product-image/', views.product_image_list),
    path('api/product-image/<int:pk>/', views.product_image_detail),

    path('api/carts/', views.cart_list),
    path('api/cart/<int:pk>/', views.cart_detail),
    path('api/cart/delete/', views.delete_user_cart),

    path('api/orders/', views.orders_list),
]
