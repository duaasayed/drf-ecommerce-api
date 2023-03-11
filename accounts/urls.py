from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/',
         views.ActivateView.as_view(), name='activate'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm",),
    path('auth-token/', views.AuthToken.as_view(), name='auth_token'),
    path('auth-user/', views.auth_user, name='auth_user')
]
