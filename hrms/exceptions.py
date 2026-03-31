from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError):
        return Response(
            {'error': 'A record with this data already exists. Please check for duplicate Employee ID or Email.'},
            status=status.HTTP_409_CONFLICT
        )

    if response is not None:
        # Flatten validation errors into a single message
        errors = response.data
        if isinstance(errors, dict):
            messages = []
            for field, msgs in errors.items():
                if isinstance(msgs, list):
                    for msg in msgs:
                        messages.append(f"{field}: {msg}")
                else:
                    messages.append(f"{field}: {msgs}")
            response.data = {'error': ' | '.join(messages)}

    return response
