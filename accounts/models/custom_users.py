from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Customer(UserModel):
    pass
