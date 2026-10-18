from django.urls import path
from . import views

urlpatterns = [
    
    # Accounts List
    path('accounts/', views.AccountListView.as_view(), name='account_list'),

    # Balance Inquiry
    path('accounts/<str:account_number>/', views.BalanceInquiryView.as_view(), name='balance_inquiry'),

    # Deposit
    path('accounts/<str:account_number>/deposit/', views.DepositView.as_view(), name='deposit'),
    
    # Withdraw
    path('accounts/<str:account_number>/withdraw/', views.WithdrawView.as_view(), name='withdraw'),

]