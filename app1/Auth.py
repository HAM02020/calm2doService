from .models import *

from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed

class UserAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get("token") #同request.GET["token"]
        user_token_obj = UserToken.objects.filter(token=token).first()

        if user_token_obj:
            return user_token_obj.user,user_token_obj.token
        else:
            raise AuthenticationFailed("认证失败")

from django.utils.deprecation import MiddlewareMixin

class DisableCSRFCheck(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening