""" This is the means for controlling what model fields are translatable as according to:

    http://django-modeltranslation.readthedocs.org/
    http://django-modeltranslation.readthedocs.org/en/latest/commands.html

    settings.py requires:

        MODELTRANSLATION_TRANSLATION_FILES = (
            'translation',
        )

        INSTALLED_APPS = (
            'modeltranslation',
        )

    You will also need to add South to the beginning of installed apps.

        INSTALLED_APPS = (
            'south',
            '...'
        )

    Adding models to the system requires South. First, make sure the app is added in south, if not:

        $ python manage.py convert_to_south APPNAME

    Then, begin a new migration for the database for the particular app within South.

        $ python manage.py schemamigration APPNAME --initial

    (Where APPNAME is f.ex. survey, courses, drill, etc.)

    Alter translation file here to add new fields that will be translated. When done, update the migration in progress:

        $ python manage.py schemamigration APPNAME --auto --update

    When you've completed the field changes (each time using --auto
    --update to reflect a change), apply the migration, and this will create the additional translation fields.

        $ python manage.py migrate APPNAME

    NB. If you have old data that you are migrating into the translation system from previously non-translateable models, no data may appear in the default field. If this is the case, migrate the old data in with the following command:

        $ python manage.py update_translation_fields

    ## Deploying new translation settings on server

    NB zOMG: This is a careful process, otherwise you will see some big
    scary (and potentially condescending) errors about choosing the
    wrong DB system which doesn't support schema transaction statements.

    The initial migration (0001_initial.py) will only run on the first
    machine it is applied on. Therefore, when bringing the new migration
    system over to another machine, we must fake the first migration and
    then run the rest. This applies for example, when deploying the new
    system on gtoahpa:

        $ svn up

    Activate South by installing it in INSTALLED_APPS, along with any
    other changes.

        $ python manage.py syncdb

    Fake the first migrations for each app:

        $ python manage.py migrate APPNAME1 0001 --fake
        $ python manage.py migrate APPNAME2 0001 --fake

    Then run the remaining migrations as normal:

        $ python manage.py migrate APPNAME1 0002
        $ python manage.py migrate APPNAME2 0002

        etc...

    Then update the translation fields.

        $ python manage.py update_translation_fields

"""
from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

from modeltranslation.translator import translator, TranslationOptions, AlreadyRegistered

Survey = oahpa_module.survey.models.Survey
SurveyQuestion = oahpa_module.survey.models.SurveyQuestion
SurveyQuestionAnswerValue = oahpa_module.survey.models.SurveyQuestionAnswerValue

Goal = oahpa_module.courses.models.Goal
CourseGoal = oahpa_module.courses.models.CourseGoal


class SurveyOptions(TranslationOptions):
    fields = ('title', 'description', )

class SurveyQuestionOptions(TranslationOptions):
    fields = ('question_text', )

class SurveyQuestionAnswerValueOptions(TranslationOptions):
    fields = ('answer_text', )

translator.register(Survey, SurveyOptions)
translator.register(SurveyQuestion, SurveyQuestionOptions)
translator.register(SurveyQuestionAnswerValue, SurveyQuestionAnswerValueOptions)

class GoalTranslationOptions(TranslationOptions):
	fields = ('short_name', )

class CourseGoalTranslationOptions(TranslationOptions):
	fields = ('short_name', 'description')

translator.register(Goal, GoalTranslationOptions)
translator.register(CourseGoal, CourseGoalTranslationOptions)
