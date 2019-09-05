from django.shortcuts import render
from django.contrib.auth.views import LoginView as BaseLoginView
# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView


from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from serializers import UserSerializer


class LoginView(APIView):
    def get(self,request):
        return render(request,"login.html")

    def post(self,request,*args,**kwargs):
        serializer_class = UserSerializer



class UserView(CreateAPIView):
    serializer_class = UserSerializer