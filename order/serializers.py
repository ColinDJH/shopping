from rest_framework import serializers

from order.models import OrderModel, OrderCommodityModel


class OrderSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    is_delete = serializers.BooleanField(write_only=True)

    class Meta:
        model = OrderModel
        fields = "__all__"


class OrderCommoditySerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    order = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderCommodityModel
        fields = "__all__"
