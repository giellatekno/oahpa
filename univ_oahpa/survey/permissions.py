from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

__all__ = [
    'IsAuthenticated',
    'GetOnly',
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
