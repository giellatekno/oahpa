from django.contrib import admin
from .models import Survey, UserSurvey, SurveyQuestion, SurveyQuestionAnswerValue

class SurveyQuestionAdmin(admin.TabularInline):
    model = SurveyQuestion

class SurveyAdmin(admin.ModelAdmin):
    """ zomg
    """
    inlines = [SurveyQuestionAdmin]

admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyQuestionAnswerValue)
admin.site.register(UserSurvey)
