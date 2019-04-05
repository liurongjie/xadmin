# Generated by Django 2.0.9 on 2019-04-05 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentid', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='评论id')),
                ('context', models.CharField(max_length=200, verbose_name='评论')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('judge', models.IntegerField(choices=[(1, '非常不满意'), (2, '不满意'), (3, '一般'), (4, '满意'), (5, '非常满意')], verbose_name='评价')),
                ('status', models.IntegerField(choices=[(0, '未核查'), (1, '已核查')], default=0, verbose_name='是否审核')),
            ],
        ),
        migrations.CreateModel(
            name='Cutting',
            fields=[
                ('cutid', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='砍价编号')),
                ('cutprice', models.FloatField(verbose_name='砍价')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='砍价时间')),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('merchantid', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='商家id')),
                ('name', models.CharField(max_length=30, verbose_name='商户名称')),
                ('location', models.CharField(max_length=50, verbose_name='商家位置')),
                ('latitude', models.FloatField(verbose_name='商家纬度')),
                ('longitude', models.FloatField(verbose_name='商家精度')),
                ('reputation', models.IntegerField(verbose_name='商家评分')),
                ('type', models.IntegerField(choices=[(1, '健身'), (2, '驾校'), (3, '考研'), (4, '小语种')], verbose_name='商户类别')),
                ('logo', models.ImageField(upload_to='photo', verbose_name='商家logo')),
                ('pic1', models.ImageField(upload_to='photo', verbose_name='商户照片1')),
                ('pic2', models.ImageField(upload_to='photo', verbose_name='商户照片2')),
                ('pic3', models.ImageField(upload_to='photo', verbose_name='商户照片3')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderid', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='订单编号')),
                ('ordertime', models.DateTimeField(auto_now=True, verbose_name='订单生成时间')),
                ('status', models.IntegerField(choices=[(0, '订单取消'), (1, '预付完成'), (2, '拼团完成'), (3, '支付完成'), (4, '订单完成'), (5, '评价完成')], default=1, verbose_name='状态')),
                ('cutprice', models.FloatField(verbose_name='参团成员砍价')),
                ('time1', models.DateTimeField(auto_now_add=True, verbose_name='预付完成时间')),
                ('time2', models.DateTimeField(blank=True, null=True, verbose_name='拼团完成时间')),
                ('time3', models.DateTimeField(blank=True, null=True, verbose_name='支付完成时间')),
                ('time4', models.DateTimeField(blank=True, null=True, verbose_name='订单完成时间')),
                ('time5', models.DateTimeField(blank=True, null=True, verbose_name='评价完成时间')),
                ('time6', models.DateTimeField(blank=True, null=True, verbose_name='订单取消时间')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='dajia.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('periodid', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='期表id')),
                ('starttime', models.DateTimeField(verbose_name='起始时间')),
                ('endtime', models.DateTimeField(verbose_name='结束时间')),
                ('startprice', models.IntegerField(verbose_name='初始价格')),
                ('bottomprice', models.IntegerField(verbose_name='底价')),
                ('type', models.IntegerField(choices=[(1, '健身'), (2, '驾校'), (3, '考研'), (4, '小语种')], verbose_name='产品类别')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='期表创建时间')),
                ('status', models.IntegerField(choices=[(0, '已结束'), (1, '正在进行中'), (2, '未开始')], verbose_name='订单状态')),
                ('cutprice', models.IntegerField(default=0, verbose_name='降价')),
                ('number', models.IntegerField(default=0, verbose_name='参团人数')),
                ('cutnumber', models.IntegerField(default=0, verbose_name='砍价人次')),
                ('saveprice', models.FloatField(default=0, verbose_name='累计节省')),
            ],
            options={
                'get_latest_by': 'time',
            },
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('productionid', models.IntegerField(primary_key=True, serialize=False, verbose_name='产品id')),
                ('name', models.CharField(max_length=20, verbose_name='产品名称')),
                ('reputation', models.IntegerField(verbose_name='产品评分')),
                ('introduction', models.CharField(max_length=100, verbose_name='产品文字介绍')),
                ('introducitonpic', models.ImageField(upload_to='production', verbose_name='产品图片介绍')),
                ('type', models.IntegerField(choices=[(1, '健身'), (2, '驾校'), (3, '考研'), (4, '小语种')], verbose_name='产品类别')),
                ('cutnumber', models.IntegerField(default=0, verbose_name='砍价人次')),
                ('saveprice', models.FloatField(default=0, verbose_name='累计节省')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='production', to='dajia.Merchant')),
            ],
        ),
        migrations.CreateModel(
            name='Steam',
            fields=[
                ('steamid', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='拼团小团队id')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='团队创建时间')),
                ('cutprice', models.FloatField(verbose_name='团队整体优惠价格')),
                ('steamnumber', models.IntegerField(verbose_name='团队人数')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('teamid', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='团队id')),
                ('teamname', models.CharField(max_length=50, verbose_name='团队名称')),
                ('logo', models.ImageField(upload_to='teamlogo', verbose_name='团队logo')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='期表创建时间')),
            ],
            options={
                'get_latest_by': 'time',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('openid', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='唯一身份标识openid')),
                ('nickname', models.CharField(max_length=30, verbose_name='昵称')),
                ('picture', models.ImageField(upload_to='userpic', verbose_name='微信头像')),
                ('gender', models.IntegerField(choices=[(0, '男'), (1, '女')], verbose_name='性别')),
                ('status', models.IntegerField(choices=[(0, '未实名认证'), (1, '实名认证通过')], verbose_name='是否完成实名认证')),
                ('number', models.CharField(blank=True, max_length=15, null=True, verbose_name='学号')),
                ('telephone', models.CharField(blank=True, max_length=11, null=True, verbose_name='联系方式')),
                ('department', models.CharField(blank=True, max_length=20, null=True, verbose_name='学院')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='dajia.Team')),
            ],
        ),
        migrations.AddField(
            model_name='steam',
            name='master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='steam', to='dajia.User'),
        ),
        migrations.AddField(
            model_name='production',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='production', to='dajia.Team'),
        ),
        migrations.AddField(
            model_name='period',
            name='production',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='period', to='dajia.Production'),
        ),
        migrations.AddField(
            model_name='order',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='dajia.Period'),
        ),
        migrations.AddField(
            model_name='order',
            name='production',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='dajia.Production'),
        ),
        migrations.AddField(
            model_name='order',
            name='steam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='dajia.Steam'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='dajia.User'),
        ),
        migrations.AddField(
            model_name='cutting',
            name='audience',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cutting', to='dajia.User'),
        ),
        migrations.AddField(
            model_name='cutting',
            name='steam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cutting', to='dajia.Steam'),
        ),
        migrations.AddField(
            model_name='comment',
            name='production',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='dajia.Production'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='dajia.User'),
        ),
    ]