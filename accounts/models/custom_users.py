from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Customer(UserModel):
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True)
