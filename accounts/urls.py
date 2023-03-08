from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('auth-token/', views.auth_tokens, name='auth_token'),
    path('auth-user/', views.auth_user, name='auth_user')
]
