from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'address-book', views.AddressBookViewset, 'address_book')
router.register(r'lists', views.ListsViewset, 'lists')
router.register(r'list-products', views.ListProductViewset, 'lists_products')

urlpatterns = router.urls

urlpatterns += [
    path('manage-2fa/', views.manage_2fa, name='manage_2fa')
]
