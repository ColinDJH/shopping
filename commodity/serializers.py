from rest_framework import serializers

from commodity.models import CommodityModel


class CommoditySerializers(serializers.ModelSerializer):
    classify = serializers.SerializerMethodField()

    class Meta:
        model = CommodityModel
        fields = "__all__"

    def get_classify(self, obj):
        return obj.get_classify_display()
