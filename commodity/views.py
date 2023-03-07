from rest_framework.response import Response
from rest_framework.views import APIView

from commodity.models import CommodityModel
from commodity.serializers import CommoditySerializers


class CommodityAPIView(APIView):
    authentication_classes = ()

    def get(self, request):
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 5))

        # 只查询上架的商品
        # commodity_list = CommodityModel.objects.filter(is_grounding=True)[offset: offset + limit]
        commodity_list = CommodityModel.objects.all()[offset: offset + limit]

        serializers = CommoditySerializers(instance=commodity_list, many=True)
        return Response({
            "code": 200,
            "message": "success",
            "data": serializers.data,
            "pagination": {
                "limit": limit,
                "offset": offset
            }
        })


class CommodityDetailAPIView(APIView):
    authentication_classes = ()

    def get(self, request, id):
        commodity = CommodityModel.objects.filter(id=id).first()

        serializers = CommoditySerializers(instance=commodity)

        return Response({
            "code": 200,
            "message": "success",
            "data": serializers.data
        })
