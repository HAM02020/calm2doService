import uuid

from django.shortcuts import render
from django.http.response import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView,View
from rest_framework import viewsets, permissions
from rest_framework import generics
from .models import *
from .serializers import *
from .Auth import *


#注册用户
class Register(APIView):

    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        result = {"code": 1, "msg": None}

        useremail = request._request.POST["email"]
        username = request._request.POST["username"]
        password = request._request.POST["password"]

        user_obj = TUser.objects.filter(user_email=useremail)
        if user_obj:
            result["code"]=2
            result["msg"]='user exist'
        else:
            #创建用户
            newUser = TUser(user_name=username,user_password=password,user_email=useremail,join_time=datetime.now())
            newUser.save()
            defultPet = TPet(user_id=newUser.user_id)
            defultPet.pet_type = 'cat'
            defultPet.save()

            result["msg"] = 'success'
            result["user"] = {"email":useremail,"username": username, "password": password}
        return Response(result)

#用户登陆 返回token
class Login(APIView):

    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self,request):
        return render(request,'login.html')

    def post(self,request):

        result = {"code":0,"msg":None,"user":None}
        try:
            email_or_name = request._request.POST["email"]
            password = request._request.POST["password"]

            user_obj = TUser.objects.filter(user_email=email_or_name,user_password=password).first()
            user_obj = user_obj if user_obj else TUser.objects.filter(user_name=email_or_name,user_password=password).first()

            if user_obj:
                userdict={"email":user_obj.user_email,"username":user_obj.user_name}
                random_str = uuid.uuid4()
                UserToken.objects.update_or_create(user=user_obj,defaults={"token":random_str})
                result["code"] = 1
                result["msg"] = "登陆成功！"
                result["user"] = userdict
                result["token"] = random_str
            else:

                result["msg"] = "用户名或密码错误！"
        except Exception as e :
            result["code"] = 2
            result["msg"] = "chuxianwenti"
        return Response(result)

class UserViewSet(viewsets.ModelViewSet):
    queryset = TUser.objects.all()
    serializer_class = TUserSerializers
    permission_classes = [permissions.IsAuthenticated]

# class UserDetail(APIView):
#
#     authentication_classes = [UserAuth]
#
#     def get_object(self,pk):
#         try:
#             return TUser.objects.get(pk=pk)
#         except TUser.DoesNotExist:
#             raise Http404
#     def get(self,request,pk,format=None):
#         user = self.get_object(pk)
#         serializer = TUserSerializers(user)
#         return Response(serializer.data)
#     def get(self,request,format=None):
#         users = TUser.objects.all()
#         serializer = TUserSerializers(users, many=True)
#         return Response(serializer.data)

class Pet(APIView):
    queryset = TPet.objects.get_queryset()
    authentication_classes = [UserAuth,CsrfExemptSessionAuthentication]
    serializer_class = PetSerializers

    def get(self,request):
        try:
            result={}
            # token = request._request.GET['token']
            # auth_obj = UserToken.objects.filter(token=token).first()
            #pet_obj = TPet.objects.filter(user=request.user)
            pet_obj = self.queryset.filter(user=request.user)
            if pet_obj:
                serializer = PetSerializers(pet_obj,many=True)
                result['code'] = 1
                result['msg'] = 'success'
                result['pet'] = serializer.data
            else:
                result['code'] = 2
                result['msg'] = 'no pet found'
                result['pet'] = None
        except Exception as e:
            result['code'] = 2
            result['msg'] = str(e)
            result['pet'] = None
        return Response(result)
    def post(self,request):
        result = {'code':1,'msg':'success','pet':None}
        pet_type = request._request.POST['pet_type']
        pet_name = request._request.POST['pet_name']

        pet_obj = TPet.objects.create(user=request.user)
        pet_obj.pet_type=pet_type
        pet_obj.pet_name=pet_name if pet_name != "" else None
        pet_obj.save()

        serializer = PetSerializers(pet_obj)
        result['pet']=serializer.data
        return Response(result)



class Info(APIView):

    authentication_classes = [UserAuth,CsrfExemptSessionAuthentication]

    def get(self,request,format=None):
        try:
            token = request._request.GET['token']
        except Exception as e:
            print(e)
        return Response()



