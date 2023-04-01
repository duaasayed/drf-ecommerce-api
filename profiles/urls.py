from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'address-book', views.AddressBookViewset, 'address_book')

urlpatterns = router.urls
