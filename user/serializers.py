from rest_framework import serializers

from user.models import UserModel


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = "__all__"


class UserLoginSerializers(UserSerializers):
    email = serializers.EmailField(read_only=True)
    address = serializers.CharField(read_only=True)


class UserReviseSerializers(UserLoginSerializers):
    user_name = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
