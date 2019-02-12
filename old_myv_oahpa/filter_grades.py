#!/usr/bin/env python2.7
"""
USAGE: python2.7 filter_grades infile outfile

# NOTES:

TODO: need to store courses.activity, and replace courses.usergrade and courses.usergradesummary "game" with "game__name"

use dumpdata to export:

    python2.7 manage.py dumpdata --natural\
      --indent 2 \
      auth.User \
      courses.UserProfile \
      courses.UserGrade \
      courses.UserGradeSummary

Ordering of export important.

auth.user
 - remove "pk"
 - remove "is_active", "is_superuser", "is_staff"
 - remove "groups"
 - remove "user_permissions"

courses.activity
 - grab "pk" and store fields/name

courses.userprofile
 - remove "pk"
 - "user" --> "user__username"; prepend "victorio-"

courses.usergrade
 - "user" --> "user__username"; prepend "victorio-"

courses.usergradesummary
 - "user" --> "user__username"; prepend "victorio-"



"""

import os
import sys
import json

class Fixer(object):
    def popKeys(self, d):
        for key in self.remove_keys:
            if key.find('/') > -1:
                ka, _, kb = key.partition('/')
                inner = d.get(ka).copy()
                inner.pop(kb)
                d[ka] = inner
            else:
                d.pop(key)
        return d
    
class Activity(Fixer):
    activity_pks_to_names = {
    }

    remove_keys = ['pk']

    def getActivity(self, aid):
    	return self.activity_pks_to_names.get(aid, False)

    def fix(self, a):
        # pop keys, store pk-to-name
        self.activity_pks_to_names[a.get('pk')] = a.get('fields').get('name')
        return self.popKeys(a.copy())

    def __init__(self):
        pass


class AuthUser(Fixer):
    user_pks_to_names = {
    }

    remove_keys = [
        "pk",
        "fields/is_active",
        "fields/is_superuser",
        "fields/is_staff",
        "fields/groups",
        "fields/user_permissions",
    ]
    def getUser(self, uid):
        return self.user_pks_to_names.get(uid, False)

    def fix(self, au):
        # pop keys, store pk-to-name
        fields = au.get('fields').copy()
        fields['username'] = 'victorio-' + fields['username']
        au['fields'] = fields

        self.user_pks_to_names[au.get('pk')] = au.get('fields').get('username')
        return self.popKeys(au.copy())

    def __init__(self):
        pass

class UserProfile(Fixer):
    remove_keys = ['pk']

    def fix(self, up):
        # switch fields/user (id) to fields/user__username
        fields = up.get('fields').copy()
        uid = fields.pop('user')
        uname = self.authusers.getUser(uid)
        fields['user__username'] = uname
        up['fields'] = fields

        # pop keys
        return self.popKeys(up)

    def __init__(self, authusers, activities):
        self.authusers = authusers
        self.activities = activities

class UserGrade(UserProfile):

    remove_keys = ['pk']

    def fix(self, ug):
        # Replace game with game__name, pass on to super for further
        # edits
    	_ug = ug.copy()
    	_ug_fields = _ug.get('fields')

    	gamename = self.activities.getActivity(_ug_fields.pop('game'))
    	_ug_fields['game__name'] = gamename
    	_ug['fields'] = _ug_fields
    	return super(UserGrade, self).fix(_ug)

class UserGradeSummary(UserGrade):

    remove_keys = ['pk']


def main(infile, outfile):
    authusers = AuthUser()
    activities = Activity()

    model_funcs = {
        'auth.user': authusers,
        'courses.activity': activities,
        'courses.userprofile': UserProfile(authusers, activities),
        'courses.usergrade': UserGrade(authusers, activities),
        'courses.usergradesummary': UserGradeSummary(authusers, activities),
    }

    with open(infile, 'r') as F:
        json_data = json.load(F)

    def replace(item):
        modelname = item.get('model')
        # print json.dumps(item)
        # print '--'
        # print json.dumps(newitem)
        # raw_input()
    	return model_funcs.get(modelname).fix(item)

    print >> sys.stderr, "%d items read." % len(json_data)
    with open(outfile, 'w') as F:
        json.dump(map(replace, json_data), F, indent=2)
    print >> sys.stderr, "Done."
    

if __name__ == "__main__":
    in_file = sys.argv[1]
    out_file = sys.argv[2]

    sys.exit(main(in_file, out_file))

