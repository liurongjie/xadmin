import xadmin

from .models import Team,User

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