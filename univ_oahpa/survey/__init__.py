""" Oahpa survey module
    -------------------

## How this works

The survey application, when installed properly, will check if the user
has a survey available every 5 page loads. If the user does, the user
will be prompted to click a link and answer a survey.

Surveys are rendered by fetching questions from the database, handled by
angularjs. This allows administrators to create new surveys at will and
deploy them.

User responses are recorded, and though the user account is stored in
the database (for tracking purposes), results are always displayed in an
anonymized format.

Results are also able to be exported to CSV using the survey list page
in the admin, via the actions dropdown menu.


## Installing

 1.) `settings.py`: add the items to the configuration tuples. `survey`
 must go after `rest_framework`, and after `courses`.
 `SurveyCheckMiddleware` must go after `GradingMiddleware`.

    INSTALLED_APPS = (
        ...
        'univ_oahpa.survey',
        ...
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'univ_oahpa.survey.context_processors.display_survey_notice',
        ...
    )

    MIDDLEWARE_CLASSES = (
        ...
        'survey.middleware.SurveyCheckMiddleware',

        ...
    )

"""
