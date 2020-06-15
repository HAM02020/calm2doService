import uuid
from datetime import datetime, timedelta
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
            if len(email_or_name) == 0:
                email_or_name = request._request.POST["username"]
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
                result["code"] = 2
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


# 1.把datetime转成字符串
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# 2.把字符串转成datetime
def string_toDatetime(st):
    return datetime.strptime(st, "%Y-%m-%d %H:%M:%S")

class BeginJx(APIView):
    authentication_classes = [UserAuth,CsrfExemptSessionAuthentication]

    def get(self,request):
        result = {}
        try:
            user = request.user
            from_time = datetime.now()

            set_timeStr = str (request._request.GET['set_time'])
            hours = set_timeStr.split(':')[0]
            minutes = set_timeStr.split(':')[1]
            set_time = from_time + timedelta(hours=float(hours),minutes=float(minutes));
            if set_time:
                #创建字段
                times = TTimes.objects.create(user=user,from_time=from_time,set_time=set_time)
                #设置返回的信息ß
                result['code']="1"
                result['msg'] = 'success'
                result['time_id'] = str(times.time_id)
            else:
                result['code'] = "2"
                result['msg'] = 'failed'
        except Exception as e:

            result['code'] = "2"
            result['msg'] = str(e)


        return Response(result)

class EndJx(APIView):

    authentication_classes = [UserAuth, CsrfExemptSessionAuthentication]

    def get(self,request):
        result={}
        try:
            user = request.user
            time_id = request._request.GET['time_id']
            now = datetime.now()

            if time_id:
                times = TTimes.objects.get(user=user,time_id=time_id)
                if times.is_finish:
                    result['code'] = 2
                    result['msg'] = '静学失败!重复请求接口'
                    return Response(result)
                deltaTime = times.set_time - now
                #如果时间差大于10秒 则JX失败
                if deltaTime.total_seconds() > 10:
                    times.to_time = now
                    times.is_finish = 0
                    times.save()

                    info = TInfo.objects.filter(user=user)
                    if not info:
                        info = TInfo.objects.create(user=user, finish_count=0, interrupt_count=0)
                    info = TInfo.objects.get(user=user)

                    info.interrupt_count += 1
                    info.save()


                    result['code'] = 2
                    result['msg'] = '静学失败!'
                    result['duration'] = deltaTime

                else:
                    times.to_time = now
                    times.is_finish=1
                    times.save()
                    deltaTime = times.set_time - times.to_time
                    deltaTime = deltaTime.total_seconds()
                    if deltaTime < 5400:
                        rewardText = "完成静学的时间,超过全球92%的用户！"
                    elif deltaTime < 3600:
                        rewardText = "完成静学的时间,超过全球83%的用户！"
                    elif deltaTime < 1800:
                        rewardText = "完成静学的时间,超过全球67%的用户！"
                    else:
                        rewardText = "完成静学的时间,超过全球99%的用户！"

                    info = TInfo.objects.filter(user=user)
                    if not info:
                        info = TInfo.objects.create(user=user,finish_count=0,interrupt_count=0)
                    info = TInfo.objects.get(user=user)

                    info.interrupt_count += 1
                    info.save()



                    result['code'] = 1
                    result['msg'] = '静学完成!'
                    result['reward'] = '获得的奖励数量'
                    result['duration'] = deltaTime
                    result['rewardText'] = rewardText

        except Exception as e:

            result['code'] = "2"
            result['msg'] = str(e)
        return Response(result)

class JXInfo(APIView):
    authentication_classes = [UserAuth, CsrfExemptSessionAuthentication]

    def get(self, request):
        result = {}
        try:
            user = request.user
            info = TInfo.objects.get(user=user)

            #1 完成的次数
            finish_count = 0

            # 2 失败的次数
            fail_count = 0

            # 3 完成的时间
            finish_duration = timedelta(seconds=0).total_seconds()

            # 4 多久的时候失败
            fail_times = []

            timeSets = TTimes.objects.filter(user=user)
            for t in timeSets:

                #成功
                if(t.is_finish == 1):
                    finish_count += 1
                    finish_duration += (t.set_time - t.from_time).total_seconds()
                #失败
                else:
                    if not t.to_time:
                        continue
                    fail_dict = {}
                    fail_count += 1
                    fail_duration = (t.to_time - t.from_time).total_seconds()
                    fail_dict['duration'] = fail_duration
                    fail_dict['time'] = t.from_time
                    fail_dict['set_time'] = (t.set_time - t.from_time).total_seconds()
                    fail_times.append(fail_dict)

            #把数据 写入respone字典
            result['code'] = 1
            result['msg'] = 'success'
            result['finish_count'] = finish_count
            result['fail_count'] = fail_count
            result['finish_duration'] = finish_duration
            result['fail_times'] = fail_times

        except Exception as e:

            result['code'] = "2"
            result['msg'] = str(e)

        return Response(result)