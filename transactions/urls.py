from django.urls import path
from . import views

urlpatterns = [
    
    # Accounts List
    path('accounts/', views.AccountListView.as_view(), name='account_list'),

    # Balance Inquiry
    path('accounts/<str:account_number>/', views.BalanceInquiryView.as_view(), name='balance_inquiry'),
]