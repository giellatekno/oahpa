from django.contrib import admin

from models import ( UserGrade
                   , UserGradeSummary
                   , UserProfile
                   , Course
                   , Activity
                   , Goal
                   , GoalParameter
                   , CourseGoal
                   )

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

class GoalParamAdmin(admin.TabularInline):
    model = GoalParameter

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserGradeSummaryInline, UserGradeInline]

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
    inlines = [InstructorInline, StudentInline, ]
    list_display = ('identifier', 'name', 'end_date',)

class GoalAdmin(admin.ModelAdmin):
    inlines = [GoalParamAdmin]


admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(CourseGoal)
