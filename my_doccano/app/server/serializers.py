from rest_framework import serializers
from rest_framework.generics import CreateAPIView

# from models import User
from api.models import User


class LoginSerializer(serializers.ModelSerializer):
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

class CreateUserSerializer(serializers.ModelSerializer):
    """创建用户的序列化器"""
    password2 = serializers.CharField(label='确认密码', write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2',"mobile")
        extra_kwargs = {
            'username': {
                'min_length': 1,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许1-20个字符的用户名',
                    'max_length': '仅允许1-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate(self, data):
        # 判断两次密码
        print(data)
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次密码不一致')
        else:
            return data


    def create(self, validated_data):
        """重写保存方法，增加密码加密"""

        # 移除数据库模型类中不存在的属性
        del validated_data['password2']


        # user = User.objects.create(username=xxx, password=xx)
        # user = User.objects.create(**validated_data)

        user = super().create(validated_data)

        user.set_password(validated_data['password'])
        user.save()
        return user