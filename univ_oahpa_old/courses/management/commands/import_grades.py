from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option
import sys
import json

# # # 
# 
#  Command class
#
# # #

class BulkDeserializer(object):
    def insert(self):
        """ Create objects for bulk insert, then do it. """

        def adjustForMaps(d, maps):
            """ If key exists in maps, replace with new key and replace
            value with lookup from the map. """
            _d = {}
            for k, v in d.iteritems():
                if k in maps:
                    _nk, _map = maps.get(k)
                    _nv = _map.get(v)
                    _d[_nk] = _nv
                else:
                    _d[k] = v
            return _d

        objs = []
        for item in self.data:
            _fields = adjustForMaps(item.get('fields'), self.maps)
            if self.debug:
                print item.get('fields')
            if self.debug:
                print _fields
            _new = self.model(**_fields)
            objs.append(_new)
            if self.debug:
                raw_input()
        self.objs = []
        for obj in objs:
            obj.save()
            self.objs.append(obj)
        # self.objs = self.model.objects.bulk_create(objs)

    def __init__(self, userdata, maps={}, debug=False):
        self.data = userdata
        self.maps = maps
        self.debug = debug

    def get(self, key):
        return self._map.get(key)

    def createMap(self, key):
        self._map = {}
        for obj in self.objs:
            self._map[obj.__getattribute__(key)] = obj

class Users(BulkDeserializer):
    from django.contrib.auth.models import User
    model = User

class Activities(BulkDeserializer):
    from courses.models import Activity
    model = Activity

class UserProfiles(BulkDeserializer):
    from courses.models import UserProfile
    model = UserProfile

    def createMap(self):
        self._map = {}
        for obj in self.objs:
            _nk = obj.user.username
            self._map[_nk] = obj

class UserGrades(BulkDeserializer):
    from courses.models import UserGrade
    model = UserGrade

class UserGradeSummaries(BulkDeserializer):
    from courses.models import UserGradeSummary
    model = UserGradeSummary

def import_grades(filename):
    with open(filename, 'r') as F:
        json_data = json.load(F)

    def modelName(n):
        def _fx(x):
            if x.get('model') == n:
                return True
            else:
                return False
        return _fx

    _users = filter(modelName("auth.user"), json_data)
    _activities = filter(modelName("courses.activity"), json_data)
    _userprofiles = filter(modelName("courses.userprofile"), json_data)
    _usergrades = filter(modelName("courses.usergrade"), json_data)
    _usergradesummaries = filter(modelName("courses.usergradesummary"), json_data)

    users = Users(_users)
    users.insert()
    users.createMap('username')
    print "%d users created" % len(users.objs)

    activities = Activities(_activities)
    activities.insert()
    activities.createMap('name')
    print "%d activities created" % len(activities.objs)

    # TODO: user__username invalid, replace using map somehow.
    userprofiles = UserProfiles(_userprofiles, maps={'user__username': ('user', users)})
    userprofiles.insert()
    userprofiles.createMap()
    print "%d userprofiles created" % len(userprofiles.objs)

    # TODO: UserGrade.user has null, silently skip failed inserts?
    usergrades = UserGrades(_usergrades, maps={
        'user__username': ('user', userprofiles),
        'game__name': ('game', activities)
    })
    usergrades.insert()
    print "%d usergrades created" % len(usergrades.objs)

    usergradesummaries = UserGradeSummaries(_usergradesummaries, maps={
        'user__username': ('user', userprofiles),
        'game__name': ('game', activities),
    })
    usergradesummaries.insert()
    print "%d usergradesummaries created" % len(usergradesummaries.objs)

class Command(BaseCommand):
    args = '--tagelement'
    help = """
    Strips tags of an element and then merges them all.
    """
    option_list = BaseCommand.option_list + (
        make_option("-f", "--file", dest="filename",
                          help="File to import"),
    )

    def handle(self, *args, **options):
        import sys, os
        filename = options['filename']
        # NOTE: for testing
        from django.contrib.auth.models import User
        User.objects.filter(username__startswith='victorio-').delete()

        import_grades(filename)


