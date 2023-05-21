from rest_framework.routers import DefaultRouter
from . import views

app_name = 'dashboard'

router = DefaultRouter()

router.register(r'products', views.ProductViewset, 'products')
router.register(r'product-specs',
                views.ProductSpecsViewset, 'product_spec'),
router.register(r'product-colors',
                views.ProductColorsViewset, 'product_colors'),
router.register(r'product-sizes',
                views.ProductSizesViewset, 'product_sizes'),
router.register(r'product-variants',
                views.ProductVariantsViewset, 'product_variants'),
router.register(r'representatives',
                views.RepresentativeViewset, 'representatives')
router.register(r'orders', views.OrderViewset, 'orders')

urlpatterns = router.urls
