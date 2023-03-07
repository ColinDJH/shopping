from rest_framework import serializers

from cars.models import CarsCommodityModel


class CarsCommoditySerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    cars = serializers.IntegerField(write_only=True)

    class Meta:
        model = CarsCommodityModel
        fields = "__all__"
