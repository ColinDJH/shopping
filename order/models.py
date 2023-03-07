from django.db import models

from commodity.models import CommodityModel
from user.models import UserModel
from utils.BaseModel import BaseModel


class OrderModel(BaseModel):
    money = models.IntegerField()
    is_delete = models.BooleanField(default=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user_order")

    class Meta:
        db_table = 'order'
        verbose_name = 'order'
        verbose_name_plural = 'order'


class OrderCommodityModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="order")
    commodity = models.ForeignKey(CommodityModel, on_delete=models.CASCADE, related_name="order_commodities")
    amount = models.IntegerField()

    class Meta:
        db_table = 'order_commodity'
        verbose_name = 'order_commodity'
        verbose_name_plural = 'order_commodity'
