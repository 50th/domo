from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class SystemView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        sys_version = {'version': settings.SYSTEM_VERSION}
        return Response(sys_version)
