from django.db import models

from commodity.models import CommodityModel
from user.models import UserModel
from utils.BaseModel import BaseModel


class CarsModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user_cars")

    class Meta:
        db_table = 'cars'
        verbose_name = 'cars'
        verbose_name_plural = 'cars'


class CarsCommodityModel(models.Model):
    cars = models.ForeignKey(CarsModel, on_delete=models.CASCADE, related_name="cars")
    commodity = models.ForeignKey(CommodityModel, on_delete=models.CASCADE, related_name="cars_commodity")
    amount = models.IntegerField()

    class Meta:
        db_table = 'car_commodity'
        verbose_name = 'car_commodity'
        verbose_name_plural = 'car_commodity'
