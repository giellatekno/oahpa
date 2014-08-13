from django.contrib import admin
from .models import Survey, UserSurvey, SurveyQuestion, SurveyQuestionAnswerValue, UserSurveyQuestionAnswer

from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

class SurveyQuestionAnswerValueInlineAdmin(admin.TabularInline):
    model = SurveyQuestionAnswerValue
    extra = 1

class EditLinkToInlineObject(object):
    """ Include a link field to edit the object, pops out to a new tab /
    window. """

    def edit_answers(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.module_name),  args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}" target="blank">edit</a>'.format(u=url))
        else:
            return ''

class SurveyQuestionInlineAdmin(EditLinkToInlineObject, admin.TabularInline):
    model = SurveyQuestion
    readonly_fields = ('edit_answers', )
    extra = 1

class SurveyQuestionAdmin(admin.ModelAdmin):
    model = SurveyQuestion
    inlines = [SurveyQuestionAnswerValueInlineAdmin]

class SurveyAdmin(admin.ModelAdmin):
    """ The main survey object with inlines for answers.
    """
    inlines = [SurveyQuestionInlineAdmin]

    def export_survey_result_csv(self, request, queryset):
        from django.core import serializers
        from django.http import HttpResponse

        from cStringIO import StringIO
        import csv

        # only serialize one at a time

        if queryset.count() > 1:
            # TODO: message about error
            # return redirect? 
            pass

        handle = StringIO()
        csvwriter = csv.writer(handle)

        survey = queryset[0]
        csv_rows = survey.serialize_survey()

        csvwriter.writerows(csv_rows)
        contents = handle.getvalue()
        handle.close()
        print contents

        self.message_user(request, "Survey exported.")
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="%s"' % "survey-results.csv"
        response.content = contents
        return response

    export_survey_result_csv.short_description = "Download a CSV of all survey results."

    actions = [export_survey_result_csv]


class UserSurveyQuestionAnswer(admin.TabularInline):
    model = UserSurveyQuestionAnswer



class UserSurveyAdmin(admin.ModelAdmin):
    model = UserSurvey

    inlines = [UserSurveyQuestionAnswer]
    list_display = ('user_anonymized', 'completed', 'survey')
    exclude = ('user', )
    ordering = ('-completed', )

admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyQuestion, SurveyQuestionAdmin)
# admin.site.register(SurveyQuestionAnswerValue)
admin.site.register(UserSurvey, UserSurveyAdmin)
