import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from cars.models import CarsModel, CarsCommodityModel, CommodityModel
from cars.serializers import CarsCommoditySerializers
from user.models import UserModel


class CarsAPIView(APIView):
    authentication_classes = ()

    def get(self, request):
        auth_token = request.META.get('HTTP_AUTHTOKEN', "")
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get("id")
        cars = CarsModel.objects.filter(user=UserModel.objects.filter(id=user_id).first()).first()
        commodity = CarsCommodityModel.objects.filter(cars=cars).all()
        serializers = CarsCommoditySerializers(instance=commodity, many=True)
        return Response({
            "code": 200,
            "message": "success",
            "data": serializers.data
        })

    def post(self, request):
        cars_data = request.data
        # {'user_id': 1, 'commodity': [{'commodity_id': 1, 'amount': 2}, {'commodity_id': 2, 'amount': 1}]}
        user = UserModel.objects.filter(id=cars_data.get("data").get('user_id')).first()
        commodities = cars_data.get('data').get("commodity")
        cars = CarsModel.objects.filter(user=user).first()
        if cars:
            for commodity in commodities:
                amount = commodity.get("amount")
                commodity_id = CommodityModel.objects.filter(id=commodity.get("commodity_id")).first()
                car_commodity = CarsCommodityModel.objects.filter(commodity=commodity_id).first()
                if car_commodity:
                    CarsCommodityModel.objects.filter(commodity=commodity_id).update(
                        amount=car_commodity.amount + amount)
                else:
                    CarsCommodityModel.objects.create(cars=cars, commodity=commodity_id, amount=amount)
            return Response({
                "code": 200,
                "message": "success",
                "data": {
                    "user_id": user.id,
                    "cars_id": cars.id
                }
            })
        else:
            cars = CarsModel.objects.create(user=user)
            for commodity in commodities:
                amount = commodity.get("amount")
                commodity_id = CommodityModel.objects.filter(id=commodity.get("commodity_id")).first()
                CarsCommodityModel.objects.create(cars=cars, commodity=commodity_id, amount=amount)
            return Response({
                "code": 200,
                "message": "success",
                "data": {
                    "user_id": user.id,
                    "cars_id": cars.id
                }
            })


class CarsDetailAPIView(APIView):
    authentication_classes = ()

    def put(self, request, cars_id):
        cars = CarsModel.objects.filter(id=cars_id).first()
        commodity_id = request.data.get('data').get('commodity_id')
        amount = request.data.get('data').get('amount')
        commodity = CommodityModel.objects.filter(id=commodity_id).first()
        CarsCommodityModel.objects.filter(cars=cars, commodity=commodity).update(amount=amount)
        return Response({
            "code": 200,
            "message": "success",
            "data": {
                "cars_id": cars.id
            }})

    def delete(self, request, cars_id):
        cars = CarsModel.objects.filter(id=cars_id).first()
        commodity_id = request.data.get("commodity_id")
        commodity = CommodityModel.objects.filter(id=commodity_id).first()
        CarsCommodityModel.objects.filter(cars=cars, commodity=commodity).delete()
        return Response({
            "code": 204,
            "message": "success"
        })
