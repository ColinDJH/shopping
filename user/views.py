from rest_framework.response import Response
from rest_framework.views import APIView
from werkzeug.security import generate_password_hash, check_password_hash

from user.models import UserModel
from user.serializers import UserSerializers, UserLoginSerializers, UserReviseSerializers
from utils.JWT import get_token
from utils.bc_requests import BCCustomers


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

        # 使用BC的API创建用户
        bc_customers = BCCustomers()
        user = {
            "email": email,
            "user_name": user_name,
            "address": address,
            "password": password_hash
        }
        data = bc_customers.create_a_customers(user=user)
        if data is False:
            return Response({
                "code": 400,
                "message": "BC创建用户失败",
            })

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


class CustomersView(APIView):
    authentication_classes = ()

    def get(self, request):
        # get a customer
        # customer_ids = [1,2,4,7,11]
        # bc_customers = BCCustomers()
        # customers = []
        # for customer_id in customer_ids:
        #     customer = bc_customers.get_a_customer(customer_id)
        #     customers.append(customer)
        # return Response({
        #     "data": customers,
        # })

        # get all customer
        bc_customers = BCCustomers()
        customers = []
        customer = bc_customers.get_all_customer()
        for customer_id in customer:
            customers.append(customer_id)
        return Response({
            "data": customers,
        })

    def post(self, request):
        # 创建用户
        # bc_customers = BCCustomers()
        # password = "test3"
        # password_hash = generate_password_hash(password)
        # user = {
        #     "email": "test3@test.com",
        #     "user_name": "test3",
        #     "address": "add1",
        #     "password": password_hash
        # }
        # data = bc_customers.create_a_customers(user=user)
        # return Response({
        #     "data": data,
        # })
        # 创建订单
        user_name = "test6"
        email = "test6@test.com"
        bc_order = BCCustomers()
        customer_id = 1
        customer = bc_order.get_all_customer()
        for customer in customer:
            customer_first_name = customer.get("first_name")
            if customer_first_name == user_name:
                customer_id = customer.get("id")
                break
        user = {
            "customer_id": customer_id,
            "email": email
        }
        data = bc_order.create_an_order(user=user)
        return Response({
            "customer_id": customer_id,
            "data": data
        })
