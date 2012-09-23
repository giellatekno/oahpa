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

    def __init__(self, authusers):
        self.authusers = authusers

class UserGrade(UserProfile):

    remove_keys = ['pk']

class UserGradeSummary(UserProfile):

    remove_keys = ['pk']


def main(infile, outfile):
    authusers = AuthUser()
    model_funcs = {
        'auth.user': authusers,
        'courses.userprofile': UserProfile(authusers),
        'courses.usergrade': UserGrade(authusers),
        'courses.usergradesummary': UserGradeSummary(authusers),
    }

    with open(infile, 'r') as F:
        json_data = json.load(F)

    print len(json_data)
    new_data = []
    for item in json_data:
        modelname = item.get('model')
        newitem = model_funcs.get(modelname).fix(item)
        new_data.append(newitem)
    
    with open(outfile, 'w') as F:
        json.dump(new_data, F, indent=2)
    

if __name__ == "__main__":
    in_file = sys.argv[1]
    out_file = sys.argv[2]

    sys.exit(main(in_file, out_file))

