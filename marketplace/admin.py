from django.contrib import admin

from marketplace.models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'productitem', 'quantity', 'updated_at')

admin.site.register(Cart, CartAdmin)
