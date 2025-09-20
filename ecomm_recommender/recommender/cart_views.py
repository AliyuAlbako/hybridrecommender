# recommender/cart_views.py
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cart, Product

# ---------------------------
# Serializers
# ---------------------------
class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "image_url", "source", "product_url")


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True, required=False)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "product", "product_id", "quantity", "total_price")

    def get_total_price(self, obj):
        # return decimal/float as string to avoid JSON serialization issues
        total = obj.total_price
        try:
            return str(total)
        except Exception:
            return total


# ---------------------------
# Views
# ---------------------------
class AddToCartView(APIView):
    """
    POST /api/cart/add/
    body: { "product_id": 1, "quantity": 2 }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response({"detail": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except Exception:
            return Response({"detail": "quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=product_id)

        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product, defaults={"quantity": quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)


class CartListView(generics.ListAPIView):
    """
    GET /api/cart/  (requires auth)
    Returns list of cart items for current user
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).select_related("product").order_by("id")


class UpdateCartItemView(APIView):
    """
    PATCH /api/cart/<item_id>/
    body: { "quantity": 3 }

    DELETE /api/cart/<item_id>/  -> remove item
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, item_id, *args, **kwargs):
        cart_item = get_object_or_404(Cart, pk=item_id, user=request.user)
        quantity = request.data.get("quantity")

        if quantity is None:
            return Response({"detail": "quantity is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            q = int(quantity)
            if q < 1:
                raise ValueError
        except Exception:
            return Response({"detail": "quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = q
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)

    def delete(self, request, item_id, *args, **kwargs):
        cart_item = get_object_or_404(Cart, pk=item_id, user=request.user)
        cart_item.delete()
        return Response({"detail": "Cart item removed."}, status=status.HTTP_204_NO_CONTENT)


class ClearCartView(APIView):
    """
    POST /api/cart/clear/
    Clears current user's cart
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Cart.objects.filter(user=request.user).delete()
        return Response({"detail": "Cart cleared."}, status=status.HTTP_200_OK)


class CheckoutView(APIView):
    """
    POST /api/cart/checkout/
    This is a lightweight placeholder for checkout:
    - computes total
    - returns order summary
    - clears the cart
    (Replace with real payment/order logic as needed.)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        items = Cart.objects.filter(user=request.user).select_related("product")
        if not items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        items_list = []
        total = 0
        for it in items:
            unit_price = it.product.price or 0
            item_total = (unit_price * it.quantity) if unit_price is not None else 0
            total += item_total
            items_list.append({
                "product_id": it.product.id,
                "name": it.product.name,
                "quantity": it.quantity,
                "unit_price": str(unit_price) if unit_price is not None else None,
                "total_price": str(item_total),
            })

        # Clear cart (simulate order creation) - in real app create Order/OrderItem records
        items.delete()

        order_summary = {
            "total": str(total),
            "currency": "USD",
            "items": items_list,
        }

        return Response({"order": order_summary}, status=status.HTTP_201_CREATED)
