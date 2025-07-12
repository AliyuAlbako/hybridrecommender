from django.urls import path
from . import views

urlpatterns = [
    # path('api/products/', views.ProductListView.as_view()),
    # path('api/recommend/<int:product_id>/', views.ContentBasedRecommendationView.as_view()),

    # Web Template Views
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('suggestions/', views.product_suggestions, name='product_suggestions'),

]
