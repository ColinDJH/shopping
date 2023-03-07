from django.db import models


class BaseModel(models.Model):
    create_time = models.DateField(auto_now=True)
    update_time = models.DateField(auto_now_add=True)

    # 抽象类
    class Meta:
        abstract = True
