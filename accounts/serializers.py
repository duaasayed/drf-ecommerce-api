from rest_framework import serializers
from .models.custom_users import Customer
from rest_framework.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email',
                  'password1', 'password2', 'is_active']
        extra_kwargs = {'is_active': {'read_only': True}}

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError('Passwords do not match')
        return super().validate(attrs)

    def create(self, validated_data):
        password = [validated_data.pop(key)
                    for key in ['password1', 'password2']][0]
        customer = self.Meta.model(**validated_data)
        customer.set_password(password)
        customer.is_active = False
        customer.save()
        return customer
