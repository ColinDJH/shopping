"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from cars.views import CarsAPIView, CarsDetailAPIView
from commodity.views import CommodityAPIView, CommodityDetailAPIView
from order.views import OrderAPIView, OrderDetailAPIView
from user.views import UserLoginAPIView, UserRegisterAPIView, UserAPIView, CustomersView, Test

urlpatterns = [
    path('admin/', admin.site.urls),
    # 登陆注册
    path('login/', UserLoginAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path('user/<int:id>/', UserAPIView.as_view()),
    # 测试redis
    path('user/', UserAPIView.as_view()),
    # 商品
    path("commodity/", CommodityAPIView.as_view()),
    path("commodity/<int:id>", CommodityDetailAPIView.as_view()),
    # 购物车
    path("cars/", CarsAPIView.as_view()),
    path("cars/<int:cars_id>/", CarsDetailAPIView.as_view()),
    # 订单
    path("order/", OrderAPIView.as_view()),
    path("order/<int:order_id>/", OrderDetailAPIView.as_view()),

    path("bc/", CustomersView.as_view()),
    path("test/", Test.as_view()),
]
