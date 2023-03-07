from django.db import models

from utils.BaseModel import BaseModel


class UserModel(BaseModel):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=200, unique=True)
    address = models.CharField(max_length=500)

    class Meta:
        db_table = 'users'
        verbose_name = 'users'
        verbose_name_plural = 'users'
