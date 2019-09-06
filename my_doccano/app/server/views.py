from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from api.models import User
from serializers import UserSerializer
from server import serializers
from server.serializers import LoginSerializer


class LoginView(APIView):
    serializer_class = UserSerializer
    def get(self,request):
        return render(request,"login_2.html")

    def post(self,request,*args,**kwargs):
    #     # s = self.get_s
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username=request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"message":"用户名或验证码有误"},status=status.HTTP_400_BAD_REQUEST)


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
    serializer_class = serializers.CreateUserSerializer


# class User(ListModelMixin):
#     def get(self):



# class UserView(CreateAPIView):
#     serializer_class = UserSerializer