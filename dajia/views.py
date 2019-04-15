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
from .models import User,Team,Steam,Cutting,Need
from .models import Order
from .models import Comment
from .models import Period
from .models import Production
from .models import Merchant
from dss.Serializer import serializer
import requests
import json
import random
import datetime
import  time


def justtry(request):
    if request.method == 'GET':
        nowtime = timezone.now()
        periods = Period.objects.filter(status=2, starttime__lte=nowtime).all()
        for period in periods:
            period.status = 1
            period.save()
        return JsonResponse({"success":True})


def handle_upload_file(file,filename):
    path='need/'     #上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+filename,'wb+')as destination:
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
                return JsonResponse({"userid": newaccount.userid,"name":newaccount.name,"team_name":newaccount.team.teamname,"number":newaccount.number[0:4],"status":1})

        else:
            newaccount=User.objects.create(openid=openid, nickname=nickname, picture=pic, gender=gender, status=0)
            return JsonResponse({"userid":newaccount.userid,"status":0})



#实名认证验证通过
#未注册给定注册以及返回数据
#已注册返回该账户已注册
def verify(request):
    if request.method == 'GET':
        userid=request.GET.get('userid','')#openid
        teamid=request.GET.get('teamid','')#teamid
        name = request.GET.get('name', '')#姓名
        number = request.GET.get('number', '')  # 学号
        department = request.GET.get('department', '')#院系
        telephone = request.GET.get('telephone', '')  # 电话号码
        team = Team.objects.get(teamid=teamid)
        User.objects.filter(userid=userid).update(name=name,number=number,department=department,telephone=telephone,status=1,team=team)
        return JsonResponse({"userid": userid, "name": name, "team_name": team.teamname,
                             "number": number[0:4], "status": 1})


#home页boat组件的信息获取

def home(request):
    if request.method == 'GET':
        pass
        teamid=request.GET.get('teamid','')
        maindata=Period.objects.filter(production__team_id=teamid,status=1).values('periodid','production','production__name', \
                                                                                   'production__introduction','production__introductionpic',\
                                                                               'startprice','starttime','endtime','type', \
                                                                               'production__merchant__location',\
                                                                               'production__merchant__latitude', 'production__merchant__longitude', \
                                                                               'number','cutnumber','saveprice','production__merchant__pic1', \
                                                                                   'cutprice',
                                                                                   'production__merchant__pic2' \
                                                                                   ,'production__reputation','production__merchant__pic3').select_related('production','production__merchant')
        maindata=serializer(maindata)
        return JsonResponse(maindata,safe=False)

#点击进入详情页，只需获取评论内容
#给定评论id，返回评论详情
#对datetime中用serializer库进行序列化用返回
#成功

def firstcomment(request):
    if request.method == 'GET':
        productionid = request.GET.get('productionid', '')
        data=Comment.objects.filter(production_id=productionid,status=1).values( 'context','user__name', \
                                                                                 'user__department','user__picture', \
                                                                                 'user__team__teamname','time').select_related('user','user__team').all()[0:15]
        data=serializer(data)
        return JsonResponse({'success': True, 'data': data})





def scancomment(request):
    if request.method == 'GET':
        number=request.GET.get('number','')
        number=int(number)
        periodid = request.GET.get('periodid', '')
        period = Period.objects.get(periodid=periodid)
        comments = Comment.objects.filter(production_id=period.production_id, status=1).values("user__team__logo",  \
                                                                                               "user__name","user__department" \
                                                                                               ,'user__team__teamname',"context", \
                                                                                               "time").select_related("user", \
                                                                                                                      "user__team").all()[number:number+5]
        comments = serializer(comments)
        return JsonResponse({'success': True, 'data': comments})
def getperiod(request):
    if request.method == 'GET':
        orderid=request.GET.get('orderid','')
        #每期都需要有自己的logo
        order=Order.objects.filter(orderid=orderid).values('period_id','period__logo','production__name', \
                                                           'period__number','period__startprice','period__cutprice', \
                                                           'period__endtime','status').select_related("period","production")

        period=serializer(order)
        return JsonResponse(period,safe=False)

#查询订单细节
#接口正常运行，细节的雕琢
def orderlist(request):
    if request.method == 'GET':
        openid = request.GET.get('openid', '')
        order=Order.objects.filter(user_id=openid).values('orderid','production__logo','production__name', \
                                                           'production__reputation','period__number','status', \
                                                           'period__endtime','period__starttime', \
                                                          'period_id',
                                                           'period__startprice','period__cutprice', \
                                                          'steam_id','steam__cutprice', \
                                                          'production__team__teamname','production__distance', \
                                                          'time1','time2','time3','time4','time5','time6').select_related("production", \
                                                                                                                          "period","steam")
        if order:
            order = serializer(order)
            return JsonResponse({"response":True,"period": order})
        else:
            return JsonResponse({"response":False})



