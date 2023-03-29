from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoriesList.as_view(), name='categories')
]
