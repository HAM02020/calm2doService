import uuid

from django.shortcuts import render
from django.http.response import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions

from .models import *
from .serializers import TUserSerializers
from .Auth import *


#注册用户
class Register(APIView):

    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        username = request._request.POST["username"]
        password = request._request.POST["password"]

        user_obj = TUser.objects.filter(user_name=username)
        if user_obj:
            return HttpResponse('用户已存在')
        else:
            TUser.objects.create(user_name=username,user_password=password)

        result = {"username": username, "password": password}
        return Response(result)

#用户登陆 返回token
class Login(APIView):

    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self,request):
        return render(request,'login.html')

    def post(self,request):

        result = {"code":0,"msg":None,"user":None}
        try:
            username = request._request.POST["username"]
            password = request._request.POST["password"]
            print(username,password)
            user_obj = TUser.objects.filter(user_name=username,user_password=password).first()
            if user_obj:
                random_str = uuid.uuid4()
                UserToken.objects.update_or_create(user=user_obj,defaults={"token":random_str})
                result["code"] = 1
                result["msg"] = "登陆成功！"
                result["user"] = username
                result["token"] = random_str
            else:
                result["msg"] = "用户名或密码错误！"
        except Exception as e :
            result["code"] = 2
            result["msg"] = str(e)
        return Response(result)

class UserViewSet(viewsets.ModelViewSet):
    queryset = TUser.objects.all()
    serializer_class = TUserSerializers
    permission_classes = [permissions.IsAuthenticated]

class UserDetail(APIView):

    authentication_classes = [UserAuth]

    def get_object(self,pk):
        try:
            return TUser.objects.get(pk=pk)
        except TUser.DoesNotExist:
            raise Http404
    def get(self,request,pk,format=None):
        user = self.get_object(pk)
        serializer = TUserSerializers(user)
        return Response(serializer.data)
    def get(self,request,format=None):
        users = TUser.objects.all()
        serializer = TUserSerializers(users, many=True)
        return Response(serializer.data)
