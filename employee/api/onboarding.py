from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from django.core.exceptions import ValidationError
from employee.services.onboarding import submit_onboarding

class OnboardingSubmitAPIView(APIView):
    """
    Public onboarding enpoint (no auth)
    """
    permission_classes = [AllowAny]

    def post(self, request, token):
        try:
            employee = submit_onboarding(token, request.data)

        except ValidationError as e:
            return Response(
                {"error":str(e)},
                status = status.HTTP_400_BAD_ERQUEST
            )

        return Response(
            {
                "status":"success",
                "employee_id":employee.employee_id
            },
            status=status.HTTP_200_OK
        )
