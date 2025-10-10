from django.contrib import admin
from .models import (
    Product, UserInteraction, Rating,
    Cart, Order, OrderItem, UserProfile
)

# ---------------------------
# Inline for Order Items (so items show inside Order in Admin)
# ---------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

# ---------------------------
# Admin Classes
# ---------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "source")
    search_fields = ("name", "category", "description")
    list_filter = ("category", "source")


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "interaction_type", "value", "timestamp")
    list_filter = ("interaction_type", "timestamp")
    search_fields = ("user__username", "product__name")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "rating", "timestamp")
    list_filter = ("rating", "timestamp")
    search_fields = ("user__username", "product__name")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "total_price")
    search_fields = ("user__username", "product__name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total", "currency", "created_at")
    list_filter = ("currency", "created_at")
    search_fields = ("user__username",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "unit_price", "total_price")
    search_fields = ("order__id", "product__name")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "hobby", "interest")
    search_fields = ("user__username", "hobby", "interest")
