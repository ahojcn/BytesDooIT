from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response


class CSRFTokenView(APIView):

    @csrf_exempt
    def post(self, request):
        """
        获取 csrf token
        """
        resp_data = {'status': 0, 'msg': 'success', 'data': {}}
        get_token(request)
        resp_obj = Response(resp_data)
        return resp_obj
