from django.contrib import admin
from .models import Survey, UserSurvey, SurveyQuestion, SurveyQuestionAnswerValue


# TODO: help_texts 
class SurveyAdmin(admin.ModelAdmin):
    """ zomg
    """

admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyQuestionAnswerValue)
admin.site.register(UserSurvey)
