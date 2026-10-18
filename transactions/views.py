from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .serializers import AccountDetailSerializer

from django.db import transaction
from .serializers import AmountInputSerializer, TransactionResponseSerializer



class BalanceInquiryView(APIView):
    """
    Balance Inquiry API
    GET /api/accounts/<account_number>/
    
    Returns the current balance of the specified account.
    """
    
    def get(self, request, account_number):
        try:
            account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            # Handles Section 2.3: Unknown account error
            return Response(
                {
                    'status': 'error',
                    'error_code': 'UNKNOWN_ACCOUNT',
                    'message': f'Account {account_number} does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AccountDetailSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class AccountListView(APIView):
    """
    List All Accounts API
    GET /api/accounts/
    
    Returns a list of all accounts with their balances.
    """
    
    def get(self, request):
        accounts = Account.objects.all().order_by('account_number')
        serializer = AccountDetailSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class DepositView(APIView):
    """
    Deposit API
    POST /api/accounts/<account_number>/deposit/
    
    Adds the specified amount to the account balance.
    Guarantees ACID properties:
    - Atomicity: Uses transaction.atomic()
    - Consistency: Balance never negative (enforced by model validator)
    - Isolation: Uses select_for_update() to lock the row
    - Durability: PostgreSQL writes to disk before response
    """
    
    def post(self, request, account_number):
        # Step 1: Validate input (handles missing fields, invalid amounts)
        serializer = AmountInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'error_code': 'INVALID_INPUT',
                    'message': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        amount = serializer.validated_data['amount']
        
        # Step 2: Execute transaction with ACID guarantees
        try:
            with transaction.atomic():
                # Lock the account row for Isolation (prevents lost updates)
                account = Account.objects.select_for_update().get(
                    account_number=account_number
                )
                
                # Perform the deposit
                account.balance += amount
                account.save()  # Durability: PostgreSQL commits to disk
                
        except Account.DoesNotExist:
            # Handles Section 2.3: Unknown account
            return Response(
                {
                    'status': 'error',
                    'error_code': 'UNKNOWN_ACCOUNT',
                    'message': f'Account {account_number} does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Step 3: Return success response in assignment format
        response_serializer = TransactionResponseSerializer({
            'status': 'success',
            'account': account.account_number,
            'balance': account.balance
        })
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)