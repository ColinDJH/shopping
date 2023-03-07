from django.contrib import admin
from django.contrib.auth.models import User, Group

from cars.models import CarsModel

admin.site.register(CarsModel)

admin.site.unregister(User)
admin.site.unregister(Group)
