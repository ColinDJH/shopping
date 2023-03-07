from rest_framework.response import Response
from rest_framework.views import APIView
from werkzeug.security import generate_password_hash, check_password_hash

from user.models import UserModel
from user.serializers import UserSerializers, UserLoginSerializers, UserReviseSerializers
from utils.JWT import get_token


class UserLoginAPIView(APIView):
    # 让这个类的所有方法不需要身份校验
    authentication_classes = ()

    def post(self, request):
        data_dict = request.data

        serializer = UserLoginSerializers(data=data_dict)
        serializer.is_valid(raise_exception=True)

        user_name = data_dict['user_name']
        password = data_dict['password']

        user = UserModel.objects.filter(user_name=user_name).first()
        if user:
            verify = check_password_hash(user.password, password)
            if verify:
                payload = {
                    "id": user.id,
                    "user_name": user.user_name,
                }
                token = get_token(payload, 10)  # 10分钟过期
                return Response({
                    "code": 200,
                    "message": "success",
                    "data": {
                        "id": user.id,
                        "authToken": token
                    }
                })
            else:
                return Response({
                    "code": 400,
                    "message": "密码错误",
                })
        else:
            return Response({
                "code": 400,
                "message": "用户不存在",
            })


class UserRegisterAPIView(APIView):
    authentication_classes = ()

    def post(self, request):
        data_dict = request.data

        serializer = UserSerializers(data=data_dict)
        serializer.is_valid(raise_exception=True)

        user_name = data_dict['user_name']
        password = data_dict['password']
        email = data_dict['email']
        address = data_dict['address']

        # 密码加密 pbkdf2:sha256
        password_hash = generate_password_hash(password)
        user = UserModel.objects.create(user_name=user_name, password=password_hash, email=email, address=address)
        return Response({
            "code": 201,
            "message": "success",
            "data": {
                "id": user.id}
        })


class UserAPIView(APIView):
    def put(self, request, id):
        data_dict = request.data

        serializer = UserReviseSerializers(data=data_dict)
        serializer.is_valid(raise_exception=True)

        old_password = data_dict['old_password']

        user = UserModel.objects.filter(id=id).first()
        if user:
            verify = check_password_hash(user.password, old_password)
            if verify:
                new_password = data_dict['new_password']
                password_hash = generate_password_hash(new_password)
                UserModel.objects.filter(id=id).update(password=password_hash)
                return Response({
                    "code": 200,
                    "message": "success",
                    "data": {
                        "id": user.id
                    }})
            else:
                return Response({
                    "code": 400,
                    "message": "原密码错误",
                })
        else:
            return Response({
                "code": 400,
                "message": "用户id不存在",
            })
