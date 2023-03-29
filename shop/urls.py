from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoriesList.as_view(), name='categories'),
    path('products/', views.ProductsList.as_view(), name='products'),
    path('brands/<slug:slug>/', views.BrandDetails.as_view(), name='brand')
]
