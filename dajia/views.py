from django.shortcuts import render
from django.utils import timezone
import pytz
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Count
from django.db.models import Max
from django.db.models import Sum
from .models import User,Team,Steam,Cutting,Need,Membership,Giftorder,Gift
from .models import Order
from .models import Comment
from .models import Production
from .models import Merchant
from dss.Serializer import serializer
import requests
import json
import random
import datetime
import uuid
import  time


def justtry(request):
    if request.method == 'GET':
        steamid=request.GET.get('steamid')
        member=Steam.objects.filter(steamid=steamid).values('member__name',"member__picture", \
                                                            "membership__cutprice","membership__time")
        member=serializer(member)
        print(member)
        return JsonResponse({"success":True})


def handle_upload_file(file,filename,path):
    allpath = 'uploads/'+path
    #上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(allpath):
        os.makedirs(allpath)
    with open(allpath+filename,'wb+')as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return path+filename

@csrf_exempt
def login(request):
    if request.method == "GET":
        pic=request.GET.get('pic')
        code = request.GET.get('code')
        nickname = request.GET.get('nickname')
        gender=request.GET.get('gender')
        appid = 'wx2b21ee85de8b10a9'
        appSecret = 'e3ce059551daa9fdd4657a6445d2b265'
        data = {
            'appid': appid,
            'secret': appSecret,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (
            appid, appSecret, code)
        r = requests.get(url=url)
        response = r.json()
        openid = response['openid']
        account = User.objects.filter(openid=openid).exists()
        if account:
            newaccount = User.objects.get(openid=openid)
            if newaccount.status == 0:
                return JsonResponse({"userid": newaccount.userid,"status":0})
            else:
                return JsonResponse({"userid": newaccount.userid,"name":newaccount.name, \
                                     "team_name":newaccount.team.teamname, \
                                     "account":newaccount.account,"number":newaccount.number[0:4],"status":1})

        else:

            newaccount=User.objects.create(openid=openid, nickname=nickname, picture=pic, gender=gender, status=0)
            return JsonResponse({"userid":newaccount.userid,"status":0})


def getphone(request):
    if request.method=='GET':
        userid=request.GET.get('userid','')
        phone=request.GET.get('phone','')
        try:
            user=User.objects.get(userid=userid)
            user.telephone=phone
            user.save()
            return JsonResponse({"success": True})
        except:
            return JsonResponse({"success":False})


#实名认证验证通过
#未注册给定注册以及返回数据
#已注册返回该账户已注册
def verify(request):
    if request.method == 'GET':
        puserid=request.GET.get('puserid','')
        userid = request.GET.get('userid', '')  # openid
        teamid = request.GET.get('teamid', '')  # teamid
        number = request.GET.get('number', '')  # 学号
        department = request.GET.get('department', '')  # 院系
        telephone = request.GET.get('telephone', '')  # 电话号码
        team = Team.objects.get(teamid=teamid)
        if User.objects.filter(userid=userid,status=2):
            return JsonResponse({'success':False,'state':0,'account': 50})
        else:
            if (puserid):
                P_User = User.objects.get(userid=puserid)
                P_User.account += 30
                P_User.save()  # 邀请人加上30贝壳
                User.objects.filter(userid=userid).update(number=number, department=department,
                                                          telephone=telephone, status=2, team=team, parentuser=P_User,account=50)
                return JsonResponse({'success':True,'state':1, 'account': 50})
            else:
                User.objects.filter(userid=userid).update( number=number, department=department,
                                                          telephone=telephone, status=2, team=team,account=50)
                return JsonResponse({'success':True,'state':2, 'account': 50})




#home页boat组件的信息获取

def home(request):
    if request.method == 'GET':
        pass
        teamid=request.GET.get('teamid','')

        maindata=Production.objects.filter(team_id=teamid).select_related('merchant').values('name','introduction','distance','startprice', \
                                                                                             'bottomprice','pic1', \
                                                                                             'pic2','pic3','merchant__location', \
                                                                                             'reputation','rank','team_id')
        maindata=serializer(maindata)
        return JsonResponse(maindata,safe=False)

#点击进入详情页，只需获取评论内容
#给定评论id，返回评论详情
#对datetime中用serializer库进行序列化用返回
#成功

def firstcomment(request):
    if request.method == 'GET':
        productionid = request.GET.get('productionid', '')
        data=Comment.objects.filter(production_id=productionid).select_related('user','user__team').values( 'context','user__nickname', \
                                                                                 'user__department','user__picture', \
                                                                                 'user__number','time').all()[0:100]
        data=serializer(data)
        return JsonResponse({'success': True, 'data': data})





























def scancomment(request):
    if request.method == 'GET':
        number=request.GET.get('number','')
        number=int(number)
        productionid = request.GET.get('productionid', '')
        data = Comment.objects.filter(production_id=productionid).select_related('user', 'user__team').values('context',   'user__nickname', \
                                                                                                              'user__department',
                                                                                                              'user__picture', \
                                                                                                              'user__number',
                                                                                                              'time').all()[number:number+50]
        data = serializer(data)
        return JsonResponse({'success': True, 'data': data})


def buybigboat(request):
    if request.method =='GET':
        userid= request.GET.get('userid', '')
        productionid=request.GET.get('productionid','')
        production=Production.objects.get(productionid=productionid)
        user = User.objects.get(userid=userid)
        now = datetime.datetime.now()
        initial=production.startprice-production.bottomprice
        price=int((production.startprice-production.bottomprice)*0.4)
        endprice=production.startprice-price
        li = []
        for i in range(16):
            r = random.randrange(0, 5)
            if i == r:
                num = random.randrange(0, 10)
                li.append(str(num))
            else:
                temp = random.randrange(65, 91)
                c = chr(temp)
                li.append(c)
        result = "".join(li)

        order=Order.objects.create(user=user,production=production,state=0,status=2,cutprice=price,endprice=endprice,time2=now,certificate=result)
        production.number=production.number+1
        production.save()
        return JsonResponse({'success': True})



def buysmallboat(request):
    userid= request.GET.get('userid', '')
    steamid = request.GET.get('steamid', '')
    productionid = request.GET.get('productionid', '')
    now = datetime.datetime.now()
    endtime = datetime.datetime(now.year, now.month, now.day + 7, 00, 00, 00, 00)
    if steamid:
        production=Production.objects.get(productionid=productionid)
        user=User.objects.get(userid=userid)
        steam = Steam.objects.get(steamid=steamid)
        initial=production.startprice-production.bottomprice
        price = random.randint(int(0.1 * initial), int(0.14 * initial))  # 砍价金额

        if steam.steamnumber < 5:
            steam.steamnumber = steam.steamnumber + 1
            steam.cutprice += price
            steam.save()
            li = []
            for i in range(16):
                r = random.randrange(0, 5)
                if i == r:
                    num = random.randrange(0, 10)
                    li.append(str(num))
                else:
                    temp = random.randrange(65, 91)
                    c = chr(temp)
                    li.append(c)
            result = "".join(li)
            order = Order.objects.create(user=user, production=production,state=1 ,status=1, steam=steam, cutprice=price,certificate=result)
            membership = Membership.objects.create(user=user, steam=steam, cutprice=price)
            production.number = production.number + 1
            production.save()
            return JsonResponse({'success': True, 'orderid': order.orderid, 'steamid': steamid, 'price': price})
        else:
            return JsonResponse({'success': False, 'reason': '团队人数已满'})
    else:
        production = Production.objects.get(productionid=productionid)
        user = User.objects.get(userid=userid)
        initial = production.startprice - production.bottomprice
        price = random.randint(int(0.1 * initial), int(0.14 * initial))  # 砍价金额
        steam=Steam.objects.create(cutprice=price,steamnumber=1,endtime=endtime)
        li = []
        for i in range(16):
            r = random.randrange(0, 5)
            if i == r:
                num = random.randrange(0, 10)
                li.append(str(num))
            else:
                temp = random.randrange(65, 91)
                c = chr(temp)
                li.append(c)
        result = "".join(li)
        order = Order.objects.create(user=user, production=production, state=1, status=1, steam=steam, \
                                         cutprice=price, certificate=result)
        membership = Membership.objects.create(user=user, steam=steam, cutprice=price)
        production.number = production.number + 1
        production.save()
        return JsonResponse({'success': True, 'orderid': order.orderid, 'steamid': steam.steamid, 'price': price})


def comment(request):
    if request.method=='GET':
        productionid=request.GET.get('productionid','')
        production=Production.objects.get(productionid=productionid)
        context=request.GET.get('context','')
        userid=request.GET.get('userid','')
        user=User.objects.get(userid=userid)
        comment=Comment.objects.create(user=user,context=context,production=production)
        return JsonResponse({'success': True})

# def comment(request):
#     if request.method == 'POST':
#         path = 'comment/'
#         filename=str(uuid.uuid4())+'.jpg'
#         pic = handle_upload_file(request.FILES['file'], filename, path)
#         orderid=request.POST.get('orderid','')
#         order=Order.objects.get(orderid=orderid)
#         comment=order.comment
#         if comment:
#             if not comment.pic1:
#                 comment.pic1=pic
#                 comment.save()
#                 return JsonResponse({'success': 'pic1'})
#             elif not comment.pic2:
#                 comment.pic2 = pic
#                 comment.save()
#                 return JsonResponse({'success': 'pic2'})
#             elif not comment.pic3:
#                 comment.pic3=pic
#                 comment.save()
#                 return JsonResponse({'success':'pic3'})
#             return JsonResponse({'success': False})
#         else:
#             context = request.POST.get('context', '')
#             judge1 = request.POST.get('judge1', '')
#             commenModel=Comment(context=context,user=order.user,status=0, \
#                                 production=order.production,judge1=judge1,judge2=5,pic1=pic)
#             nowtime = timezone.now()
#             commenModel.save()
#             order.time5 = nowtime
#             order.comment=commenModel
#             order.status=5
#             order.save()
#             return JsonResponse({'success': True})
#     if request.method == 'GET':
#         return JsonResponse({'get': True})





def orderlist(request):
    if request.method == 'GET':
        userid = request.GET.get('userid', '')
        order=Order.objects.filter(user_id=userid).values('orderid','production__logo','production__name', \
                                                           'status','state','production__merchant__telephone','production__startprice' ,\
                                                           'time2', 'steam__cutprice','certificate',\
                                                          'endprice',
                                                         )
        if order:
            order = serializer(order)
            return JsonResponse({"success":True,"period": order})
        else:
            return JsonResponse({"success":False})


























#查看我的团和分享页展示内容
def getperiod(request):
    if request.method == 'GET':
        productionid=request.GET.get('productionid','')
        production=Production.objects.filter(productionid=productionid).values('productionid','logo','name','startprice')
        production=serializer(production)
        return JsonResponse({'success':True,'production':production})

#查询订单细节
#接口正常运行，细节的雕琢




def orderdetail(request):
    if request.method == 'GET':
        steamid = request.GET.get('steamid', '')
        onecut = Steam.objects.filter(steamid=steamid).values('member__userid','member__nickname', "member__picture", \
                                                              "membership__cutprice","member__department","endtime")
        twocut=Cutting.objects.filter(steamid=steamid).select_related("audience").values('audience__picture','audience__nickname','audience__name','cutprice')
        onecut = serializer(onecut)
        twocut = serializer(twocut)
        return JsonResponse({'onecut': onecut, 'twocut': twocut})

#对取消接口进行验证
#取消接口验证完成

def cancel(request):
    if request.method == 'GET':
        orderid=request.GET.get('orderid','')
        order=Order.objects.get(orderid=orderid)
        order.status=0
        nowtime = timezone.now()
        order.time6 = nowtime
        order.save()

        return JsonResponse({'success':True})
#评论
#验证成功
#立即靠岸
def completeorder(request):
    if request.method=='GET':
        orderid=request.GET.get('orderid','')
        order = Order.objects.get(orderid=orderid)
        order.status = 4
        nowtime = timezone.now()
        order.time4 = nowtime
        order.endprice = order.period.startprice - order.period.cutprice - order.steam.cutprice
        order.save()
        return JsonResponse({'success': True})




#给定openid,teamid,
#验证成功




#团队外成员砍价
def cutprice(request):
    if request.method == 'GET':
        userid=request.GET.get('userid','')
        steamid=request.GET.get('steamid','')
        productionid=request.GET.get('productionid','')
        production=Production.objects.get(productionid=productionid)
        # 差价初值
        initial = production.startprice - production.bottomprice
        user=User.objects.get(userid=userid)
        steam=Steam.objects.get(steamid=steamid)

        if steam.cutprice<=0.7:
            price=random.randint(int(0.1*initial),int(0.7*initial))
        elif steam.cutprice<=0.8:
            price = random.randint(int(0.05 * initial), int(0.3 * initial))
        else:
            price = random.randint(int(0.01 * initial), int(0.1 * initial))

        price=price/100
        judge=Cutting.objects.filter(steamid=steamid,audience_id=userid).exists()
        if judge:
            return JsonResponse({'success': False})
        else:
            steam.cutprice += price
            steam.save()
            cutting=Cutting.objects.create(audience=user,steamid=steamid, cutprice=price)
            return JsonResponse({'success': True, 'price': price})


def need(request):
    if request.method =="POST":
        path = 'need/'
        pic = handle_upload_file(request.FILES['file'], str(request.FILES['file']),path)
        userid=request.POST.get('userid',"")
        user=User.objects.get(userid=userid)
        nowtime = timezone.now()
        teamname=user.team.teamname
        Need.objects.create(user=user,time=nowtime,teamname=teamname)
        return JsonResponse({'success': True})

# def sign(request):
#     if request.method == 'GET':
#         userid = request.GET.get('userid', "")
#         user = User.objects.get(userid=userid)
#         gain=User.objects.get('gain','')
# #异常捕获
#         try:
#             Sign.objects.create(user=user,gain=gain)
#             user.account+=gain
#             return JsonResponse({'success': "签到成功"})
#         except:
#             return JsonResponse({'success': "签到成功"})

#抽奖礼物获得，奖项几率有待商榷
def getgift(request):
    if request.method == 'GET':
        userid=request.GET.get('userid','')
        user=User.objects.get(userid=userid)
        if user.account>=30:
            # 随机数
            new = random.randint(1, 100)
            if new == 1:
                gift = Gift.objects.get(id=1)
                user.account=user.account-30
                user.save()
                order = Giftorder.objects.create(user=user, gift=gift, status=0)
                return JsonResponse({'prize': 1,'account':user.account})
            elif new == 2:
                gift = Gift.objects.get(id=2)
                user.account = user.account - 30
                user.save()
                order = Giftorder.objects.create(user=user, gift=gift, status=0)
                return JsonResponse({'prize': 2,'account':user.account})
            elif new == 3:
                gift = Gift.objects.get(id=3)
                user.account = user.account - 30
                user.save()
                order = Giftorder.objects.create(user=user, gift=gift, status=0)
                return JsonResponse({'prize': 3,'account':user.account})
            elif new in range(4, 9):
                gift = Gift.objects.get(id=4)
                user.account = user.account+30
                user.save()
                order = Giftorder.objects.create(user=user, gift=gift, status=0)
                return JsonResponse({'prize': 4,'account':user.account})
            elif new in range(9, 15):
                gift = Gift.objects.get(id=5)
                user.account = user.account - 30
                user.save()
                order = Giftorder.objects.create(user=user, gift=gift, status=0)
                return JsonResponse({'prize': 5,'account':user.account})
            elif new in range(15, 50):
                gift = Gift.objects.get(id=6)
                user.account = user.account - 30
                user.save()
                order = Giftorder.objects.create(user=user, gift=gift, status=0)
                return JsonResponse({'prize': 6,'account':user.account})
            else:
                gift = Gift.objects.get(id=7)
                user.account = user.account - 25
                user.save()
                order = Giftorder.objects.create(user=user, gift=gift, status=0)
                return JsonResponse({'prize': 7,'account':user.account})
        else:
            return JsonResponse({'error': "账户余额不足"})



def accountdetail(request):
    if request.method=='GET':
        userid=request.GET.get('userid','')
        invitation=User.objects.filter(puser__userid=userid).values('puser__name')
        invitation=serializer(invitation)
        gorder=Giftorder.objects.filter(user_id=userid).values("gift__name",'time')
        gorder=serializer(gorder)
        return JsonResponse({'invitation': invitation,"gorder":gorder})

















