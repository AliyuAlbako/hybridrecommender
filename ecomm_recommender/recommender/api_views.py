# recommender/api_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .evaluate import run_all_evaluations
from .recommendation.hybrid import get_hybrid_recommendations
from .models import Product, UserInteraction, Rating
from .serializers import (
    UserSerializer, RegisterSerializer, ProductSerializer
)

# # ---------- AUTH ----------
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "User registered successfully."}, status=201)
#     return Response(serializer.errors, status=400)
#
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def profile(request):
#     serializer = UserSerializer(request.user)
#     return Response(serializer.data)
#
# # ---------- PRODUCTS ----------
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)
#
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)
#
# # ---------- INTERACTIONS ----------
# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def product_interact(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     itype = request.data.get("interaction_type", "view")
#     value = float(request.data.get("value", 1.0))
#     UserInteraction.objects.create(
#         user=request.user,
#         product=product,
#         interaction_type=itype,
#         value=value,
#     )
#     return Response({"status": "interaction recorded"})
#
# # ---------- RATING ----------
# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def product_rate(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     rating_val = float(request.data.get("rating", 0))
#     Rating.objects.update_or_create(
#         user=request.user,
#         product=product,
#         defaults={"rating": rating_val},
#     )
#     return Response({"status": "rating saved"})
#
# # ---------- HYBRID RECOMMENDATIONS ----------
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def product_recommendations(request, pk):
#     """Return hybrid recommendations for a given product pk (internal + external)."""
#     get_object_or_404(Product, pk=pk)
#
#     recs = get_hybrid_recommendations(
#         user_id=request.user.id if request.user.is_authenticated else None,
#         product_id=pk,
#         top_n=6,
#         alpha=0.6
#     )
#
#     # Serialize internal DB products
#     internal = ProductSerializer(recs["internal"], many=True).data
#
#     # External recommendations are already dicts
#     external = recs["external"]
#
#     return Response({
#         "internal_recommendations": internal,
#         "external_recommendations": external,
#     })
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def evaluate_system(request):
#     """
#     API endpoint: GET /api/evaluate/
#     Returns recommendation system evaluation metrics
#     """
#     results = run_all_evaluations()
#     return Response(results)

# fix 1

# recommender/api_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .evaluate import run_all_evaluations
from .recommendation.hybrid import get_hybrid_recommendations
from .models import Product, UserInteraction, Rating, UserProfile
from .serializers import (
    UserSerializer, RegisterSerializer, ProductSerializer
)


# ---------- AUTH ----------
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully."}, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    """Return logged-in user's profile (with hobby & interest)."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# ---------- PRODUCTS ----------
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def product_list(request):
#     """
#     GET /api/products/
#     Supports optional query params:
#       ?hobby=Music&interest=Tech
#     Also automatically personalizes results for logged-in users.
#     """
#     products = Product.objects.all()
#
#     hobby = request.GET.get("hobby", "")
#     interest = request.GET.get("interest", "")
#
#     # ✅ If user is authenticated, use their saved hobby & interest
#     if request.user.is_authenticated:
#         try:
#             profile = UserProfile.objects.get(user=request.user)
#             hobby = hobby or (profile.hobby or "")
#             interest = interest or (profile.interest or "")
#         except UserProfile.DoesNotExist:
#             pass
#
#     # ✅ Filter products based on hobby/interest keywords
#     if hobby or interest:
#         products = products.filter(
#             Q(category__icontains=hobby)
#             | Q(description__icontains=hobby)
#             | Q(category__icontains=interest)
#             | Q(description__icontains=interest)
#         ).distinct()
#
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# ---------- PRODUCTS ----------
@api_view(["GET"])
@permission_classes([AllowAny])
def product_list(request):
    """
    Returns products.
    - If user is authenticated → filter based on hobby/interest.
    - Else → return all products.
    """
    products = Product.objects.all()

    if request.user.is_authenticated:
        profile = getattr(request.user, "userprofile", None)
        if profile:
            hobby = profile.hobby or ""
            interest = profile.interest or ""

            # Match either hobby or interest in product name, description, or category
            from django.db.models import Q
            products = products.filter(
                Q(name__icontains=hobby) |
                Q(description__icontains=hobby) |
                Q(category__icontains=hobby) |
                Q(name__icontains=interest) |
                Q(description__icontains=interest) |
                Q(category__icontains=interest)
            )

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([AllowAny])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


# ---------- INTERACTIONS ----------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def product_interact(request, pk):
    product = get_object_or_404(Product, pk=pk)
    itype = request.data.get("interaction_type", "view")
    value = float(request.data.get("value", 1.0))
    UserInteraction.objects.create(
        user=request.user,
        product=product,
        interaction_type=itype,
        value=value,
    )
    return Response({"status": "interaction recorded"})


# ---------- RATING ----------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def product_rate(request, pk):
    product = get_object_or_404(Product, pk=pk)
    rating_val = float(request.data.get("rating", 0))
    Rating.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={"rating": rating_val},
    )
    return Response({"status": "rating saved"})


# ---------- HYBRID RECOMMENDATIONS ----------
@api_view(["GET"])
@permission_classes([AllowAny])
def product_recommendations(request, pk):
    """Return hybrid recommendations for a given product pk (internal + external)."""
    get_object_or_404(Product, pk=pk)

    recs = get_hybrid_recommendations(
        user_id=request.user.id if request.user.is_authenticated else None,
        product_id=pk,
        top_n=6,
        alpha=0.6
    )

    internal = ProductSerializer(recs["internal"], many=True).data
    external = recs["external"]

    return Response({
        "internal_recommendations": internal,
        "external_recommendations": external,
    })


# ---------- EVALUATION ----------
@api_view(["GET"])
@permission_classes([AllowAny])
def evaluate_system(request):
    """Return model evaluation metrics."""
    results = run_all_evaluations()
    return Response(results)
