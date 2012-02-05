from django.contrib import admin
from models import UserGrade, UserGradeSummary, UserProfile, Course, Activity
from models import CourseRelationship

from django.db.models import Q
import datetime

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

	####	def queryset(self, request):
	####		""" Allows instructors to only see students of their courses. Admin
	####		sees all.

	####		This method just returns the queryset that will be viewable in the
	####		admin interface.
	####		"""

	####		# UserProfiles
	####		qs = super(UserProfileAdmin, self).queryset(request)

	####		if request.user.is_superuser:
	####			return qs
	####		elif request.user.is_staff:
	####			# Get instructor's courses
	####			courses = request.user.courserelationship_set.filter(
	####				Q(end_date__isnull=True) |\
	####				Q(end_date__gt=datetime.datetime.now())
	####			)

	####			courses = [c.course for c in courses]

	####			# Return only user profiles which are in instructor's course
	####			# and which are students
	####			return qs.filter(
	####				user__courserelationship__course__in=courses,
	####				user__courserelationship__relationship_type__name='Students')
	
# TODO: possible to set a default role option in admin so that separate 
#		roles are more apparent?

class InstructorInline(admin.TabularInline):
	from django.contrib.auth.models import Group
	model = CourseRelationship
	extra = 1

	def queryset(self, request):
		""" Filter relationships by Instructor group """
		qs = super(InstructorInline, self).queryset(request)
		
		return qs.filter(relationship_type__name='Instructors')

class StudentInline(admin.TabularInline):
	model = CourseRelationship
	extra = 1

	def queryset(self, request):
		""" Filter relationships by Student group """
		qs = super(StudentInline, self).queryset(request)
		
		return qs.filter(relationship_type__name='Students')

class UserProfileInlineAdmin(admin.TabularInline):
	model = UserProfile
	extra = 3

class UserActivityInline(admin.TabularInline):
	model = UserGrade
	ordering = ['game']
	extra = 0

class UserActivitySummaryInline(admin.TabularInline):
	model = UserGradeSummary
	ordering = ['game']
	extra = 0


def merge_activities(modeladmin, request, queryset):
	main = queryset[0]
	tail = queryset[1:]
	related = main._meta.get_all_related_objects()
	valnames = dict()
    
	for r in related:
		valnames.setdefault(r.model, []).append(r.field.name)
    
	for model_object in tail:
		for model, field_names in valnames.iteritems():
			for field_name in field_names:
				model.objects.filter(**{field_name: model_object}).update(**{field_name: main})
		model_object.delete()
	
	msg = " %s is merged with other tags, now you can give it a canonical name." % main
	
	modeladmin.message_user(request, msg)

merge_activities.short_description = "Merge activities, copying user grade records"


class ActivityAdmin(admin.ModelAdmin):
	inlines = [UserActivitySummaryInline, UserActivityInline]
	list_display = ('name', 'useractivitycount', 'usersummarycount',)
	actions = [merge_activities]

	def queryset(self, request):
		from django.db.models import Count
		return super(ActivityAdmin, self).queryset(request)\
						.annotate(recordcount=Count('usergrade'))\
						.annotate(summarycount=Count('usergradesummary'))

	def useractivitycount(self, instance):
		return instance.recordcount

	def usersummarycount(self, instance):
		return instance.summarycount

class CourseAdmin(admin.ModelAdmin):
	inlines = [InstructorInline, StudentInline]
	list_display = ('identifier', 'name', 'end_date',)

	####	def queryset(self, request):
	####		""" Filter only courses that request user is instructor of.
	####			Admin sees all.
	####		"""

	####		qs = super(CourseAdmin, self).queryset(request)
	####		if request.user.is_superuser:
	####			return qs
	####		elif request.user.is_staff:
	####			qs = qs.filter(
	####				Q(courserelationship__user=request.user, courserelationship__end_date__isnull=True) |\
	####				Q(courserelationship__user=request.user, courserelationship__end_date__gt=datetime.datetime.now())
	####			).distinct()

	####			return qs

	####		else:
	####			return qs


admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Activity, ActivityAdmin)

