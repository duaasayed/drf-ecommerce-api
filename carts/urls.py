from . import views
from rest_framework.routers import DefaultRouter

app_name = 'carts'

router = DefaultRouter()
router.register(r'products', views.CartProductViewset, 'cart')

urlpatterns = router.urls
