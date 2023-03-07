import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from commodity.models import CommodityModel
from order.models import OrderCommodityModel, OrderModel
from order.serializers import OrderSerializers, OrderCommoditySerializers
from user.models import UserModel


class OrderAPIView(APIView):
    def post(self, request):
        auth_token = request.META.get('HTTP_AUTHTOKEN', "")
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get("id")
        user = UserModel.objects.filter(id=user_id).first()
        order_data = request.data
        order = OrderModel.objects.create(money=0, user=user)
        money = 0
        for commodity in order_data.get("data"):
            commodity_id = commodity.get('commodity_id')
            amount = commodity.get("amount")
            commodities = CommodityModel.objects.filter(id=commodity_id).first()
            OrderCommodityModel.objects.create(order=order, commodity=commodities, amount=amount)
            money += commodities.price * amount
        OrderModel.objects.filter(id=order.id).update(money=money)
        return Response({
            "code": 200,
            "message": "success",
            "data": {
                "user_id": user_id,
                "order_id": order.id
            }})


class OrderDetailAPIView(APIView):
    def get(self, request, order_id):
        order = OrderModel.objects.filter(id=order_id, is_delete=False).first()
        if order:
            commodity = OrderCommodityModel.objects.filter(order=order)
            order_data = OrderSerializers(instance=order)
            commodity_data = OrderCommoditySerializers(instance=commodity, many=True)
            data = dict(order_data.data)
            commodities = []
            for i in commodity_data.data:
                commodities.append({
                    "commodity_id": i.get('commodity'),
                    "amount": i.get('amount')
                })
            data['commodity'] = commodities
            return Response({
                "code": 200,
                "message": "success",
                "data": data})
        else:
            return Response({
                "code": 404,
                "message": "success"})

    def delete(self, request, order_id):
        OrderModel.objects.filter(id=order_id, is_delete=False).update(is_delete=True)
        return Response({
            "code": 204,
            "message": "success"
        })
