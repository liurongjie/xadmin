from django.db import models
import uuid
class Team(models.Model):
    teamid=models.AutoField(primary_key=True,verbose_name="团队id")
    teamname=models.CharField(max_length=50,unique=True,verbose_name="团队名称")
    logo=models.ImageField(upload_to="teamlogo",verbose_name="团队logo")
    time = models.DateTimeField(auto_now_add=True, verbose_name="期表创建时间")
    class Meta:
        db_table = "Team"
        verbose_name="大团队"
        verbose_name_plural = verbose_name
        get_latest_by = "time"
class User(models.Model):
    userid = models.BigAutoField(primary_key=True,verbose_name="用户id")
    openid=models.CharField(max_length=100,unique=True,db_index=True,verbose_name="唯一身份标识openid")#建立索引
    nickname = models.CharField(max_length=30, verbose_name="昵称")
    picture = models.CharField( max_length=150,verbose_name="微信头像")
    CHOICEgender = (
        (0, "未知"),
        (1, "男"),
        (2,"女"),
    )
    gender=models.SmallIntegerField(choices=CHOICEgender,verbose_name="性别")
    CHOICE = (
        (0, "仅仅获取昵称"),
        (1, "获取手机号"),
        (2, "院系信息"),
    )
    status = models.SmallIntegerField(choices=CHOICE, verbose_name="当前状态")
    name=models.CharField(null=True, blank=True,max_length=15,verbose_name="姓名")
    number=models.CharField(null=True, blank=True,max_length=15,verbose_name="学号")
    telephone=models.CharField(null=True, blank=True,max_length=11,verbose_name="联系方式")
    department=models.CharField(null=True, blank=True,max_length=20,verbose_name="学院")
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL,related_name="user")#外键连接名称
    parentuser=models.ForeignKey('self',null=True, blank=True, on_delete=models.SET_NULL,related_name="puser")#链接向自己的邀请人
    account=models.IntegerField(default=0,verbose_name="账户贝壳数目")
    time = models.DateTimeField(null=True, blank=True, verbose_name="实名认证时间")
    class Meta:
        db_table = "User"
        verbose_name="用户"
        verbose_name_plural = verbose_name


class Merchant(models.Model):
    merchantid=models.BigAutoField(primary_key=True,verbose_name="商家id")
    name=models.CharField(max_length=30,verbose_name="商户名称")
    location = models.CharField(max_length=50, verbose_name="商家位置")
    latitude=models.FloatField(verbose_name="商家纬度")
    longitude=models.FloatField(verbose_name="商家精度")
    CHOICE = (
        (1, "健身"),
        (2, "驾校"),
        (3, "考研"),
        (4, "小语种"),
    )
    type=models.SmallIntegerField(choices=CHOICE,verbose_name="商户类别")
    logo = models.ImageField(upload_to="photo", verbose_name="商家logo")
    telephone=models.SmallIntegerField(verbose_name="商家电话")
    class Meta:
        db_table = "Merchant"
        verbose_name="商家"
        verbose_name_plural = verbose_name
#不同学校对应不同的产品
class  Production(models.Model):
    productionid=models.BigAutoField(primary_key=True,verbose_name="产品id")
    team=models.ForeignKey(Team,models.CASCADE,related_name="production")
    merchant=models.ForeignKey(Merchant,on_delete=models.CASCADE,related_name="production")
    name=models.CharField(max_length=20,verbose_name="产品名称")
    rank=models.SmallIntegerField(verbose_name="排名（例子1）")
    reputation=models.FloatField(verbose_name="好评率(例子91.5）")
    CHOICE = (
        (1, "健身"),
        (2, "驾校"),
        (3, "考研"),
        (4, "小语种"),
    )
    introduction=models.CharField(max_length=100,verbose_name="产品文字介绍")
    introductionpic=models.ImageField(upload_to="production",verbose_name="产品图片介绍")
    type = models.SmallIntegerField(choices=CHOICE, verbose_name="产品类别")
    logo = models.ImageField(upload_to="prologo", verbose_name="产品logo")
    distance=models.FloatField(verbose_name="距离")
    startprice = models.IntegerField(verbose_name="初始价格")
    bottomprice = models.IntegerField(verbose_name="底价")
    pic1 = models.ImageField(upload_to="production", verbose_name="照片1")
    pic2 = models.ImageField(upload_to="production", verbose_name="照片2")
    pic3 = models.ImageField(upload_to="production", verbose_name="照片3")
    number=models.IntegerField(verbose_name="参团人次")
    class Meta:
        db_table = "Production"
        verbose_name="产品"
        verbose_name_plural = verbose_name



class Comment(models.Model):
    commentid=models.BigAutoField(primary_key=True,verbose_name="评论id")
    production=models.ForeignKey(Production,on_delete=models.CASCADE,related_name="comment")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment")
    context=models.CharField(max_length=200,verbose_name="评论")
    pic1 = models.ImageField(upload_to="comment", null=True, blank=True, verbose_name="评论图片1")
    pic2 = models.ImageField(upload_to="comment",null=True, blank=True,  verbose_name="评论图片2")
    pic3 = models.ImageField(upload_to="comment", null=True, blank=True, verbose_name="评论图片3")
    CHOICE = (
        (0, "未核查"),
        (1, "已核查"),
    )
    status=models.SmallIntegerField(default=0,choices=CHOICE,verbose_name="是否审核")
    time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    class Meta:
        db_table = "Comment"
        verbose_name="评论"
        verbose_name_plural = verbose_name
        index_together=["production","status"]
        ordering = ['-time']


