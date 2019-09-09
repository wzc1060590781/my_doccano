from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

# from api.models import User

# from my_doccano.app.api.serializers import UserSerializer
from api.models import User


from server import serializers
from server.my_permissions import RegisterPermission

class Register(APIView):
    print(2)
    permission_classes = [IsAuthenticated]
    def get(self,request):
        print(1)
        return render(request,"register.html")


class LoginView(APIView):
    def get(self,request):
        return render(request,"login.html")


# 检验用户名
class UsernameCountView(APIView):
    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)

# 检验手机号
class MobileCountView(APIView):
    """
    手机号数量
    """
    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)

class UserView(CreateAPIView):
    """
    用户注册
    传入参数：
        username, password, password2, sms_code, mobile, allow
    """
    permission_classes = [IsAuthenticated,RegisterPermission]
    serializer_class = serializers.CreateUserSerializer


# class User(ListModelMixin):
#     def get(self):



# class UserView(CreateAPIView):
#     serializer_class = UserSerializer