from rest_framework import serializers
from .models import Account


class AccountDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Balance Inquiry API.
    Read-only, returns only account_number and balance.
    """
    class Meta:
        model = Account
        fields = ['account_number', 'balance']
        read_only_fields = ['account_number', 'balance']
