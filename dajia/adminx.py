import xadmin

from .models import Team,User,Merchant,Production,Period,Steam,Comment,Order,Cutting

class Teamxadmin(object):
    list_display={'teamid','teamname','logo','time'}
    search_fields={'teamname'}
    list_filter={'teamname'}
xadmin.site.register(Team,Teamxadmin)

class Userxadmin(object):
    list_display = {'openid', 'nickname', 'picture','gender', 'status','number','telephone','department','team'}
    search_fields = {'team__teamname','nickname'}
    list_filter = {'gender','status'}
xadmin.site.register(User,Userxadmin)

class Merchantxadmin(object):
    list_display = {'merchantid','name','location','latitude','longitude','reputation','type','logo','pic1','pic2','pic3'}
    search_fields = {'name','location'}
    list_filter = {'type','reputation'}
xadmin.site.register(Merchant,Merchantxadmin)

class Productionxadmin(object):
    list_display = {'productionid','team','merchant','name','reputation','introduction','introductionpic','type','cutnumber','saveprice'}
    search_fields = {'team__name','merchant__name'}
    list_filter = {'type'}
xadmin.site.register(Production,Productionxadmin)


class Periodxadmin(object):
    list_display = {'periodid','production','starttime','endtime','startprice','bottomprice','type','time','status','cutprice','number','cutnumber','saveprice'}
    search_fields = {'prodution__name'}
    list_filter = {'type','status'}
xadmin.site.register(Period,Periodxadmin)


class Steamxadmin(object):
    list_display = {'steamid','time','cutprice','steamnumber','master'}
    search_fields = {'steamid','master__name'}
    list_filter = {'cutprice'}
xadmin.site.register(Steam,Steamxadmin)


class Commentxadmin(object):
    list_display = {'commentid','production','user','context','time','status','judge'}
    search_fields = {'production__name','user__name'}
    list_filter = {'status','judge'}
xadmin.site.register(Comment,Commentxadmin)


class Orderxadmin(object):
    list_display = {'orderid','user','period','production','steam','status','cutprice','time1','time2','time3','time4','time5','time6','comment'}
    search_fields = {'user__name','production__name'}
    list_filter = {'status'}
xadmin.site.register(Order,Orderxadmin)

class Cuttingxadmin(object):
    list_display = {'cutid','audience','steam','cutprice','time'}
    search_fields = {'steam__steamid','steam__master__name'}
    list_filter = {'cutprice'}
xadmin.site.register(Cutting,Cuttingxadmin)

