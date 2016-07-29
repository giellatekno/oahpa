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
        'davvi_oahpa.survey',
        ...
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'davvi_oahpa.survey.context_processors.display_survey_notice',
        ...
    )

    MIDDLEWARE_CLASSES = (
        ...
        'survey.middleware.SurveyCheckMiddleware',

        ...
    )

## Managing surveys within the Admin interface

TODO: going to write this here first and hten move it to a suitable location

Note that due to lcalization, some of the names of buttons may vary.

1.) Log in to the admin interface

### Adding a survey

2.) Within the survey admin group, click the grey '+ Add a survey'
    button in the upper right-hand corner.

3.) Fill out the title and description, clicking on the tabs for any
    languages you wish to have supported and filling those out too.

  - If you wish to target a specific course, select it from the dropdown
  menu. Only users of this course will have the option to fill out the survey.

#### Adding a question to a survey

4.) In the section below the survey metadata, enter some question text
    and select an answer type. Note that for some answer types, you will
    have to enter each individual answer as well. In order to do this,
    you must save the question text first: this way the question will be
    stored. To save: click "Save and continue to edit"

#### Adding answers to a question

After saving the question prompt, look for a link next to the question
type in the 'edit answers' column that says "edit". Click this, and a
new window or tab will pop up  presenting you with the list of possible answers.

In the answers section enter an answer. If you need more possible
answers than there are fields, click "Save and continue editing" and
more fields will appear.

When you save, you may go back to the survey page to add more questions.

NB: You will only need to add answers for 'single choice' and 'multiple
choice' question types. 'yes/no' will be automatically populated, and
'freeform text' naturally does not require answers.


"""
