from django.contrib import admin

from api import models



admin.site.register(models.MotherCategory)
admin.site.register(models.Category)
admin.site.register(models.Country)
admin.site.register(models.City)
admin.site.register(models.State)
admin.site.register(models.Product)
admin.site.register(models.Variant)
admin.site.register(models.ProductImage)
admin.site.register(models.Cart)

admin.site.register(models.Order)
admin.site.register(models.OrderItem)


