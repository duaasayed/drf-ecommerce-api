from rest_framework.routers import DefaultRouter
from . import views

app_name = 'dashboard'

router = DefaultRouter()

router.register(r'products', views.ProductViewset, 'products')
router.register(r'representatives',
                views.RepresentativeViewset, 'representatives')
router.register(r'orders', views.OrderViewset, 'orders')

urlpatterns = router.urls
