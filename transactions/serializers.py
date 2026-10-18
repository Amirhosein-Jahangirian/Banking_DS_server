from rest_framework import serializers
from .models import Account
from decimal import Decimal

class AccountDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Balance Inquiry API.
    Read-only, returns only account_number and balance.
    """
    class Meta:
        model = Account
        fields = ['account_number', 'balance']
        read_only_fields = ['account_number', 'balance']


class AmountInputSerializer(serializers.Serializer):
    """
    Validates the amount field for deposit/withdraw operations.
    Handles Section 2.3: Negative or invalid amount, Missing fields
    """
    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        min_value=Decimal('0.01'),  # Must be positive
        error_messages={
            'invalid': 'Amount must be a valid number',
            'min_value': 'Amount must be greater than zero',
            'required': 'Amount field is required'
        }
    )


class TransactionResponseSerializer(serializers.Serializer):
    """
    Formats the success response to match the assignment example:
    {"status": "success", "account": "A1001", "balance": 800}
    """
    status = serializers.CharField(default='success')
    account = serializers.CharField()
    balance = serializers.DecimalField(max_digits=15, decimal_places=2)
    
    
