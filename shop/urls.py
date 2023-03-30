from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('categories/', views.CategoriesList.as_view(), name='categories'),
    path('products/', views.ProductsList.as_view(), name='products'),
    path('brands/<slug:slug>/', views.BrandDetails.as_view(), name='brand'),
    path('sellers/<slug:slug>/', views.SellerDetails.as_view(), name='seller'),
    path('categories/<slug:slug>/',
         views.CategoryDetails.as_view(), name='category'),
    path('products/<slug:slug>/', views.ProductDetails.as_view(), name='product')
]
