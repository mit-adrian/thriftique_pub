from django.contrib import admin

from menu.models import CategoryModel, ProductModel

class CatergoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'vendor', 'updated_at',)
    search_fields = ('category_name', 'vendor__vendor_name',)

class ProductModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_title',)}
    list_display = ('product_title', 'category', 'vendor', 'price', 'is_available', 'updated_at',)
    search_fields = ('product_title', 'category__category_name', 'vendor__vendor_name', 'price',)
    list_filter = ('is_available',)


# Register your models here.

admin.site.register(CategoryModel, CatergoryModelAdmin)
admin.site.register(ProductModel, ProductModelAdmin)