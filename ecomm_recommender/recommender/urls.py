
from django.urls import path
from . import views
from django.urls import path
from .views_auth import RegisterView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api_views

urlpatterns = [

# Auth
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", api_views.profile, name="profile"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", LoginView.as_view(), name="login"),


    # Products
    path("products/", api_views.product_list, name="product_list"),
    path("products/<int:pk>/", api_views.product_detail, name="product_detail"),
    path("products/<int:pk>/recommendations/", api_views.product_recommendations, name="product_recommendations"),

    # Interactions & Ratings
    path("products/<int:pk>/interact/", api_views.product_interact, name="product_interact"),
    path("products/<int:pk>/rate/", api_views.product_rate, name="product_rate"),
]
