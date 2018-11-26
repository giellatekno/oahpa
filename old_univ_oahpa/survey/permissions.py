from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from .models import UserSurvey

__all__ = [
    'IsAuthenticated',
    'GetOnly',
    'PostOnly',
    'CanCreateSurvey',
]

### class CanCreateAndUpdateGoal(permissions.BasePermission):
### 
###     def has_permission(self, request, view, obj=None):
###         return True
### 
###     def has_object_permission(self, request, view, obj):
###         if request.method in permissions.SAFE_METHODS:
###             return True
### 
###         # If there's a course, only the instructors can edit
###         if obj.course:
###             return obj.course in request.user.get_profile().instructorships
###         # Otherwise, this is the user's personal goal.
###         else:
###             return obj.created_by == request.user
###         return False

class GetOnly(permissions.BasePermission):

    def has_permission(self, request, view, obj=None):
        if request.method == 'GET':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return False

class PostOnly(permissions.BasePermission):

    def has_permission(self, request, view, obj=None):
        if request.method == 'POST':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True
        return False

class CanCreateSurvey(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print "CanCreateSurvey: Has object permission"
        print request
        print view
        print obj
        return False
        if request.method == 'POST':
            print "CanCreateSurvey: POST"
            if obj is not None:
                surveys = UserSurvey.objects.filter(user=request.user, id=obj.id).exists()
            else:
                print "None"
                return False

            if obj and surveys:
                return False
            elif obj and not surveys:
                return True

            return False

    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True

    #     # If there's a course, only the instructors can edit
    #     if obj.course:
    #         return obj.course in request.user.get_profile().instructorships
    #     # Otherwise, this is the user's personal goal.
    #     else:
    #         return obj.created_by == request.user
    #     return False
