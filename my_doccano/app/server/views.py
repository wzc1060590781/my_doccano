from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

# from api.models import User

# from my_doccano.app.api.serializers import UserSerializer
from api.models import User, Project

from server import serializers
from server.my_permissions import RegisterPermission
from server.serializers import ProjectSerializer


class Register(APIView):
    # print(2)
    permission_classes = [IsAuthenticated,RegisterPermission]
    def get_object(self):
        print("get_object")
        return self.request.user

        # return render(request,"register.html")

    # def


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
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CreateUserSerializer
    def get_object(self):
        print("request.user",self.request.user.Role)
        return self.request.user

#
class ProjectView(ListModelMixin,RetrieveModelMixin,CreateModelMixin,GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return self.request.user.project_set.all()
    # def get_queryset(self):
    #     Project.object.filter(pk = self.request.user.)

    # def get(self,request):



# class UserView(CreateAPIView):
#     serializer_class = UserSerializer