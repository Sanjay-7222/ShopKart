from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')

class ProductAdmin(admin.ModelAdmin):
    list_display =('name', 'category', 'description')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(Favourite)
admin.site.register(Chekout)