from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()

router.register(r'', views.OrderViewset, 'orders')

urlpatterns = router.urls

urlpatterns += [
    path('<int:pk>/invoice/', views.generate_invoices, name='invoice')
]
