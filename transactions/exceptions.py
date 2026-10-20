from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    request = context.get('request')
    
    # Ensure logging data exists even if the view was never reached
    if request and not hasattr(request, 'transaction_data'):
        request.transaction_data = {
            'action': 'unknown',
            'account': 'unknown',
            'result': 'error:malformed_request',
            'balance': 'N/A'
        }
    elif request and hasattr(request, 'transaction_data'):
        request.transaction_data['result'] = 'error:malformed_request'

    # Handle Broken JSON specifically
    if isinstance(exc, ParseError):
        return Response(
            {
                'status': 'error',
                'error_code': 'MALFORMED_REQUEST',
                'message': 'Invalid JSON or broken request payload'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Handle Unsupported Action (404/405 from RESTful routing)
    if response is not None and response.status_code in [404, 405]:
        if request and hasattr(request, 'transaction_data'):
            request.transaction_data['result'] = 'error:unsupported_action'
        return Response(
            {
                'status': 'error',
                'error_code': 'UNSUPPORTED_ACTION',
                'message': 'The requested action or endpoint is not supported'
            },
            status=response.status_code
        )

    return response