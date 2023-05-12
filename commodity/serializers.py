from rest_framework import serializers

from commodity.models import CommodityModel


class CommoditySerializers(serializers.ModelSerializer):
    classify = serializers.SerializerMethodField()

    class Meta:
        model = CommodityModel
        fields = "__all__"

    # 让分类显示类别，而不是类别代码
    def get_classify(self, obj):
        return obj.get_classify_display()