class Steam(models.Model):
    steamid=models.BigAutoField(primary_key=True,verbose_name="拼团小团队id")
    cutprice=models.FloatField(verbose_name="团队整体优惠价格")
    steamnumber=models.IntegerField(verbose_name="团队人数")
    member=models.ManyToManyField(User,through="Membership")
    time = models.DateTimeField(auto_now_add=True, verbose_name="团队创建时间")
    endtime=models.DateTimeField(verbose_name="最迟靠岸时间")
    class Meta:
        db_table = "Steam"
        verbose_name="小团"
        verbose_name_plural = verbose_name

class Membership(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="id")
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    steam=models.ForeignKey(Steam,on_delete=models.CASCADE,verbose_name="小团队")
    cutprice = models.FloatField(verbose_name="参团成员砍价")
    time = models.DateTimeField(auto_now_add=True, verbose_name="参团时间")
    class Meta:
        db_table="membership"
        verbose_name = "小团成员关系"
        verbose_name_plural = verbose_name

class Order(models.Model):
    orderid=models.BigAutoField(primary_key=True,verbose_name="订单编号")
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_index=True,related_name="order")
    production=models.ForeignKey(Production,on_delete=models.CASCADE,related_name="order")
    steam=models.ForeignKey(Steam,on_delete=models.CASCADE,related_name="order")
    CHOICE = (
        (0, "订单取消"),
        (1, "预付完成"),
        (2, "拼团完成"),
        (3, "支付完成"),
        (4, "订单完成"),
    )
    status=models.IntegerField(choices=CHOICE,default=1,verbose_name="状态")
    stateCHOICE = (
        (0, "大船"),
        (1, "小船"),
    )
    state=models.SmallIntegerField(choices=stateCHOICE,verbose_name="发船类型")
    cutprice=models.FloatField(verbose_name="参团成员砍价")
    endprice=models.FloatField(default=0,verbose_name="最终价格")
    gain = models.SmallIntegerField(default=0,verbose_name="付款所得")
    time1 = models.DateTimeField(auto_now_add=True, verbose_name="预付完成时间")
    time2 = models.DateTimeField(null=True, blank=True, verbose_name="拼团完成时间")
    time3 = models.DateTimeField(null=True, blank=True, verbose_name="支付完成时间")
    time4 = models.DateTimeField(null=True, blank=True, verbose_name="订单完成时间")
    time5=models.DateTimeField(null=True, blank=True, verbose_name="订单取消时间")
    certificate=models.CharField(max_length=30,verbose_name="凭证")
    class Meta:
        db_table = "Order"
        verbose_name="订单"
        verbose_name_plural = verbose_name

class Cutting(models.Model):
    cutid=models.BigAutoField(primary_key=True,verbose_name="砍价编号")
    audience = models.ForeignKey(User, on_delete=models.CASCADE,related_name="cutting")
    steamid=models.IntegerField(db_index=True,verbose_name="拼团小团队id")
    cutprice=models.FloatField(verbose_name="砍价")
    time = models.DateTimeField(auto_now_add=True, verbose_name="砍价时间")
    class Meta:
        db_table = "Cutting"
        verbose_name="砍价"
        verbose_name_plural = verbose_name
        index_together = ["audience", "steamid"]


class Need(models.Model):
    needid=models.BigAutoField(primary_key=True,verbose_name="需求编号")#自增组件字段
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="need")
    teamname=models.CharField(max_length=50,verbose_name="团队名称")
    pic=models.ImageField(upload_to="need", verbose_name="需求图片")
    time = models.DateTimeField(auto_now_add=True,  verbose_name="需求提交时间")
    class Meta:
        db_table = "Need"
        verbose_name = "需求提交"
        verbose_name_plural = verbose_name


class Gift(models.Model):
    id=models.AutoField(primary_key=True,verbose_name="小礼品id")
    name=models.CharField(max_length=20,verbose_name="小礼品名称")
    worth=models.SmallIntegerField(verbose_name="价值贝壳数量")
    pic = models.ImageField(upload_to="gift", verbose_name="礼品图片")
    time=models.DateTimeField(auto_now_add=True,verbose_name="礼品创立时间")
    class Meta:
        db_table = "Gift"
        verbose_name = "摇奖"
        verbose_name_plural = verbose_name

class Giftorder(models.Model):
    id=models.BigAutoField(primary_key=True,verbose_name="礼品定义")
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="购买者")
    gift=models.ForeignKey(Gift,on_delete=models.CASCADE,verbose_name="礼物")
    CHOICE = (
        (0, '未处理'),
        (1, "已处理"),
    )
    status = models.SmallIntegerField(default=0, choices=CHOICE, verbose_name="是否处理")
    time = models.DateTimeField(auto_now_add=True, verbose_name="礼品创立时间")
    class Meta:
        db_table = "Giftorder"
        verbose_name = "礼品订单"
        verbose_name_plural = verbose_name


# Create your models here.
