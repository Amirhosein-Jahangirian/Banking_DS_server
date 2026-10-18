from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .serializers import AccountDetailSerializer


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