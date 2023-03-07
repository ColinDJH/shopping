import datetime

import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from user.models import UserModel


def get_token(payload, timeout):
    salt = settings.SECRET_KEY
    headers = {
        "typ": "jwt_",
        "alg": "HS256",
    }
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)  # 设置到期时间
    token = jwt.encode(payload=payload, key=salt, headers=headers, algorithm='HS256')
    return token


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.META.get('HTTP_AUTHTOKEN', "")
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        except (jwt.DecodeError, jwt.InvalidSignatureError):
            raise exceptions.AuthenticationFailed('Invalid Token')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        user_id = payload.get("id")
        user = UserModel.objects.filter(id=user_id).first()
        if not user:
            raise exceptions.AuthenticationFailed("Unauthenticated")

        return user, None
