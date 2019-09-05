from rest_framework import serializers
from rest_framework.generics import CreateAPIView

from models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label="确认密码",write_only=True)
    # password2 = serializers.CharField(label='确认密码',write_only=True)
    class Meta:
        model = User
        fields = ("mobile","username")
        extra_kwargs = {
            "username":{
                "min_length":0,
                "max_length":20,
                "error_messages":{
                    "min_length":"用户名不得超过20个字符"
                }
            },
            "password":{
                "write_only":True,
                "min_length":8,
                "max_length":20,
                "error_messages":{
                    "min_length":"仅允许8-20个字符的密码",
                    "max_length":"仅允许8-20个字符的密码"
                }
            }
        }
    def validate(self, attrs):
        if attrs["password"] !=attrs["password2"]:
            raise serializers.ValidationError("两次密码不一致")

    def create(self, validated_data):
        del validated_data["password2"]
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user