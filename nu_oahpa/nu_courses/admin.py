from django.contrib import admin
from oahpa.courses.models import Activity, UserGrade,\
									UserGradeSummary, UserProfile,\
									Course, UserLogin

class ActivityInline(admin.TabularInline):
	model = UserGradeSummary

class UserGradeInline(admin.TabularInline):
	model = UserGrade
	ordering = ['game']
	extra = 0
	def queryset(self, request):
		""" Return grade summaries only for instructors' students.
		"""
		qs = super(UserGradeInline, self).queryset(request)
		if request.user.is_superuser:
			return qs
		elif request.user.is_staff:
			return qs.filter(user__user__studentships__instructors=request.user)


class UserGradeSummaryInline(admin.TabularInline):
	model = UserGradeSummary
	extra = 0
	def queryset(self, request):
		""" Return grade summaries only for instructors' students.
		"""
		qs = super(UserGradeSummaryInline, self).queryset(request)
		if request.user.is_superuser:
			return qs
		elif request.user.is_staff:
			return qs.filter(user__user__studentships__instructors=request.user)
	

class ActivityAdmin(admin.ModelAdmin):
	inlines = [UserGradeSummaryInline, UserGradeInline]
		

class UserLoginInline(admin.TabularInline):
	model = UserLogin
	extra = 0
	ordering = ['+timestamp']
	

class UserProfileAdmin(admin.ModelAdmin):
	inlines = [UserGradeSummaryInline, UserGradeInline, UserLoginInline]
	list_display = ['user', 'login_count', 'last_login']

	def queryset(self, request):
		""" Allows instructors to only see students
			of their courses. Admin sees all.
		"""
		qs = super(UserProfileAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		elif request.user.is_staff:
			return qs.filter(user__studentships__instructors=request.user)
	
class StudentInline(admin.TabularInline):
	model = Course.students.through

class UserProfileInlineAdmin(admin.TabularInline):
	model = UserProfile
	extra = 3

class CourseAdmin(admin.ModelAdmin):
	inlines = [StudentInline]
	list_display = ['identifier']  # , 'name']

	def queryset(self, request):
		""" Filter only courses that request user is instructor of.
			Admin sees all.
		"""
		qs = super(CourseAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		elif request.user.is_staff:
			return qs.filter(instructors=request.user)
		else:
			return qs


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

