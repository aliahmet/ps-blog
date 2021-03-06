import logging
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import exception_handler as base_exception_handler

logger = logging.getLogger(__name__)


def exception_handler(exc, context):
    response = base_exception_handler(exc, context)

    if not response:
        logger.error(exc)
        response = Response({
            "details": exc.args if settings.DEBUG else "not sure",
            "message": "Houston, we have a problem!"
        }, status=500)
    return response
