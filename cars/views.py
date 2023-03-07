from rest_framework.response import Response
from rest_framework.views import APIView

from cars.models import CarsModel, CarsCommodityModel, CommodityModel
from user.models import UserModel


class CarsAPIView(APIView):
    authentication_classes = ()

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

    def post(self, request):
        pass

    def delete(self, request):
        pass
