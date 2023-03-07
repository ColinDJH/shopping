from django.db import models

from utils.BaseModel import BaseModel


class CommodityModel(BaseModel):
    classify_choices = (
        (1, "女装"), (2, "男装"), (3, "母婴用品"),
        (4, "鞋类箱包"), (5, "护肤彩妆"), (6, "美食"),
        (7, "珠宝配饰"), (8, "家装建材"), (9, "百货市场"),
    )
    commodity_name = models.CharField(max_length=255)
    describe = models.TextField()
    classify = models.SmallIntegerField(choices=classify_choices)
    amount = models.IntegerField()
    price = models.IntegerField()
    is_grounding = models.BooleanField()

    class Meta:
        db_table = 'commodity'
        verbose_name = 'commodity'
        verbose_name_plural = 'commodity'