def orderdetail(request):
    if request.method == 'GET':
        steamid = request.GET.get('steamid', '')
        onecut = Steam.objects.filter(steamid=steamid).values('steamid','steamnumber', 'order__user__picture',
                                                              'order__user__name', \
                                                              'order__cutprice').select_related("order")
        twocut=Cutting.objects.filter(steam_id=steamid).values('steam_id','audience__picture','audience__nickname','audience__name','cutprice').select_related("audience")
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
def completeorder(request):
    if request.method=='GET':
        orderid=request.GET.get('orderid','')
        order = Order.objects.get(orderid=orderid)
        order.status = 4
        nowtime = timezone.now()
        order.time4 = nowtime
        order.save()
        return JsonResponse({'success': True})


def comment(request):
    if request.method == 'GET':
        orderid=request.GET.get('orderid','')
        context=request.GET.get('context','')
        judge=request.GET.get('judge','')
        order=Order.objects.get(orderid=orderid)
        user=order.user
        commentid=user.openid+order.period_id
        judge=Comment.objects.filter(commentid=commentid).exists()
        if judge:
            comment1=Comment.objects.get(commentid=commentid)
            comment1.context=context
            comment1.save()
        else:
            commenModel=Comment(commentid=commentid,context=context,user=user,order=order,status=0, \
                                production=order.production,judge=judge)
            nowtime = timezone.now()
            commenModel.save()
            order.time5 = nowtime
            order.comment=commenModel
            order.save()
        return JsonResponse({'success': True})
#给定openid,teamid,
#验证成功
def buyalone(request):
    if request.method =='GET':
        userid= request.GET.get('userid', '')
        periodid = request.GET.get('periodid', '')
        period = Period.objects.get(periodid=periodid)
        user = User.objects.get(userid=userid)
        now = datetime.datetime.now()
        initial=period.startprice-period.bottomprice
        price = random.randint(int(0.1*initial), int(0.14*initial))  # 砍价金额


        period.number = period.number + 1
        period.cutnumber = period.cutnumber + 1
        period.saveprice += price
        period.save()


        #每人砍价
        if period.number<=100:
            cutprice = 0.001 * initial
            period.cutprice += cutprice
        period.save()
        steam = Steam.objects.create(cutprice=price, steamnumber=1, master=user)
        order = Order.objects.create( user=user, period=period, status=1, steam=steam, cutprice=price,
                      production=period.production)
        return JsonResponse({'success': True, 'orderid':order.orderid,'steamid':steam.steamid, 'price': price})



def buytogether(request):
    userid= request.GET.get('userid', '')
    steamid = request.GET.get('steamid', '')
    periodid = request.GET.get('periodid', '')
    period = Period.objects.get(periodid=periodid)
    user = User.objects.get(userid=userid)
    # 差价初值
    initial = period.startprice - period.bottomprice
    price = random.randint(int(0.1 * initial), int(0.14 * initial))  # 砍价金额
    steam = Steam.objects.get(steamid=steamid)
    if steam.steamnumber <= 4:
        period.cutnumber = period.cutnumber + 1
        period.saveprice += price
        period.save()
        steam.steamnumber = steam.steamnumber + 1
        steam.cutprice += price
        steam.save()
        period.number = period.number + 1
        if period.number <= 100:
            cutprice = 0.0001 * initial
            period.cutprice += cutprice
        order = Order.objects.create(user=user, period=period, status=1, steam=steam, cutprice=price,
                                     production=period.production)
        period.save()
        return JsonResponse({'success': True, 'orderid':order.orderid, 'steamid':steamid,'price': price})
    else:
        return JsonResponse({'success': False, 'reason': '团队人数已满'})



#团队外成员砍价
def cutprice(request):
    if request.method == 'GET':
        userid=request.GET.get('userid','')
        steamid=request.GET.get('steamid','')
        periodid=request.GET.get('periodid','')
        period=Period.objects.get(periodid=periodid)
        # 差价初值
        initial = period.startprice - period.bottomprice
        user=User.objects.get(userid=userid)
        steam=Steam.objects.get(steamid=steamid)
        if steam.cutprice<=0.7:
            price=random.randint(int(0.1*initial),int(0.7*initial))
        elif steam.cutprice<=0.8:
            price = random.randint(int(0.05 * initial), int(0.3 * initial))
        else:
            price = random.randint(int(0.01 * initial), int(0.1 * initial))
        price=price/100
        period.cutprice+=price
        period.cutnumber=period.cutnumber+1
        period.save()
        judge=Cutting.objects.filter(steam_id=steamid,audience_id=userid).exists()
        if judge:
            return JsonResponse({'success': False})
        else:
            steam.cutprice += price
            steam.save()
            cutting=Cutting.objects.create(audience=user, steam=steam, cutprice=price)
            return JsonResponse({'success': True, 'data': price})


def need(request):
    if request.method =="POST":
        pic = handle_upload_file(request.FILES['file'], str(request.FILES['file']))
        userid=request.POST.get('userid',"")
        user=User.objects.get(userid=userid)
        nowtime = timezone.now()
        teamname=User.team.teamname
        Need.objects.create(user=user,time=nowtime,teamname=teamname)
        return JsonResponse({'success': True})















