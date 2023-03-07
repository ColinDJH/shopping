from rest_framework import serializers

from cars.models import CarsModel, CarsCommodityModel


class CarsSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarsModel
        fields = "__all__"


class CarsCommoditySerializers(serializers.ModelSerializer):
    class Meta:
        model = CarsCommodityModel
        fields = "__all__"
