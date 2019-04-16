# Generated by Django 2.0.9 on 2019-04-16 18:48

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
                ('commentid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='评论id')),
                ('context', models.CharField(max_length=200, verbose_name='评论')),
                ('pic1', models.ImageField(blank=True, null=True, upload_to='comment', verbose_name='评论图片1')),
                ('pic2', models.ImageField(blank=True, null=True, upload_to='comment', verbose_name='评论图片2')),
                ('pic3', models.ImageField(blank=True, null=True, upload_to='comment', verbose_name='评论图片3')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('judge', models.IntegerField(choices=[(1, '非常不满意'), (2, '不满意'), (3, '一般'), (4, '满意'), (5, '非常满意')], verbose_name='评价')),
                ('status', models.IntegerField(choices=[(0, '未核查'), (1, '已核查')], default=0, verbose_name='是否审核')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
                'db_table': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='Cutting',
            fields=[
                ('cutid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='砍价编号')),
                ('steamid', models.IntegerField(db_index=True, verbose_name='拼团小团队id')),
                ('cutprice', models.FloatField(verbose_name='砍价')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='砍价时间')),
            ],
            options={
                'verbose_name': '砍价',
                'verbose_name_plural': '砍价',
                'db_table': 'Cutting',
            },
        ),
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='小礼品id')),
                ('name', models.CharField(max_length=20, verbose_name='小礼品名称')),
                ('worth', models.SmallIntegerField(verbose_name='价值贝壳数量')),
                ('pic', models.ImageField(upload_to='gift', verbose_name='礼品图片')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='礼品创立时间')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('cutprice', models.FloatField(verbose_name='参团成员砍价')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='参团时间')),
            ],
            options={
                'verbose_name': '小团成员关系',
                'verbose_name_plural': '小团成员关系',
                'db_table': 'membership',
            },
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('merchantid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='商家id')),
                ('name', models.CharField(max_length=30, verbose_name='商户名称')),
                ('location', models.CharField(max_length=50, verbose_name='商家位置')),
                ('latitude', models.FloatField(verbose_name='商家纬度')),
                ('longitude', models.FloatField(verbose_name='商家精度')),
                ('reputation', models.IntegerField(verbose_name='商家评分')),
                ('type', models.SmallIntegerField(choices=[(1, '健身'), (2, '驾校'), (3, '考研'), (4, '小语种')], verbose_name='商户类别')),
                ('logo', models.ImageField(upload_to='photo', verbose_name='商家logo')),
                ('pic1', models.ImageField(upload_to='photo', verbose_name='商户照片1')),
                ('pic2', models.ImageField(upload_to='photo', verbose_name='商户照片2')),
                ('pic3', models.ImageField(upload_to='photo', verbose_name='商户照片3')),
            ],
            options={
                'verbose_name': '商家',
                'verbose_name_plural': '商家',
                'db_table': 'Merchant',
            },
        ),
        migrations.CreateModel(
            name='Need',
            fields=[
                ('needid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='需求编号')),
                ('teamname', models.CharField(max_length=50, verbose_name='团队名称')),
                ('pic', models.ImageField(upload_to='need', verbose_name='需求图片')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='需求提交时间')),
            ],
            options={
                'verbose_name': '需求提交',
                'verbose_name_plural': '需求提交',
                'db_table': 'Need',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='订单编号')),
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
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
                'db_table': 'Order',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('periodid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='期表id')),
                ('starttime', models.DateTimeField(verbose_name='起始时间')),
                ('endtime', models.DateTimeField(verbose_name='结束时间')),
                ('startprice', models.IntegerField(verbose_name='初始价格')),
                ('bottomprice', models.IntegerField(verbose_name='底价')),
                ('type', models.SmallIntegerField(choices=[(1, '健身'), (2, '驾校'), (3, '考研'), (4, '小语种')], verbose_name='产品类别')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='期表创建时间')),
                ('status', models.SmallIntegerField(choices=[(0, '已结束'), (1, '正在进行中'), (2, '未开始')], verbose_name='订单状态')),
                ('cutprice', models.IntegerField(default=0, verbose_name='降价')),
                ('number', models.IntegerField(default=0, verbose_name='参团人数')),
                ('cutnumber', models.IntegerField(default=0, verbose_name='砍价人次')),
                ('saveprice', models.FloatField(default=0, verbose_name='累计节省')),
            ],
            options={
                'verbose_name': '期表',
                'verbose_name_plural': '期表',
                'db_table': 'Period',
            },
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('productionid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='产品id')),
                ('name', models.CharField(max_length=20, verbose_name='产品名称')),
                ('reputation', models.FloatField(verbose_name='好评率')),
                ('introduction', models.CharField(max_length=100, verbose_name='产品文字介绍')),
                ('introductionpic', models.ImageField(upload_to='production', verbose_name='产品图片介绍')),
                ('type', models.SmallIntegerField(choices=[(1, '健身'), (2, '驾校'), (3, '考研'), (4, '小语种')], verbose_name='产品类别')),
                ('logo', models.ImageField(upload_to='prologo', verbose_name='产品logo')),
                ('cutnumber', models.IntegerField(default=0, verbose_name='砍价人次')),
                ('saveprice', models.FloatField(default=0, verbose_name='累计节省')),
                ('distance', models.FloatField(verbose_name='距离')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='production', to='dajia.Merchant')),
            ],
            options={
                'verbose_name': '产品',
                'verbose_name_plural': '产品',
                'db_table': 'Production',
            },
        ),
        migrations.CreateModel(
            name='Steam',
            fields=[
                ('steamid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='拼团小团队id')),
                ('cutprice', models.FloatField(verbose_name='团队整体优惠价格')),
                ('steamnumber', models.IntegerField(verbose_name='团队人数')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='团队创建时间')),
            ],
            options={
                'verbose_name': '小团',
                'verbose_name_plural': '小团',
                'db_table': 'Steam',
            },
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='意见编号')),
                ('teamname', models.CharField(max_length=50, verbose_name='团队名称')),
                ('pic', models.ImageField(upload_to='suggetion', verbose_name='意见图片')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='需求提交时间')),
            ],
            options={
                'verbose_name': '意见',
                'verbose_name_plural': '意见',
                'db_table': 'Suggestion',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('teamid', models.AutoField(primary_key=True, serialize=False, verbose_name='团队id')),
                ('teamname', models.CharField(max_length=50, unique=True, verbose_name='团队名称')),
                ('logo', models.ImageField(upload_to='teamlogo', verbose_name='团队logo')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='期表创建时间')),
            ],
            options={
                'verbose_name': '大团队',
                'verbose_name_plural': '大团队',
                'db_table': 'Team',
                'get_latest_by': 'time',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='用户id')),
                ('openid', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='唯一身份标识openid')),
                ('nickname', models.CharField(max_length=30, verbose_name='昵称')),
                ('picture', models.CharField(max_length=150, verbose_name='微信头像')),
                ('gender', models.SmallIntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], verbose_name='性别')),
                ('status', models.SmallIntegerField(choices=[(0, '未实名认证'), (1, '实名认证通过')], verbose_name='是否完成实名认证')),
                ('name', models.CharField(blank=True, max_length=15, null=True, verbose_name='姓名')),
                ('number', models.CharField(blank=True, max_length=15, null=True, verbose_name='学号')),
                ('telephone', models.CharField(blank=True, max_length=11, null=True, verbose_name='联系方式')),
                ('department', models.CharField(blank=True, max_length=20, null=True, verbose_name='学院')),
                ('account', models.IntegerField(default=0, verbose_name='账户贝壳数目')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='dajia.Team')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'User',
            },
        ),
        migrations.AddField(
            model_name='suggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggestion', to='dajia.User'),
        ),
        migrations.AddField(
            model_name='steam',
            name='member',
            field=models.ManyToManyField(through='dajia.Membership', to='dajia.User'),
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
            model_name='need',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='need', to='dajia.User'),
        ),
        migrations.AddField(
            model_name='membership',
            name='steam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dajia.Steam', verbose_name='小团队'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dajia.User', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='cutting',
            name='audience',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cutting', to='dajia.User'),
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
        migrations.AlterIndexTogether(
            name='period',
            index_together={('status', 'production')},
        ),
        migrations.AlterIndexTogether(
            name='cutting',
            index_together={('audience', 'steamid')},
        ),
        migrations.AlterIndexTogether(
            name='comment',
            index_together={('production', 'status')},
        ),
    ]
