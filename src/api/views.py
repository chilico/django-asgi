from adrf.decorators import api_view as async_api_view
from asgiref.sync import sync_to_async
from django.db import connection
from rest_framework.response import Response
from rest_framework.status import HTTP_503_SERVICE_UNAVAILABLE, HTTP_200_OK


@sync_to_async
def check_db():
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")


@async_api_view(["GET"])
async def healthcheck(request):
    """
    Health check endpoint to verify service and database connectivity.
    """
    try:
        await check_db()

        return Response(
            {"status": "healthy", "database": "connected"}, status=HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"status": "unhealthy", "database": "disconnected", "error": str(e)},
            status=HTTP_503_SERVICE_UNAVAILABLE,
        )
