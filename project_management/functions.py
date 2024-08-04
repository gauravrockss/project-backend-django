from rest_framework.response import Response
from rest_framework import status

class BaseResponseView:
    def success_response(self, message, data=None, status_code=status.HTTP_200_OK):
        response = {"success": message}
        if data is not None:
            response["data"] = data
        return Response(response, status=status_code)

    def error_response(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        return Response({"success": message}, status=status_code)
