from django.contrib import admin
from models import UserGrade, UserGradeSummary, UserProfile, Course

class UserGradeInline(admin.TabularInline):
	model = UserGrade
	ordering = ['game']
	extra = 0

class UserGradeSummaryInline(admin.TabularInline):
	model = UserGradeSummary
	ordering = ['game']
	extra = 0

class UserProfileAdmin(admin.ModelAdmin):
	inlines = [UserGradeSummaryInline, UserGradeInline]

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


admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

