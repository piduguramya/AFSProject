from .models import UserAccount,Account
from rest_framework import serializers

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserAccount
        fields='__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields='__all__'

