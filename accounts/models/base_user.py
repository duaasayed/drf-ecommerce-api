from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserManager(BaseUserManager):
    def _create_user(self, first_name, last_name, email, password, **extra_fields):
        if not first_name:
            raise ValueError("The given first_name must be set")

        if not last_name:
            raise ValueError("The given last_name must be set")

        if not email:
            raise ValueError("The given email must be set")

        extra_fields.setdefault('is_superuser', False)
        email = self.normalize_email(email)
        user = self.model(first_name=first_name,
                          last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(first_name, last_name, email, password, **extra_fields)

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(first_name, last_name, email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('Email', null=False, unique=True)
    first_name = models.CharField(
        "first name", max_length=150, null=False)
    last_name = models.CharField(
        "last name", max_length=150, null=False)
    is_active = models.BooleanField(
        "active", default=False, help_text="Designates whether this user should be treated as active.")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    @property
    def is_customer(self):
        return hasattr(self, 'customer')

    @property
    def is_store_representative(self):
        return hasattr(self, 'storerepresentative')
