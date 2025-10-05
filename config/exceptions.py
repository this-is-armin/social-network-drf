from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {'detail': 'Something went wrong on the server.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    if response.data.get('code') == 'user_not_found':
        return Response(
            {'detail': 'This user account no longer exists. Please log in aagain.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    
    return response