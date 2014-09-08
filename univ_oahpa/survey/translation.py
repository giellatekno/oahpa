""" This is the means for controlling what model fields are translatable as according to:

    http://django-modeltranslation.readthedocs.org/
    http://django-modeltranslation.readthedocs.org/en/latest/commands.html

    settings.py requires:

        MODELTRANSLATION_TRANSLATION_FILES = (
            'survey.translation',
        )

        INSTALLED_APPS = (
            'modeltranslation',
        )

"""

from modeltranslation.translator import translator, TranslationOptions, AlreadyRegistered

from .models import Survey, SurveyQuestion, SurveyQuestionAnswerValue

class SurveyOptions(TranslationOptions):
    fields = ('title', 'description', )

class SurveyQuestionOptions(TranslationOptions):
    fields = ('question_text', )

class SurveyQuestionAnswerValueOptions(TranslationOptions):
    fields = ('answer_text', )

translator.register(Survey, SurveyOptions)
translator.register(SurveyQuestion, SurveyQuestionOptions)
translator.register(SurveyQuestionAnswerValue, SurveyQuestionAnswerValueOptions)
