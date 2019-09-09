from rest_framework import serializers
from rest_framework.generics import CreateAPIView

# from models import User
# from rest_framework.settings import api_settings
from rest_framework_jwt.settings import api_settings
from api.models import User
from app import settings

class CreateUserSerializer(serializers.ModelSerializer):
    """创建用户的序列化器"""
    password2 = serializers.CharField(label='确认密码', write_only=True)
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2',"mobile","token")
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
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        user.save()
        return user