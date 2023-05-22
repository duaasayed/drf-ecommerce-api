from django.contrib import admin
from .models import Order, OrderProduct, OrderChangeHistory
# Register your models here.


class OrderProductInline(admin.StackedInline):
    model = OrderProduct


class OrderHistoryInline(admin.StackedInline):
    model = OrderChangeHistory


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline, OrderHistoryInline]


admin.site.register(Order, OrderAdmin)
