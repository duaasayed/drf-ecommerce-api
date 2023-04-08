from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'shop'

router = DefaultRouter()
router.register(r'reviews', views.ReviewViewset, 'reviews')
router.register(r'questions', views.QuestionViewset, 'questions')
router.register(r'questions/(?P<question_id>\d+)/answers',
                views.AnswerViewset, 'answers')


urlpatterns = [
    path('categories/', views.CategoriesList.as_view(), name='categories'),
    path('products/', views.ProductsList.as_view(), name='products'),
    path('brands/<slug:slug>/', views.BrandDetails.as_view(), name='brand'),
    path('sellers/<slug:slug>/', views.SellerDetails.as_view(), name='seller'),
    path('categories/<slug:slug>/',
         views.CategoryDetails.as_view(), name='category'),
    path('products/<slug:slug>/', views.ProductDetails.as_view(), name='product'),
    path('products/<int:product_id>/', include(router.urls))
]
