from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,CategoryAdmin)
admin.site.register(Cart)
admin.site.register(Favourite)