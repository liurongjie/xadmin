import xadmin
from xadmin import views
from .models import Team,User,Merchant,Production,Steam,Comment,Order,Cutting,Need,Membership
from .models import Gift,Giftorder
# 创建xadmin的最基本管理器配置，并与view绑定
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True

# 全局修改，固定写法
class GlobalSettings(object):
    site_title='Boat后台管理系统'
    site_footer="珞珈云顶工坊"
    menu_style = 'accordion'
# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)

# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView,GlobalSettings)

class Teamxadmin(object):
    list_display={'teamid','teamname','logo','time'}
    search_fields={'teamname'}
    list_filter={'teamname'}
xadmin.site.register(Team,Teamxadmin)

class Userxadmin(object):
    list_display = {'userid','openid', 'nickname', 'picture','gender', 'status','number','telephone','department','team','account'}
    search_fields = {'team__teamname','nickname'}
    list_filter = {'gender','status','team__teamname'}
xadmin.site.register(User,Userxadmin)

class Merchantxadmin(object):
    list_display = {'merchantid','name','location','latitude','longitude','type','logo','telephone'}
    search_fields = {'name'}
    list_filter = {'type'}
xadmin.site.register(Merchant,Merchantxadmin)

class Productionxadmin(object):
    list_display = {'productionid','team','merchant','name','rank','reputation','introduction','introductionpic','type','logo','distance', \
                    'startprice','bottomprice','pic1','pic2','pic3','number'}
    search_fields = {'team__name','merchant__name'}
    list_filter = {'type'}
xadmin.site.register(Production,Productionxadmin)




class Steamxadmin(object):
    list_display = {'steamid','time','cutprice','steamnumber','member','endtime'}
    search_fields = {'steamid'}
    list_filter = {'cutprice','endtime'}
xadmin.site.register(Steam,Steamxadmin)

class Memberxadmin(object):
    list_display = {'id','user','steam','cutprice','time'}
    search_fields = {'user__name'}

xadmin.site.register(Membership,Memberxadmin)

class Commentxadmin(object):
    list_display = {'commentid','production','user','context','time','status',}
    search_fields = {'production__name','user__name'}
    list_filter = {'status'}
xadmin.site.register(Comment,Commentxadmin)


class Orderxadmin(object):
    list_display = {'orderid','user','production','steam','state','status','cutprice','time1','time2','time3','time4','time5','certificate'}
    search_fields = {'user__name','production__name'}
    list_filter = {'status'}
xadmin.site.register(Order,Orderxadmin)

class Cuttingxadmin(object):
    list_display = {'cutid','audience','steamid','cutprice','time'}
    search_fields = {'steamid'}
    list_filter = {'cutprice'}
xadmin.site.register(Cutting,Cuttingxadmin)

class Needxadmin(object):
    list_display = {'needid','user','teamname','pic','time'}
    search_fields = {'teamname'}
    list_filter = {}
xadmin.site.register(Need,Needxadmin)



class Giftxadmin(object):
    list_display = {'id','name','worth','pic','time'}
    search_fields = {}
    list_filter = {}
xadmin.site.register(Gift,Giftxadmin)

class Giftorderxadmin(object):
    list_display = {'id','user','gift','status','time'}
    search_fields = {}
    list_filter = {"user__name","status","gift__name"}
xadmin.site.register(Giftorder,Giftorderxadmin)




